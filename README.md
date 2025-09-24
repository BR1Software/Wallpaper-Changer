🖼️ # Python Wallpaper Tray App (Auto-Rotator)
🔧 Features
- Rotates wallpapers every 30 minutes from a local folder
- Runs in the system tray with a toggle to enable/disable rotation
- Works on Windows, Linux, and macOS
- Uses Tkinter, Pillow, and pystray

📦 ### Step 1: Install Dependencies
```
pip install pillow pystray schedule
```

On Linux, you may also need:
```
sudo apt install libnotify-bin
```

To create an exe run:
```
pyinstaller --onefile --windowed --icon=wallpaper.ico main.py
```
