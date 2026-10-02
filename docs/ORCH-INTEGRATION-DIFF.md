# Diff propuesto de integración de orch — Lead Flow

> Estado: **PROPUESTO; NO APLICADO**  
> Fecha: 2026-10-02  
> Versión inspeccionada: `orch v0.16.0`

Este documento es el diff específico que exige GATE 0 antes de crear los
artefactos operativos de orch. No crea `tasks.json`, configuración ni scripts.
Su función es hacer revisable la integración antes de que Gemini/Antigravity
pueda recibir una tarea.

## 1. Resultado deseado

La integración propuesta tendrá estos artefactos versionados:

```text
tasks.json
.orchestrator/config.yaml
.orchestrator/model_router.yaml
.orchestrator/budgets.yaml
scripts/task-start.sh
scripts/task-finish.sh
scripts/task-block.sh
scripts/task-reset.sh
```

El estado runtime quedará fuera de Git:

```text
.orchestrator/state/
```

No se crearán todavía porque la versión instalada debe validar primero el
esquema exacto de los campos y el Product Owner debe aprobar este diff.

## 2. Contrato que se aplicará

`tasks.json` conservará únicamente los doce IDs del plan maestro:

```text
LEADFLOW-01 ... LEADFLOW-12
```

Cada entrada deberá conservar, como mínimo, esta información lógica:

| Campo | Regla | Fuente |
| --- | --- | --- |
| `id` | único, `LEADFLOW-XX` | plan maestro |
| `specRef` | ruta a SPEC o marcador de refinamiento | SPEC/STATE |
| `status` | `todo`, `ready`, `blocked`, etc. según el enum real de orch | estado comprobado |
| `deps` | solo dependencias del plan maestro | plan maestro |
| `model` | modelo resoluble por el router | routing aprobado |
| `files` | allowlist de alcance | SPEC |
| `description` | resumen sin sustituir el SPEC | plan/SPEC |

La asociación agente/skills no se inferirá del título. Se conservará en el
contrato de routing que acepte `orch` o, si la versión no admite esos campos,
en una fuente de routing versionada que el script de validación compruebe antes
de aceptar una tarea.

## 3. Routing inicial

El executor previsto es Gemini mediante Antigravity. La ruta concreta queda
pendiente de resolver contra el catálogo local; la visibilidad de un modelo no
se tratará como prueba de inferencia exitosa.

Reglas propuestas:

- `LEADFLOW-01`: `documentation-writer`; documentación, shell seguro y
  verificación.
- `LEADFLOW-02`, `LEADFLOW-05`: `database-architect`; diseño, migración,
  pruebas y seguridad.
- `LEADFLOW-03`, `LEADFLOW-09`: `test-engineer`/`qa-automation-engineer`;
  pruebas y validación.
- `LEADFLOW-04`, `LEADFLOW-07`: `frontend-specialist`; Preact interno,
  Web Components y Shadow DOM.
- `LEADFLOW-06`, `LEADFLOW-08`: `backend-specialist`; API e integración,
  sin autorización remota implícita.
- `LEADFLOW-10`: `devops-engineer`; operación y staging, detrás de GATE 2.
- `LEADFLOW-11`: `security-auditor`; privacidad, seguridad y evidencias.
- `LEADFLOW-12`: `product-owner`; piloto y decisión de continuidad.

Las skills exactas están en `docs/ORCH-AGENT-SKILL-MATRIX.md`; esta propuesta
no añade skills globales ni carga automáticamente la familia `caveman-*`.

## 4. Preservación de gates

- Ninguna tarea iniciará como `ready` sin SPEC aprobado y dependencias
  completas.
- Toda tarea que toque Supabase, n8n, Evolution API, despliegue o proveedor
  externo seguirá con `remote_write: false` hasta un GATE 2 exacto.
- `auto_merge` permanecerá desactivado.
- La concurrencia inicial será uno.
- La integración no ejecutará producto durante su validación.
- Codex revisa el diff y la evidencia; Gemini/Antigravity ejecuta solo una
  tarea autorizada; el Product Owner concede los gates.

## 5. Secuencia después de aprobar este diff

1. Confirmar el esquema real de `tasks.json`, `config.yaml`, router y scripts
   para `orch v0.16.0`.
2. Crear los artefactos mínimos manualmente, sin `orch init`.
3. Validar que todos los agentes y skills de la matriz existen.
4. Ejecutar solo `orch atomize --list`, `orch validate` y `orch router validate`.
5. Revisar `orch tasks`/`orch explain` y la allowlist de cada tarea.
6. Probar el bloqueo de una tarea sin SPEC/GATE sin despachar producto.
7. Adjuntar evidencia y solicitar la aprobación de integración.

## 6. Criterios de rechazo

El diff no se aplica si:

- el esquema obliga a perder agente, skills, gate, allowlist o dependencia;
- un ticket aparece ejecutable con SPEC pendiente;
- el router no puede resolver la ruta Gemini/Antigravity de forma comprobable;
- `orch` habilita auto-merge o más de una tarea concurrente;
- se requiere tocar un servicio remoto o mostrar secretos;
- la versión de orch exige `orch init` para un artefacto que podamos escribir
  manualmente sin perder el contrato.

