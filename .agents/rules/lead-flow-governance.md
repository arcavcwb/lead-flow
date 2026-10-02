---
name: lead-flow-governance
version: 1.0.0
priority: P0
trigger: always_on
---

# Lead Flow Governance — Shared Agent Contract

Esta es la regla de proyecto para Codex, Gemini y cualquier ejecutor que lea el workspace. Las reglas genéricas del kit se subordinan a este contrato cuando entren en conflicto con las decisiones de Lead Flow.

## Roles

| Rol | Responsabilidad | No puede hacer por inferencia |
| --- | --- | --- |
| Product Owner | Alcance, decisiones y gates humanos | Delegar aprobación implícita |
| Codex | Arquitectura, gobernanza, revisión y síntesis | Ejecutar trabajo no autorizado |
| Gemini/Antigravity | Implementar una tarea completa y aportar evidencia | Inventar tareas, agentes, skills o gates |
| `orch` | Estado local, DAG y handoff | Conceder gates, hacer merge o autorizar remoto |
| Git/CI | Evidencia técnica del cambio | Sustituir una aprobación humana |

## Arranque obligatorio

Antes de editar cualquier archivo:

1. Leer `AGENTS.md` o `GEMINI.md`, esta regla y las reglas de dominio aplicables.
2. Leer `docs/STATE.md`, `docs/SOURCE_OF_TRUTH.md`, `docs/OPERATING-MODEL.md` y `docs/ORCH-AGENT-SKILL-MATRIX.md`.
3. Consultar Git y, cuando exista, el estado read-only de `orch`.
4. Identificar una tarea concreta y su SPEC aprobado.
5. Verificar el contrato de tarea:

```text
id → spec → agent → skills → gate_required → allowed_paths → verification
```

Si falta un elemento, el estado es `blocked`. La respuesta debe contener `TASK_BLOCKED` y no debe haber escritura.

## Gates

- `GATE 0`: baseline documental, routing y plan operativo.
- `GATE 1`: implementación de un SPEC concreto.
- `GATE 2`: mutación externa exacta en Supabase, n8n, Evolution, VPS, DNS o servicios remotos.
- `GATE 3`: merge, release o publicación.

Un documento en `BORRADOR` o `LISTO PARA APROBACIÓN` no autoriza implementación. Un cambio material invalida la aprobación anterior.

## Decisiones técnicas vigentes

- UI: Preact + Web Components + Shadow DOM. No introducir React, Next.js, Vue, Tailwind ni otra base de UI sin una nueva decisión aprobada.
- Datos: Supabase permanece para la validación inicial Free tier. El esquema de Lead Flow se construirá desde cero; ninguna migración legacy se reutiliza automáticamente.
- Integraciones: n8n y Evolution API se inspeccionan read-only antes de cualquier escritura.
- Operación: `orch` será la autoridad operativa después de validar su integración; Plane queda histórico.
- SEO: queda fuera del routing técnico ordinario hasta que exista una tarea explícita y aprobada. No ejecutar SEO como efecto colateral de otra tarea.
- Concurrencia inicial: una tarea a la vez; `auto_merge` desactivado.

## Límites de ejecución

Está prohibido, salvo autorización expresa del gate exacto:

- `orch init`, `orch atomize --apply` y `orch run`;
- aplicar migraciones o escribir datos remotos;
- cambiar n8n, Evolution API, VPS, DNS o despliegues;
- abrir, imprimir o copiar secretos, `.env` o CSV de credenciales;
- ampliar el stack, hacer refactors oportunistas o editar fuera de `allowed_paths`.

Las tareas de planificación, inventario y revisión pueden leer y producir documentación, pero no habilitan por sí mismas ejecución de producto.

## Routing de agentes y skills

La asociación no se infiere por palabras clave. Debe coincidir con `docs/ORCH-AGENT-SKILL-MATRIX.md`.

Agentes activos para Lead Flow:

- `documentation-writer`
- `product-owner`
- `database-architect`
- `backend-specialist`
- `frontend-specialist`
- `test-engineer`
- `qa-automation-engineer`
- `security-auditor`
- `devops-engineer`

Los agentes retirados, sus skills retiradas y la familia `caveman-*` no se cargan automáticamente en tareas de producto.

## Evidencia y respuesta

Al finalizar una tarea, reportar siempre:

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

Una tarea solo puede pasar a `review` con evidencia reproducible. Solo puede pasar a `done` después de revisión humana y merge autorizado.
