# Plan gobernado de Supabase — Lead Flow

> Estado: **BORRADOR; NO AUTORIZA COMANDOS REMOTOS**
> Última verificación de documentación oficial: 2026-10-02.
> Perfil remoto propuesto: un proyecto Supabase Free para MVP/piloto; ver `SUPABASE-FREE-TIER-READINESS.md`.

## 1. Propósito

Definir cómo Gemini debe preparar y verificar Supabase de forma local antes de solicitar autorización para vincular o cambiar un proyecto remoto.

## 2. Estado observado

- Existe `supabase/config.toml`.
- La migración local antigua fue retirada; LEADFLOW-05 debe crear un conjunto de migraciones nuevo, revisable y compatible con PRD/arquitectura v2.
- El Product Owner cree que ya existe un proyecto remoto Free, pero no se confirmó su referencia, plan, región, schema ni estado.
- El contenido de `.env` no fue inspeccionado.

No existe una migración legacy aprobada para reutilizar. Gemini debe diseñar el baseline de schema desde cero dentro de `SPEC-LEADFLOW-05`; no puede ejecutar cambios remotos sin GATE 2.

## 3. Decisiones

- Workflow de schema: migraciones imperativas versionadas.
- Desarrollo: local-first mediante Supabase CLI y runtime compatible con Docker.
- Navegador: no accede directamente a tablas internas.
- MCP: opcional y read-only para inventario/auditoría; no aplica SQL.
- Deploy remoto: CLI con preview/dry-run y GATE 2.
- Datos local/staging: sintéticos.
- Producción: no se crea ni modifica durante Cycle 0/1 sin ticket y gate explícitos.
- Free tier: se usa para MVP/piloto sin SLA; cuota, uso y posible estado read-only son riesgos operativos explícitos.

## 4. Secretos

| Secreto/dato | Ubicación permitida | Prohibido |
| --- | --- | --- |
| Supabase access token | Login/almacén seguro del operador | Git, orch, chat |
| Database password | Prompt/secret store autorizado | `.env.example`, comando visible |
| Edge Function secrets | Local env ignorado; Supabase Secrets remoto | Variables `VITE_*`, logs |
| Publishable key | Solo donde el diseño público la requiera | Confundirla con autorización de tablas |
| Secret/service-role key | Entorno servidor exclusivamente | SDK/browser/documentos |

El SDK de Lead Flow llama Edge Functions y no necesita una clave de servicio. Un prefijo público como `VITE_` nunca se usa para secretos.

## 5. Flujo local que deberá ejecutar Gemini

Solo después de GATE 1 de LEADFLOW-02/05:

1. Descubrir comandos y versión con `supabase --help` y `supabase --version`; no adivinar flags.
2. Verificar runtime local y compatibilidad de `config.toml`.
3. Resolver el borrador de migración existente según decisión humana.
4. Crear migraciones nuevas mediante `supabase migration new <nombre>`.
5. Aplicar desde cero en local con el comando vigente de reset local.
6. Cargar solo seed sintético.
7. Ejecutar tests de constraints, grants y RLS.
8. Ejecutar advisors disponibles y revisar funciones/vistas.
9. Generar tipos desde local cuando el código los consuma.
10. Adjuntar evidencia sin URLs ni credenciales.

## 6. Requisitos de schema y seguridad

- `GRANT`/`REVOKE` explícitos en la misma migración que crea objetos.
- RLS habilitado como defensa adicional en tablas de esquemas expuestos.
- Sin `INSERT`, `SELECT`, `UPDATE` o `DELETE` de `anon` sobre tablas internas.
- Sin políticas públicas `USING (true)` o `WITH CHECK (true)` para leads.
- Funciones privilegiadas fuera del schema expuesto, con `search_path` controlado, permisos revocados y revisión específica.
- Vistas expuestas solo si son necesarias y con semantics `security_invoker` compatibles.
- Índices/constraints de tenant, idempotencia, outbox y retries probados.
- Migrations reproducibles desde base vacía.

Supabase separa privilegios de objeto y RLS; ambos deben probarse. Los nuevos defaults de Data API exigen no depender de grants implícitos.

## 7. Inventario remoto y preparación

El primer contacto con el proyecto candidato es un inventario read-only conforme a `SUPABASE-FREE-TIER-READINESS.md`. Si se encuentra estado previo no decidido, se bloquea: no se enlaza, limpia ni migra.

Antes de solicitar GATE 2, Gemini presenta:

```text
Project ref (redacted/parcial):
Entorno: staging | production
Plan/capacidad: Free confirmado | no confirmado; uso observado y umbral de alerta
CLI version:
Linked project actual (si existe):
Migration list local/remota:
Dry-run:
Objetos afectados:
Backup/rollback:
Tests locales:
Riesgos:
```

La ejecución autorizada debe:

1. Confirmar target inmediatamente antes del comando.
2. Ejecutar solo el dry-run/aplicación aprobados.
3. No incluir seed en producción.
4. Reconsultar migration history y objetos esperados.
5. Ejecutar smoke tests negativos/positivos.
6. Registrar el resultado en los eventos de orch y `STATE.md` sin secretos.

## 8. Comandos prohibidos

- `supabase db reset --linked` sobre producción.
- SQL directo en producción para “probar rápido”.
- MCP `execute_sql` como bypass del flujo de migraciones.
- `db push` sin dry-run, backup/rollback y GATE 2.
- Imprimir `.env`, tokens o connection strings.
- Copiar credenciales a argumentos que queden en historial/logs.
- Aplicar la migración borrador actual.
- Asumir que Free evita restricciones, pausas o modo read-only.

## 9. Smoke tests requeridos

- Las tablas esperadas existen y ninguna extra fue creada.
- `anon` no puede consultar ni insertar en tablas internas.
- El contexto servidor puede ejecutar únicamente la operación necesaria.
- Una captura atómica crea lead + outbox o ninguno.
- Tenant A no puede leer/modificar tenant B.
- Idempotency constraint evita duplicados.
- Retry indexes soportan reclamar pendientes sin full scan evidente.
- No hay funciones públicas privilegiadas no aprobadas.

## 10. Referencias oficiales

- Local workflow y deploy: <https://supabase.com/docs/guides/local-development/cli-workflows>
- Database migrations: <https://supabase.com/docs/guides/local-development/database-migrations>
- Data API, grants y RLS: <https://supabase.com/docs/guides/api/securing-your-api>
- Edge Function secrets: <https://supabase.com/docs/guides/functions/secrets>
- Breaking changes: <https://supabase.com/changelog?types=breaking-change>
