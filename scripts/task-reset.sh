#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?task-reset.sh <task-id> [author] [note]}"
AUTHOR="${2:-orch}"
NOTE="${3:-reset}"
echo "Lead Flow task-reset blocked: explicit human review is required." >&2
exit 78
