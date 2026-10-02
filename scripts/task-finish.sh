#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?task-finish.sh <task-id> \"<summary>\" <author>}"
SUMMARY="${2:?missing summary}"
AUTHOR="${3:-agent}"
echo "Lead Flow task-finish blocked: Codex review and human merge gate are required." >&2
exit 78
