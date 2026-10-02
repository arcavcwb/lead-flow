# Plan maestro de ejecución — Lead Flow

> Estado: **GATE 0 APROBADO; commit documental pendiente**
> Versión: 2.0
> Fecha base: 2026-10-02
> Este archivo planifica trabajo futuro. **No autoriza implementación, despliegues ni cambios remotos.**

## Objetivo

Validar que Lead Flow puede capturar un prospecto desde una web, persistirlo de forma segura y entregar una alerta al vendedor en menos de cinco segundos, con recuperación automática ante fallos y evidencia suficiente para operar un piloto pagado.

## Regla de ejecución

Cada ticket debe pasar por `SPEC → aprobación humana → implementación → pruebas → revisión → merge humano`. Gemini/Antigravity no puede usar este plan como sustituto del SPEC ni cruzar un gate por cuenta propia.

## Secuencia

| Orden | Ticket | Resultado verificable | Dependencias |
| --- | --- | --- | --- |
| 1 | `LEADFLOW-01` | Gobernanza v2 sincronizada, secretos fuera del árbol y estado real documentado | GATE 0 |
| 2 | `LEADFLOW-02` | Monorepo y Supabase local reproducibles desde un clon limpio; inventario Free remoto solo lectura preparado | 01 |
| 3 | `LEADFLOW-03` | CI honesto: lint, tipos, pruebas y builds fallan ante errores o paquetes ausentes | 02 |
| 4 | `LEADFLOW-05` | Esquema multi-tenant, grants explícitos y RLS probados localmente | 03 |
| 5 | `LEADFLOW-06` | Endpoints de configuración y captura con validación, consentimiento, idempotencia y abuso controlado | 05 |
| 6 | `LEADFLOW-08` | Outbox durable, reintentos e integración gobernada con n8n + Evolution API existentes | 06 |
| 7 | `LEADFLOW-04` | SDK mínimo con Preact interno, expuesto como Web Component aislado y compilable | 03, 06 |
| 8 | `LEADFLOW-07` | Formulario config-driven, accesible y sin código por cliente | 04, 06 |
| 9 | `LEADFLOW-09` | E2E, seguridad, resiliencia y métricas de rendimiento con evidencia | 07, 08 |
| 10 | `LEADFLOW-11` | Privacidad, retención, atención al titular y runbook de incidentes aprobados | 05, 06 |
| 11 | `LEADFLOW-10` | Staging desplegado y demo operativa; producción sigue detrás de gate | 09, 11 |
| 12 | `LEADFLOW-12` | Piloto de 1–3 clientes medido; decisión de continuar, corregir o detener | 10 |

## Ruta crítica

`01 → 02 → 03 → 05 → 06 → 08 → 09 → 10 → 12`

`04` y `07` pueden avanzar después de estabilizar el contrato de `06`. `11` puede avanzar en paralelo con `08–09`, pero debe terminar antes de cualquier piloto externo.

## Stop conditions

Detener y devolver el ticket a refinamiento si ocurre cualquiera de estas condiciones:

- El SPEC contradice `docs/1_PRD.md` o `docs/3_ARCHITECTURE.md`.
- Falta una decisión humana que cambia seguridad, costo, proveedor o alcance.
- Un comando devuelve verde sin ejecutar trabajo real.
- Se necesita una credencial no disponible en el almacén autorizado.
- La implementación exige escribir en un servicio remoto sin `GATE 2`.
- La prueba requiere datos personales reales sin consentimiento y entorno aprobado.

## MVP terminado cuando

- 20 de 20 solicitudes válidas se persisten una sola vez.
- La inserción directa anónima en la bóveda es rechazada.
- 20 de 20 eventos llegan al proveedor o quedan pendientes de reintento durable.
- Una caída deliberada del proveedor no pierde ni duplica el lead.
- La latencia `submission_received → provider_accepted` cumple `p95 ≤ 5 s` en el entorno piloto definido.
- El widget funciona en HTML plano y WordPress sin contaminación CSS.
- Consentimiento, retención, eliminación y trazabilidad están documentados y probados.
- Al menos un piloto confirma disposición real a pagar; de lo contrario no se declara product-market fit.

## Documentos que gobiernan este plan

- Producto: `docs/1_PRD.md`
- Arquitectura: `docs/3_ARCHITECTURE.md`
- Calidad: `docs/5_QA_PROTOCOL.md`
- Decisiones y riesgos: `docs/6_ARCHITECT_REVIEW.md`
- Operación de agentes: `docs/OPERATING-MODEL.md`
- Handoffs y gates: `docs/HANDOFF-PROTOCOL.md`
- Estado factual: `docs/STATE.md`
