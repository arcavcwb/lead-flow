# SPEC-LEADFLOW-02 — Workspace reproducible y Supabase local

> Estado: **BORRADOR; REQUIERE GATE 1**
> Depende de: LEADFLOW-01
> Mutación remota: **NO PERMITIDA**.

## 1. Objetivo

Conseguir que un clon limpio pueda instalar dependencias, reconocer el workspace SDK y levantar/recrear Supabase local sin credenciales cloud. Preparar además el formato de inventario para el proyecto Supabase Free candidato, sin conectarse a él.

## 2. Alcance

- Declarar versiones compatibles de Node y pnpm.
- Mantener lockfile reproducible.
- Configurar workspaces reales; ningún patrón cuenta como paquete si no tiene manifest.
- Crear el shell mínimo de `apps/sdk` necesario para que herramientas puedan encontrar el paquete; la UI corresponde a LEADFLOW-04.
- Validar `supabase/config.toml` contra la versión de CLI descubierta.
- Identificar servicios locales habilitados que no pertenecen al MVP (Auth, Storage, Realtime, Vector) y proponer su desactivación o justificación sin modificar el remoto.
- Preparar el template de inventario read-only definido en `SUPABASE-FREE-TIER-READINESS.md`.
- Añadir seed sintético si `config.toml` lo referencia.
- Añadir plantillas de variables con nombres y comentarios, nunca valores reales.
- Documentar start/stop/reset local usando ayuda de la CLI instalada.

## 3. Fuera de alcance

- Vincular proyecto remoto.
- Inventariar o cambiar el proyecto remoto Free cuando no existan a la vez GATE 0 y autorización humana explícita.
- Ejecutar `db push`, deploy de funciones o cambios de secrets.
- Crear schema de producto.
- Implementar widget, API o n8n/Evolution.
- Leer valores actuales de `.env`.

## 4. Fronteras de variables

- SDK: conoce `LEAD_FLOW_API_BASE_URL`; `client_id` se pasa en el snippet/atributo.
- Edge local: usa variables servidor en archivo ignorado.
- No introducir `VITE_SUPABASE_SECRET_KEY`, `VITE_SERVICE_ROLE` ni equivalente.
- Una publishable key solo se añade si un SPEC futuro demuestra que el browser debe usarla; la arquitectura v2 no la necesita para tablas.

## 5. Criterios Gherkin

```gherkin
Escenario: Instalación reproducible
  Dado un clon limpio con las versiones documentadas
  Cuando se instalan dependencias con lockfile congelado
  Entonces la instalación termina sin modificar el lockfile
```

```gherkin
Escenario: El SDK es un workspace real
  Dado la configuración pnpm
  Cuando se enumeran workspaces
  Entonces aparece exactamente el paquete sdk esperado
  Y un filtro inexistente produce un fallo detectable en el gate correspondiente
```

```gherkin
Escenario: Supabase local inicia sin cloud
  Dado Docker/runtime y CLI compatibles
  Cuando se inicia el stack local
  Entonces aplica configuración y seed sintético
  Y no solicita credenciales de un proyecto remoto
```

```gherkin
Escenario: el Free Tier candidato no se asume configurado
  Dado un proyecto remoto que el Product Owner cree existente
  Cuando se prepara LEADFLOW-02
  Entonces se completa solo el template de inventario sin secretos
  Y no se ejecuta login, link ni consulta remota
```

```gherkin
Escenario: Reset local es reproducible
  Dado el stack local con cambios temporales
  Cuando se ejecuta el reset local documentado
  Entonces el estado final coincide con migraciones y seed versionados
```

```gherkin
Escenario: No hay secretos versionados
  Dado las plantillas de entorno
  Cuando se revisan Git y los archivos example
  Entonces solo aparecen nombres/placeholders seguros
  Y los archivos con valores están ignorados
```

## 6. Artefactos esperados

- Manifest/versiones raíz.
- `pnpm-workspace.yaml` coherente.
- Shell mínimo `apps/sdk` sin funcionalidad de producto.
- `supabase/config.toml` compatible.
- `supabase/seed.sql` sintético si está habilitado.
- `.env.example`/equivalentes sin secretos.
- Instrucciones locales en README o documento vinculado.

## 7. Verificación prevista

- Instalación con lockfile congelado.
- Enumeración de workspaces.
- Start, health y reset local.
- Diff limpio de lockfile después de instalación.
- Escaneo de secretos sobre archivos versionados.

## 8. Done

El entorno local es reproducible desde cero y no depende de Supabase, n8n o Evolution remotos. GATE 2 no se solicita en este ticket.
