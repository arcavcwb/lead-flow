---
name: lead-flow-execute
description: Execute one approved Lead Flow task under orch, agent, skill and gate controls.
version: 1.0.0
requires_agents: orchestrator
requires_skills: verify-changes, verify-and-stop
artifact_outputs: changed-files, validation-report, handoff
---

# /lead-flow-execute — Controlled Handoff

$ARGUMENTS

## Contract

You are Gemini/Antigravity executing one task handed off by `orch`. Codex remains the architecture and review authority. The Product Owner remains the only person who grants gates.

## Pre-flight

1. Read `AGENTS.md`, `GEMINI.md`, `.agents/rules/lead-flow-governance.md`, `docs/SOURCE_OF_TRUTH.md`, `docs/STATE.md`, `docs/ORCH-SETUP.md` and `docs/ORCH-AGENT-SKILL-MATRIX.md`.
2. Resolve the task ID and read its SPEC.
3. Confirm `agent`, `skills`, `gate_required`, `allowed_paths` and `verification`.
4. Confirm the required gate is approved for the current document version/SHA.
5. If anything is missing or contradictory, stop with `TASK_BLOCKED` and perform no write.

## Execution rules

- Load only the assigned agent and allowlisted skills.
- Keep changes inside `allowed_paths`.
- Use Preact/Web Components/Shadow DOM for UI work.
- Do not run SEO as a side effect.
- Treat Supabase, n8n, Evolution, VPS, DNS and deploys as remote writes requiring GATE 2.
- Do not run `orch init`, `orch atomize --apply` or `orch run` unless the task itself explicitly carries the required authorization.
- Never expose secrets or real personal data.

## Handoff

Return exactly this evidence structure:

```text
TASK_ID:
AGENT:
SKILLS:
GATE:
SCOPE:
CHANGES:
VALIDATION:
BLOCKERS:
NEXT_ACTION:
```

Do not declare `done`; use `review` until Codex and the Product Owner approve the evidence and merge.
