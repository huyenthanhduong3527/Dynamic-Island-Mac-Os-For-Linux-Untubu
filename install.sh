#!/usr/bin/env bash
# Installation script for Dynamic Island & macOS Menu Bar for GNOME
# Sets up desktop launcher, system autostart, and top menu bar extension

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/scalable/apps"
AUTOSTART_DIR="${HOME}/.config/autostart"
EXT_DIR="${HOME}/.local/share/gnome-shell/extensions/macos-menu-bar@Nguyenthanhtam"

echo "========================================================"
echo "🏝️  Installing Dynamic Island & macOS Menu Bar for GNOME"
echo "========================================================"

# 1. Check system dependencies (GTK3, PyGObject, Cairo, DBus, psutil, X11 tools)
echo "📦 Checking system dependencies..."
MISSING_PKGS=()
for pkg in python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-psutil python3-dbus x11-xserver-utils; do
    if ! dpkg -s "$pkg" >/dev/null 2>&1; then
        MISSING_PKGS+=("$pkg")
    fi
done

if [ ${#MISSING_PKGS[@]} -ne 0 ]; then
    echo "⚠️  Missing required packages: ${MISSING_PKGS[*]}"
    if command -v sudo >/dev/null 2>&1; then
        echo "   Installing via apt..."
        sudo apt update && sudo apt install -y "${MISSING_PKGS[@]}"
    else
        echo "   Please install them manually using: sudo apt install -y ${MISSING_PKGS[*]}"
    fi
else
    echo "✅ All required system packages are installed."
fi

# 2. Create necessary directories
mkdir -p "${APP_DIR}" "${ICON_DIR}" "${AUTOSTART_DIR}" "${EXT_DIR}"

# 2. Generate App Icon SVG
echo "🎨 Installing high-res application icon..."
cat << 'SVG_EOF' > "${ICON_DIR}/dynamic-island.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#c084fc"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <rect x="20" y="46" width="88" height="36" rx="18" fill="#000000" stroke="url(#glow)" stroke-width="2.5"/>
  <circle cx="38" cy="64" r="6" fill="#38bdf8"/>
  <rect x="52" y="61" width="36" height="6" rx="3" fill="#ffffff" opacity="0.8"/>
  <circle cx="98" cy="64" r="3" fill="#22c55e"/>
</svg>
SVG_EOF

# 3. Update & install desktop file
echo "🖥️  Configuring desktop entry and autostart..."
sed "s|Exec=.*|Exec=${SCRIPT_DIR}/run.sh|g" "${SCRIPT_DIR}/dynamic-island.desktop" > "${APP_DIR}/dynamic-island.desktop"
chmod +x "${APP_DIR}/dynamic-island.desktop"
cp "${APP_DIR}/dynamic-island.desktop" "${AUTOSTART_DIR}/dynamic-island.desktop"

# 4. Install GNOME Shell Extension
echo "🍏 Installing macOS Menu Bar GNOME Shell Extension..."
ln -sfn "${SCRIPT_DIR}" "${HOME}/.local/share/dynamic-island"
chmod +x "${SCRIPT_DIR}/run.sh" "${SCRIPT_DIR}/main.py" "${SCRIPT_DIR}/install.sh"

if [ -d "${SCRIPT_DIR}/extensions/macos-menu-bar@Nguyenthanhtam" ]; then
    cp -rf "${SCRIPT_DIR}/extensions/macos-menu-bar@Nguyenthanhtam/"* "${EXT_DIR}/"
    echo "   - Copied extension files to ${EXT_DIR}"
    
    # Enable in gsettings
    if command -v gsettings >/dev/null 2>&1; then
        CURRENT_EXTS=$(gsettings get org.gnome.shell enabled-extensions)
        if [[ "$CURRENT_EXTS" != *"macos-menu-bar@Nguyenthanhtam"* ]]; then
            NEW_EXTS=$(echo "$CURRENT_EXTS" | sed "s/]/, 'macos-menu-bar@Nguyenthanhtam']/")
            gsettings set org.gnome.shell enabled-extensions "$NEW_EXTS" 2>/dev/null || true
            echo "   - Added to org.gnome.shell enabled-extensions"
        fi
        gsettings set org.gnome.mutter check-alive-timeout 0 2>/dev/null || true
    fi

    # Try enabling extension via CLI
    if command -v gnome-extensions >/dev/null 2>&1; then
        gnome-extensions enable macos-menu-bar@Nguyenthanhtam 2>/dev/null || true
    fi
fi

# 5. Update system icon & desktop database caches
update-desktop-database "${APP_DIR}" 2>/dev/null || true
gtk-update-icon-cache "${HOME}/.local/share/icons/hicolor" 2>/dev/null || true

# 6. Suppress native GNOME Shell volume OSD in user themes so it only displays on Dynamic Island
if [ -d "${HOME}/.themes" ]; then
    for css in "${HOME}/.themes"/*/gnome-shell/gnome-shell.css; do
        if [ -f "$css" ] && ! grep -q "Suppress Native GNOME OSD" "$css"; then
            cat << 'CSS_EOF' >> "$css"

/* Suppress Native GNOME OSD (Volume & Brightness HUD Popups) */
.osd-window, .osd-window * {
    opacity: 0 !important;
    min-width: 0px !important;
    min-height: 0px !important;
    width: 0px !important;
    height: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
    border: none !important;
    background-color: transparent !important;
    box-shadow: none !important;
    color: transparent !important;
}
CSS_EOF
        fi
    done
fi

echo ""
echo "========================================================"
echo "✨ Installation completed successfully!"
echo "   - Dynamic Island launcher added to GNOME Application Grid"
echo "   - Autostart enabled on user login"
echo "   - macOS Menu Bar extension configured in GNOME Shell"
echo "   - To start immediately: ./run.sh"
echo "========================================================"
