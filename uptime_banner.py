import tkinter as tk
import psutil
from datetime import datetime
import time
import threading
import json
import os
import sys
import platform

APP_NAME = "Uptime_Banner"

BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # тимчасовий каталог PyInstaller
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOCALES_FILE = os.path.join(BASE_DIR, "locales.json")

# default config
config = {
    "topmost": True,
    "dark_theme": True,
    "autostart": False,
    "fixed_position": False,
    "window_position": "+100+100",
    "language": "en"
}

# === Localization ===
with open(os.path.join(BASE_DIR, "locales.json"), "r", encoding="utf-8") as f:
    translations = json.load(f)

def t(key):
    lang = config.get("language", "en")
    return translations.get(lang, translations["en"]).get(key, key)

def load_config():
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                loaded_config = json.load(f)
                wp = loaded_config.get("window_position")
                if isinstance(wp, dict) and "x" in wp and "y" in wp:
                    loaded_config["window_position"] = f"+{wp['x']}+{wp['y']}"
                config.update(loaded_config)
            except Exception as e:
                print(f"Помилка завантаження конфігурації: {e}")

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def set_autostart(enabled):
    if platform.system() != "Windows":
        print("Autostart does not work on this OS.")
        return

    import winreg

    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
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

    year = t("year")
    day = t("day")
    hour = t("hour")
    minute = t("minute")

    if total_seconds >= 365 * 24 * 3600:
        years = total_seconds // (365 * 24 * 3600)
        total_seconds %= (365 * 24 * 3600)
        days = total_seconds // (24 * 3600)
        total_seconds %= (24 * 3600)
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        return f"\U0001F552 {years} {year} {days} {day} {hours} {hour} {minutes} {minute}"
    elif total_seconds >= 24 * 3600:
        days = total_seconds // (24 * 3600)
        total_seconds %= (24 * 3600)
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        return f"\U0001F552 {days} {day} {hours} {hour} {minutes} {minute}"
    else:
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        return f"\U0001F552 {hours} {hour} {minutes} {minute}"

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

# === Menu functions ===
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

def toggle_fixed_position():
    config["fixed_position"] = not config["fixed_position"]
    save_config()
    update_menu()

def reset_to_defaults():
    global config
    config = {
        "topmost": True,
        "dark_theme": True,
        "autostart": False,
        "fixed_position": False,
        "window_position": "+100+100",
        "language": "en"
    }
    save_config()
    apply_theme()
    root.attributes("-topmost", config["topmost"])
    root.geometry(config["window_position"])
    set_autostart(config["autostart"])
    update_menu()
    refresh_uptime_label()

def refresh_uptime_label():
    uptime = get_uptime()
    label.config(text=uptime)

def set_language(lang_code):
    config["language"] = lang_code
    save_config()
    update_menu()
    refresh_uptime_label()

def safe_exit():
    try:
        label.unbind("<Button-3>")
        label.unbind("<Button-2>")
        menu.destroy()
    except Exception as e:
        print(f"Error during cleanup: {e}")
    root.destroy()

def update_menu():
    menu.entryconfig(0, label=f"{t('always_on_top')} {'✔' if config['topmost'] else ''}")
    menu.entryconfig(1, label=f"{t('dark_theme')} {'✔' if config['dark_theme'] else ''}")
    if platform.system() == "Windows":
        menu.entryconfig(2, label=f"{t('autostart')} {'✔' if config['autostart'] else ''}")
        menu.entryconfig(2, state='normal')
    else:
        menu.entryconfig(2, label=t('autostart'))
        menu.entryconfig(2, state='disabled')
    menu.entryconfig(3, label=f"{t('fixed_position')} {'✔' if config['fixed_position'] else ''}")
    lang_menu.entryconfig(0, label=t("lang_uk"))
    lang_menu.entryconfig(1, label=t("lang_en"))
    lang_menu.entryconfig(2, label=t("lang_ru"))
    menu.entryconfig(5, label=t("reset"))
    menu.entryconfig(6, label=t("exit"))
    menu.entryconfig(4, label=t("language"))

# === GUI ===
load_config()
set_autostart(config["autostart"])

root = tk.Tk()
root.title("Uptime Widget")
root.overrideredirect(True)
root.attributes("-topmost", config["topmost"])
root.attributes("-alpha", 0.9)
root.geometry(config.get("window_position", "+100+100"))

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
    config["window_position"] = geometry
    save_config()

label.bind("<ButtonPress-1>", start_move)
label.bind("<B1-Motion>", do_move)

menu = tk.Menu(root, tearoff=0)
menu.add_command(label=t("always_on_top"), command=toggle_topmost)
menu.add_command(label=t("dark_theme"), command=toggle_theme)
if platform.system() == "Windows":
    menu.add_command(label=t("autostart"), command=toggle_autostart)
else:
    menu.add_command(label=t("autostart"), command=None, state='disabled')
menu.add_command(label=t("fixed_position"), command=toggle_fixed_position)

lang_menu = tk.Menu(menu, tearoff=0)
lang_menu.add_command(label=t("lang_uk"), command=lambda: set_language("uk"))
lang_menu.add_command(label=t("lang_en"), command=lambda: set_language("en"))
lang_menu.add_command(label=t("lang_ru"), command=lambda: set_language("ru"))
menu.add_cascade(label=t("language"), menu=lang_menu)

menu.add_command(label=t("reset"), command=reset_to_defaults)
menu.add_command(label=t("exit"), command=safe_exit)

def show_menu(event):
    if not str(menu) or not menu.winfo_exists():
        return
    update_menu()
    try:
        menu.tk_popup(event.x_root, event.y_root)
    except tk.TclError:
        pass
    finally:
        try:
            menu.grab_release()
        except tk.TclError:
            pass

if platform.system() == "Darwin":
    label.bind("<Button-2>", show_menu)
    label.bind("<Button-3>", show_menu)
else:
    label.bind("<Button-3>", show_menu)

threading.Thread(target=update_label, daemon=True).start()

root.mainloop()
