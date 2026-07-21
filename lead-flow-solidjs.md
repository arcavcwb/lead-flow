# Implementation Plan: Lead Flow SolidJS

## Overview
Implement the Lead Flow Engine SDK and backend infrastructure based on "Option A". The goal is to build an injectable, ultra-lightweight web widget that captures B2B leads, isolates styles, and reliably forwards data to WhatsApp under 5 seconds.

## Project Type
**WEB** (SDK Component) & **BACKEND** (Supabase Edge / n8n)

## Success Criteria
1. SDK Bundle Size: `< 50kb` (gzippeado).
2. TTI (Time to Interactive): `< 200ms`.
3. Latency: Lead capture to WhatsApp alert in `< 5.0s`.
4. Visual Isolation: 100% immune to external CSS via Shadow DOM.

## Tech Stack
*   **Frontend:** SolidJS, `solid-element` (Web Components), Vite.
*   **Styling:** CSS Modules / Vanilla CSS (No Tailwind to save weight).
*   **Backend:** Supabase (PostgreSQL + Edge Functions).
*   **Automation:** n8n (Webhook-only mode).
*   **Testing:** Playwright (E2E), Vitest (Unit).

---

## File Structure
```text
/lead-flow/
├── apps/
│   ├── sdk/                  # SolidJS Widget
│   │   ├── src/
│   │   │   ├── components/   # Solid Components
│   │   │   ├── index.ts      # Web Component Definition (solid-element)
│   │   │   └── styles/       # Vanilla CSS variables
│   │   └── vite.config.ts    # Bundler config
├── supabase/
│   ├── functions/            # Edge Functions (Deno)
│   └── migrations/           # DB Schema
└── tests/                    # Playwright E2E tests
```

---

## Task Breakdown (Backlog for Plane.so)

### Epic 1: Scaffold & Architecture Foundation
- **Task 1.1: Initialize Monorepo and SolidJS SDK**
  - **Agent:** `@frontend-specialist`
  - **INPUT:** Empty directory.
  - **OUTPUT:** Vite + SolidJS project with `solid-element` installed.
  - **VERIFY:** `npm run build` generates a single JS file.
- **Task 1.2: Setup Supabase Local Environment**
  - **Agent:** `@database-architect`
  - **INPUT:** Architecture docs.
  - **OUTPUT:** `clients`, `clients_config`, and `leads_vault` tables with initial RLS policies.
  - **VERIFY:** `supabase start` succeeds and tables are visible in studio.

### Epic 2: Frontend SDK (Shadow DOM & UI)
- **Task 2.1: Web Component Wrapper & CSS Injection**
  - **Agent:** `@frontend-specialist`
  - **INPUT:** SolidJS scaffold.
  - **OUTPUT:** `<lead-flow-widget>` Custom Element registering successfully with isolated ShadowRoot.
  - **VERIFY:** Widget loads in an external HTML file without bleeding styles.
- **Task 2.2: Lead Form Component Development**
  - **Agent:** `@frontend-specialist`
  - **INPUT:** Design requirements (mobile-first, `type="tel"`).
  - **OUTPUT:** SolidJS form with validation, using native CSS variables for `theme_color`.
  - **VERIFY:** Form handles inputs correctly and updates state without full re-renders.

### Epic 3: Backend & Automation
- **Task 3.1: Supabase Edge Function (Gatekeeper)**
  - **Agent:** `@backend-specialist`
  - **INPUT:** Form payload structure.
  - **OUTPUT:** Deno Edge Function that validates CORS, inserts into `leads_vault`, and calls n8n.
  - **VERIFY:** `curl` request to the function successfully adds a row to the DB.
- **Task 3.2: n8n Workflow & Dead Letter Queue**
  - **Agent:** `@backend-specialist`
  - **INPUT:** n8n webhook endpoint.
  - **OUTPUT:** Flow capturing the webhook, formatting the message, sending to Evolution API, and handling errors (Catch node).
  - **VERIFY:** Triggering the webhook results in a WhatsApp message.

### Epic 4: Quality Assurance & Testing
- **Task 4.1: Playwright E2E Shadow DOM Test**
  - **Agent:** `@test-engineer`
  - **INPUT:** Compiled SDK.
  - **OUTPUT:** Playwright test suite injecting the SDK into a mock "hostile" page (Bootstrap CSS).
  - **VERIFY:** `npx playwright test` passes visually and functionally.

---

## Phase X: Verification
- [ ] Lint & Type Check: `npm run lint && tsc --noEmit`
- [ ] Bundle Size Check: Ensure SDK output is `< 50kb`.
- [ ] Security Scan: Validate RLS and Edge Function CORS.
- [ ] End-to-End: Lead flow from browser to WhatsApp completes.
