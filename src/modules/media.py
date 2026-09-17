"""
Universal Audio & Media Manager for Dynamic Island.
Detects ANY audio playing on the system via PipeWire / WirePlumber streams (SoundCloud,
browser tabs, Spotify, games, VLC, videos, etc.) and integrates with MPRIS2 D-Bus.
Features a high-efficiency background thread to monitor playback with zero UI latency.
"""

import time
import subprocess
import json
import re
import threading
import dbus
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
from src.utils.artwork import fetch_online_artwork_async, load_artwork_pixbuf

DEMO_PLAYLIST = [
    {
        "title": "Die With A Smile",
        "artist": "Lady Gaga & Bruno Mars",
        "album": "Single",
        "length": 251,
    },
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "length": 200,
    },
    {
        "title": "Nơi Này Có Anh",
        "artist": "Sơn Tùng M-TP",
        "album": "Single",
        "length": 260,
    },
    {
        "title": "Birds of a Feather",
        "artist": "Billie Eilish",
        "album": "HIT ME HARD AND SOFT",
        "length": 190,
    }
]

GENERIC_TITLES = {
    "audiostream", "playback", "audiocallbackdriver", "pulseaudio",
    "output", "stream", "alsa playback", "bell", "system sound"
}

def clean_media_title(raw_title, app_name):
    """Clean and extract artist/title from raw stream names or web audio titles."""
    if not raw_title:
        return f"{app_name} Audio", app_name

    import unicodedata
    raw_title = unicodedata.normalize('NFC', raw_title)
    raw_title = re.sub(r'^\s*[\(\[]cut[\)\]]\s*', '', raw_title, flags=re.I)

    title = raw_title.strip()
    if title.lower() in GENERIC_TITLES:
        return f"{app_name} Audio", app_name

    # Remove file extension if playing local files e.g. .mp3, .flac, .wav
    title = re.sub(r'\.(mp3|flac|wav|m4a|ogg|opus|aac|webm)$', '', title, flags=re.IGNORECASE).strip()

    # Split SoundCloud-style: "Song Title by Artist"
    if " by " in title:
        parts = title.rsplit(" by ", 1)
        t = parts[0].strip()
        a = parts[1].strip()
        # Clean common tags
        for tag in ["FREE DOWNLOAD", "[FREE DOWNLOAD]", "(FREE DOWNLOAD)", "Free Download", "Official Audio", "(Official Video)"]:
            t = t.replace(tag, "").strip()
        t = re.sub(r'[\(\[\{]\s*[\)\]\}]', '', t).strip()
        return t or title, f"{a} • {app_name}"

    # Split "Artist - Title" or "Title - Artist"
    if " - " in title:
        parts = title.split(" - ", 1)
        return parts[0].strip(), f"{parts[1].strip()} • {app_name}"

    return title, app_name


class MediaManager:
    def __init__(self, on_track_change=None):
        self.on_track_change = on_track_change
        self.player_name = "System Audio"
        self.app_binary = ""
        self.title = "No Media Playing"
        self.artist = "Play any music or audio"
        self.album = ""
        self.art_url = None
        self.status = "Stopped" # "Playing", "Paused", "Stopped"
        self.position = 0
        self.duration = 0
        self.is_demo = False
        self.is_stream_audio = False
        self.stream_id = None

        # Demo state
        self._demo_index = 0
        self._demo_playing = False
        self._demo_last_tick = time.time()

        self._bus = None
        try:
            self._bus = dbus.SessionBus()
        except Exception as e:
            print(f"[Media] DBus session bus error: {e}")

        self._lock = threading.Lock()
        self._running = True

        # Start background polling thread for real-time audio detection
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def is_playing(self):
        with self._lock:
            return self.status == "Playing"

    def refresh(self):
        """Called by UI tick to sync any state changes."""
        # Non-blocking: background thread keeps data updated
        pass

    def get_app_icon(self, size=18):
        """Fetch themed application icon for the currently playing source."""
        theme = Gtk.IconTheme.get_default()
        candidates = []
        if self.app_binary:
            candidates.append(self.app_binary.lower())
        if self.player_name:
            candidates.append(self.player_name.lower())
            candidates.append(self.player_name.lower().replace(" ", "-"))

        for c in candidates:
            if c and theme.has_icon(c):
                try:
                    return theme.load_icon(c, size, 0)
                except Exception:
                    pass
        return None

    def _monitor_loop(self):
        """Background thread that queries PipeWire streams and MPRIS every 1s."""
        while self._running:
            try:
                self._poll_status()
            except Exception as e:
                pass
            time.sleep(1.0)

    def _poll_status(self):
        active_stream = self._get_active_pipewire_stream()
        mpris_playing, mpris_paused = self._query_mpris_players()

        old_title = self.title
        old_status = self.status

        with self._lock:
            # CASE 1: Active MPRIS player is explicitly "Playing" (e.g. Spotify, YouTube with MPRIS)
            if mpris_playing:
                self._apply_mpris(mpris_playing)

            # CASE 2: Any active PipeWire stream is actively outputting sound (SoundCloud, browser, videos, games)
            elif active_stream:
                self.is_demo = False
                self.is_stream_audio = True
                self.status = "Playing"
                self.player_name = active_stream['app']
                self.app_binary = active_stream.get('binary', '')
                self.stream_id = active_stream.get('id')

                # Check if matching MPRIS has richer metadata
                matching_mpris = None
                if mpris_paused:
                    app_lower = active_stream['app'].lower()
                    for p in mpris_paused:
                        if app_lower in p.get('bus_name', '').lower() or app_lower in p.get('name', '').lower():
                            matching_mpris = p
                            break

                raw_title = active_stream['title']
                t, a = clean_media_title(raw_title, active_stream['app'])

                # If stream title was generic, but matching MPRIS has a track title
                if (not raw_title or raw_title.lower() in GENERIC_TITLES) and matching_mpris and matching_mpris.get('title'):
                    self.title = matching_mpris['title']
                    self.artist = matching_mpris.get('artist') or active_stream['app']
                    self.album = matching_mpris.get('album', '')
                    self.art_url = matching_mpris.get('art_url')
                    self.duration = matching_mpris.get('duration', 0)
                    self.position = matching_mpris.get('position', 0)
                else:
                    if self.title != t:
                        self.title = t
                        self.artist = a
                        self.art_url = None
                    else:
                        self.artist = a
                    self.album = ""
                    self.duration = 0
                    self.position += 1 # Live playback ticker

                # Automatically fetch online album artwork if missing
                if not self.art_url and self.title and self.title != "No Media Playing":
                    fetch_online_artwork_async(self.title, self.artist, self._on_online_art_found)

            # CASE 3: No active audio stream, but an MPRIS player was paused recently
            elif mpris_paused:
                self._apply_mpris(mpris_paused[0])
                self.status = "Paused"

            # CASE 4: Nothing playing anywhere
            else:
                if self.is_demo and self._demo_playing:
                    self._update_demo()
                else:
                    self.status = "Stopped"
                    self.title = "No Media Playing"
                    self.artist = "Play any music or audio"
                    self.album = ""
                    self.art_url = None
                    self.position = 0
                    self.duration = 0
                    self.is_stream_audio = False

        if (self.title != old_title or self.status != old_status) and self.status == "Playing" and self.on_track_change:
            GLib.idle_add(self.on_track_change, self.title, self.artist)

    def _apply_mpris(self, p):
        self.is_demo = False
        self.is_stream_audio = False
        self.status = p.get('status', 'Playing')
        self.player_name = p.get('name', 'Media Player')
        self.app_binary = p.get('binary', p.get('name', '').lower())
        self.title = p.get('title') or "Unknown Title"
        self.artist = p.get('artist') or "Unknown Artist"
        self.album = p.get('album', '')
        self.art_url = p.get('art_url')
        self.duration = p.get('duration', 0)
        self.position = p.get('position', 0)
        self._mpris_bus_name = p.get('bus_name')

    def _on_online_art_found(self, art_url):
        if not art_url:
            return
        with self._lock:
            if self.status == "Playing" and not self.art_url:
                self.art_url = art_url
        # Pre-cache pixbufs so they are ready
        load_artwork_pixbuf(art_url, size=48, radius=10, on_ready_callback=None)
        load_artwork_pixbuf(art_url, size=18, radius=5, on_ready_callback=None)
        if self.on_track_change:
            GLib.idle_add(self.on_track_change, self.title, self.artist)

    def _get_active_pipewire_stream(self):
        """Query PipeWire nodes for any running audio output stream."""
        # Method 1: pw-dump Node (fastest & most detailed)
        try:
            out = subprocess.check_output(['pw-dump', 'Node'], text=True, timeout=0.8)
            data = json.loads(out)
            for obj in data:
                info = obj.get('info', {})
                props = info.get('props', {})
                if props.get('media.class') == 'Stream/Output/Audio':
                    state = info.get('state', '')
                    corked = props.get('pulse.corked', False)
                    if state == 'running' and not corked:
                        app = props.get('application.name') or props.get('node.name') or 'Audio'
                        if 'speech-dispatcher' in app.lower():
                            continue
                        title = props.get('media.name') or ''
                        binary = props.get('application.process.binary') or ''
                        return {
                            'id': obj.get('id'),
                            'app': app,
                            'title': title,
                            'binary': binary
                        }
        except Exception:
            pass

        # Method 2: wpctl status fallback
        try:
            out = subprocess.check_output(['wpctl', 'status'], text=True, timeout=0.8)
            streams_idx = out.find('Streams:')
            if streams_idx != -1:
                streams_section = out[streams_idx:]
                lines = streams_section.split('\n')
                current_app = None
                for line in lines:
                    m_app = re.search(r'^\s*(\d+)\.\s+([^\s].+)', line)
                    if m_app:
                        current_app = m_app.group(2).strip()
                    if '[active]' in line and current_app:
                        if 'speech-dispatcher' in current_app.lower():
                            continue
                        return {
                            'id': None,
                            'app': current_app,
                            'title': f'{current_app} Audio',
                            'binary': current_app.lower()
                        }
        except Exception:
            pass

        return None

    def _query_mpris_players(self):
        """Query MPRIS players on DBus. Returns (first_playing_player, list_of_paused_players)."""
        if not self._bus:
            return None, []

        playing = []
        paused = []
        try:
            names = [s for s in self._bus.list_names() if s.startswith("org.mpris.MediaPlayer2.")]
            for n in names:
                try:
                    obj = self._bus.get_object(n, "/org/mpris/MediaPlayer2")
                    props = dbus.Interface(obj, "org.freedesktop.DBus.Properties")
                    status = str(props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus", timeout=0.2))
                    metadata = props.Get("org.mpris.MediaPlayer2.Player", "Metadata", timeout=0.2)

                    raw_name = n.replace("org.mpris.MediaPlayer2.", "")
                    app_name = raw_name.split(".")[0].capitalize()

                    title = str(metadata.get("xesam:title", ""))
                    artists = metadata.get("xesam:artist", [])
                    if isinstance(artists, (list, tuple, dbus.Array)):
                        artist = ", ".join([str(a) for a in artists])
                    else:
                        artist = str(artists)

                    length_us = metadata.get("mpris:length", 0)
                    dur = int(length_us / 1_000_000) if length_us else 0

                    pos = 0
                    try:
                        pos_us = props.Get("org.mpris.MediaPlayer2.Player", "Position", timeout=0.2)
                        pos = int(pos_us / 1_000_000)
                    except Exception:
                        pass

                    info = {
                        "bus_name": str(n),
                        "name": app_name,
                        "binary": raw_name.split(".")[0].lower(),
                        "status": status,
                        "title": title,
                        "artist": artist,
                        "album": str(metadata.get("xesam:album", "")),
                        "art_url": str(metadata.get("mpris:artUrl", "")),
                        "duration": dur,
                        "position": pos
                    }

                    if status == "Playing":
                        playing.append(info)
                    elif status == "Paused":
                        paused.append(info)
                except Exception:
                    pass
        except Exception:
            pass

        first_playing = playing[0] if playing else None
        return first_playing, paused

    def _update_demo(self):
        self.is_demo = True
        track = DEMO_PLAYLIST[self._demo_index]
        self.title = track["title"]
        self.artist = track["artist"]
        self.album = track["album"]
        self.duration = track["length"]
        self.art_url = track.get("art_url", "")
        self.status = "Playing" if self._demo_playing else "Paused"

        now = time.time()
        dt = now - self._demo_last_tick
        self._demo_last_tick = now

        if self._demo_playing:
            self.position += int(dt)
            if self.position >= self.duration:
                self.next_track()

    def play_pause(self):
        if self.is_demo:
            self._demo_playing = not self._demo_playing
            self.status = "Playing" if self._demo_playing else "Paused"
            return

        # 1. Try MPRIS if active player has an MPRIS bus name
        bus_name = getattr(self, '_mpris_bus_name', None)
        if not bus_name and self._bus:
            # Search for any MPRIS player matching current player name
            names = [s for s in self._bus.list_names() if s.startswith("org.mpris.MediaPlayer2.")]
            for n in names:
                if self.player_name.lower() in n.lower() or self.app_binary in n.lower():
                    bus_name = n
                    break

        if self._bus and bus_name:
            try:
                obj = self._bus.get_object(bus_name, "/org/mpris/MediaPlayer2")
                player = dbus.Interface(obj, "org.mpris.MediaPlayer2.Player")
                player.PlayPause()
                time.sleep(0.05)
                self._poll_status()
                return
            except Exception as e:
                pass

        # 2. Toggle mute on default audio sink if it's a generic stream without MPRIS
        try:
            subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"], check=False)
        except Exception:
            pass

    def next_track(self):
        if self.is_demo:
            self._demo_index = (self._demo_index + 1) % len(DEMO_PLAYLIST)
            self.position = 0
            self._update_demo()
            if self.on_track_change:
                self.on_track_change(self.title, self.artist)
            return

        bus_name = getattr(self, '_mpris_bus_name', None)
        if self._bus and bus_name:
            try:
                obj = self._bus.get_object(bus_name, "/org/mpris/MediaPlayer2")
                player = dbus.Interface(obj, "org.mpris.MediaPlayer2.Player")
                player.Next()
                time.sleep(0.05)
                self._poll_status()
            except Exception:
                pass

    def prev_track(self):
        if self.is_demo:
            self._demo_index = (self._demo_index - 1) % len(DEMO_PLAYLIST)
            self.position = 0
            self._update_demo()
            if self.on_track_change:
                self.on_track_change(self.title, self.artist)
            return

        bus_name = getattr(self, '_mpris_bus_name', None)
        if self._bus and bus_name:
            try:
                obj = self._bus.get_object(bus_name, "/org/mpris/MediaPlayer2")
                player = dbus.Interface(obj, "org.mpris.MediaPlayer2.Player")
                player.Previous()
                time.sleep(0.05)
                self._poll_status()
            except Exception:
                pass

    def stop(self):
        self._running = False
