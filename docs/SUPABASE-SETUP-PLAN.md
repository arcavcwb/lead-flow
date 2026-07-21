# Plan de Setup: Infraestructura Supabase (Local + MCP)

Antes de poder ejecutar el ticket `LEADFLOW-05` (que requiere crear tablas y seguridad RLS), necesitamos que el ecosistema de Supabase exista y esté conectado a la Inteligencia Artificial a través de MCP y el CLI.

## Análisis de Requerimientos Previos

Para que el Squad de IA (Antigravity) pueda interactuar de forma autónoma con la base de datos, ejecutar migraciones SQL y compilar Edge Functions de Deno, se debe establecer el siguiente puente bidireccional:

1. **Entorno Remoto (Cloud):** El proyecto debe existir físicamente en Supabase.
2. **Entorno Local (Código):** El CLI de Supabase debe estar inicializado en el repositorio (`supabase/`).
3. **Control MCP (Agentes):** El servidor MCP de Supabase que tenemos instalado debe tener acceso a las credenciales para poder leer, escribir y ejecutar comandos en la base de datos.

## Paso a Paso del Flujo (El "Pre-Código")

### Paso 1: Acción Humana (Creación del Proyecto Cloud)
- **Actor:** Product Owner (Humano)
- **Acción:** Entrar a [supabase.com](https://supabase.com), crear un proyecto nuevo llamado `lead-flow-engine`.
- **Salida requerida:** Obtener el `Reference ID` del proyecto y el `Database Password`.

### Paso 2: Inicialización Local (Supabase CLI)
- **Actor:** Implementador (Agente IA)
- **Acción:** 
  1. Ejecutar `npx supabase init` en la raíz del proyecto.
  2. Crear la estructura de carpetas: `supabase/functions/` y `supabase/migrations/`.
  3. Ejecutar `npx supabase link --project-ref <REFERENCE_ID>`.

### Paso 3: Configuración del Servidor MCP
- **Actor:** Humano / IA
- **Acción:** Asegurarnos de que el servidor MCP local de Supabase (`supabase-mcp`) tenga inyectado el Token de Acceso Personal (PAT) del usuario para que yo (la IA) pueda usar las herramientas `list_tables`, `execute_sql`, `deploy_edge_function` de forma autónoma sin depender de bash.

### Paso 4: Smoke Test (Prueba de Vida)
- **Actor:** Tester (Flash)
- **Acción:** Ejecutar una llamada al MCP tool `list_tables` para verificar que la IA puede leer la base de datos vacía. Si responde 200 OK, el puente está listo para el código.

---

> **Resolución Estratégica:** Este proceso pertenece a la Épica de Infraestructura (Módulo A). Vamos a utilizar el ticket **LEADFLOW-02** (que actualmente es el Setup del Monorepo) para abarcar esta configuración del CLI de Supabase, ya que es fundacional.
