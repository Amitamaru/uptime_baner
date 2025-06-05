import json
import os
import subprocess
import shutil

# Єдине джерело правди
metadata = {
    "APP_NAME": "uptime_widget",
    "APP_VERSION": "1.3.3"
}

# Записуємо у metadata.json
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

# Формуємо назву exe
output_name = f"{metadata['APP_NAME'].replace('_', ' ')} v{metadata['APP_VERSION']}.exe"

# Збірка
subprocess.run([
    "pyinstaller",
    "--noconsole",
    "--onefile",
    "--icon=uptime_icon.ico",
    "--add-data=locales.json;.",
    "--add-data=links.json;.",
    "--add-data=metadata.json;.",
    "uptime_widget.py"
])

# Перейменування
dist_path = os.path.join("dist", f"{metadata['APP_NAME']}.exe")
new_path = os.path.join("dist", output_name)

if os.path.exists(dist_path):
    shutil.move(dist_path, new_path)
    print(f"[+] Output renamed to: {output_name}")
else:
    print("[!] Build failed: .exe not found.")
