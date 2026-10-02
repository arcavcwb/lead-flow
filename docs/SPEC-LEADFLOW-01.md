# SPEC-LEADFLOW-01 — Baseline de gobernanza y seguridad del repositorio

> Estado: **LISTO PARA GATE 1; NO APROBADO**
> Baseline: PRD/arquitectura v2
> Tipo: documentación, trazabilidad y secret hygiene.

## 1. Objetivo

Dejar el repositorio listo para que Gemini ejecute tickets sin usar documentación contradictoria, perder cambios del usuario ni versionar secretos.

## 2. Alcance

- Verificar remote, branch y convenciones Git sin cambiar historia.
- Validar enlaces y estados de la documentación v2.
- Reconciliar `STATE.md` con Git y orch después de autorización.
- Inventariar archivos no trackeados sin abrir credenciales.
- Asegurar reglas de exclusión para `.env`, credenciales, sesiones y exports sensibles.
- Definir owners de GATE 0–3 y evidencias.
- Integrar orch únicamente después de GATE 0 y aprobación del diff, sin ejecutar producto.

## 3. Fuera de alcance

- Implementar producto.
- Corregir CI o Supabase.
- Rotar credenciales directamente.
- Reescribir commits o hacer merge.

## 4. Higiene de baseline

Los artefactos legacy detectados antes de esta baseline fueron retirados del workspace sin abrir el CSV potencialmente sensible. El ticket conserva la regla: ningún secreto se abre, imprime, versiona o rota automáticamente. Si el dueño de la cuarentena confirma que el CSV contenía una credencial real, la rotación queda como acción humana independiente.

## 5. Artefactos permitidos

- `.gitignore`
- `README.md`
- `lead-flow-execution-plan.md`
- `docs/*.md`
- Archivos mínimos de integración orch dentro del alcance aprobado

No modificar `.env`, migraciones, código o archivos no trackeados ajenos.

## 6. Criterios Gherkin

```gherkin
Escenario: La documentación tiene una única baseline activa
  Dado el repositorio después de la replanificación
  Cuando se recorren enlaces y estados contractuales
  Entonces cada documento canónico existe
  Y ninguno presenta una versión anterior como aprobada
```

```gherkin
Escenario: Los secretos no pueden versionarse por accidente
  Dado un archivo de entorno o credencial con un patrón protegido
  Cuando se consulta git check-ignore
  Entonces el archivo queda excluido
  Y ningún valor secreto se muestra en la evidencia
```

```gherkin
Escenario: Los archivos del usuario se preservan
  Dado un working tree con cambios no relacionados
  Cuando se completa LEADFLOW-01
  Entonces ningún archivo ajeno fue eliminado, revertido o incluido en el commit
```

```gherkin
Escenario: orch representa el DAG sin duplicar
  Dado GATE 0 y un diff de integración aprobado
  Cuando se crea y valida tasks.json
  Entonces cada ticket conserva un único ID y sus dependencias
  Y no se ejecuta ninguna tarea de producto
```

```gherkin
Escenario: GATE 0 queda trazable
  Dado que el humano aprueba la baseline v2
  Cuando se registra la decisión
  Entonces constan persona, fecha, versión y commit SHA
```

## 7. Verificación prevista

- Link checker Markdown.
- Búsqueda de términos/versiones obsoletos.
- `git status`, `git diff` y `git ls-files` sin mostrar secretos.
- Verificación de ignores por ruta sintética o segura.
- Salida de `orch validate`, `orch router validate`, `orch explain` y `orch tasks`, sin ejecución de producto.

## 8. Done

- Gherkin completos.
- Posible credencial tratada sin exposición.
- orch/Git/STATE reconciliados o discrepancia bloqueada.
- Commit documental aislado.
- Revisión independiente y merge humano.
