# DOC 5: Protocolo de Aseguramiento de Calidad (QA) (v1.0)

Antes de cualquier despliegue a producción, el sistema **debe superar los 4 escenarios críticos** descritos a continuación. Ninguno es opcional.

---

## 1. Testing de Frontend — Aislamiento CSS

**Objetivo:** Garantizar que el Shadow DOM sea inmune a cualquier CSS externo.

### Procedimiento:
1. Inyectar el SDK compilado en una página que contenga simultáneamente:
   - Bootstrap 5 (con su reset CSS global)
   - Tailwind CSS (con `@layer base`)
   - CSS nativo con reglas `!important` conflictivas
2. Inspeccionar visualmente cada elemento del formulario.

### Criterios de Aceptación (Definition of Done):
- [ ] Ningún `<input>` modifica su `font-size`, `padding` o `border` por estilos externos.
- [ ] El `<button type="submit">` mantiene su diseño White-Label exacto.
- [ ] No hay filtración de variables CSS del host hacia el Shadow Root.
- [ ] `font-size` de todos los inputs es **≥ 16px** (anti-zoom iOS Safari).
- [ ] `min-height` del botón submit es **≥ 48px**.
- [ ] `type="tel"` + `inputMode="numeric"` abren teclado numérico en iOS y Android.

---

## 2. Testing de Seguridad — Penetration Test Básico

**Objetivo:** Verificar que la superficie de ataque esté cerrada a nivel de Base de Datos y Edge Function.

### 2.1. Bypass de RLS (Row Level Security)
- **Herramienta:** Postman / cURL
- **Acción:** Intentar insertar un registro directamente en `leads_vault` usando la `anon_key` pública de Supabase sin pasar por la Edge Function.
- **Resultado Exigido:** `HTTP 401` o `HTTP 403`. Inserción bloqueada.

### 2.2. Falsificación de CORS (Domain Spoofing)
- **Acción:** Invocar la Edge Function con un header `Origin` de un dominio no registrado en la tabla `clients`.
- **Resultado Exigido:** Bloqueo CORS. La Edge Function retorna `HTTP 403` y no procesa el payload.

### 2.3. Ataque de Bots (Honeypot)
- **Acción:** Enviar un formulario con el campo honeypot (invisible para humanos) completado.
- **Resultado Exigido:** La Edge Function descarta el request silenciosamente (`HTTP 200` para no revelar el mecanismo) pero no inserta nada en `leads_vault`.

### 2.4. Rate Limiting por IP
- **Acción:** Enviar > X requests desde la misma IP en menos de 60 segundos.
- **Resultado Exigido:** Las requests que superen el límite son bloqueadas con `HTTP 429 Too Many Requests`.

---

## 3. Testing de Carga y Resiliencia — Stress Test

**Objetivo:** Verificar estabilidad bajo condiciones de pico de tráfico (campaña exitosa).

### Procedimiento:
- Enviar **100 solicitudes simultáneas** a la Edge Function desde un script de carga (ej. `k6` o `artillery`).

### Criterios de Aceptación:
- [ ] Supabase Edge Function responde a todas las requests sin errores `5xx`.
- [ ] Los 100 registros aparecen en `leads_vault`.
- [ ] n8n encola los webhooks sin colapsar (modo webhook-only aguanta la carga).
- [ ] WAHA (WhatsApp HTTP API) mantiene la cadencia de envío sin que WhatsApp detecte spam (ajustar delays en n8n si p99 > umbral).

---

## 4. Fallback Test — Caída Crítica de WAHA (WhatsApp HTTP API)

**Objetivo:** Verificar que una caída del servicio de mensajería NO causa pérdida de datos ni mala experiencia al usuario.

### Procedimiento:
1. Apagar deliberadamente el contenedor de Docker de WAHA (WhatsApp HTTP API) en el VPS.
2. Realizar un envío de lead desde el formulario.

### Resultados Exigidos (todos deben cumplirse):
- [ ] **Supabase:** El lead está guardado correctamente en `leads_vault`. `processed_by_n8n = false`.
- [ ] **UX del Usuario Final:** El SDK muestra el mensaje de éxito ("Gracias por registrarse"). El usuario no ve ningún error de servidor.
- [ ] **n8n:** El Catch Node registra el error internamente con timestamp y detalles.
- [ ] **Reintento Automático (DLQ):** n8n tiene programado un reintento a los 2, 5 y 15 minutos.
- [ ] **Respaldo:** El lead llega a Google Sheets independientemente del fallo de WhatsApp.

---

## 5. Checklist de Pre-Deploy (Gate de Producción)

| Check | Estado |
| :--- | :--- |
| Lint & Type Check (`npm run lint && tsc --noEmit`) | ☐ |
| Bundle Size < 50kb (Gzip) verificado con `vite-bundle-analyzer` | ☐ |
| TTI < 200ms en simulación 4G (Lighthouse) | ☐ |
| Aislamiento CSS ✓ (Escenario 1 superado) | ☐ |
| RLS + CORS Pen Test ✓ (Escenario 2 superado) | ☐ |
| Stress Test 100 reqs ✓ (Escenario 3 superado) | ☐ |
| Fallback Test ✓ (Escenario 4 superado) | ☐ |
| Variables de entorno en producción configuradas (no `.env` expuesto) | ☐ |
| RLS de Supabase en producción (no en modo `service_role` abierto) | ☐ |
