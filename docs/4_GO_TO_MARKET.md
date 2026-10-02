# Go-to-market — Lead Flow v2.0

> Estado: **BORRADOR PARA GATE 0**
> Etapa: descubrimiento y piloto. No hay autorización para publicar claims ni contactar prospectos desde este documento.

## 1. Posicionamiento

**Lead Flow ayuda a equipos que venden por WhatsApp a recibir cada prospecto con rapidez y trazabilidad, sin reemplazar su sitio actual.**

La venta comienza por el problema comercial —tiempo de respuesta y leads invisibles— y demuestra la solución con datos. No se presentan detalles de Preact, Supabase, n8n o Evolution API como propuesta de valor principal.

## 2. ICP inicial

Prioridad:

- Empresa con campañas activas y formularios web.
- Venta consultiva o de ticket suficiente para valorar cada lead.
- WhatsApp ya forma parte de la atención.
- Director comercial/propietario accesible.
- Sitio WordPress, HTML o stack compatible.
- Disposición a medir tiempo de respuesta antes y después.

No priorizar inicialmente:

- Mensajería masiva o listas compradas.
- Sectores con datos sensibles sin revisión especializada.
- Clientes que exijan SLA alto antes del piloto.
- Casos que dependan de automatización conversacional compleja.

## 3. Reglas de claims

### Permitido

- Datos medidos para ese prospecto, con fecha, herramienta y condiciones.
- Objetivos identificados como objetivos.
- Resultados agregados de pilotos con muestra y periodo.
- Limitaciones del proveedor y del entorno.

### Prohibido

- “Tenemos 50 clientes” sin evidencia real.
- “99.9% garantizado” sin contrato, monitoreo e historial.
- “Nunca se pierde un lead” sin prueba de recuperación y límites definidos.
- “Reduce 40% el abandono” sin fuente aplicable.
- “Misma infraestructura de grandes retailers” sin caso verificable.
- Simular que se probó un formulario o campaña cuando no ocurrió.

## 4. Descubrimiento antes de vender

Registrar respuestas, no inferencias:

1. ¿De dónde llegan hoy los leads?
2. ¿Quién los ve primero y cuánto tarda?
3. ¿Cuántos se pierden o quedan sin respuesta?
4. ¿Qué canal usa ventas realmente?
5. ¿Quién controla la web y cuánto tarda un cambio?
6. ¿Qué datos pide el formulario y por qué?
7. ¿Qué consentimiento y política de privacidad existen?
8. ¿Qué volumen máximo genera una campaña?
9. ¿Qué costo tiene un lead y una venta?
10. ¿Qué falla sería inaceptable?

## 5. Oferta de piloto

El piloto debe tener límites explícitos:

- Un sitio y un formulario.
- Un equipo/ruta de notificación.
- Duración y volumen definidos.
- Datos mínimos.
- Proveedor de mensajería y riesgo informados.
- Métricas acordadas antes de empezar.
- Responsable del cliente.
- Precio piloto o compromiso de compra condicionado a resultados.

### Métricas del piloto

- Capturas iniciadas, válidas y rechazadas.
- Leads persistidos.
- Alertas aceptadas/fallidas/reintentadas.
- Latencia p50/p95/p99.
- Tiempo humano de onboarding y soporte.
- Tiempo de primera respuesta comercial, si el cliente lo comparte.
- Conversión posterior, si puede medirse legalmente.

## 6. Demo de velocidad

La demo puede pedir el teléfono del visitante únicamente si:

- Explica que enviará un mensaje de prueba.
- Muestra finalidad, responsable y enlace de privacidad.
- Registra la aceptación requerida.
- No reutiliza el número para marketing no informado.
- Permite eliminar el dato según la política.
- Usa datos de latencia reales del evento, no una animación simulada.

La pantalla debe distinguir:

```text
Guardado: sí/no
Proveedor aceptó: sí/no
Tiempo observado: N ms
```

## 7. Mensaje outbound honesto

Plantilla adaptable, solo con mediciones reales:

> Revisé la experiencia móvil de `[sitio]` el `[fecha]`. Observé `[dato verificable]`. Lead Flow instala un flujo que guarda cada solicitud y mide cuánto tarda en llegar al equipo comercial. Estamos abriendo un piloto limitado para empresas que venden por WhatsApp. ¿Tiene sentido revisar durante 15 minutos cómo reciben hoy sus leads?

No enviar formularios reales de terceros como “prueba” sin autorización. Para auditar velocidad se prefieren herramientas no invasivas y datos públicos.

## 8. Funnel inicial

```text
20 conversaciones de descubrimiento
        ↓
5 diagnósticos con datos
        ↓
2 propuestas de piloto
        ↓
1 piloto activo
        ↓
decisión basada en evidencia
```

Los números son un objetivo operativo inicial, no una tasa de conversión esperada.

## 9. Pruebas de precio

Probar un precio completo, no “¿cuánto pagarías?”:

- Setup definido.
- MRR definido.
- Qué incluye y qué queda fuera.
- Límite de formularios, sitios, volumen y soporte.
- Proveedor de mensajería incluido o trasladado.
- Tratamiento de sobrecostos.

Registrar aceptación, objeción concreta y alternativa solicitada. No reducir precio sin identificar qué alcance se elimina.

## 10. Onboarding piloto

1. Confirmar responsables, finalidad y datos.
2. Aprobar proveedor de mensajería y riesgo.
3. Configurar staging con datos sintéticos.
4. Instalar el snippet en una página controlada.
5. Ejecutar pruebas de captura, fallo y recuperación.
6. Aprobar privacidad y copy del formulario.
7. Obtener `GATE 2` para producción.
8. Activar volumen limitado y observar.
9. Entregar reporte del piloto y decisión.

“24 horas” es un objetivo a medir desde que todas las dependencias del cliente están disponibles; no empieza antes de recibir accesos, textos y aprobación.

## 11. Evidencia comercial

| Nivel | Evidencia | Claim permitido |
| --- | --- | --- |
| 0 | Documento/arquitectura | “Estamos desarrollando” |
| 1 | Demo controlada | “En esta prueba observamos…” |
| 2 | Piloto real | “En este piloto y periodo…” |
| 3 | Varios pilotos comparables | Resultado agregado con muestra |
| 4 | Operación estable | SLA contractual dentro de condiciones |

Cada material comercial debe indicar el nivel real. Gemini no puede elevarlo por inferencia.
