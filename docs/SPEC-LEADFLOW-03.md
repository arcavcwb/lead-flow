# SPEC-LEADFLOW-03: Reglas de Calidad, Linting y CI/CD (GitHub Actions)

## 1. Resumen de la Tarea
Establecer la fundación de calidad del proyecto. Esto incluye la configuración de ESLint, Prettier y TypeScript de forma estricta, y la implementación de un validador automatizado (Continuous Integration) mediante GitHub Actions. Este CI actuará como el juez final, bloqueando cualquier Pull Request que no cumpla con los estándares de calidad o falle los tests.

## 2. Requerimientos Técnicos
- **Herramientas de Calidad (Monorepo):**
  - Dependencias de desarrollo instaladas en la raíz: `eslint`, `prettier`, `typescript`.
  - Scripts en `package.json` raíz: 
    - `"lint": "eslint ."`
    - `"typecheck": "tsc --noEmit --workspaces"`
    - `"test": "echo 'Run tests here'"` (placeholder hasta que se instale Playwright/Vitest en otros tickets).
- **Integración Continua (GitHub Actions):**
  - Crear archivo `.github/workflows/ci.yml`.
  - Trigger: Evento `pull_request` apuntando a la rama `main`.
  - Entorno: `ubuntu-latest`, Node.js v20.
  - Pasos del Workflow:
    1. Checkout del código.
    2. Setup de `pnpm` (usando `pnpm/action-setup`).
    3. Instalación de dependencias (`pnpm install --frozen-lockfile`).
    4. Ejecución del Portón de Calidad: Lint, Typecheck, Build de SDK.

## 3. Escenarios Gherkin (Criterios de Aceptación)

```gherkin
Escenario: El código tiene errores de tipos
  Dado un Pull Request que contiene un error de TypeScript en la carpeta del SDK
  Cuando GitHub Actions ejecuta el workflow de CI
  Entonces el job debe fallar en el paso "Typecheck"
  Y el Pull Request debe ser bloqueado automáticamente por GitHub

Escenario: El código no respeta las reglas de estilo
  Dado un archivo con errores de estilo o variables no usadas
  Cuando el desarrollador ejecuta "pnpm lint" en local o el CI lo ejecuta
  Entonces el comando debe lanzar un código de error (exit code 1)
```

## 4. Notas de Implementación (Solo para el Implementador)
- No configures Playwright en este ticket; ese framework se instalará en los tickets de QA de Frontend. Aquí solo se sientan las bases del CI.
- El archivo `ci.yml` debe usar caché de dependencias para garantizar que el workflow termine en menos de 2 minutos.
