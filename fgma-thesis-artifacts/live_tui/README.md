# FGMA Live TUI Demo

This optional demo runs a live wrong-prior recovery validation session against configured model APIs. It is included for inspection and local reproduction, but it does not include API credentials.

## Setup

```bat
install.bat
copy .env.example .env
```

Edit `.env` locally and add the API keys you are allowed to use. Do not commit `.env`.

## Run

```bat
run_live_tui.bat
```

Manual launch:

```bat
.venv\Scripts\activate
python scripts\fgma_live_tui.py --quick-demo --model deepseek_chat --case-id fs001 --condition C2
```

The demo writes runtime logs to `outputs/live_tui/`, which is ignored by Git.
