import urllib.request
import json
import ssl
import os
import glob
import subprocess

API_KEY = "plane_api_512377479beb4978a69cce11b70cac71"
WORKSPACE = "lead-flow"
PROJECT_ID = "ec68b235-edb3-4884-8d8f-6333fd34a2db"
BASE_URL = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def request(method, path, data=None):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode("utf-8")
    
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code} on {path}: {e.read().decode()}")
        return None

# 1. Obtener todas las pages actuales
print("Obteniendo pages existentes...")
pages_response = request("GET", "/pages/")
existing_pages = {p["name"]: p["id"] for p in pages_response.get("results", [])}

docs_dir = "/home/arcav/projects/lead-flow/docs"
md_files = glob.glob(os.path.join(docs_dir, "*.md"))

for file_path in md_files:
    filename = os.path.basename(file_path)
    page_name = filename.replace(".md", "")
    
    # Convertir a HTML real usando npx marked
    print(f"Convirtiendo {filename} a HTML...", flush=True)
    result = subprocess.run(["npx", "--yes", "marked", file_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error procesando {filename} con marked: {result.stderr}", flush=True)
        continue
        
    html_content = result.stdout
    
    payload = {
        "name": page_name,
        "description_html": html_content
    }
    
    if page_name in existing_pages:
        print(f"Eliminando page vieja {page_name}...", flush=True)
        page_id = existing_pages[page_name]
        request("DELETE", f"/pages/{page_id}/")
        
    print(f"Creando nueva page formateada {page_name}...", flush=True)
    request("POST", "/pages/", payload)
    
print("Proceso de formateo finalizado.", flush=True)
