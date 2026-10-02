# Revisión arquitectónica y ADR — Lead Flow v2.0

> Estado: **APROBADO EN GATE 0; COMMIT PENDIENTE**
> Fecha de revisión: 2026-10-02
> Veredicto técnico: viable para MVP condicionado a las decisiones y gates de este documento.

## 1. Conclusión ejecutiva

La propuesta es viable si se construye como una vertical pequeña y se elimina la dependencia conceptual de “webhook enviado = entrega garantizada”. Las decisiones anteriores sobre SDK ligero y persistencia temprana se conservan. Se corrigen cinco puntos: outbox durable, acceso server-only a datos, configuración realmente dinámica, proveedor de mensajería reemplazable y claims respaldados por evidencia.

## 2. Decisiones propuestas

### ADR-001 — Construir una vertical antes de la plataforma

**Estado:** Propuesto.

**Contexto:** El roadmap anterior entregaba valor de extremo a extremo en el último ciclo.

**Decisión:** implementar primero un tenant, un formulario, captura, outbox y un proveedor; ampliar después.

**Trade-off:** se difieren dashboard, escala masiva y landing pages, pero se valida pronto el riesgo comercial y técnico principal.

**Revisar cuando:** exista un piloto estable o una dependencia real que obligue a generalizar antes.

### ADR-002 — Preact dentro de Web Component + Shadow DOM

**Estado:** Aceptado por Product Owner el 2026-10-02; su implementación sigue condicionada a GATE 0, SPEC de LEADFLOW-04 y pruebas.

**Decisión:** usar Preact como implementación interna, empaquetada con Vite dentro de un Custom Element. La API pública del SDK se limita a atributos, propiedades y eventos DOM para que las páginas cliente no dependan de Preact y el framework pueda reemplazarse sin romper integraciones.

**Trade-off:** Preact reduce el riesgo de adopción y permite reutilizar parte del ecosistema React, pero `preact/compat` no garantiza compatibilidad universal. Shadow DOM añade complejidad en formularios, eventos y estilos. No se afirmará aislamiento absoluto; se mantiene una matriz de hosts soportados.

**Revisar cuando:** el bundle incumpla presupuesto, una dependencia requiera demasiado `compat`, la compatibilidad con hosts falle o una implementación nativa más pequeña resulte suficiente.

### ADR-003 — El navegador no accede a tablas

**Estado:** Propuesto.

**Decisión:** configuración y captura pasan por Edge Functions. `anon` no recibe permisos directos sobre tablas internas.

**Trade-off:** cada carga de configuración consume una función/cache, pero la superficie pública queda explícita y no filtra webhooks ni datos multi-tenant.

**Revisar cuando:** exista autenticación de clientes finales o una API pública deliberada.

### ADR-004 — Transactional outbox como garantía de entrega

**Estado:** Propuesto.

**Decisión:** crear lead y obligación de entrega atómicamente. El primer intento puede ser inmediato; los reintentos se basan siempre en el outbox.

**Trade-off:** añade tablas, worker y estados. A cambio elimina la ventana de pérdida entre PostgreSQL y n8n/proveedor.

**Revisar cuando:** una cola administrada ofrezca la misma atomicidad, trazabilidad y costo con menor operación.

### ADR-005 — Evolution API como gateway inicial detrás de un adaptador

**Estado:** Propuesto.

**Decisión:** usar la instancia Evolution API existente como primer `MessagingProvider`. El dominio no depende de sus endpoints. Antes del piloto se identifica si la conexión es Baileys o WhatsApp Cloud API oficial y se aprueba el riesgo correspondiente.

**Trade-off:** reutilizar infraestructura acelera el piloto, pero una instancia compartida aumenta el impacto de cambios. Se exige inventario, aislamiento lógico, healthcheck y rollback antes de escribir.

**Revisar cuando:** existan datos comparables de costo, estabilidad y aceptación del cliente.

### ADR-006 — Usar n8n existente sin convertirlo en garantía de entrega

**Estado:** Propuesto.

**Decisión:** la instancia n8n existente enruta Google Sheets/CRM/Evolution API, pero no posee la única copia del evento ni se expone al cliente. Su licencia debe validarse para alojar workflows/credenciales de clientes.

**Trade-off:** n8n acelera la integración, pero añade operación, licencia y riesgo compartido. El outbox y la idempotencia permanecen fuera del workflow.

**Revisar cuando:** el primer flujo requiera múltiples destinos o se confirme el modelo comercial/licencia.

### ADR-007 — Objetivos SLO antes de SLA

**Estado:** Propuesto.

**Decisión:** `<50 KiB`, `p95 ≤5 s`, onboarding de 24 h y disponibilidad son objetivos de validación. Solo pasan a contrato con medición, capacidad y soporte.

**Trade-off:** el marketing inicial es menos categórico, pero reduce riesgo reputacional y contractual.

## 3. Registro de riesgos

| ID | Riesgo | Severidad | Control obligatorio | Owner |
| --- | --- | --- | --- | --- |
| `R-01` | Lead persistido pero evento nunca entregado | Crítica | Outbox atómico + worker + alerta por edad | Backend |
| `R-02` | Inserción/lectura directa anónima | Crítica | Revoke/grants explícitos + RLS + tests negativos | Database |
| `R-03` | Fuga de webhook o secreto en config pública | Crítica | Endpoint allowlist + secrets manager | Backend/Security |
| `R-04` | Evolution usa Baileys y la cuenta se desconecta/bloquea | Alta | Detectar modo, healthcheck, aceptación de riesgo y alternativa | Product/Ops |
| `R-05` | Licencia n8n incompatible | Alta | Revisión escrita antes del piloto | Product/Legal |
| `R-06` | Duplicados por retry/concurrencia | Alta | Idempotencia + unique constraint + locks recuperables | Backend |
| `R-07` | Spam pese a CORS | Alta | Rate limit durable, validación, honeypot y monitoreo | Backend |
| `R-08` | PII en logs o exports | Alta | Minimización, redacción y tests | Security/Privacy |
| `R-09` | VPS como punto único de fallo | Alta | Persistencia previa, healthchecks y recuperación; no SLA prematuro | Ops |
| `R-10` | Config JSON inválida rompe todos los widgets | Media | Schema versionado, validación y rollback | Frontend/Backend |
| `R-11` | CI falso verde | Alta | Anti-false-green tests y evidencia por SHA | DevOps |
| `R-12` | Claims comerciales falsos | Alta | Reglas de evidencia y aprobación humana | Product/Sales |
| `R-13` | Retención indefinida de PII | Alta | Política y job probado antes de piloto | Privacy |
| `R-14` | Instancias n8n/Evolution compartidas sufren impacto cruzado | Alta | Inventario, aislamiento, backups y cambios con GATE 2 | Ops |

## 4. Alternativas consideradas

| Tema | Opción elegida | Alternativa diferida/rechazada | Motivo |
| --- | --- | --- | --- |
| Frontend embebible | Preact interno + Web Component + Shadow DOM | SolidJS, DOM nativo o iframe | Menor riesgo de mantenimiento y API pública independiente; iframe sigue como fallback si compatibilidad lo exige |
| Persistencia/entrega | PostgreSQL + outbox | Webhook fire-and-forget | El webhook solo no es durable |
| Exposición de config | Edge Function | SELECT público a tabla | Reduce filtración y acoplamiento al schema |
| Mensajería | Evolution API detrás de adapter | Acoplamiento directo | Permite cambiar conexión/proveedor y aislar secretos |
| Automatización | n8n existente + outbox externo | n8n como única cola | Evita perder eventos por fallo del workflow |
| Campos dinámicos | JSON schema versionado | Columnas distintas por cliente | Evita migraciones por cliente sin aceptar JSON arbitrario |
| Dashboard | Operación interna inicial | Portal cliente v1 | No hay evidencia de demanda; alto costo de auth/UX |

## 5. Decisiones todavía humanas

Antes de implementar los tickets afectados, el Product Owner debe aprobar:

- Modo de conexión de Evolution API y riesgo aceptado para el piloto.
- Uso comercial de n8n y licencia aplicable.
- Política de retención y base legal/consentimiento con asesoría correspondiente.
- Precio y límites del piloto.
- Región y proyecto cloud de staging/producción.
- Condiciones que permitirían publicar un SLA.

Gemini no puede convertir el valor por defecto del documento en aprobación humana.

## 6. Disparadores para reabrir arquitectura

- El p95 no cumple el objetivo después de optimizar la vertical.
- El proveedor no ofrece idempotencia o estado suficiente.
- Outbox crece más rápido que la capacidad de drenaje.
- Se incorporan datos sensibles o sector regulado.
- Un cliente necesita acceso directo o autoservicio.
- Se superan 10 tenants o la capacidad medida del entorno piloto.
- Cambian materialmente n8n, Evolution API, su licencia o modo de conexión.
- Supabase cambia grants, runtime o flujo de migraciones relevante.

## 7. Referencias externas

Verificadas el 2026-10-02:

- Supabase: grants y RLS son controles separados: <https://supabase.com/docs/guides/api/securing-your-api>
- Supabase: flujo local y despliegue de migraciones: <https://supabase.com/docs/guides/local-development/cli-workflows>
- Evolution API: tipos de conexión, autenticación y eventos: <https://github.com/evolution-foundation/evolution-api>
- n8n: orientación de licencia por caso comercial: <https://support.n8n.io/article/can-i-use-your-license-for-my-use-case>
- ANPD: seguridad para agentes de pequeño porte: <https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte>

## 8. Registro de aprobación

Completar únicamente por acción humana:

```text
Estado: BORRADOR | APROBADO | RECHAZADO
Persona:
Fecha:
Commit SHA:
Excepciones aceptadas:
```
