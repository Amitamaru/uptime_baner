
# 🕒 Uptime Widget

A small widget for Windows that displays system uptime in a compact window, always on top. Built in Python using `tkinter` GUI.

## 📦 Features

- Displays system uptime in days / hours / minutes
- Toggle between light / dark themes
- Optional "always on top" mode
- Remembers window position across restarts
- Lock window position to prevent accidental movement
- Automatic launch at Windows startup
- Right-click context menu for controls
- Supports **3 languages**: Ukrainian, English, Russian
- Reset all settings to defaults
- Fully self-contained `.exe` file (via PyInstaller)

## 🌐 Supported Languages

- 🇺🇦 Ukrainian
- 🇬🇧 English
- 🇷🇺 Russian

Language can be changed instantly via context menu → **Language**.

## ⚙️ Configuration

All settings are stored in a local `config.json` file in the same directory:

```json
{
  "topmost": true,
  "dark_theme": true,
  "autostart": false,
  "fixed_position": false,
  "window_position": "+100+100",
  "language": "uk"
}
```

## 🛠 How to Create `.exe` (Windows)

To convert the Python script into a `.exe` file, use PyInstaller:

### Steps:

1. Install PyInstaller (one-time):

   ```
   pip install pyinstaller
   ```

2. Navigate to the script directory and run:

   ```
   pyinstaller --noconsole --onefile uptime_widget.py
   ```

   - `--onefile`: creates a single `.exe` file
   - `--noconsole`: hides the black console window (for GUI apps)

3. After execution, these folders will be created:
   - `dist/` — contains the final `uptime_widget.exe` file
   - `build/` — temporary build files
   - `uptime_widget.spec` — build config (can be reused)

4. You can now run `dist/uptime_widget.exe`. A `config.json` file will be created next to it on first launch.

### Optional: Add icon

To include your own `.ico` file as icon:

```
pyinstaller --noconsole --onefile --icon=my_icon.ico uptime_widget.py
```

## 🏁 How to Run

1. Ensure Python is installed:
   ```
   python --version
   ```

2. Install dependencies:
   ```
   pip install psutil
   ```

3. Launch the script:
   ```
   python uptime_widget.py
   ```

## 🧹 Reset Settings

Right-click the widget → **Reset settings** to restore defaults:

- Language: **English**
- Theme: **Dark**
- Position: **+100+100**
- Other features: disabled

---

## 🔁 Autostart

When **Autostart with Windows** is enabled, the app adds a registry entry at:

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

This enables automatic launch on user login.

---

## 🧠 Author

Developed by Dmytro for personal use and to learn Python GUI development.  
Contributions welcome 😉
