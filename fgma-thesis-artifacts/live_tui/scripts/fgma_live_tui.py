from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "live_tui"
OUT.mkdir(parents=True, exist_ok=True)

ERROR_TYPES = [
    "factual_error",
    "persona_drift",
    "tone_mismatch",
    "memory_omission",
    "contradiction",
    "overclaim_safety",
]
SCOPES = ["current_turn", "current_user", "current_persona", "global"]
CONDITIONS = {
    "C0": "No memory",
    "C1": "Positive-only memory",
    "C2": "Error-diagnostic memory",
    "C3": "Mixed feedback memory",
    "C4": "Direct correction baseline",
}


@dataclass
class ModelSpec:
    model_id: str
    label: str
    provider: str
    api_key: str
    base_url: str
    model: str


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_models() -> list[ModelSpec]:
    load_dotenv(ROOT / ".env")
    openrouter_base = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
    deepseek_base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/chat/completions")
    specs = [
        ModelSpec(
            "key1_qwen_72b",
            "KEY1 / OpenRouter / Qwen2.5-72B-Instruct",
            "openrouter",
            os.getenv("OPENROUTER_KEY1", ""),
            openrouter_base,
            os.getenv("OPENROUTER_MODEL_KEY1", "qwen/qwen-2.5-72b-instruct"),
        ),
        ModelSpec(
            "key2_llama_8b",
            "KEY2 / OpenRouter / Llama-3.1-8B-Instruct",
            "openrouter",
            os.getenv("OPENROUTER_KEY2", ""),
            openrouter_base,
            os.getenv("OPENROUTER_MODEL_KEY2", "meta-llama/llama-3.1-8b-instruct"),
        ),
        ModelSpec(
            "key3_gemma_12b",
            "KEY3 / OpenRouter / Gemma-3-12B-IT",
            "openrouter",
            os.getenv("OPENROUTER_KEY3", ""),
            openrouter_base,
            os.getenv("OPENROUTER_MODEL_KEY3", "google/gemma-3-12b-it"),
        ),
        ModelSpec(
            "deepseek_chat",
            "DeepSeek / deepseek-chat",
            "deepseek",
            os.getenv("DEEPSEEK_API_KEY", ""),
            deepseek_base,
            os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        ),
    ]
    return [s for s in specs if s.api_key]


def load_personas() -> list[dict[str, Any]]:
    return read_json(ROOT / "data" / "personas" / "full_synthetic_personas.json")


def load_scenarios() -> list[dict[str, Any]]:
    return read_json(ROOT / "data" / "scenarios" / "full_scenarios.json")


def wrong_prior_for(persona: dict[str, Any], fact_key: str) -> dict[str, Any]:
    for item in persona.get("wrong_prior_versions", []):
        if item.get("fact_key") == fact_key:
            return item
    raise KeyError(f"wrong prior not found for {persona.get('persona_id')} / {fact_key}")


def case_rows() -> list[dict[str, Any]]:
    personas = {p["persona_id"]: p for p in load_personas()}
    rows = []
    for scenario in load_scenarios():
        persona = personas[scenario["persona_id"]]
        wrong = wrong_prior_for(persona, scenario["fact_key"])
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "persona_id": persona["persona_id"],
                "persona_name": persona["name_or_alias"],
                "fact_key": scenario["fact_key"],
                "correct_fact": wrong["correct_fact"],
                "wrong_fact": wrong["wrong_fact"],
                "initial_question": scenario["turn_templates"][0],
                "followups": scenario["turn_templates"][1:],
            }
        )
    return rows


def corrupted_facts(persona: dict[str, Any], fact_key: str) -> dict[str, str]:
    facts = dict(persona.get("factual_knowledge", {}))
    facts[fact_key] = wrong_prior_for(persona, fact_key)["wrong_fact"]
    return facts


def persona_block(persona: dict[str, Any], scenario: dict[str, Any], use_wrong_prior: bool) -> str:
    facts = corrupted_facts(persona, scenario["fact_key"]) if use_wrong_prior else persona.get("factual_knowledge", {})
    lines = [
        f"Persona name: {persona['name_or_alias']}",
        f"Profile: {persona['basic_profile']}",
        "Persona facts:",
    ]
    lines += [f"- {k}: {v}" for k, v in facts.items()]
    lines += [
        "Style traits: " + ", ".join(persona.get("style_traits", [])),
        "Common phrases: " + ", ".join(persona.get("common_phrases", [])),
        "Safety boundaries:",
    ]
    lines += [f"- {x}" for x in persona.get("safety_boundaries", [])]
    if use_wrong_prior:
        wrong = wrong_prior_for(persona, scenario["fact_key"])
        lines += [
            "Injected wrong prior for controlled validation:",
            f"- {scenario['fact_key']}: {wrong['wrong_fact']}",
        ]
    return "\n".join(lines)


def build_memory_entry(
    persona: dict[str, Any],
    scenario: dict[str, Any],
    failed_response: str,
    error_type: str,
    corrected_fact: str,
    migration_scope: str,
) -> dict[str, Any]:
    fact_key = scenario["fact_key"]
    wrong = wrong_prior_for(persona, fact_key)["wrong_fact"]
    return {
        "feedback_type": "error_diagnostic",
        "error_type": error_type,
        "failed_response_summary": f"The response used or followed the wrong {fact_key}: {wrong}.",
        "corrective_feedback": f"Use corrected {fact_key}: {corrected_fact}; reject the old value {wrong}.",
        "corrected_fact_or_rule": corrected_fact,
        "negative_constraint": f"Do not answer {fact_key} as {wrong} for this persona.",
        "migration_scope": migration_scope,
        "retrieval_keywords": [fact_key, str(corrected_fact).lower(), str(wrong).lower()],
    }


def build_prompt(
    persona: dict[str, Any],
    scenario: dict[str, Any],
    condition: str,
    user_message: str,
    memory_entry: dict[str, Any] | None,
    dialogue_history: list[dict[str, str]] | None = None,
) -> str:
    fact_key = scenario["fact_key"]
    wrong = wrong_prior_for(persona, fact_key)
    sections = [
        "[PERSONA BLOCK]",
        persona_block(persona, scenario, use_wrong_prior=condition in {"C0", "C1", "C2", "C3"}),
        "",
        "[DIALOGUE BLOCK]",
    ]
    if dialogue_history:
        for turn in dialogue_history:
            sections.append(f"{turn['role']}: {turn['content']}")
    else:
        sections.append("(no prior dialogue)")
    sections.append("")

    if condition in {"C1", "C3"}:
        sections += [
            "[POSITIVE MEMORY BLOCK]",
            f"Positive memory: Keep responses concise and persona-consistent when answering {fact_key}.",
            "",
        ]
    if condition in {"C2", "C3"} and memory_entry:
        sections += [
            "[ERROR MEMORY BLOCK]",
            json.dumps(memory_entry, ensure_ascii=False, indent=2),
            "",
        ]
    if condition == "C4":
        sections += [
            "[DIRECT CORRECTION BLOCK]",
            f"The correct {fact_key} is {wrong['correct_fact']}. Do not use {wrong['wrong_fact']}.",
            "",
        ]

    sections += [
        "[SAFETY CONSTRAINTS BLOCK]",
        "- Do not claim to be the real person.",
        "- Do not invent private or unverifiable details.",
        "- If correcting a prior, state the corrected fact plainly.",
        "",
        "[USER MESSAGE]",
        user_message,
    ]
    return "\n".join(sections)


def call_chat(model: ModelSpec, messages: list[dict[str, str]], timeout: int = 90) -> tuple[str, dict[str, Any]]:
    headers = {"Authorization": f"Bearer {model.api_key}", "Content-Type": "application/json"}
    if model.provider == "openrouter":
        headers["HTTP-Referer"] = os.getenv("OPENROUTER_REFERER", "https://fgma.local")
        headers["X-Title"] = os.getenv("OPENROUTER_TITLE", "FGMA Live TUI")
    payload = {
        "model": model.model,
        "messages": messages,
        "temperature": float(os.getenv("FGMA_TEMPERATURE", "0")),
        "max_tokens": int(os.getenv("FGMA_MAX_TOKENS", "256")),
    }
    start = time.perf_counter()
    resp = requests.post(model.base_url, headers=headers, json=payload, timeout=timeout)
    latency_ms = int((time.perf_counter() - start) * 1000)
    if resp.status_code >= 400:
        raise RuntimeError(f"{model.provider} API error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    content = data["choices"][0]["message"]["content"].strip()
    usage = data.get("usage", {})
    meta = {
        "latency_ms": latency_ms,
        "provider": model.provider,
        "model": model.model,
        "usage": usage,
    }
    return content, meta


def evaluate_response(text: str, correct: str, wrong: str) -> dict[str, Any]:
    low = text.lower()
    correct_hit = correct.lower() in low
    wrong_hit = wrong.lower() in low
    return {
        "correction_success": bool(correct_hit and not wrong_hit),
        "repeated_error": bool(wrong_hit and not correct_hit),
        "correct_fact_mentioned": bool(correct_hit),
        "wrong_fact_mentioned": bool(wrong_hit),
    }


def mask_model_key(label: str) -> str:
    return label


def render_model_table(console: Console, models: list[ModelSpec]) -> None:
    table = Table(title="Available live API models", box=box.SIMPLE_HEAVY)
    table.add_column("#", justify="right")
    table.add_column("Binding")
    table.add_column("Provider")
    table.add_column("Model")
    for i, model in enumerate(models, 1):
        table.add_row(str(i), mask_model_key(model.label), model.provider, model.model)
    console.print(table)


def render_case_table(console: Console, cases: list[dict[str, Any]], limit: int = 12) -> None:
    table = Table(title="Original validation cases", box=box.SIMPLE_HEAVY)
    table.add_column("#", justify="right")
    table.add_column("Scenario")
    table.add_column("Persona")
    table.add_column("Fact")
    table.add_column("Wrong prior")
    table.add_column("Correct")
    for i, case in enumerate(cases[:limit], 1):
        table.add_row(str(i), case["scenario_id"], case["persona_name"], case["fact_key"], case["wrong_fact"], case["correct_fact"])
    console.print(table)


def panel_json(title: str, payload: Any, style: str = "cyan") -> Panel:
    return Panel(json.dumps(payload, ensure_ascii=False, indent=2), title=title, border_style=style)


def run_session(
    console: Console,
    model: ModelSpec,
    case: dict[str, Any],
    condition: str,
    quick: bool = False,
) -> Path:
    personas = {p["persona_id"]: p for p in load_personas()}
    scenarios = {s["scenario_id"]: s for s in load_scenarios()}
    persona = personas[case["persona_id"]]
    scenario = scenarios[case["scenario_id"]]
    wrong = wrong_prior_for(persona, scenario["fact_key"])
    session_id = datetime.now().strftime("fgma_live_%Y%m%d_%H%M%S")
    log_path = OUT / f"{session_id}.jsonl"
    summary_path = OUT / f"{session_id}_summary.md"

    console.rule("[bold]1. Persona profile loading screen")
    console.print(Panel(persona_block(persona, scenario, use_wrong_prior=True), title="Persona + injected wrong prior", border_style="yellow"))

    initial_question = case["initial_question"]
    if not quick:
        initial_question = Prompt.ask("Initial user message", default=initial_question)

    initial_prompt = build_prompt(persona, scenario, "C0", initial_question, None, [])
    console.rule("[bold]2. Dialogue session with wrong-prior response")
    console.print(Panel(initial_question, title="User message", border_style="white"))
    initial_response, initial_meta = call_chat(
        model,
        [
            {"role": "system", "content": "You are a controlled AI companion experiment participant. Follow the supplied persona context."},
            {"role": "user", "content": initial_prompt},
        ],
    )
    console.print(Panel(initial_response, title="Model response before FGMA", border_style="red"))

    default_error_type = "factual_error"
    default_scope = "current_persona"
    corrected_fact = wrong["correct_fact"]
    if not quick:
        console.rule("[bold]3. Structured feedback input screen")
        console.print("Applying structured thesis validation feedback automatically.")
        error_type = default_error_type
        migration_scope = default_scope
    else:
        error_type = default_error_type
        migration_scope = default_scope

    memory_entry = build_memory_entry(persona, scenario, initial_response, error_type, corrected_fact, migration_scope)
    console.print(panel_json("Feedback input", {"error_type": error_type, "corrected_fact_or_rule": corrected_fact, "migration_scope": migration_scope}, "blue"))
    console.rule("[bold]4. FGMA memory update view")
    console.print(panel_json("Structured FGMA memory entry", memory_entry, "green"))

    followups = case["followups"]
    followup = followups[1] if len(followups) > 1 else followups[0]
    if not quick:
        console.print("\nCopy-ready follow-up questions:")
        for i, item in enumerate(followups, 1):
            console.print(f"  {i}. {item}")
        followup = Prompt.ask("Follow-up user message", default=followup)

    dialogue_history = [
        {"role": "user", "content": initial_question},
        {"role": "assistant", "content": initial_response},
    ]
    reconstructed_prompt = build_prompt(persona, scenario, condition, followup, memory_entry, dialogue_history)
    console.rule("[bold]5. Prompt reconstruction view")
    console.print(Panel(reconstructed_prompt, title=f"Reconstructed prompt / {condition} {CONDITIONS[condition]}", border_style="cyan"))

    console.rule("[bold]6. Follow-up correction test")
    console.print(Panel(followup, title="Follow-up question", border_style="white"))
    followup_response, followup_meta = call_chat(
        model,
        [
            {"role": "system", "content": "You are a controlled AI companion experiment participant. Use the reconstructed FGMA context exactly."},
            {"role": "user", "content": reconstructed_prompt},
        ],
    )
    console.print(Panel(followup_response, title="Model response after FGMA", border_style="green"))
    metrics = evaluate_response(followup_response, corrected_fact, wrong["wrong_fact"])

    dashboard = Table(title="7. Evaluation dashboard", box=box.SIMPLE_HEAVY)
    dashboard.add_column("Metric")
    dashboard.add_column("Value")
    dashboard.add_row("Condition", f"{condition} / {CONDITIONS[condition]}")
    dashboard.add_row("Correction success", str(metrics["correction_success"]))
    dashboard.add_row("Repeated error", str(metrics["repeated_error"]))
    dashboard.add_row("Correct fact mentioned", str(metrics["correct_fact_mentioned"]))
    dashboard.add_row("Wrong fact mentioned", str(metrics["wrong_fact_mentioned"]))
    dashboard.add_row("Initial latency ms", str(initial_meta["latency_ms"]))
    dashboard.add_row("Follow-up latency ms", str(followup_meta["latency_ms"]))
    dashboard.add_row("Input token count", str((initial_meta.get("usage") or {}).get("prompt_tokens", "provider_not_returned")))
    dashboard.add_row("Output token count", str((followup_meta.get("usage") or {}).get("completion_tokens", "provider_not_returned")))
    console.print(dashboard)

    rows = [
        {
            "event": "initial_dialogue",
            "session_id": session_id,
            "model_label": model.label,
            "provider": model.provider,
            "model": model.model,
            "scenario_id": scenario["scenario_id"],
            "persona_id": persona["persona_id"],
            "condition": "C0",
            "prompt": initial_prompt,
            "user_message": initial_question,
            "response": initial_response,
            "meta": initial_meta,
        },
        {
            "event": "feedback_memory",
            "session_id": session_id,
            "memory_entry": memory_entry,
        },
        {
            "event": "followup_test",
            "session_id": session_id,
            "model_label": model.label,
            "provider": model.provider,
            "model": model.model,
            "scenario_id": scenario["scenario_id"],
            "persona_id": persona["persona_id"],
            "condition": condition,
            "prompt": reconstructed_prompt,
            "user_message": followup,
            "response": followup_response,
            "metrics": metrics,
            "meta": followup_meta,
        },
    ]
    for row in rows:
        write_jsonl(log_path, row)

    summary = f"""# FGMA Live TUI Session Summary

- Session: `{session_id}`
- Model binding: {model.label}
- Provider/model: {model.provider} / `{model.model}`
- Scenario: {scenario["scenario_id"]} / {persona["name_or_alias"]} / `{scenario["fact_key"]}`
- Injected wrong prior: `{wrong["wrong_fact"]}`
- Correct fact/rule: `{corrected_fact}`
- Follow-up condition: {condition} / {CONDITIONS[condition]}
- Correction success: {metrics["correction_success"]}
- Repeated error: {metrics["repeated_error"]}
- Initial latency: {initial_meta["latency_ms"]} ms
- Follow-up latency: {followup_meta["latency_ms"]} ms

## Initial question
{initial_question}

## Initial response
{initial_response}

## Structured FGMA memory
```json
{json.dumps(memory_entry, ensure_ascii=False, indent=2)}
```

## Follow-up question
{followup}

## Follow-up response
{followup_response}

## Log file
`{log_path.name}`
"""
    summary_path.write_text(summary, encoding="utf-8")
    console.rule("[bold]8. Exported log/session summary screen")
    console.print(Panel(f"JSONL log: {log_path}\nMarkdown summary: {summary_path}", title="Export complete", border_style="magenta"))
    return log_path


def choose_model(console: Console, models: list[ModelSpec], model_id: str | None = None) -> ModelSpec:
    if model_id:
        for model in models:
            if model.model_id == model_id or model_id.lower() in model.label.lower() or model_id.lower() in model.model.lower():
                return model
        raise SystemExit(f"Model not found: {model_id}")
    render_model_table(console, models)
    idx = IntPrompt.ask("Select model #", default=1)
    idx = max(1, min(idx, len(models)))
    return models[idx - 1]


def choose_case(console: Console, cases: list[dict[str, Any]], case_id: str | None = None) -> dict[str, Any]:
    if case_id:
        for case in cases:
            if case["scenario_id"] == case_id:
                return case
        raise SystemExit(f"Scenario not found: {case_id}")
    render_case_table(console, cases)
    idx = IntPrompt.ask("Select validation case #", default=1)
    idx = max(1, min(idx, len(cases)))
    return cases[idx - 1]


def main() -> None:
    parser = argparse.ArgumentParser(description="FGMA live API TUI for wrong-prior recovery validation.")
    parser.add_argument("--quick-demo", action="store_true", help="Run one default live session without prompts.")
    parser.add_argument("--model", default=None, help="Model binding id, provider model id, or label fragment.")
    parser.add_argument("--case-id", default=None, help="Scenario id, for example fs001.")
    parser.add_argument("--condition", choices=sorted(CONDITIONS), default="C2")
    args = parser.parse_args()

    console = Console()
    models = load_models()
    if not models:
        raise SystemExit("No API keys found. Copy .env.example to .env and add local API keys before running live API validation.")
    cases = case_rows()

    console.print(Panel("FGMA Live TUI - real API validation for wrong-prior recovery", border_style="bold cyan"))
    model = choose_model(console, models, args.model if args.quick_demo else args.model)
    case = choose_case(console, cases, args.case_id if args.quick_demo else args.case_id)
    condition = args.condition if args.quick_demo else Prompt.ask("Follow-up condition", choices=sorted(CONDITIONS), default=args.condition)
    try:
        run_session(console, model, case, condition, quick=args.quick_demo)
    except KeyboardInterrupt:
        console.print("\nSession cancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
