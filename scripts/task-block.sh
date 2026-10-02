#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?task-block.sh <task-id> \"<reason>\" <author>}"
REASON="${2:?missing reason}"
AUTHOR="${3:-agent}"
PROJECT_ROOT="${PROJECT_ROOT:-.}"
exec orch task-status "$TASK_ID" blocked --author "$AUTHOR" --note "$REASON" --project-root "$PROJECT_ROOT"
