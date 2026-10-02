#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?task-start.sh <task-id> [--author <author>] [--project-root PATH]}"
shift || true
AUTHOR="orch"
PROJECT_ROOT="."
while [[ $# -gt 0 ]]; do
  case "$1" in
    --author) AUTHOR="$2"; shift 2 ;;
    --project-root) PROJECT_ROOT="$2"; shift 2 ;;
    *) shift ;;
  esac
done
echo "Lead Flow task-start blocked: SPEC/GATE validation is required before execution." >&2
exit 78
