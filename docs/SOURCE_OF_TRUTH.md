# Lead Flow Engine: Fuente de Verdad (v1.0)

Este directorio contiene toda la documentación técnica, comercial y operativa del **Motor de Captura B2B**, consolidada en el PRD Maestro v1.0 y el Modelo Operacional del squad IA.

Esta documentación es la **única fuente de verdad** para el desarrollo, ventas y control de calidad del ecosistema Lead Flow Engine. Cualquier decisión técnica o comercial que contradiga estos documentos debe ser primero aprobada y luego reflejada aquí.

---

## Documentos — Estrategia y Producto

| # | Documento | Descripción |
| :-- | :--- | :--- |
| 1 | [1_PRD.md](./1_PRD.md) | PRD Maestro — Visión, Personas, KPIs, Alcance, Modelo de Datos |
| 2 | [2_BUSINESS_MODEL.md](./2_BUSINESS_MODEL.md) | Modelo de Negocio — Tiers, Unit Economics, Ventaja Competitiva |
| 3 | [3_ARCHITECTURE.md](./3_ARCHITECTURE.md) | Arquitectura — Las 4 Capas, Flujo de Datos, Schema de BD |
| 4 | [4_GO_TO_MARKET.md](./4_GO_TO_MARKET.md) | Go-To-Market — Outbound, Simulador en Vivo, Manejo de Objeciones |
| 5 | [5_QA_PROTOCOL.md](./5_QA_PROTOCOL.md) | Protocolo QA — 4 Escenarios Críticos + Checklist de Pre-Deploy |
| 6 | [6_ARCHITECT_REVIEW.md](./6_ARCHITECT_REVIEW.md) | Revisión Arquitectónica — Riesgos, Decisiones y Alternativas Descartadas |

## Documentos — Modelo Operacional del Squad IA

| Documento | Descripción |
| :--- | :--- |
| [OPERATING-MODEL.md](./OPERATING-MODEL.md) | Modelo operacional completo: roles, modelos IA (Pro/Flash), ciclo de tickets, Gates humanos |
| [HANDOFF-PROTOCOL.md](./HANDOFF-PROTOCOL.md) | Protocolo de transiciones: tabla maestra T0→T5, etiquetas Plane, DoR y DoD |
| [PLANE-AGILE-SETUP.md](./PLANE-AGILE-SETUP.md) | Arquitectura del espacio de trabajo en Plane (Cycles, Modules, Views, Pages) |
| [STATE.md](./STATE.md) | Estado vivo del proyecto: entregas, convenciones, línea de handoff |

---

## Modelo Operacional (resumen ejecutivo)

**Un solo motor IA — Antigravity/Gemini — con selección de modelo por tarea:**

| Tarea | Modelo | Rol |
| --- | --- | --- |
| Análisis, SPEC, planning | **Gemini Pro** | Analista |
| Implementación de código | **Gemini Pro** | Implementador |
| Testing, validaciones Gherkin, linting | **Gemini Flash ⚡** | Tester |
| **Auditoría PR vs. SPEC** | **Claude Opus 🔵** | Revisor (perspectiva independiente) |
| Gates estratégicos (PRD, SPEC, Merge) | **Humano** | Product Owner |

**Flujo de un ticket:**
```
Backlog → Refinado → En desarrollo → En pruebas → En revisión → Hecho
            ↑ GATE 1 (humano)                         ↑ GATE final (merge)
```

---

## Principios No Negociables

1. **El lead nunca se pierde.** Supabase persiste primero, WhatsApp notifica después.
2. **Cero código a medida.** Toda personalización del cliente va a `clients_config`, no al código.
3. **El widget es inmune.** Shadow DOM garantiza que ningún CSS externo rompa el formulario.
4. **La infraestructura es fija.** El costo no crece linealmente con los clientes. El margen es ~90%.
5. **Plane es la única fuente de verdad operacional.** Lo que no está en Plane, no existe.
6. **Los Gherkin son el único criterio de aceptación.** Escenario sin test = criterio no cumplido.
7. **Flash para velocidad, Pro para profundidad.** Selección de modelo intencional en cada tarea.
