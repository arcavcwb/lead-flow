# Revisión de GATE 0 — Lead Flow

> Estado: **APROBADO — baseline consolidada en `39f954e`**
> Fecha de preparación: 2026-10-02
> La aprobación fue confirmada por el Product Owner en la sesión del 2026-10-02. El SHA final debe registrarse cuando se consolide la baseline en un commit.

## Objetivo

Aprobar o rechazar la baseline documental y las reglas de operación antes de crear `tasks.json`, inicializar la integración de `orch` o ejecutar cualquier tarea de producto.

## Baseline a revisar

- [x] [`docs/1_PRD.md`](1_PRD.md)
- [x] [`docs/2_BUSINESS_MODEL.md`](2_BUSINESS_MODEL.md)
- [x] [`docs/3_ARCHITECTURE.md`](3_ARCHITECTURE.md)
- [x] [`docs/4_GO_TO_MARKET.md`](4_GO_TO_MARKET.md)
- [x] [`docs/5_QA_PROTOCOL.md`](5_QA_PROTOCOL.md)
- [x] [`docs/6_ARCHITECT_REVIEW.md`](6_ARCHITECT_REVIEW.md)
- [x] [`docs/OPERATING-MODEL.md`](OPERATING-MODEL.md)
- [x] [`docs/HANDOFF-PROTOCOL.md`](HANDOFF-PROTOCOL.md)
- [x] [`docs/SOURCE_OF_TRUTH.md`](SOURCE_OF_TRUTH.md)
- [x] [`lead-flow-execution-plan.md`](../lead-flow-execution-plan.md)
- [x] [`docs/ORCH-SETUP.md`](ORCH-SETUP.md)
- [x] [`docs/ORCH-AGENT-SKILL-MATRIX.md`](ORCH-AGENT-SKILL-MATRIX.md)

## Decisiones que deben quedar confirmadas

- [x] Producto: Lead Flow como vertical para 1–3 pilotos.
- [x] Frontend: Preact interno + Web Component + Shadow DOM.
- [x] Datos: Supabase se conserva para validación Free tier.
- [x] Operación: `orch` sustituirá a Plane como autoridad operativa cuando pase su validación.
- [x] Ejecución: Gemini/Antigravity implementa; Codex revisa; el Product Owner concede gates.
- [x] Integraciones: n8n y Evolution solo se inspeccionan read-only hasta GATE 2.
- [x] SEO: queda fuera de la ejecución técnica ordinaria salvo tarea explícita.
- [x] Concurrencia: una tarea; `auto_merge: false`.

## Bloqueos antes de registrar la aprobación

- [x] El CSV potencialmente sensible fue retirado del workspace sin abrir su contenido y no está versionado.
- [x] La migración local antigua fue retirada del workspace; LEADFLOW-05 nace desde un esquema limpio.
- [x] El Product Owner confirmó las decisiones de producto, stack, Supabase, orch y roles de agentes.
- [x] El worktree fue separado en cambios revisables antes del commit de baseline.
- [x] Se registró el commit SHA exacto de la baseline aprobada.

## Registro de decisión

```text
Decisión: APROBADO PARA PREPARAR LA INTEGRACIÓN DE ORCH
Persona: Product Owner
Fecha: 2026-10-02
Commit SHA revisado: 39f954e
Alcance aprobado: Lead Flow, Preact, Supabase Free, orch, Gemini ejecutor, Codex revisor
Exclusiones: producto, remoto, despliegue, WhatsApp real, SEO incidental
Observaciones: diff de orch aprobado por el Product Owner; integración manual aplicada y validada sin ejecución de producto
```

## Después de aprobar

La integración manual de `orch` quedó aplicada y validada. La primera tarea de producto autorizable seguirá siendo `LEADFLOW-01`, pero requiere su propio GATE 1; no se debe usar `orch init` ni el estado `todo` como autorización de ejecución.
