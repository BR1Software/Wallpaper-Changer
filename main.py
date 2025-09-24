import sys
import os
import json
import random
import time
import threading
from pathlib import Path
import schedule
import pystray
from pystray import MenuItem as item
import ctypes
from PIL import Image

# DEFAULT CONFIG
DEFAULT_WALLPAPER_DIR = Path.home() / "Documents" / "Backgrounds"
DEFAULT_INTERVAL_MINUTES = 30
rotation_enabled = True


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def app_dir():
    """Directory for reading/writing config (next to exe when frozen)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def config_path():
    return os.path.join(app_dir(), 'config.json')


def load_config():
    cfg = {}
    try:
        with open(config_path(), 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}
    # Support both lower/upper keys gracefully
    dir_val = cfg.get('wallpaper_dir') or cfg.get('WALLPAPER_DIR')
    interval_val = cfg.get('interval_minutes') or cfg.get('INTERVAL_MINUTES')
    wp_dir = Path(dir_val) if dir_val else DEFAULT_WALLPAPER_DIR
    try:
        interval = int(interval_val) if interval_val is not None else DEFAULT_INTERVAL_MINUTES
        if interval <= 0:
            interval = DEFAULT_INTERVAL_MINUTES
    except Exception:
        interval = DEFAULT_INTERVAL_MINUTES
    return wp_dir, interval


WALLPAPER_DIR, INTERVAL_MINUTES = load_config()


def get_random_image(folder: Path):
    try:
        if not folder.exists():
            return None
        images = [
            f for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']
        ]
        if not images:
            return None
        return random.choice(images)
    except Exception:
        return None


def set_wallpaper(image_path: Path):
    if image_path is None:
        return
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 3)


def rotate_wallpaper():
    if rotation_enabled:
        img = get_random_image(WALLPAPER_DIR)
        if img:
            set_wallpaper(img)
            print(f"Wallpaper set to: {img.name}")
        else:
            print(f"No images found in: {WALLPAPER_DIR}")


def run_scheduler():
    schedule.every(INTERVAL_MINUTES).minutes.do(rotate_wallpaper)
    while True:
        schedule.run_pending()
        time.sleep(1)


def build_menu():
    return pystray.Menu(
        item("Change Now", lambda icon, item: rotate_wallpaper(), default=True),
        item("Enable Rotation" if not rotation_enabled else "Disable Rotation", toggle_rotation),
        item("Quit", quit_app)
    )


def set_icon_image(icon: pystray.Icon):
    icon_file = "wallpaper-disabled.ico" if not rotation_enabled else "wallpaper.ico"
    icon.icon = Image.open(resource_path(icon_file))


def toggle_rotation(icon, item):
    global rotation_enabled
    rotation_enabled = not rotation_enabled
    # Update icon and menu to reflect new state
    set_icon_image(icon)
    icon.menu = build_menu()
    try:
        icon.update_menu()
    except Exception:
        pass


def quit_app(icon, item):
    icon.stop()


def create_tray_icon():
    icon_image = Image.open(resource_path("wallpaper.ico"))
    icon = pystray.Icon("WallpaperRotator", icon_image, "Wallpaper Rotator", build_menu())
    # Ensure correct icon if starting in disabled state
    set_icon_image(icon)
    icon.run()


if __name__ == "__main__":
    rotate_wallpaper()  # Change wallpaper immediately on launch
    threading.Thread(target=run_scheduler, daemon=True).start()
    create_tray_icon()