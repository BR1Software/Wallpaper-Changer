🖼️ # Python Wallpaper Tray App (Auto-Rotator)
🔧 Features
- Rotates wallpapers every 30 minutes from a local folder
- Runs in the system tray with a toggle to enable/disable rotation
- Works on Windows, Linux, and macOS
- Uses Tkinter, Pillow, and pystray

📦 ### Step 1: Install Dependencies
```
pip install pillow pystray schedule pyinstaller
```
Or use the requirements.txt file

To create an exe run:
```
pyinstaller --clean --onefile --windowed --icon=wallpaper.ico \
  --add-data "wallpaper.ico;." \
  --add-data "wallpaper-disabled.ico;." \
  main.py
```

Alternatively, if you prefer using the spec file (which already bundles both icons), run:
```
pyinstaller main.spec --clean
```

### Autostart on Login:
- Press Win + R, type shell:startup
- Place a shortcut to your .exe in that folder
