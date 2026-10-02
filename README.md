# Lead Flow

Lead Flow captura prospectos desde sitios existentes, los guarda antes de cualquier integración externa y entrega una alerta al equipo comercial con trazabilidad de extremo a extremo.

## Estado actual

El proyecto está en **replanificación v2**. La arquitectura y la gobernanza fueron aprobadas para preparar la integración de `orch`, pero Gemini todavía no puede implementar tickets sin SPEC y GATE 1.

No se debe interpretar la presencia de scaffolding, configuración de CI o migraciones como una entrega terminada. El estado verificable se mantiene en [`docs/STATE.md`](docs/STATE.md).

## Resultado que se quiere validar

```text
Prospecto → widget → captura segura → persistencia + outbox
                                      ↓
                               entrega + reintentos
                                      ↓
                                   vendedor
```

El objetivo piloto es que la alerta sea aceptada por el proveedor de mensajería en `p95 ≤ 5 s`, sin perder ni duplicar el lead cuando una integración falle.

## Lectura obligatoria para Gemini/Antigravity

1. [`AGENTS.md`](AGENTS.md) y [`GEMINI.md`](GEMINI.md) — roles y contrato compartido.
2. [`docs/STATE.md`](docs/STATE.md) — realidad actual y bloqueos.
3. [`docs/SOURCE_OF_TRUTH.md`](docs/SOURCE_OF_TRUTH.md) — precedencia documental.
4. [`docs/ORCH-AGENT-SKILL-MATRIX.md`](docs/ORCH-AGENT-SKILL-MATRIX.md) — asociación tarea/agente/skills.
5. [`lead-flow-execution-plan.md`](lead-flow-execution-plan.md) — orden y dependencias.
6. [`docs/1_PRD.md`](docs/1_PRD.md) — contrato de producto.
7. [`docs/3_ARCHITECTURE.md`](docs/3_ARCHITECTURE.md) — límites técnicos.
8. [`docs/SUPABASE-FREE-TIER-READINESS.md`](docs/SUPABASE-FREE-TIER-READINESS.md) — límites, inventario y salida de Free.
9. [`docs/OPERATING-MODEL.md`](docs/OPERATING-MODEL.md) — roles y permisos.
10. [`docs/HANDOFF-PROTOCOL.md`](docs/HANDOFF-PROTOCOL.md) — estados, gates y evidencia.
11. El SPEC aprobado del ticket asignado.

## Regla de inicio

Gemini no debe empezar implementación porque una tarea aparezca en `tasks.json`. Solo puede hacerlo cuando el ticket esté `ready`, tenga un SPEC con estado `APROBADO` y el humano haya registrado el gate correspondiente en el repositorio. `orch run` nunca concede autoridad por sí mismo.

Las migraciones, despliegues, envíos reales de WhatsApp y cualquier otra escritura remota requieren además `GATE 2` explícito.

## Documentación

| Documento | Propósito |
| --- | --- |
| [`docs/1_PRD.md`](docs/1_PRD.md) | Problema, usuarios, alcance y éxito del MVP |
| [`docs/2_BUSINESS_MODEL.md`](docs/2_BUSINESS_MODEL.md) | Oferta y economía como hipótesis medibles |
| [`docs/3_ARCHITECTURE.md`](docs/3_ARCHITECTURE.md) | Arquitectura objetivo y fronteras de seguridad |
| [`docs/SUPABASE-FREE-TIER-READINESS.md`](docs/SUPABASE-FREE-TIER-READINESS.md) | Perfil Free, inventario remoto y límites operativos |
| [`docs/4_GO_TO_MARKET.md`](docs/4_GO_TO_MARKET.md) | Descubrimiento, piloto y reglas de claims |
| [`docs/5_QA_PROTOCOL.md`](docs/5_QA_PROTOCOL.md) | Pruebas y evidencia obligatoria |
| [`docs/6_ARCHITECT_REVIEW.md`](docs/6_ARCHITECT_REVIEW.md) | ADR, riesgos y disparadores de revisión |
| [`docs/ORCH-SETUP.md`](docs/ORCH-SETUP.md) | Diseño de integración y operación local de orch |
| [`AGENTS.md`](AGENTS.md) / [`GEMINI.md`](GEMINI.md) | Puente compartido para Codex y Gemini |
| [`docs/ORCH-AGENT-SKILL-MATRIX.md`](docs/ORCH-AGENT-SKILL-MATRIX.md) | Routing explícito de tareas |
| [`docs/GATE-0-REVIEW.md`](docs/GATE-0-REVIEW.md) | Checklist para aprobar la baseline antes de orch |

## Restricciones no negociables

- No publicar secretos, `.env`, PAT, contraseñas ni claves de servicio.
- No exponer tablas internas directamente al navegador.
- No hacer self-merge ni autoaprobar gates.
- No prometer SLA, escala, margen o clientes sin evidencia.
- No prometer SLA sobre Evolution API hasta inventariar la instancia existente, confirmar si usa Baileys o WhatsApp Cloud API y medir su operación.
- No marcar un ticket como hecho con comandos vacíos, omitidos o falsamente verdes.
