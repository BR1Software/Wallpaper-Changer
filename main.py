import os
import random
import time
import threading
from pathlib import Path
from PIL import Image
import schedule
import pystray
from pystray import MenuItem as item
import ctypes

# CONFIG
WALLPAPER_DIR = Path.home() / "Documents" / "Backgrounds"
INTERVAL_MINUTES = 30
rotation_enabled = True

def get_random_image(folder):
    return random.choice([
        f for f in folder.iterdir()
        if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']
    ])

def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 3)

def rotate_wallpaper():
    if rotation_enabled:
        img = get_random_image(WALLPAPER_DIR)
        set_wallpaper(img)
        print(f"Wallpaper set to: {img.name}")

def run_scheduler():
    schedule.every(INTERVAL_MINUTES).minutes.do(rotate_wallpaper)
    while True:
        schedule.run_pending()
        time.sleep(1)

def toggle_rotation(icon, item):
    global rotation_enabled
    rotation_enabled = not rotation_enabled
    item.text = "Enable Rotation" if not rotation_enabled else "Disable Rotation"

def quit_app(icon, item):
    icon.stop()

def create_tray_icon():
    from PIL import Image
    icon_image = Image.open("wallpaper.ico")

    menu = (
        item("Change Now", lambda icon, item: rotate_wallpaper()),
        item("Disable Rotation", toggle_rotation),
        item("Quit", quit_app)
    )
    icon = pystray.Icon("WallpaperRotator", icon_image, "Wallpaper Rotator", menu)
    icon.run()

if __name__ == "__main__":
    rotate_wallpaper()  # Change wallpaper immediately on launch
    threading.Thread(target=run_scheduler, daemon=True).start()
    create_tray_icon()