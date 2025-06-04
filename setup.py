from setuptools import setup

APP = ['uptime_widget.py']
DATA_FILES = [('resources', ['config.json'])]  # змінено структуру
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'uptime_icon.icns',
    'packages': ['psutil'],
    'includes': ['tkinter'],
    'plist': {
        'CFBundleName': 'Uptime Banner',
        'CFBundleDisplayName': 'Uptime Banner',
        'CFBundleIdentifier': 'com.desmont.uptimebanner',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

