# SPEC-LEADFLOW-02: Setup Infraestructura Monorepo y Supabase CLI

## 1. Resumen de la Tarea
Establecer la estructura base del monorepo (`pnpm workspaces`) para separar el Frontend (SDK) del Backend (Supabase). Inicializar el entorno local de Supabase y registrar las variables de entorno para que el servidor MCP o el CLI tengan control sobre el proyecto remoto en la nube.

## 2. Requerimientos Técnicos
- **Workspaces pnpm:** Definir `apps/sdk` y `supabase/` en `pnpm-workspace.yaml`.
- **Estructura Supabase:** Ejecutar `supabase init` para crear la carpeta `/supabase`.
- **Variables de Entorno:**
  - Crear archivo `.env` en la raíz.
  - Inyectar `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY`.
- **Conexión Remota:** Verificar que el CLI pueda listar el proyecto remoto (ID: `rltjarnwguvendyagtdm`) usando el Personal Access Token (PAT).

## 3. Escenarios Gherkin (Criterios de Aceptación)

```gherkin
Escenario: Inicialización de Supabase Local
  Dado un repositorio de Git limpio
  Cuando ejecuto la inicialización de supabase
  Entonces debe existir el directorio "/supabase" con su archivo "config.toml"

Escenario: Configuración de Variables de Entorno Seguras
  Dado el Reference ID y la clave pública
  Cuando genero el archivo de entorno base
  Entonces el archivo ".env" debe contener VITE_SUPABASE_URL y VITE_SUPABASE_ANON_KEY
  Y el archivo ".env" debe estar excluido en ".gitignore"

Escenario: Verificación de Permisos CLI
  Dado el PAT proporcionado por el usuario
  Cuando ejecuto "supabase projects list" con el token
  Entonces la respuesta debe listar el proyecto "lead-flow"
```

## 4. Notas de Implementación
- El servidor MCP de Supabase está bloqueado por reglas de seguridad locales, por lo que toda migración futura se escribirá como archivo `.sql` local y el humano o CLI validado hará el push a producción.
- No realizar el `link` interactivo; solo inicializar y comprobar lectura con el token.
