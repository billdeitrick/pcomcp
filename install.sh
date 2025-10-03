#! /bin/bash

uv run fastmcp install claude-desktop app.py --project "$(dirname "$0")" --env-file .env
