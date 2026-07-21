import os
import glob

dirs = ["/home/arcav/projects/lead-flow/docs/*.md", "/home/arcav/projects/lead-flow/.agents/scripts/*.py"]

for pattern in dirs:
    for filepath in glob.glob(pattern):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "WAHA" in content or "evolution" in content:
            # Primero reemplazamos la frase completa
            new_content = content.replace("WAHA (WhatsApp HTTP API)", "WAHA (WhatsApp HTTP API)")
            # Luego reemplazamos menciones sueltas
            new_content = new_content.replace("WAHA", "WAHA")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Actualizado: {filepath}")

print("Reemplazo global de WAHA (WhatsApp HTTP API) por WAHA completado.")
