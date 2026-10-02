# Protocolo de calidad — Lead Flow v2.0

> Estado: **BORRADOR PARA GATE 0**
> Regla: una salida verde solo vale si el comando ejecutó pruebas reales sobre el alcance del ticket y quedó vinculada al commit revisado.

## 1. Principios

1. Cada criterio de aceptación tiene al menos una prueba o una evidencia manual justificada.
2. Los casos negativos son obligatorios para seguridad y resiliencia.
3. CI no puede ignorar workspaces ausentes ni sustituir pruebas por `echo`.
4. Los datos de prueba son sintéticos salvo autorización explícita.
5. Staging y producción requieren credenciales y evidencias separadas.
6. Una compilación exitosa no demuestra comportamiento, seguridad ni composición visual.
7. Las pruebas destructivas solo se ejecutan en local o staging desechable aprobado.

## 2. Contrato del quality gate

`LEADFLOW-03` debe convertir estos nombres en comandos reales y reproducibles:

| Gate | Obligación |
| --- | --- |
| Formato/lint | Analiza todos los archivos aplicables y sale distinto de cero ante errores |
| Typecheck | Ejecuta el compilador de cada workspace TypeScript existente |
| Unit tests | Ejecuta suites reales; falla si no encuentra las suites obligatorias del ticket |
| Build | Construye artefactos reales; falla si el paquete objetivo no existe |
| Database tests | Recrea Supabase local desde cero y prueba grants/RLS |
| Free-tier readiness | Confirma inventario, presupuesto de datos, alerta de cuota y retención antes de datos reales |
| E2E | Ejecuta flujos del widget contra servicios locales/staging controlado |
| Security checks | Comprueba acceso público, secretos y aislamiento multi-tenant |

El contrato final puede usar comandos como `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build` y `supabase db reset`, pero el SPEC de `LEADFLOW-03` debe comprobar primero la CLI instalada y definirlos según la estructura real. No se adivinan flags.

### Prueba anti-falso-verde

CI debe tener pruebas que demuestren:

- Un error TypeScript hace fallar typecheck.
- Un error de lint hace fallar lint.
- Eliminar/renombrar el workspace SDK hace fallar su build.
- Una suite obligatoria ausente hace fallar tests.
- Un comando que solo imprime texto no satisface el gate.

## 3. Matriz de verificación por ticket

| Tipo de cambio | Verificación mínima |
| --- | --- |
| Documentación/gobernanza | Enlaces internos, estados, IDs, contradicciones y diff |
| Tooling/CI | Prueba positiva + prueba deliberadamente fallida |
| Migración SQL | Reset local, test de constraints, grants, RLS y advisors |
| Edge Function | Unit/integration, errores, límites, CORS y logs sin PII |
| Outbox/worker | Idempotencia, concurrencia, retry, lock recovery y dead letter |
| SDK | Unit, build, tamaño, Shadow DOM, accesibilidad y hosts de prueba |
| Proveedor | Contract tests y staging; no enviar a números reales sin GATE 2 |
| Deploy | Smoke test, métricas, rollback y revisión de secretos |

## 4. Escenarios críticos del MVP

### 4.1 Configuración pública mínima

```gherkin
Escenario: El widget obtiene solo configuración pública
  Dado un cliente activo y un origen permitido
  Cuando solicita su configuración
  Entonces recibe campos, tema, textos, versión y privacidad
  Y no recibe webhooks, claves, proveedor ni configuración privada
```

```gherkin
Escenario: Un origen no permitido consulta configuración
  Dado un client_id válido desde un origen no registrado
  Cuando solicita configuración
  Entonces la respuesta no revela configuración operativa
  Y el evento queda registrado sin PII
```

### 4.2 Captura y persistencia atómica

```gherkin
Escenario: Una captura válida queda durable
  Dado un payload válido con consentimiento e idempotency key nueva
  Cuando se invoca capture
  Entonces existe exactamente un lead
  Y existe exactamente un evento pending asociado
  Y la respuesta incluye lead_id y correlation_id
```

```gherkin
Escenario: No se responde éxito ante escritura parcial
  Dado un fallo al crear el evento de entrega
  Cuando se intenta capturar un lead
  Entonces no queda un lead huérfano
  Y la API no responde accepted
```

### 4.3 Idempotencia

```gherkin
Escenario: Un retry del navegador no duplica
  Dado un lead ya aceptado para una idempotency key
  Cuando se repite la solicitud equivalente
  Entonces se devuelve el resultado original
  Y no se crea otro lead ni otro evento
```

### 4.4 Seguridad de base de datos

```gherkin
Escenario: Anon no accede a tablas internas
  Dado un cliente con publishable key
  Cuando intenta SELECT o INSERT directo en clients, leads o delivery_outbox
  Entonces Postgres/Data API rechaza la operación
```

```gherkin
Escenario: No hay lectura cruzada
  Dado datos de dos tenants
  Cuando un contexto limitado al tenant A consulta datos
  Entonces ninguna fila del tenant B es visible o modificable
```

Las pruebas deben distinguir permisos de objeto (`GRANT/REVOKE`) de políticas de fila (RLS).

### 4.5 Fallo y recuperación del proveedor

```gherkin
Escenario: La mensajería está caída
  Dado un evento pending y un proveedor no disponible
  Cuando el dispatcher intenta entregarlo
  Entonces el lead permanece persistido
  Y el evento pasa a retry_scheduled con error sanitizado
  Y el prospecto no recibe un error posterior al accepted original
```

```gherkin
Escenario: El proveedor se recupera
  Dado un evento retry_scheduled cuyo next_attempt_at venció
  Cuando el worker lo reprocesa
  Entonces el proveedor lo acepta una sola vez
  Y el evento queda accepted con timestamps y provider_message_id cuando exista
```

```gherkin
Escenario: Un worker muere con un lock
  Dado un evento processing con lock vencido
  Cuando otro worker ejecuta recuperación
  Entonces el evento vuelve a ser reclamable sin crear otra obligación
```

### 4.6 Rate limiting y bots

- Honeypot lleno: no crea lead; la respuesta pública no explica la heurística.
- Payload por encima del límite: `413` o código definido; cero escrituras.
- JSON inválido/campos inesperados: `400/422`; cero escrituras.
- Exceso por clave/IP: `429`; no depende de memoria local del isolate.
- `Origin` falsificado: no se considera autenticación suficiente.
- Headers de proxy: solo se confían desde infraestructura conocida.

### 4.7 Privacidad

- Consentimiento requerido cuando el diseño aprobado lo exija.
- Se persisten versión, fecha y fuente del consentimiento.
- Logs y traces no contienen teléfono/email completos.
- Exportación localiza únicamente el titular correcto.
- Eliminación o anonimización respeta dependencias y queda auditada.
- Retención elimina/anomiza registros vencidos en entorno de prueba.

### 4.8 SDK y aislamiento

Probar en fixtures controladas con:

- Bootstrap/reset global.
- Tailwind preflight.
- Selectores universales y `!important` del host.
- Dos instancias del widget en la misma página.
- Carga tardía y repetida del script.
- CSP documentada del host.
- Navegación por teclado y lector de pantalla básico.
- Input de teléfono móvil y errores asociados por `aria-describedby`.
- Zoom, viewport estrecho y texto ampliado.

La frase correcta es “aislamiento probado contra la matriz soportada”, no “inmunidad absoluta”. CSS heredable, custom properties y decisiones del host deben considerarse explícitamente.

## 5. Rendimiento

### Bundle

- Medir artefacto de producción minificado.
- Reportar tamaño raw, gzip y Brotli.
- Fallar CI si el presupuesto aprobado se supera.
- Registrar qué incluye y excluye el artefacto.

### Latencia

Definiciones:

```text
capture_latency = response_sent_at - submission_received_at
provider_latency = provider_accepted_at - submission_received_at
recovery_latency = accepted_after_recovery_at - provider_outage_started_at
```

Reportar p50, p95, p99, tamaño de muestra, región, entorno, proveedor y periodo. No usar una única medición como garantía.

### Carga

La prueba inicial usa perfiles progresivos, no solo “100 requests simultáneas”:

1. Baseline secuencial.
2. Burst corto de captura.
3. Carga sostenida esperada del piloto.
4. Proveedor lento/caído mientras siguen entrando leads.
5. Recuperación del backlog.

Los límites y volúmenes se fijan en el SPEC con base en el piloto previsto.

## 6. Seguridad operacional

Antes de staging o producción:

- Escanear archivos versionados por patrones de secretos.
- Confirmar que `.env`, CSV de credenciales y archivos de sesión no están trackeados.
- Revisar grants efectivos y políticas RLS.
- Ejecutar asesores de Supabase disponibles para la versión instalada.
- Verificar que Evolution API/n8n no estén expuestos directamente a internet sin controles aprobados, y que ningún secreto llegue al browser o a los logs.
- Confirmar TLS, firewall, backups, restore y rotación de claves.
- Probar rollback sin destruir datos remotos.

## 7. Evidencia obligatoria de entrega

El comentario de handoff incluye:

```markdown
Commit probado: <sha>
Entorno: local | staging
SPEC: docs/SPEC-LEADFLOW-XX.md @ <versión>

Comandos ejecutados:
- <comando> → PASS/FAIL, N tests

Gherkin:
- [x] <escenario> → <archivo/test>

Métricas:
- <métrica, muestra, resultado>

Riesgos/exclusiones:
- <pendiente explícito>
```

No pegar tokens, URLs con credenciales, payloads reales ni salidas que los contengan.

## 8. Gate de release

Un ticket no pasa a `En revisión` hasta que:

- Todos sus criterios tienen evidencia.
- El SHA probado coincide con el SHA entregado.
- CI ejecutó gates reales.
- No hay cambios no explicados dentro del alcance.
- El diff no contiene secretos ni PII.
- La documentación afectada fue actualizada.
- Existe plan de rollback cuando cambia estado remoto.
- Las excepciones están aprobadas; no se ocultan como “warning”.

Producción requiere además `GATE 2` y smoke test posterior. El merge por sí solo no autoriza deploy.

En un proyecto Supabase Free, el smoke test incluye verificar el plan/estado observados, tamaño de base de datos, egress y uso de funciones sin publicar secretos. Una cuota cercana, estado read-only o proyecto pausado bloquea el piloto hasta decisión humana.
