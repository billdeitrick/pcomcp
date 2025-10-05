#! /bin/bash
echo "Installing in project dir: $(dirname "$0")"

uv run fastmcp install claude-desktop app.py --project "$(dirname "$0")" --env-file .env
