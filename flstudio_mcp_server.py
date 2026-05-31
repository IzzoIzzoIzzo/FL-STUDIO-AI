"""
FL Studio MCP Server - HTTP API for Claude Code / OpenCode
Full-featured beat making integration with generative AI tools
"""

import json
import random
import threading
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available - install with: pip install flask")

try:
    import pythonosc
    from pythonosc.udp_client import SimpleUDPClient
    OSC_AVAILABLE = True
except ImportError:
    OSC_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


app = Flask(__name__)


class MusicTheory:
    """Music theory utilities for generative music"""

    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "pentatonic": [0, 2, 5, 7, 10],
        "blues": [0, 3, 5, 6, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
    }

    CHORDS = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "diminished": [0, 3, 6],
        "augmented": [0, 4, 8],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7],
        "6": [0, 4, 7, 9],
        "7": [0, 4, 7, 10],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "min7b5": [0, 3, 6, 10],
        "9": [0, 4, 7, 10, 14],
        "maj9": [0, 4, 7, 11, 14],
    }

    DRUM_NOTES = {
        "kick": 36,
        "snare": 38,
        "hihat_closed": 42,
        "hihat_open": 46,
        "crash": 49,
        "ride": 51,
        "tom_high": 48,
        "tom_mid": 45,
        "tom_low": 41,
        "clap": 39,
        "rim": 37,
    }

    @staticmethod
    def midi_to_note(midi: int) -> str:
        octave = (midi // 12) - 1
        note = MusicTheory.NOTES[midi % 12]
        return f"{note}{octave}"

    @staticmethod
    def note_to_midi(note: str) -> int:
        note = note.upper().replace("B#", "C").replace("CB", "B")
        for i, n in enumerate(MusicTheory.NOTES):
            if note.startswith(n):
                octave = int(note[len(n):])
                return (octave + 1) * 12 + i
        return 60

    @staticmethod
    def get_scale_notes(root: int, scale_name: str) -> list[int]:
        intervals = MusicTheory.SCALES.get(scale_name, [0, 2, 4, 5, 7, 9, 11])
        return [root + i for i in intervals]

    @staticmethod
    def get_chord_notes(root: int, chord_type: str) -> list[int]:
        intervals = MusicTheory.CHORDS.get(chord_type, [0, 4, 7])
        return [root + i for i in intervals]


class GenerativeMusicEngine:
    """AI-powered generative music engine"""

    def __init__(self):
        self.history = []
        self.style_weights = {
            "trap": {"kick": 0.4, "snare": 0.2, "hihat": 0.3, "808": 0.1},
            "house": {"kick": 0.35, "snare": 0.2, "hihat": 0.25, "clap": 0.2},
            "techno": {"kick": 0.4, "hihat": 0.3, "perc": 0.2, "snare": 0.1},
            "hiphop": {"kick": 0.3, "snare": 0.25, "hihat": 0.25, "perc": 0.2},
        }

    def generate_drum_pattern(
        self,
        style: str = "basic",
        bars: int = 1,
        complexity: int = 3,
        swing: float = 0.0
    ) -> dict:
        """Generate drum pattern with full rhythm data"""

        base_patterns = {
            "basic": {
                "kick": [1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0],
                "hihat": [1, 0, 1, 0, 1, 0, 1, 0],
            },
            "trap": {
                "kick": [1, 0, 0, 1, 0, 0, 1, 0],
                "snare": [0, 0, 1, 0, 0, 0, 1, 1],
                "hihat": [1, 1, 0, 1, 1, 0, 1, 1],
                "808": [1, 0, 0, 1, 0, 1, 0, 1],
            },
            "house": {
                "kick": [1, 0, 0, 1, 1, 0, 0, 1],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0],
                "hihat": [1, 0, 1, 0, 1, 0, 1, 0],
                "clap": [0, 0, 1, 0, 0, 0, 1, 0],
            },
            "techno": {
                "kick": [1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0],
                "hihat": [1, 1, 1, 1, 1, 1, 1, 1],
                "perc": [0, 1, 0, 1, 0, 1, 0, 1],
            },
            "hiphop": {
                "kick": [1, 0, 0, 1, 0, 0, 1, 0],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0],
                "hihat": [1, 0, 1, 0, 1, 0, 1, 1],
                "perc": [1, 0, 1, 0, 0, 1, 0, 0],
            },
            "lofi": {
                "kick": [1, 0, 0, 0, 1, 0, 0, 0],
                "snare": [0, 0, 1, 0, 0, 0, 0, 0],
                "hihat": [1, 0, 0, 1, 0, 0, 1, 0],
                "vinyl": [0, 1, 0, 0, 0, 1, 0, 0],
            },
            "dubstep": {
                "kick": [1, 0, 0, 1, 0, 0, 0, 1],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0],
                "hihat": [1, 1, 0, 1, 0, 1, 0, 1],
                "sub": [1, 0, 1, 0, 0, 1, 0, 1],
            },
            "jungle": {
                "kick": [1, 0, 1, 0, 1, 0, 1, 0],
                "snare": [0, 0, 1, 0, 0, 1, 0, 0],
                "hihat": [1, 1, 0, 1, 1, 0, 1, 1],
            },
        }

        pattern = base_patterns.get(style, base_patterns["basic"]).copy()

        if complexity > 3:
            complexity_factor = (complexity - 3) * 0.2
            for drum in pattern:
                for i in range(len(pattern[drum])):
                    if random.random() < complexity_factor:
                        pattern[drum][i] = 1 - pattern[drum][i]

        if swing > 0:
            for drum in pattern:
                for i in range(1, len(pattern[drum]), 2):
                    if pattern[drum][i]:
                        pattern[drum][i] = 0
                        if i + 1 < len(pattern[drum]):
                            pattern[drum][i + 1] = 1

        pattern_data = []
        steps_per_bar = 8 * bars
        for step in range(steps_per_bar):
            events = []
            for drum, hits in pattern.items():
                hit_index = step % len(hits)
                if hits[hit_index]:
                    velocity = random.randint(80, 127) if random.random() > 0.1 else random.randint(50, 79)
                    events.append({
                        "drum": drum,
                        "midi": MusicTheory.DRUM_NOTES.get(drum, 36),
                        "velocity": velocity,
                        "timing": step / steps_per_bar
                    })
            if events:
                pattern_data.append({"step": step, "events": events})

        return {
            "style": style,
            "bars": bars,
            "complexity": complexity,
            "swing": swing,
            "pattern": pattern,
            "sequence": pattern_data,
            "midi_events": [
                {"midi": e["midi"], "velocity": e["velocity"], "timing": e["timing"]}
                for step_data in pattern_data
                for e in step_data["events"]
            ]
        }

    def generate_bass_line(
        self,
        root: int = 36,
        scale: str = "minor",
        length: int = 8,
        pattern_type: str = "walking"
    ) -> dict:
        """Generate bass line with multiple pattern types"""

        scale_notes = MusicTheory.get_scale_notes(root, scale)

        patterns = {
            "walking": [0, 2, 0, 3, 0, 2, 0, 1],
            "drone": [0, 0, 0, 0, 0, 0, 0, 0],
            "driving": [0, 0, 2, 0, 0, 0, 3, 0],
            "syncopated": [0, 0, 2, 0, 0, 2, 0, 3],
            "plucks": [0, 0, 2, 0, 3, 0, 2, 0],
            "offbeat": [0, 2, 0, 3, 0, 2, 0, 3],
        }

        base_pattern = patterns.get(pattern_type, patterns["walking"])

        bass_notes = []
        for i in range(length):
            interval_index = base_pattern[i % len(base_pattern)]
            if interval_index < len(scale_notes):
                note = scale_notes[interval_index]
            else:
                note = root

            octave_shift = random.choice([0, 0, 0, 12]) if random.random() < 0.1 else 0
            note += octave_shift

            velocity = random.randint(70, 110)
            duration = random.choice([0.5, 1, 1, 1.5])

            bass_notes.append({
                "index": i,
                "note": note,
                "note_name": MusicTheory.midi_to_note(note),
                "velocity": velocity,
                "duration": duration,
                "timing": i
            })

        return {
            "root": root,
            "root_note": MusicTheory.midi_to_note(root),
            "scale": scale,
            "pattern_type": pattern_type,
            "length": length,
            "notes": bass_notes,
            "midi_events": [
                {"midi": n["note"], "velocity": n["velocity"], "duration": n["duration"], "timing": n["timing"]}
                for n in bass_notes
            ]
        }

    def generate_melody(
        self,
        key: int = 60,
        scale: str = "minor",
        length: int = 8,
        note_range: tuple = (4, 6),
        rhythm_density: float = 0.7
    ) -> dict:
        """Generate melodic phrase"""

        scale_notes = []
        for octave in range(note_range[0], note_range[1] + 1):
            for interval in MusicTheory.SCALES.get(scale, [0, 2, 4, 5, 7, 9, 11]):
                note = key + interval + (octave - 4) * 12
                if 24 <= note <= 108:
                    scale_notes.append(note)

        scale_notes = sorted(set(scale_notes))

        melody = []
        current_idx = random.randint(0, len(scale_notes) - 1)

        for i in range(length):
            if random.random() < rhythm_density:
                direction = random.choice([-1, 1, 1, 1, 0, 0])

                if direction == 0:
                    current_idx = random.randint(0, len(scale_notes) - 1)
                else:
                    current_idx = max(0, min(len(scale_notes) - 1, current_idx + direction))

                note = scale_notes[current_idx]

                if random.random() < 0.15:
                    current_idx = max(0, min(len(scale_notes) - 1, current_idx + random.choice([-2, 2])))

                duration = random.choice([0.25, 0.5, 0.5, 1, 1, 1.5, 2])
                velocity = random.randint(60, 120)

                melody.append({
                    "index": i,
                    "note": note,
                    "note_name": MusicTheory.midi_to_note(note),
                    "duration": duration,
                    "velocity": velocity,
                    "timing": sum(m.get("duration", 1) for m in melody)
                })

        return {
            "key": key,
            "key_note": MusicTheory.midi_to_note(key),
            "scale": scale,
            "length": length,
            "notes": melody,
            "midi_events": [
                {"midi": m["note"], "velocity": m["velocity"], "duration": m["duration"], "timing": m["timing"]}
                for m in melody
            ]
        }

    def generate_chord_progression(
        self,
        key: int = 60,
        style: str = "pop",
        bars: int = 4,
        voicing: str = "spread"
    ) -> dict:
        """Generate chord progression with multiple styles"""

        progressions = {
            "pop": ["I", "V", "vi", "IV", "I", "V", "vi", "IV"],
            "pop_alt": ["I", "IV", "V", "IV", "I", "IV", "V", "I"],
            "jazz": ["IIm7", "V7", "Imaj7", "IVm7", "IIm7", "V7", "Imaj7", "VI7"],
            "jazz_ii_v": ["IIm7", "V7", "Imaj7", "IIm7", "V7", "Imaj7", "IVm7", "V7"],
            "cinematic": ["Im", "VII", "III", "VI", "IV", "I", "V", "I"],
            "edm": ["I", "IV", "V", "I", "i", "VI", "IV", "V"],
            "soul": ["I", "vi", "IV", "V", "I", "vi", "IV", "V"],
            "rock": ["I", "IV", "I", "V", "I", "IV", "V", "I"],
            "blues": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "V7"],
            "reggae": ["I", "IV", "I", "V", "I", "IV", "V", "I"],
        }

        roman_numerals = progressions.get(style, progressions["pop"])

        chord_types = {
            "I": "major",
            "i": "minor",
            "II": "major",
            "IIm7": "minor",
            "III": "major",
            "III7": "major",
            "IV": "major",
            "IVm7": "minor",
            "V": "major",
            "V7": "major",
            "VI": "major",
            "VI7": "major",
            "VII": "major",
            "vi": "minor",
        }

        voicings = {
            "root": lambda n, c: [n, n + 12],
            "spread": lambda n, c: [n, n + 4, n + 7],
            "block": lambda n, c: [n, n + 4, n + 7, n + 12],
            "jazz": lambda n, c: [n - 12, n, n + 3, n + 7],
            "inversions": lambda n, c: [n, n + 12, n + 19] if c else [n, n + 12, n + 24],
        }

        voicing_func = voicings.get(voicing, voicings["spread"])

        chords = []
        for i in range(bars):
            roman = roman_numerals[i % len(roman_numerals)]
            root_offset = {
                "I": 0, "i": 0, "II": 2, "IIm7": 2, "III": 4, "III7": 4,
                "IV": 5, "IVm7": 5, "V": 7, "V7": 7, "VI": 9, "VI7": 9, "VII": 11,
                "vi": 9
            }.get(roman, 0)

            root = key + root_offset
            chord_type = chord_types.get(roman, "major")
            chord_notes = MusicTheory.get_chord_notes(root, chord_type)
            voiced_notes = voicing_func(root, "7" in roman)

            chords.append({
                "index": i,
                "roman": roman,
                "root": root,
                "root_note": MusicTheory.midi_to_note(root),
                "type": chord_type,
                "notes": chord_notes,
                "voiced": voiced_notes,
                "duration": 4
            })

        return {
            "key": key,
            "key_note": MusicTheory.midi_to_note(key),
            "style": style,
            "bars": bars,
            "voicing": voicing,
            "chords": chords,
            "midi_events": [
                {"midi": n, "velocity": 80, "duration": 4, "timing": c["index"] * 4}
                for c in chords for n in c["voiced"]
            ]
        }

    def generate_full_track(
        self,
        style: str = "house",
        key: int = 60,
        scale: str = "minor",
        bars: int = 8,
        tempo: int = 120
    ) -> dict:
        """Generate complete track with all elements"""

        drums = self.generate_drum_pattern(style=style, bars=bars // 4, complexity=3)
        bass = self.generate_bass_line(
            root=key - 24,
            scale=scale,
            length=bars,
            pattern_type=random.choice(["walking", "driving", "syncopated"])
        )
        melody = self.generate_melody(key=key, scale=scale, length=bars * 2, note_range=(4, 6))
        chords = self.generate_chord_progression(key=key, style=style.replace("lofi", "pop"), bars=bars)

        return {
            "metadata": {
                "style": style,
                "key": key,
                "key_note": MusicTheory.midi_to_note(key),
                "scale": scale,
                "tempo": tempo,
                "bars": bars,
                "generated_at": datetime.now().isoformat()
            },
            "drums": drums,
            "bass": bass,
            "melody": melody,
            "chords": chords,
            "arrangement": {
                "intro": [0, 4],
                "verse": [4, 8],
                "chorus": [8, 16],
                "outro": [16, bars]
            }
        }


class FLStudioController:
    """Main FL Studio controller with full functionality"""

    def __init__(self, osc_port: int = 5005):
        self.osc_port = osc_port
        self.connected = False
        self.project_path = ""
        self.current_pattern = 1
        self.tempo = 120

        if OSC_AVAILABLE:
            try:
                self.osc_client = SimpleUDPClient("127.0.0.1", self.osc_port)
                self.connected = True
            except:
                pass

        self.generative = GenerativeMusicEngine()
        self.history = []
        self.playlist = []

    def _send_osc(self, address: str, *args) -> bool:
        if self.connected:
            try:
                self.osc_client.send_message(address, list(args))
                return True
            except:
                pass
        return False

    def _key(self, *keys) -> bool:
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press(keys)
                return True
            except:
                pass
        return False

    def _combo(self, *keys) -> bool:
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey(*keys)
                return True
            except:
                pass
        return False

    def play(self) -> dict:
        self._send_osc("/play") or self._key("space")
        return self._response("Playing")

    def stop(self) -> dict:
        self._send_osc("/stop") or self._key("space")
        return self._response("Stopped")

    def pause(self) -> dict:
        self._send_osc("/pause")
        return self._response("Paused")

    def record(self) -> dict:
        self._send_osc("/record") or self._combo("r")
        return self._response("Recording enabled")

    def restart(self) -> dict:
        self._send_osc("/restart") or self._key("home")
        return self._response("Restarted to beginning")

    def set_position(self, bar: int = 1) -> dict:
        self._send_osc("/position", bar)
        return self._response(f"Position set to bar {bar}")

    def set_tempo(self, bpm: int) -> dict:
        bpm = max(30, min(300, bpm))
        self.tempo = bpm
        self._send_osc("/tempo", bpm)
        return self._response(f"Tempo set to {bpm} BPM")

    def volume(self, channel: int, level: float) -> dict:
        level = max(0, min(1, level))
        self._send_osc(f"/mixer/{channel}/volume", int(level * 128))
        return self._response(f"Channel {channel} volume: {level:.0%}")

    def pan(self, channel: int, position: float) -> dict:
        position = max(-1, min(1, position))
        self._send_osc(f"/mixer/{channel}/pan", int((position + 1) * 64))
        return self._response(f"Channel {channel} pan: {position:.0%}")

    def mute(self, channel: int, state: bool) -> dict:
        self._send_osc(f"/mixer/{channel}/mute", 1 if state else 0)
        return self._response(f"Channel {channel} {'muted' if state else 'unmuted'}")

    def solo(self, channel: int, state: bool) -> dict:
        self._send_osc(f"/mixer/{channel}/solo", 1 if state else 0)
        return self._response(f"Channel {channel} solo: {state}")

    def master_volume(self, level: float) -> dict:
        level = max(0, min(1, level))
        self._send_osc("/master/volume", int(level * 128))
        return self._response(f"Master volume: {level:.0%}")

    def select_pattern(self, num: int) -> dict:
        self.current_pattern = max(1, min(99, num))
        self._send_osc("/pattern", num)
        return self._response(f"Selected pattern {num}")

    def create_pattern(self, name: str = None) -> dict:
        self._combo("ctrl", "n")
        return self._response(f"Created new pattern: {name or 'Untitled'}")

    def open_piano_roll(self, channel: int = 0) -> dict:
        self._send_osc("/pianoroll", channel) or self._combo("f6")
        return self._response(f"Opened piano roll for channel {channel}")

    def close_piano_roll(self) -> dict:
        self._key("escape")
        return self._response("Closed piano roll")

    def add_note(self, pitch: int, start: float, duration: float, velocity: int = 100) -> dict:
        self._send_osc("/note", pitch, start, duration, velocity)
        return self._response(f"Added note {MusicTheory.midi_to_note(pitch)} at beat {start}")

    def clear_piano_roll(self) -> dict:
        self._combo("ctrl", "a", "backspace")
        return self._response("Cleared piano roll")

    def save_project(self, path: str) -> dict:
        self.project_path = path
        self._send_osc("/save", path) or self._combo("ctrl", "s")
        return self._response(f"Saved project: {path}")

    def new_project(self) -> dict:
        self._combo("ctrl", "shift", "n")
        return self._response("Created new project")

    def _response(self, message: str, **extra) -> dict:
        return {"status": "success", "message": message, "timestamp": datetime.now().isoformat(), **extra}


controller = FLStudioController()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "osc_connected": controller.connected})


@app.route("/tools", methods=["GET"])
def list_tools():
    return jsonify({"tools": TOOLS})


@app.route("/call/<tool_name>", methods=["POST"])
def call_tool(tool_name):
    try:
        args = request.get_json() or {}
    except:
        args = {}

    result = handle_tool(tool_name, args)
    return jsonify(result)


@app.route("/generate/drums", methods=["POST"])
def generate_drums():
    data = request.get_json() or {}
    result = controller.generative.generate_drum_pattern(
        style=data.get("style", "house"),
        bars=data.get("bars", 1),
        complexity=data.get("complexity", 3),
        swing=data.get("swing", 0)
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/bass", methods=["POST"])
def generate_bass():
    data = request.get_json() or {}
    result = controller.generative.generate_bass_line(
        root=data.get("root", 36),
        scale=data.get("scale", "minor"),
        length=data.get("length", 8),
        pattern_type=data.get("pattern", "walking")
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/melody", methods=["POST"])
def generate_melody():
    data = request.get_json() or {}
    result = controller.generative.generate_melody(
        key=data.get("key", 60),
        scale=data.get("scale", "minor"),
        length=data.get("length", 8)
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/chords", methods=["POST"])
def generate_chords():
    data = request.get_json() or {}
    result = controller.generative.generate_chord_progression(
        key=data.get("key", 60),
        style=data.get("style", "pop"),
        bars=data.get("bars", 4)
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/track", methods=["POST"])
def generate_track():
    data = request.get_json() or {}
    result = controller.generative.generate_full_track(
        style=data.get("style", "house"),
        key=data.get("key", 60),
        scale=data.get("scale", "minor"),
        bars=data.get("bars", 8),
        tempo=data.get("tempo", 120)
    )
    return jsonify({"status": "success", **result})


@app.route("/transport/<action>", methods=["POST"])
def transport_control(action):
    actions = {
        "play": controller.play,
        "stop": controller.stop,
        "pause": controller.pause,
        "record": controller.record,
        "restart": controller.restart,
    }
    if action in actions:
        return jsonify(actions[action]())
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/mixer/volume", methods=["POST"])
def mixer_volume():
    data = request.get_json() or {}
    return jsonify(controller.volume(data.get("channel", 0), data.get("level", 0.8)))


@app.route("/mixer/pan", methods=["POST"])
def mixer_pan():
    data = request.get_json() or {}
    return jsonify(controller.pan(data.get("channel", 0), data.get("position", 0)))


@app.route("/mixer/mute", methods=["POST"])
def mixer_mute():
    data = request.get_json() or {}
    return jsonify(controller.mute(data.get("channel", 0), data.get("state", True)))


@app.route("/mixer/solo", methods=["POST"])
def mixer_solo():
    data = request.get_json() or {}
    return jsonify(controller.solo(data.get("channel", 0), data.get("state", True)))


@app.route("/mixer/master", methods=["POST"])
def mixer_master():
    data = request.get_json() or {}
    return jsonify(controller.master_volume(data.get("level", 0.8)))


@app.route("/pattern/<action>", methods=["POST"])
def pattern_control(action):
    data = request.get_json() or {}
    if action == "select":
        return jsonify(controller.select_pattern(data.get("number", 1)))
    elif action == "create":
        return jsonify(controller.create_pattern(data.get("name")))
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/pianoroll/<action>", methods=["POST"])
def pianoroll_control(action):
    data = request.get_json() or {}
    if action == "open":
        return jsonify(controller.open_piano_roll(data.get("channel", 0)))
    elif action == "close":
        return jsonify(controller.close_piano_roll())
    elif action == "clear":
        return jsonify(controller.clear_piano_roll())
    elif action == "note":
        return jsonify(controller.add_note(
            data.get("pitch", 60),
            data.get("start", 0),
            data.get("duration", 1),
            data.get("velocity", 100)
        ))
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/project/<action>", methods=["POST"])
def project_control(action):
    data = request.get_json() or {}
    if action == "new":
        return jsonify(controller.new_project())
    elif action == "save":
        return jsonify(controller.save_project(data.get("path", "project.flp")))
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/tempo", methods=["POST"])
def set_tempo():
    data = request.get_json() or {}
    return jsonify(controller.set_tempo(data.get("bpm", 120)))


@app.route("/position", methods=["POST"])
def set_position():
    data = request.get_json() or {}
    return jsonify(controller.set_position(data.get("bar", 1)))


TOOLS = [
    {"name": "flstudio_play", "description": "Start playback"},
    {"name": "flstudio_stop", "description": "Stop playback"},
    {"name": "flstudio_pause", "description": "Pause playback"},
    {"name": "flstudio_record", "description": "Toggle recording"},
    {"name": "flstudio_restart", "description": "Restart from beginning"},
    {"name": "flstudio_set_tempo", "description": "Set tempo (BPM)", "input": {"bpm": "int"}},
    {"name": "flstudio_set_position", "description": "Jump to bar", "input": {"bar": "int"}},
    {"name": "flstudio_volume", "description": "Set channel volume", "input": {"channel": "int", "level": "float"}},
    {"name": "flstudio_pan", "description": "Set channel pan", "input": {"channel": "int", "position": "float"}},
    {"name": "flstudio_mute", "description": "Toggle mute", "input": {"channel": "int", "state": "bool"}},
    {"name": "flstudio_solo", "description": "Toggle solo", "input": {"channel": "int", "state": "bool"}},
    {"name": "flstudio_master_volume", "description": "Set master volume", "input": {"level": "float"}},
    {"name": "flstudio_select_pattern", "description": "Select pattern", "input": {"number": "int"}},
    {"name": "flstudio_create_pattern", "description": "Create new pattern", "input": {"name": "str"}},
    {"name": "flstudio_open_piano_roll", "description": "Open piano roll", "input": {"channel": "int"}},
    {"name": "flstudio_close_piano_roll", "description": "Close piano roll"},
    {"name": "flstudio_add_note", "description": "Add note", "input": {"pitch": "int", "start": "float", "duration": "float"}},
    {"name": "flstudio_clear_piano_roll", "description": "Clear all notes"},
    {"name": "flstudio_save_project", "description": "Save project", "input": {"path": "str"}},
    {"name": "flstudio_new_project", "description": "Create new project"},
    {"name": "flstudio_generate_drums", "description": "Generate drum pattern", "input": {"style": "str"}},
    {"name": "flstudio_generate_bass", "description": "Generate bass line", "input": {"root": "int", "scale": "str"}},
    {"name": "flstudio_generate_melody", "description": "Generate melody", "input": {"key": "int", "scale": "str"}},
    {"name": "flstudio_generate_chords", "description": "Generate chord progression", "input": {"key": "int", "style": "str"}},
    {"name": "flstudio_generate_track", "description": "Generate full track", "input": {"style": "str", "key": "int"}},
]


def handle_tool(name: str, args: dict = None) -> dict:
    args = args or {}

    handlers = {
        "flstudio_play": lambda: controller.play(),
        "flstudio_stop": lambda: controller.stop(),
        "flstudio_pause": lambda: controller.pause(),
        "flstudio_record": lambda: controller.record(),
        "flstudio_restart": lambda: controller.restart(),
        "flstudio_set_tempo": lambda: controller.set_tempo(args.get("bpm", 120)),
        "flstudio_set_position": lambda: controller.set_position(args.get("bar", 1)),
        "flstudio_volume": lambda: controller.volume(args.get("channel", 0), args.get("level", 0.8)),
        "flstudio_pan": lambda: controller.pan(args.get("channel", 0), args.get("position", 0)),
        "flstudio_mute": lambda: controller.mute(args.get("channel", 0), args.get("state", True)),
        "flstudio_solo": lambda: controller.solo(args.get("channel", 0), args.get("state", True)),
        "flstudio_master_volume": lambda: controller.master_volume(args.get("level", 0.8)),
        "flstudio_select_pattern": lambda: controller.select_pattern(args.get("number", 1)),
        "flstudio_create_pattern": lambda: controller.create_pattern(args.get("name")),
        "flstudio_open_piano_roll": lambda: controller.open_piano_roll(args.get("channel", 0)),
        "flstudio_close_piano_roll": lambda: controller.close_piano_roll(),
        "flstudio_add_note": lambda: controller.add_note(args.get("pitch", 60), args.get("start", 0), args.get("duration", 1)),
        "flstudio_clear_piano_roll": lambda: controller.clear_piano_roll(),
        "flstudio_save_project": lambda: controller.save_project(args.get("path", "project.flp")),
        "flstudio_new_project": lambda: controller.new_project(),
    }

    if name in handlers:
        return handlers[name]()

    if "generate" in name:
        gen = controller.generative
        parts = name.split("_")
        if len(parts) >= 3:
            element = parts[2]
            if element == "drums":
                return gen.generate_drum_pattern(args.get("style", "house"), args.get("bars", 1), args.get("complexity", 3))
            elif element == "bass":
                return gen.generate_bass_line(args.get("root", 36), args.get("scale", "minor"), args.get("length", 8))
            elif element == "melody":
                return gen.generate_melody(args.get("key", 60), args.get("scale", "minor"), args.get("length", 8))
            elif element == "chords":
                return gen.generate_chord_progression(args.get("key", 60), args.get("style", "pop"), args.get("bars", 4))
            elif element == "track":
                return gen.generate_full_track(args.get("style", "house"), args.get("key", 60), args.get("scale", "minor"), args.get("bars", 8))

    return {"status": "error", "message": f"Unknown tool: {name}"}


if __name__ == "__main__":
    print("=" * 50)
    print("FL Studio MCP Server")
    print("=" * 50)
    print(f"OSC Connection: {'Active' if controller.connected else 'Fallback to keyboard'}")
    print(f"Tools available: {len(TOOLS)}")
    print("Server starting on http://localhost:5000")
    print("=" * 50)

    if FLASK_AVAILABLE:
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        print("ERROR: Flask not installed. Run: pip install flask")