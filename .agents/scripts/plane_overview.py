import urllib.request
import json
import ssl

API_KEY = "plane_api_512377479beb4978a69cce11b70cac71"
WORKSPACE = "lead-flow"
PROJECT_ID = "ec68b235-edb3-4884-8d8f-6333fd34a2db"
BASE_URL = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}/"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

overview_content = """
<h1>🚀 Lead Flow Engine</h1>
<p><strong>El ecosistema SaaS B2B "White-Label" de captura de leads ultrarrápida.</strong></p>

<h2>🎯 Propuesta de Valor</h2>
<p>Desacoplamos la capa de captura (SDK SolidJS + Shadow DOM) de las webs heredadas de los clientes para garantizar un <strong>TTI &lt; 200ms</strong>, burlando problemas de CSS, rate limits y bots. El prospecto deja su teléfono, e inyectamos el lead directamente en el WhatsApp del vendedor comercial en <strong>menos de 5 segundos</strong>.</p>

<h2>🏗️ Arquitectura Técnica en 4 Capas</h2>
<ol>
<li><strong>Frontend (SDK Inyectable):</strong> <code>SolidJS</code> compilado en un Web Component (<code>solid-element</code>) bajo Shadow DOM. Aislamiento CSS al 100%. Huella: &lt; 50kb.</li>
<li><strong>Gatekeeper (Serverless API):</strong> <code>Supabase Edge Functions (Deno)</code> con validación CORS, mitigación de ataques (Honeypot) y rate limiting por IP.</li>
<li><strong>Bóveda (Persistencia):</strong> <code>Supabase PostgreSQL</code> con Row Level Security (RLS). Cero pérdida de datos, incluso si todo lo demás falla.</li>
<li><strong>Motor de Enrutamiento:</strong> <code>n8n</code> en VPS Dockerizado modo Webhook-only hacia <code>WAHA (WhatsApp HTTP API)</code> para alertas WhatsApp inmediatas, con Dead Letter Queue (DLQ).</li>
</ol>

<h2>🤖 Modelo Operacional AGILE / IA</h2>
<p>El proyecto es orquestado íntegramente por un <strong>Squad de Inteligencia Artificial (Antigravity)</strong>, operando bajo un modelo de separación de roles y responsabilidades:</p>
<ul>
<li><strong>Product Owner (Tú):</strong> Define requerimientos (PRD) y aprueba <strong>Gates</strong>.</li>
<li><strong>Analista (Pro):</strong> Escribe el contrato técnico y escenarios Gherkin (SPEC).</li>
<li><strong>Implementador (Pro):</strong> Construye la solución ciñéndose estricta y ciegamente al SPEC.</li>
<li><strong>Tester (Flash):</strong> Valida Gherkin y automatiza tests (Playwright).</li>
<li><strong>Revisor (Claude):</strong> Audita el PR de forma independiente para autorizar el pase a Producción.</li>
</ul>

<blockquote>🛡️ <em>Regla de Oro: Plane es la única Fuente de Verdad. Los roles IA se comunican exclusivamente a través del estado de los tickets, comentarios y etiquetas. Ningún código se implementa sin un SPEC ni un ticket previo.</em></blockquote>
"""

payload = {
    "description_html": overview_content
}

req = urllib.request.Request(BASE_URL, method="PATCH", headers=headers)
req.data = json.dumps(payload).encode("utf-8")
ctx = ssl.create_default_context()

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print("Overview del proyecto actualizado exitosamente.")
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
