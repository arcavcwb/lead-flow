# STATE — Lead Flow

> Snapshot del repositorio: **2026-10-02**
> Orquestación: **orch v0.16.0 instalado; integración manual validada; commit pendiente**
> Baseline v2: **GATE 0 APROBADO; commit documental pendiente**
> Gobernanza de agentes: **puente AGENTS/GEMINI + regla P0 + workflow controlado preparados; no autorizan ejecución**

## 1. Qué debe saber una sesión nueva

Lead Flow está replanificado como una vertical de captura y entrega durable. GATE 0 y el diff específico fueron aprobados; la integración manual de orch está validada. Esto todavía no autoriza ejecutar producto ni mutar servicios remotos.

Lectura: `AGENTS/GEMINI → reglas P0 → SOURCE_OF_TRUTH → plan maestro → PRD → arquitectura → modelo operativo → SPEC del ticket`.

## 2. Realidad observada del repositorio

- Branch observado: `main`, alineado con `origin/main` al iniciar la revisión.
- Existen commits de LEADFLOW-01/02/03 y configuración de Husky/CI.
- No existe `apps/sdk` ni implementación de Edge Functions.
- Existe `supabase/config.toml`.
- El Product Owner cree que existe un proyecto Supabase Free, pero no se ha realizado inventario remoto; tratarlo como no verificado.
- La migración local antigua fue retirada del workspace; LEADFLOW-05 comenzará con un esquema nuevo y revisable desde cero.
- Existen varias skills nuevas no trackeadas; pertenecen al usuario y quedan fuera de este plan.
- El CSV potencialmente sensible fue retirado del workspace sin abrir su contenido y quedó en cuarentena temporal fuera del repositorio. No se versiona.
- `.env` está ignorado; sus valores no fueron inspeccionados.

## 3. Quality gate observado antes de la replanificación

| Comando | Resultado observado | Interpretación |
| --- | --- | --- |
| `pnpm lint` | FAIL: ESLint no encontró archivos para `.` | Gate no operativo |
| `pnpm typecheck` | FAIL: `--workspaces` no es opción de TypeScript | Gate no operativo |
| `pnpm build:sdk` | Exit 0, pero ningún proyecto coincide con `sdk` | Falso verde |
| `pnpm test` | Exit 0 ejecutando un `echo` | Falso verde |

No volver a llamar “verde” al repositorio hasta que `LEADFLOW-03` demuestre fallos deliberados y pases reales.

## 4. Estado documental v2

| Documento | Estado |
| --- | --- |
| PRD, negocio, arquitectura, GTM, QA, ADR | Baseline aprobada; commit pendiente |
| Plan maestro | Baseline aprobada; commit pendiente |
| Modelo operativo, handoff y orch setup | Baseline aprobada; commit pendiente |
| SPEC 01/02/03/05 | Deben revalidarse bajo baseline v2; no están aprobados automáticamente |
| SPEC 04/06/07/08/09/10/11/12 | A redactar just-in-time por el Analista después de priorización |

## 5. Evaluación de tickets basada solo en Git

Esta tabla es la fuente para crear el primer `tasks.json`; no autoriza `orch run`.

| Ticket | Evidencia actual | Estado recomendado al sincronizar |
| --- | --- | --- |
| `01` | Gobernanza y artefactos legacy tratados; commit de baseline pendiente | Integración de orch validada; requiere GATE 1 |
| `02` | Workspace/Supabase parcial; falta reproducibilidad comprobada | Backlog |
| `03` | CI existe, pero gates rotos/falsos verdes | Backlog prioritario |
| `04` | SDK ausente | Backlog |
| `05` | No existe migración legacy; schema debe nacer desde cero | Backlog; SPEC nuevo |
| `06` | API ausente | Backlog |
| `07` | Formulario ausente | Backlog |
| `08` | Outbox/entrega ausentes | Backlog |
| `09` | E2E ausente | Backlog |
| `10` | Deploy objetivo no verificado | Backlog |
| `11` | Privacidad/runbooks ausentes | Crear en Backlog just-in-time |
| `12` | Piloto/economía sin evidencia | Crear en Backlog tras GATE 0 |

## 6. Decisiones vigentes propuestas

- Nombre del producto: **Lead Flow**.
- MVP: vertical completa para 1–3 pilotos, no plataforma de 50 clientes.
- Browser → Edge Functions; sin acceso directo a tablas.
- SDK como Web Component con Shadow DOM; Preact fue elegido por el Product Owner como implementación interna y no forma parte del contrato público. Implementación aún bloqueada por los gates.
- Lead + outbox atómicos.
- Se usarán las instancias existentes de n8n y Evolution API, preservándolas hasta completar inventario read-only y GATE 2.
- Evolution API sigue detrás de un adaptador; su modo real de conexión (Baileys o Cloud API oficial) está pendiente de verificación.
- n8n sigue sujeto a validación de licencia para el modelo comercial.
- Objetivos de rendimiento no son SLA.
- Privacidad y retención bloquean producción.
- Supabase Free es el perfil propuesto para MVP/piloto; sus cuotas y estado remoto se validan antes de cualquier GATE 2.

La baseline de decisiones ya tiene GATE 0 aprobado; cada SPEC sigue requiriendo su propio GATE 1 antes de implementación.

## 7. Próximo paso autorizado

Con la integración de orch preparada, el siguiente alcance permitido es:

- Revisar `docs/ORCH-INTEGRATION-DIFF.md` y los archivos operativos aplicados.
- Consultar Git y la ayuda/configuración de orch en modo read-only.
- Preparar un GATE 1 concreto antes de cualquier tarea de producto.

La decisión y sus límites están registrados en `docs/GATE-0-REVIEW.md`. El commit SHA final de la baseline sigue pendiente.

La primera sesión Gemini debe asumir rol de **Analista/Orch Integration**, no Implementador:

```text
Revisa docs/STATE.md, docs/SOURCE_OF_TRUTH.md, docs/ORCH-SETUP.md y
lead-flow-execution-plan.md. Propón el diff exacto de tasks.json, configuración y
scripts. No ejecutes orch init, atomize --apply ni orch run. No implementes producto.
```

Probe read-only de `orch`: `orch atomize --list --file docs/SPEC-LEADFLOW-01.md` quedó bloqueado porque faltan `tasks.json` y `scripts/task-start.sh`; no escribió archivos.

## 8. Condiciones de alarma

Detener inmediatamente si:

- Alguien propone reutilizar una migración legacy o aplicar schema remoto sin el SPEC aprobado.
- Una credencial aparece en diff, log o ticket.
- orch dice `done` pero Git/CI no contiene evidencia.
- Un agente afirma que el plan aprobado equivale a SPEC aprobado.
- Se solicita modificar n8n/Evolution API o enviar WhatsApp real sin consentimiento, inventario y GATE 2.
