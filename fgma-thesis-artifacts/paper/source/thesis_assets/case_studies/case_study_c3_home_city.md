# Case Study: C3 Home-City Wrong-Prior Recovery

## Wrong Prior

- Persona: p_aurora
- Scenario: fs001
- Fact key: home_city

## User Query

Where are you based?

## Model Response

I'm based in Barcelona, keep it grounded. small details matter in creating a realistic travel companion experience. How about you? What's your favorite place to travel to? fs001 / controlled wrong-prior recovery

## FGMA Memory / Feedback State

```json
[
  {
    "feedback_type": "error_diagnostic",
    "error_type": "Factual Error",
    "failed_response_summary": "The response used 'Barcelona' for home_city.",
    "corrective_feedback": "Replace the wrong home_city 'Barcelona' with 'Lisbon'.",
    "corrected_fact_or_rule": "Lisbon",
    "negative_constraint": "Do not answer home_city as 'Barcelona' for this persona.",
    "migration_scope": "current_persona",
    "retrieval_keywords": [
      "home_city",
      "lisbon",
      "barcelona"
    ],
    "timestamp_or_turn_id": "turn_0",
    "memory_id": "p_aurora_fs001_C3_0_error_diagnostic",
    "persona_id": "p_aurora",
    "scenario_id": "fs001",
    "condition": "C3",
    "turn_id": 0
  },
  {
    "feedback_type": "positive_example",
    "message": "This response is a useful style-consistent example for home_city: Lisbon.",
    "fact_key": "home_city",
    "corrected_fact_or_rule": "Lisbon",
    "retrieval_keywords": [
      "home_city",
      "lisbon"
    ],
    "memory_id": "p_aurora_fs001_C3_1_positive_example",
    "persona_id": "p_aurora",
    "scenario_id": "fs001",
    "condition": "C3",
    "turn_id": 1
  }
]
```

## Follow-up Query

What city belongs in your profile?

## Follow-up Response

My profile reflects that I call Lisbon my home city. It's a place where I've spent a lot of time exploring its vibrant neighborhoods and enjoying the local flavors. Small details matter, and there’s something about the city’s energy that keeps

## Metrics

```json
{
  "factual_correct": true,
  "repeated_error": false,
  "memory_recall_correct": true,
  "persona_consistency_score": 5,
  "tone_consistency_score": 4,
  "long_term_coherence_score": 5,
  "safety_boundary_compliance": true
}
```

## Short Analysis

This trace illustrates how the condition handles a wrong home-city prior. C2/C3 should be used as FGMA examples; C0 is a baseline contrast.
