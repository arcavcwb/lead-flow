# Configuración Agile en Plane (Fuente de Verdad)

> **Propósito:** Este documento define la arquitectura exacta del espacio de trabajo en **Plane** para el proyecto Lead Flow Engine. Plane no es solo un tablero Kanban; es el cerebro operacional que orquesta el código que vive en GitHub.

---

## 1. Workflow y Estados (La Máquina de Estados)

En la configuración del proyecto en Plane, debes modificar el flujo de estados por defecto para que coincida exactamente con nuestro protocolo de handoff. Los estados obligatorios son:

| Estado Plane | Tipo en Plane | Rol que actúa | Gate Humano Previo |
|--------------|---------------|---------------|--------------------|
| **Backlog** | Unstarted | Product Owner | GATE 0 (Crea el ticket) |
| **Refinado** | Unstarted | Analista (Pro) | - |
| **En desarrollo**| Started | Implementador (Pro) | GATE 1 (Aprueba SPEC) |
| **En pruebas** | Started | Tester (Flash) | - |
| **En revisión** | Started | Revisor (Claude) | - |
| **Hecho** | Completed | Humano (Merge) | GATE FINAL (Merge PR) |

---

## 2. Modules (Las Épicas Arquitectónicas)

Los **Modules** en Plane representan los pilares del sistema. Agrupan tickets funcionalmente, sin importar cuándo se ejecutan. 

1. **Módulo A: Infraestructura y DevOps**
   - *Lead:* Humano / Antigravity
   - *Contenido:* Setup de GitHub, Monorepo pnpm, Reglas de Linting, CI/CD, despliegue en VPS (Docker/Caddy).
2. **Módulo B: SDK Frontend (Widget)**
   - *Lead:* Implementador (Pro)
   - *Contenido:* SolidJS, Web Components (Shadow DOM), UI del formulario.
3. **Módulo C: Backend & Bóveda (Supabase)**
   - *Lead:* Implementador (Pro)
   - *Contenido:* Tablas (clients, config, leads), Políticas RLS, Edge Functions (Gatekeeper).
4. **Módulo D: Automatización y Mensajería (n8n + WAHA)**
   - *Lead:* Implementador (Pro)
   - *Contenido:* Flujo de webhooks, resiliencia (Dead Letter Queue), conexión a WhatsApp.

---

## 3. Cycles (Sprints de Ejecución)

Los **Cycles** definen *cuándo* se hace el trabajo. Dado el ritmo acelerado de los agentes IA, usaremos ciclos cortos orientados a valor demostrable.

*   **Cycle 0: Setup y Trazabilidad Base (Semana 1)**
    *   *Objetivo:* Tener el repo en GitHub, monorepo pnpm, tickets en Plane y CI/CD básico.
    *   *Tickets:* LEADFLOW-01, LEADFLOW-02, LEADFLOW-03.
*   **Cycle 1: El Gatekeeper y la Bóveda (Semana 1)**
    *   *Objetivo:* API endpoint seguro en Supabase recibiendo datos y guardándolos con RLS.
    *   *Tickets:* LEADFLOW-05, LEADFLOW-06.
*   **Cycle 2: El Widget Inmune (Semana 2)**
    *   *Objetivo:* Formulario inyectable en cualquier web sin contaminación CSS.
    *   *Tickets:* LEADFLOW-04, LEADFLOW-07, LEADFLOW-09 (E2E Shadow DOM).
*   **Cycle 3: Motor de Alertas (Semana 2)**
    *   *Objetivo:* El lead llega al WhatsApp en < 5 segundos.
    *   *Tickets:* LEADFLOW-08, LEADFLOW-10 (Deploy final).

---

## 4. Pages (Documentación Viva)

Las **Pages** de Plane deben sincronizarse o contener los enlaces directos a la carpeta `/docs` de GitHub, garantizando que el equipo comercial/operativo no tenga que abrir el código para entender el negocio.

*   **Page: PRD Maestro & Negocio** → Vinculada a `1_PRD.md` y `2_BUSINESS_MODEL.md`.
*   **Page: Arquitectura Técnica** → Vinculada a `3_ARCHITECTURE.md` y `6_ARCHITECT_REVIEW.md`.
*   **Page: Protocolos del Squad (Reglas)** → Vinculada a `OPERATING-MODEL.md` y `HANDOFF-PROTOCOL.md`.
*   **Page: Contratos (SPECs)** → Cada vez que el Analista cree un `SPEC-EX.md`, se debe referenciar aquí.

---

## 5. Views (Dashboards de Control)

Las **Views** son filtros guardados para monitorear los cuellos de botella (Gates). Debes crear las siguientes vistas en Plane:

1. 🚦 **Vista: "Aguardando GATE 1 (Aprobación Humana)"**
   - *Filtro:* Estado = `Refinado`
   - *Uso:* El Product Owner (vos) entra acá cada mañana para leer SPECs y dar luz verde a los agentes.
2. 🚨 **Vista: "Aguardando GATE Final (Merge)"**
   - *Filtro:* Estado = `En revisión` AND Etiqueta = `aprobado-para-merge`
   - *Uso:* Último chequeo visual antes de hacer merge en GitHub.
3. ♻️ **Vista: "Rechazos y Correcciones"**
   - *Filtro:* Etiqueta = `cambios-solicitados`
   - *Uso:* Monitorear qué tickets rebotaron el Tester o el Revisor y volvieron a desarrollo.
4. 🤖 **Vista: "Frente de Agentes (Trabajo Activo)"**
   - *Filtro:* Estado = `En desarrollo` OR `En pruebas`
   - *Uso:* Ver en qué están trabajando los modelos (Pro/Flash) en tiempo real.

---

## Regla de Integración GitHub-Plane
1. Cada branch en GitHub se debe nombrar con el ID del issue en Plane: `feature/LEADFLOW-XX-breve-desc`.
2. Cada commit debe empezar con el ID: `feat(LEADFLOW-XX): setup supabase rls`.
3. El PR en GitHub debe contener `Fixes LEADFLOW-XX` en la descripción para que Plane mueva el ticket automáticamente si configurás la integración de GitHub en Plane.
