#!/usr/bin/env python3
"""
Dynamic Island for GNOME on Ubuntu.
An Apple-style, physics-animated Dynamic Island for Linux.
"""

import os
import sys
import signal

# Force GDK to use X11 backend for precise overlay positioning and input shaping on Wayland/XWayland
os.environ["GDK_BACKEND"] = "x11"

# Add current directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from src.window import DynamicIslandWindow
from src.ipc import send_command, IPCServer

def main():
    # Parse CLI flags
    args = sys.argv[1:]
    if args:
        cmd_name = args[0].lstrip("-")
        rest = " ".join(args[1:])
        cmd = f"{cmd_name} {rest}".strip()

        # Try sending to running instance
        if send_command(cmd):
            print(f"Sent '{cmd}' to running Dynamic Island.")
            return

        if cmd_name in ("theme", "toggle-theme", "dark", "light"):
            from src.utils.theme import toggle_dark_mode
            is_dark = toggle_dark_mode()
            print(f"✨ Theme switched to {'Dark' if is_dark else 'Light'} mode.")
            return

        # If it was a control command, do not start a redundant second process
        if cmd_name in ("toggle", "expand", "collapse", "tab", "media", "vitals", "controls", "timer", "settings", "notifs", "quit", "hide"):
            print(f"Notice: Dynamic Island is not currently active to handle '{cmd}'.")
            return
    else:
        # If already running, toggle expand/collapse without spawning duplicate
        if send_command("toggle"):
            print("✨ Dynamic Island is already running. Toggled window.")
            return

    # Check if another instance is already running via ping
    if send_command("ping"):
        print("✨ Dynamic Island is already running.")
        return

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Disable GNOME Mutter unresponsiveness modal for seamless background overlay
    import subprocess
    try:
        subprocess.run(
            ["gsettings", "set", "org.gnome.mutter", "check-alive-timeout", "0"],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=0.5
        )
    except Exception:
        pass

    print("🚀 Starting Dynamic Island for GNOME...")
    app = DynamicIslandWindow()
    ipc = IPCServer(app)

    try:
        Gtk.main()
    except KeyboardInterrupt:
        print("\n👋 Exiting Dynamic Island...")
    finally:
        ipc.stop()
        app.quit_app()

if __name__ == "__main__":
    main()
