# GATE 1 — LEADFLOW-01

> Estado: **APROBADO POR EL PRODUCT OWNER**
> Baseline revisada: `9873666`
> Fecha: 2026-10-02

## Aprobación humana

```text
Persona: Product Owner
Decisión: APROBADO GATE 1 para LEADFLOW-01
Autorización: Gemini/Antigravity puede ejecutar únicamente este alcance
Prohibiciones: Supabase, n8n, Evolution API, servicios remotos y despliegues
Registro: aprobación explícita recibida en la sesión del 2026-10-02
```

## Ticket

- ID: `LEADFLOW-01`
- SPEC: `docs/SPEC-LEADFLOW-01.md`
- Agente executor: `documentation-writer`
- Executor operativo: Gemini mediante Antigravity (`agy/gemini-3.8-flash-low`)
- Revisor: Codex (`gpt-5.6-luna`, esfuerzo `medium`)
- Skills: `documentation-templates`, `bash-linux`, `verify-and-stop`

## Alcance permitido

- Revisar gobernanza, estado factual y trazabilidad.
- Confirmar que `tasks.json` representa el DAG sin duplicados.
- Confirmar que agente, skills, gate y allowlist se resuelven.
- Verificar ignores y referencias sin abrir secretos.
- Ejecutar validaciones estáticas de orch, Git y documentación.
- Preparar evidencia y handoff para revisión de Codex.

## Alcance prohibido

- Implementar producto.
- Crear o modificar schema/migraciones de Supabase.
- Escribir en Supabase, n8n, Evolution API, VPS, DNS o cualquier servicio remoto.
- Ejecutar `orch run`, `orch init` o `orch atomize --apply`.
- Abrir, imprimir, versionar o rotar secretos.
- Hacer merge, deploy o declarar `done`.

## Archivos permitidos

```text
AGENTS.md
GEMINI.md
.agents/rules/lead-flow-governance.md
.agents/workflows/lead-flow-execute.md
README.md
docs/
.gitignore
tasks.json
.orchestrator/config.yaml
.orchestrator/model_router.yaml
.orchestrator/budgets.yaml
scripts/task-*.sh
```

## Validación requerida

```text
orch validate --json
orch router validate --json
orch tasks --json
git diff --check
git status --short
```

La evidencia debe informar explícitamente si existe alguna discrepancia entre
Git, `STATE.md`, `tasks.json` y el estado SQLite de orch.

## Handoff esperado

```text
TASK_ID: LEADFLOW-01
AGENT: documentation-writer
SKILLS: documentation-templates, bash-linux, verify-and-stop
GATE: GATE 1 — pendiente de aprobación
SCOPE: gobernanza, trazabilidad y validación estática
CHANGES: lista exacta de archivos modificados
VALIDATION: comandos y resultados
BLOCKERS: discrepancias o ninguno
NEXT_ACTION: revisión Codex y decisión del Product Owner
```

El gate quedó concedido únicamente para este ticket y este alcance. Las demás
tareas permanecen sin autorización. El estado de `orch` puede pasar a ejecución
controlada solo mediante `orch run --only LEADFLOW-01 --max-tasks 1 --no-push`.
