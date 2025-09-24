import os
import sys
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# Defaults must match main.py
DEFAULT_WALLPAPER_DIR = Path.home() / "Documents" / "Backgrounds"
DEFAULT_INTERVAL_MINUTES = 30


def app_dir():
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
    dir_val = cfg.get('wallpaper_dir') or cfg.get('WALLPAPER_DIR')
    interval_val = cfg.get('interval_minutes') or cfg.get('INTERVAL_MINUTES')
    wallpaper_dir = str(dir_val) if dir_val else str(DEFAULT_WALLPAPER_DIR)
    try:
        interval = int(interval_val) if interval_val is not None else DEFAULT_INTERVAL_MINUTES
        if interval <= 0:
            interval = DEFAULT_INTERVAL_MINUTES
    except Exception:
        interval = DEFAULT_INTERVAL_MINUTES
    return wallpaper_dir, interval


def save_config(wallpaper_dir: str, interval_minutes: int):
    data = {
        'wallpaper_dir': wallpaper_dir,
        'interval_minutes': int(interval_minutes)
    }
    with open(config_path(), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


class SettingsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Wallpaper Rotator Settings")
        self.root.resizable(False, False)

        wp_dir, interval = load_config()

        # Wallpaper folder
        tk.Label(root, text="Wallpaper Folder:").grid(row=0, column=0, padx=10, pady=(12, 6), sticky='w')
        self.dir_var = tk.StringVar(value=wp_dir)
        self.dir_entry = tk.Entry(root, textvariable=self.dir_var, width=48)
        self.dir_entry.grid(row=1, column=0, padx=10, pady=4, sticky='w')
        tk.Button(root, text="Browse...", command=self.browse_dir).grid(row=1, column=1, padx=10, pady=4)

        # Interval
        tk.Label(root, text="Change Interval (minutes):").grid(row=2, column=0, padx=10, pady=(12, 6), sticky='w')
        self.interval_var = tk.IntVar(value=interval)
        self.interval_spin = tk.Spinbox(root, from_=1, to=1440, textvariable=self.interval_var, width=10)
        self.interval_spin.grid(row=3, column=0, padx=10, pady=4, sticky='w')

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=12)
        tk.Button(btn_frame, text="Save", width=12, command=self.save).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Close", width=12, command=root.destroy).pack(side='left', padx=5)

    def browse_dir(self):
        current = self.dir_var.get() or str(DEFAULT_WALLPAPER_DIR)
        chosen = filedialog.askdirectory(initialdir=current, title="Choose Wallpaper Folder")
        if chosen:
            self.dir_var.set(chosen)

    def save(self):
        folder = self.dir_var.get().strip()
        try:
            interval = int(self.interval_var.get())
        except Exception:
            interval = 0
        if interval <= 0:
            messagebox.showerror("Invalid Interval", "Please enter a positive number of minutes.")
            return
        if not folder:
            messagebox.showerror("Invalid Folder", "Please choose a wallpaper folder.")
            return
        p = Path(folder)
        if not p.exists() or not p.is_dir():
            messagebox.showerror("Invalid Folder", "The selected folder does not exist.")
            return
        try:
            save_config(folder, interval)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")
            return
        messagebox.showinfo("Saved", "Settings have been saved.\n\nNote: Restart the tray app to apply changes.")


if __name__ == '__main__':
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()
