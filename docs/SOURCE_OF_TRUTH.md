# Fuente de verdad — Lead Flow

> Versión: 2.0
> Estado: **APROBADO COMO BASELINE; COMMIT PENDIENTE**
> Propósito: evitar que orch, Git, documentos y sesiones de IA produzcan instrucciones incompatibles.

## 1. Autoridad por tipo de información

No existe una única herramienta que gobierne todo. Cada tipo de información tiene una autoridad concreta:

| Información | Fuente canónica | Qué no la reemplaza |
| --- | --- | --- |
| Problema, usuarios y alcance | `docs/1_PRD.md` aprobado | Comentarios, código o marketing |
| Arquitectura y seguridad | `docs/3_ARCHITECTURE.md` + decisiones de `docs/6_ARCHITECT_REVIEW.md` | Un SPEC aislado o una migración existente |
| Orden de ejecución | `lead-flow-execution-plan.md` aprobado | El número del ticket o una sesión anterior |
| Contrato de un ticket | `docs/SPEC-LEADFLOW-XX.md` aprobado | Descripción breve de `tasks.json` |
| DAG y estado operativo | `tasks.json` + eventos/SQLite de orch | `STATE.md` sin sincronizar |
| Estado del código | Git, commit y PR concretos | Estado declarado por orch |
| Evidencia de calidad | Salida reproducible en CI vinculada al SHA | “Funcionó en mi sesión” |
| Autorización humana | Registro de gate versionado y, cuando aplique, aprobación del PR | Inferencias del agente u orch |

La autoridad de ejecución de agentes se comparte mediante `AGENTS.md`, `GEMINI.md` y `.agents/rules/lead-flow-governance.md`. Codex y Gemini pueden tener paneles distintos, pero deben leer el mismo contrato versionado.

## 2. Precedencia ante conflictos

1. Seguridad, privacidad y una instrucción humana explícita detienen cualquier acción incompatible.
2. El PRD aprobado define **qué** se construye.
3. La arquitectura aprobada define **cómo y dentro de qué límites**.
4. El SPEC aprobado concreta el ticket sin ampliar los dos anteriores.
5. Git demuestra lo que existe; orch registra en qué etapa de ejecución se encuentra.
6. `STATE.md` es un snapshot de arranque, no puede contradecir evidencia más reciente de Git u orch.

Si dos fuentes del mismo nivel se contradicen, Gemini debe marcar `BLOCKED_BY_CONFLICT`, citar ambas y detener la implementación. No elige silenciosamente la versión más conveniente.

## 3. Estados documentales

Cada documento contractual debe declarar uno de estos estados:

| Estado | Significado |
| --- | --- |
| `BORRADOR` | Puede analizarse, pero no autoriza trabajo |
| `LISTO PARA APROBACIÓN` | Completo y esperando gate humano |
| `APROBADO` | Puede gobernar trabajo dentro de su alcance y versión |
| `SUPERADO` | Se conserva como historia, no debe ejecutarse |

La aprobación debe registrar persona, fecha, versión y commit SHA. Una aprobación anterior no se hereda automáticamente después de cambios materiales.

## 4. Mapa documental

| Archivo | Responsabilidad exclusiva |
| --- | --- |
| `README.md` | Entrada rápida; no contiene decisiones nuevas |
| `lead-flow-execution-plan.md` | Secuencia, dependencias y stop conditions |
| `docs/1_PRD.md` | Producto y criterios de éxito |
| `docs/2_BUSINESS_MODEL.md` | Hipótesis de oferta, precio y costos |
| `docs/3_ARCHITECTURE.md` | Componentes, datos, API y seguridad |
| `docs/SUPABASE-FREE-TIER-READINESS.md` | Perfil remoto Free, cuotas, inventario y salida de plan |
| `docs/4_GO_TO_MARKET.md` | Descubrimiento y piloto comercial |
| `docs/5_QA_PROTOCOL.md` | Estrategia de verificación y release evidence |
| `docs/6_ARCHITECT_REVIEW.md` | ADR y registro de riesgos |
| `docs/OPERATING-MODEL.md` | Roles, permisos y gates |
| `docs/HANDOFF-PROTOCOL.md` | Transiciones y formatos de handoff |
| `docs/ORCH-SETUP.md` | Representación del flujo ejecutable en orch |
| `docs/ORCH-AGENT-SKILL-MATRIX.md` | Routing explícito de tarea, agente y skills |
| `docs/GATE-0-REVIEW.md` | Checklist y registro de decisión de la baseline; no concede el gate |
| `docs/PLANE-AGILE-SETUP.md` | Documento histórico superado; no ejecutar |
| `docs/STATE.md` | Snapshot factual y siguiente gate |
| `docs/SPEC-LEADFLOW-XX.md` | Contrato ejecutable de un solo ticket |
| `AGENTS.md` / `GEMINI.md` | Puente de roles y arranque común; no sustituyen un gate |
| `.agents/rules/lead-flow-governance.md` | Regla P0 de límites del ejecutor y handoff |

## 5. Reglas de actualización

- Una decisión de producto cambia primero el PRD y luego sus SPEC afectados.
- Una decisión arquitectónica material se registra primero en `6_ARCHITECT_REVIEW.md`.
- Un cambio de estado se realiza mediante orch y después se refleja en `STATE.md` cuando cambie el snapshot de gobernanza.
- Una implementación no puede editar retroactivamente el criterio para hacer pasar sus pruebas.
- Los enlaces externos deben incluir fecha de verificación cuando sustenten una decisión volátil.
- Los datos que no estén confirmados se escriben como `HIPÓTESIS`, nunca como hechos.

## 6. Secretos y datos personales

Nunca son fuente de verdad documental ni deben pegarse en tickets, comentarios, commits o logs:

- Contraseñas de base de datos.
- PAT y tokens OAuth.
- Claves secretas o `service_role`.
- API keys de mensajería.
- Archivos `.env` o CSV de credenciales.
- Payloads reales con nombres, teléfonos o emails.

Los documentos solo registran el **nombre lógico** de una variable y el sistema autorizado donde debe existir.

## 7. Arranque en frío

Una sesión nueva debe:

1. Leer `STATE.md` y comprobar Git de forma read-only.
2. Identificar el ticket y su estado real con `orch explain`, `orch tasks` y Git.
3. Leer este archivo, el plan maestro, PRD, arquitectura y SPEC.
4. Verificar que todos los gates requeridos existen.
5. Declarar alcance, archivos permitidos y comandos de verificación antes de editar.

Si falta alguno de esos elementos, la sesión puede investigar y redactar una propuesta, pero no implementar ni mutar servicios externos.
