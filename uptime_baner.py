import tkinter as tk
import psutil
from datetime import datetime
import time
import threading
import json
import os
import sys
import winreg

APP_NAME = "UptimeWidget"


# === Шлях до директорії, де лежить exe або py-файл ===
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# Конфіг за замовчуванням
config = {
    "topmost": True,
    "dark_theme": True,
    "autostart": False,
    "fixed_position": False,  # 🆕 Фіксація положення
    "window_position": "+100+100"  # 🆕 Позиція вікна
}

def load_config():
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                loaded_config = json.load(f)

                # 🛠 Автовиправлення формату window_position
                wp = loaded_config.get("window_position")
                if isinstance(wp, dict) and "x" in wp and "y" in wp:
                    loaded_config["window_position"] = f"+{wp['x']}+{wp['y']}"

                config.update(loaded_config)
            except Exception as e:
                print(f"Помилка завантаження конфігурації: {e}")


def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Автозапуск
def set_autostart(enabled):
    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run",
                         0, winreg.KEY_SET_VALUE)
    if enabled:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
    else:
        try:
            winreg.DeleteValue(key, APP_NAME)
        except FileNotFoundError:
            pass
    key.Close()

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    total_seconds = int(uptime.total_seconds())

    if total_seconds >= 365 * 24 * 3600:
        years = total_seconds // (365 * 24 * 3600)
        total_seconds %= (365 * 24 * 3600)
        days = total_seconds // (24 * 3600)
        total_seconds %= (24 * 3600)
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        return f"🕒 {years} рік(и) {days} дн {hours} год {minutes} хв"
    elif total_seconds >= 24 * 3600:
        days = total_seconds // (24 * 3600)
        total_seconds %= (24 * 3600)
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        return f"🕒 {days} дн {hours} год {minutes} хв"
    else:
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        return f"🕒 {hours} год {minutes} хв"

def update_label():
    while True:
        uptime = get_uptime()
        label.config(text=uptime)
        time.sleep(60)

def apply_theme():
    bg = "#222" if config["dark_theme"] else "#f0f0f0"
    fg = "white" if config["dark_theme"] else "black"
    label.config(bg=bg, fg=fg)
    root.config(bg=bg)

# === Функції меню ===
def toggle_topmost():
    config["topmost"] = not config["topmost"]
    root.attributes("-topmost", config["topmost"])
    save_config()
    update_menu()

def toggle_theme():
    config["dark_theme"] = not config["dark_theme"]
    apply_theme()
    save_config()
    update_menu()

def toggle_autostart():
    config["autostart"] = not config["autostart"]
    set_autostart(config["autostart"])
    save_config()
    update_menu()

# 🆕 Фіксація позиції
def toggle_fixed_position():
    config["fixed_position"] = not config["fixed_position"]
    save_config()
    update_menu()

# 🆕 Скидання до дефолтних значень
def reset_to_defaults():
    global config
    config = {
        "topmost": True,
        "dark_theme": True,
        "autostart": False,
        "fixed_position": False,
        "window_position": "+100+100"
    }
    save_config()
    apply_theme()
    root.attributes("-topmost", config["topmost"])
    root.geometry(config["window_position"])
    set_autostart(config["autostart"])
    update_menu()

def update_menu():
    menu.entryconfig(0, label=f"Завжди поверх вікон {'✔' if config['topmost'] else ''}")
    menu.entryconfig(1, label=f"Темна тема {'✔' if config['dark_theme'] else ''}")
    menu.entryconfig(2, label=f"Автозапуск з Windows {'✔' if config['autostart'] else ''}")
    menu.entryconfig(3, label=f"Фіксувати положення {'✔' if config['fixed_position'] else ''}")

# === GUI ===
load_config()
set_autostart(config["autostart"])  # синхронізація

root = tk.Tk()
root.title("Uptime Widget")
root.overrideredirect(True)
root.attributes("-topmost", config["topmost"])
root.attributes("-alpha", 0.9)
root.geometry(config.get("window_position", "+100+100"))  # 🆕 Початкове положення

label = tk.Label(root, text="", font=("Segoe UI", 14), padx=10, pady=5)
label.pack()

apply_theme()

def start_move(event):
    if config.get("fixed_position"):
        return
    root.x = event.x
    root.y = event.y

def do_move(event):
    if config.get("fixed_position"):
        return
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    geometry = f"+{x}+{y}"
    root.geometry(geometry)
    config["window_position"] = geometry  # зберігаємо як рядок!
    save_config()


label.bind("<ButtonPress-1>", start_move)
label.bind("<B1-Motion>", do_move)

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="", command=toggle_topmost)
menu.add_command(label="", command=toggle_theme)
menu.add_command(label="", command=toggle_autostart)
menu.add_command(label="", command=toggle_fixed_position)  # 🆕
menu.add_separator()
menu.add_command(label="Скинути налаштування", command=reset_to_defaults)  # 🆕
menu.add_command(label="Вийти", command=root.destroy)

def show_menu(event):
    update_menu()
    menu.tk_popup(event.x_root, event.y_root)

label.bind("<Button-3>", show_menu)

threading.Thread(target=update_label, daemon=True).start()

root.mainloop()
