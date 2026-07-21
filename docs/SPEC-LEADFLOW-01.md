# SPEC-LEADFLOW-01: Configuración Git y Trazabilidad Base

## 1. Resumen de la Tarea
Este ticket establece la fundación del proyecto. Consiste en inicializar el repositorio local, vincularlo al remoto en GitHub, asegurar la identidad correcta del desarrollador (`arcavcwb`) y realizar el commit inicial con toda la documentación estratégica y el kit de agentes (`.agents/`).

## 2. Requerimientos Técnicos
- **Repositorio Remoto:** `https://github.com/arcavcwb/lead-flow.git`
- **Identidad Git:** 
  - User: `arcav`
  - Email: `armandocastrocwb@gmail.com`
- **Archivos a incluir:** 
  - Directorio `/docs` completo (PRD, Arquitectura, Specs, etc.).
  - Directorio `/.agents` completo (Configuración de IA).
  - Archivo `.gitlocal` (ya creado).
  - Archivo `.gitignore` adecuado.
- **Rama principal:** `main`

## 3. Escenarios Gherkin (Criterios de Aceptación)

```gherkin
Escenario: Inicialización de Repositorio y Vínculo Remoto
  Dado un directorio de proyecto no inicializado o inicializado localmente
  Cuando ejecuto la inicialización y vinculo el origen remoto
  Entonces el remote "origin" debe apuntar a "https://github.com/arcavcwb/lead-flow.git"
  Y la rama actual debe llamarse "main"

Escenario: Configuración de Identidad y Exclusión de Archivos
  Dado el repositorio git inicializado
  Cuando reviso la configuración local
  Entonces user.name debe ser "arcav" y user.email debe ser "armandocastrocwb@gmail.com"
  Y debe existir un archivo ".gitignore" que excluya node_modules y archivos de entorno

Escenario: Commit Inicial con Memoria del Proyecto
  Dado el entorno configurado correctamente
  Cuando agrego los directorios "/docs" y "/.agents"
  Y realizo el commit con el mensaje "chore(LEADFLOW-01): initial commit with docs and agent kit"
  Entonces el árbol de trabajo (working tree) debe estar limpio
```

## 4. Notas de Implementación (Solo para el Implementador)
- No instales dependencias de Node.js en este paso.
- El archivo `.gitignore` debe contener mínimamente `node_modules`, `.env`, `.env.*` y `.DS_Store`.
- No toques el código fuente, este ticket es puramente de infraestructura Git.
