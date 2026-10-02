# Lead Flow — Agent Contract

> Estado: BORRADOR PARA GATE 0. Este archivo gobierna la lectura y el handoff; no autoriza trabajo de producto.

Lead Flow se trabaja con una separación explícita de responsabilidades:

- El Product Owner decide el alcance y concede los gates.
- Codex actúa como cerebro de arquitectura, gobernanza y revisión.
- Gemini dentro de Antigravity ejecuta únicamente tareas autorizadas.
- `orch` es el registro operativo local y el mecanismo de handoff.
- Git y la evidencia reproducible demuestran el resultado técnico.

## Antes de cualquier cambio

1. Leer `.agents/rules/lead-flow-governance.md` y las reglas aplicables de `.agents/rules/`.
2. Leer `docs/STATE.md`, `docs/SOURCE_OF_TRUTH.md`, `docs/OPERATING-MODEL.md` y el SPEC de la tarea.
3. Confirmar que existe una tarea de `orch` con `id`, `spec`, `agent`, `skills`, `gate_required`, `allowed_paths` y `verification`.
4. Si falta un campo, hay conflicto documental o el gate no está aprobado, investigar y reportar; no editar.
5. No inicializar `orch`, ejecutar tareas, aplicar migraciones ni escribir en servicios remotos sin autorización explícita.

## Decisiones vigentes

- Frontend: Preact dentro de Web Components y Shadow DOM.
- Backend/DB: Supabase se conserva para validación en Free tier; no se elimina.
- Integraciones: n8n y Evolution API existentes se inspeccionan primero; cualquier escritura remota requiere GATE 2.
- Operación: `orch` sustituirá a Plane como autoridad operativa cuando la integración pase GATE 0; Plane queda histórico.
- SEO: no forma parte de la ejecución técnica ordinaria; se mantiene fuera del routing de producto hasta que exista una tarea explícita.

## Formato de salida del ejecutor

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

La fuente detallada de routing es `docs/ORCH-AGENT-SKILL-MATRIX.md`. La integración de `orch` está descrita en `docs/ORCH-SETUP.md` y sigue bloqueada hasta el gate correspondiente.
