# Matriz orch → agente → skills — Lead Flow

> Estado: **APLICADA EN `tasks.json`; VALIDACIÓN ESTÁTICA APROBADA; EJECUCIÓN BLOQUEADA**  
> Propósito: impedir que orch cree o despache tareas sin responsable técnico y contexto de skills explícito.  
> No autoriza `orch init`, `atomize --apply` ni `orch run`.

> Handoff: Codex define/revisa; `orch` registra y entrega; Gemini/Antigravity ejecuta una tarea aprobada; el Product Owner concede gates.

## 1. Regla central

Cada tarea de `tasks.json` debe poder resolver esta cadena sin inferencias:

```text
LEADFLOW-XX
  → SPEC aprobado
  → agente primario existente
  → skills permitidas y existentes
  → archivos permitidos
  → gate requerido
  → comandos de verificación
```

Si falta un elemento, la tarea queda `blocked` y no puede entrar en `ready`.

`orch atomize` puede extraer títulos, IDs, dependencias y contenido desde Markdown, pero no se considera responsable de inventar el agente o las skills. La asociación se declara en la fuente de routing aprobada y se valida antes de generar/aplicar `tasks.json`.

## 2. Contrato de routing

La integración debe conservar, como mínimo, estos campos lógicos por tarea:

```yaml
id: LEADFLOW-05
spec: docs/SPEC-LEADFLOW-05.md
agent: database-architect
skills:
  - database-design
  - migration
  - testing-patterns
  - vulnerability-scanner
gate_required: GATE 1
remote_write: false
allowed_paths:
  - supabase/
  - docs/SPEC-LEADFLOW-05.md
verification:
  - supabase local reset
  - grants/RLS tests
```

Los nombres de campos exactos que soporte la versión instalada de orch se deben confirmar contra su esquema/documentación antes de crear archivos. Este contrato lógico no autoriza asumir que cualquier clave YAML será entendida automáticamente.

## 3. Matriz inicial

| Tarea | Agente primario | Skills permitidas | Gate | Estado de preparación |
| --- | --- | --- | --- | --- |
| `LEADFLOW-01` | `documentation-writer` | `documentation-templates`, `bash-linux`, `verify-and-stop` | GATE 0 | Lista para revisión GATE 0 |
| `LEADFLOW-02` | `database-architect` | `database-design`, `migration`, `bash-linux`, `verify-changes` | GATE 1 | Requiere GATE 0 + SPEC aprobado |
| `LEADFLOW-03` | `test-engineer` | `testing-patterns`, `tdd-workflow`, `lint-and-validate`, `verify-changes` | GATE 1 | Requiere LEADFLOW-02 + SPEC aprobado |
| `LEADFLOW-05` | `database-architect` | `database-design`, `migration`, `testing-patterns`, `vulnerability-scanner` | GATE 1 | Schema nuevo desde cero; SPEC pendiente |
| `LEADFLOW-06` | `backend-specialist` | `api-patterns`, `nodejs-best-practices`, `database-design`, `vulnerability-scanner`, `testing-patterns` | GATE 1; GATE 2 si remoto | Routing listo; SPEC pendiente |
| `LEADFLOW-08` | `backend-specialist` | `api-patterns`, `nodejs-best-practices`, `migration`, `testing-patterns`, `vulnerability-scanner` | GATE 1; GATE 2 para n8n/Evolution | Routing listo; inventario remoto pendiente |
| `LEADFLOW-04` | `frontend-specialist` | `frontend-architecture`, `design-spec`, `frontend-design`, `web-design-guidelines`, `webapp-testing`, `lint-and-validate` | GATE 1 | Routing Preact listo; DESIGN.md y SPEC pendientes |
| `LEADFLOW-07` | `frontend-specialist` | `frontend-architecture`, `design-spec`, `web-design-guidelines`, `webapp-testing`, `testing-patterns` | GATE 1 | Routing Preact listo; SPEC pendiente |
| `LEADFLOW-09` | `qa-automation-engineer` | `webapp-testing`, `testing-patterns`, `lint-and-validate`, `verify-changes`, `vulnerability-scanner` | GATE 1 | Disponible; revisar alcance de seguridad |
| `LEADFLOW-11` | `security-auditor` | `vulnerability-scanner`, `api-patterns`, `documentation-templates`, `testing-patterns` | GATE 1; GATE 2 si real | Disponible |
| `LEADFLOW-10` | `devops-engineer` | `deployment-procedures`, `server-management`, `bash-linux`, `verify-changes` | GATE 1; GATE 2 | Routing listo; objetivo de staging pendiente |
| `LEADFLOW-12` | `product-owner` | `plan-writing`, `brainstorming`, `documentation-templates`, `verify-and-stop` | GATE 3/piloto | Disponible |

## 4. Skills que no se cargan por defecto

No se cargan por nombre del repositorio ni por disponibilidad global. Quedan fuera del routing de Lead Flow salvo cambio de alcance aprobado:

- skills de juegos, móvil nativo, Rust, Python, PowerShell, Tailwind, Next.js/React específico, SEO y GEO;
- `mcp-builder` salvo que el ticket construya un servidor MCP;
- `app-builder` salvo una reconstrucción autorizada del proyecto;
- `skillify` salvo creación deliberada de una skill nueva;
- familia `caveman-*` salvo observabilidad/costo de agentes solicitada explícitamente.

La skill `caveman` se conserva disponible como herramienta de comunicación/compresión, pero no se añade automáticamente a una tarea de producto.

## 5. Validaciones obligatorias antes de `tasks.json`

1. Cada `agent` tiene un archivo existente en `.agents/agent/`.
2. Cada skill referenciada existe en `.agents/skills/` o está declarada como dependencia externa autorizada.
3. No hay referencias a skills retiradas.
4. El agente primario puede leer el SPEC y operar solo en los archivos permitidos.
5. Las skills son suficientes para el ticket, pero no incluyen dominios irrelevantes.
6. El gate de la tarea coincide con `OPERATING-MODEL.md`.
7. `remote_write` es `false` para todo ticket que no tenga GATE 2 exacto.
8. El routing pasa revisión humana antes de `atomize --apply`.

## 6. Estado actual de los agentes

La limpieza de skills y la alineación de gobernanza ya corrigieron los manifests que participan en Lead Flow:

- `backend-specialist`: Node/API/DB, sin Python, PowerShell ni Rust;
- `devops-engineer`: operación Linux, sin PowerShell;
- `frontend-specialist`: Preact/Web Components/Shadow DOM, sin carga automática de React/Next/Tailwind;
- `orchestrator`: coordinación por contrato, sin dependencia del Agent Tool nativo;
- `game-developer`, `mobile-developer` y `seo-specialist`: manifiestos retirados y fuera del routing.

La validación de integridad sigue siendo obligatoria antes de generar `tasks.json`. Las referencias históricas que permanezcan dentro de documentos genéricos no son skills activas ni autorizan routing.

## 7. Orden correcto de integración

1. Validar que cada skill y agente de la matriz resuelven.
2. Confirmar el esquema real que `orch atomize` acepta.
3. Ejecutar `orch atomize --list` sobre un preview aislado.
4. Revisar el diff de tareas sin aplicarlo.
5. Solicitar GATE 0 para la integración.
6. Aplicar `tasks.json` solo después de la aprobación.
7. Validar `orch validate` y `orch router validate`.
8. Probar bloqueos de gate sin ejecutar una tarea de producto.

## 8. Criterio de terminado

- No existe tarea sin agente primario.
- No existe agente con skill ausente.
- Cada tarea tiene una allowlist de skills.
- El routing Preact no carga Next.js/Tailwind.
- LEADFLOW-05 carga skills de base de datos/migración/seguridad.
- LEADFLOW-08 carga skills de API/integración/reintentos, pero no obtiene autorización remota implícita.
- `atomize --list` muestra el DAG esperado en un preview.
- `tasks.json` se aplicó después de GATE 0 y la aprobación del diff; ninguna tarea se ejecuta sin SPEC aprobado, gate específico y revisión humana.
