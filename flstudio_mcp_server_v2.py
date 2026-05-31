"""
FL STUDIO AI - Claude Code / OpenCode MCP Integration
======================================================
Proper MCP (Model Context Protocol) server for AI beat making

This server exposes FL Studio capabilities as MCP tools that Claude Code
and OpenCode can call to create beats, melodies, and full tracks.

Usage:
1. Start the server: python flstudio_mcp_server.py
2. Configure Claude Code to use MCP at localhost:5000
3. Ask Claude to make beats!

Version: MCP 1.0 Compatible
"""

import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("ERROR: Flask not installed. Run: pip install flask")
    sys.exit(1)

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("WARNING: pyautogui not installed - keyboard control disabled")

app = Flask(__name__)


# ==================== MUSIC THEORY ENGINE ====================

class MusicEngine:
    """Core music generation engine"""

    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic": [0, 2, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }

    CHORD_PROGRESSIONS = {
        "pop": ["I", "V", "vi", "IV"],
        "jazz": ["IIm7", "V7", "Imaj7"],
        "sad": ["i", "VI", "III", "VII"],
        "trap": ["im", "IVm", "VII", "III"],
    }

    DRUM_PATTERNS = {
        "trap": [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        "house": [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
        "hiphop": [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    }

    @staticmethod
    def midi_note(midi: int) -> str:
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        return f"{notes[midi % 12]}{(midi // 12) - 1}"

    @staticmethod
    def generate_scale_notes(root: int, scale: str, octaves: int = 2) -> list:
        intervals = MusicEngine.SCALES.get(scale, [0, 2, 4, 5, 7, 9, 11])
        notes = []
        for octave in range(octaves):
            for interval in intervals:
                note = root + interval + (octave * 12)
                if 0 <= note <= 127:
                    notes.append(note)
        return notes

    @staticmethod
    def generate_drums(style: str = "trap", bars: int = 1) -> dict:
        pattern = MusicEngine.DRUM_PATTERNS.get(style, [1, 0, 0, 1, 0, 0, 1, 0] * 2)
        pattern = pattern * bars

        kick_notes = [36 if pattern[i] else None for i in range(0, 16 * bars, 2)]
        snare_notes = [38 if pattern[i] else None for i in range(2, 16 * bars, 4)]
        hihat_notes = [42 if pattern[i] else None for i in range(16 * bars)]

        notes = []
        for i, (kick, snare, hihat) in enumerate(zip(kick_notes, snare_notes, hihat_notes)):
            if kick:
                notes.append({"midi": kick, "velocity": 120, "timing": i * 0.5, "duration": 0.1, "track": "kick"})
            if snare:
                notes.append({"midi": snare, "velocity": 100, "timing": i * 0.5, "duration": 0.1, "track": "snare"})
            if hihat:
                notes.append({"midi": hihat, "velocity": 80, "timing": i * 0.25, "duration": 0.05, "track": "hihat"})

        return {"style": style, "bars": bars, "notes": notes, "pattern": pattern}

    @staticmethod
    def generate_bass(root: int = 36, scale: str = "minor", length: int = 16) -> dict:
        scale_notes = MusicEngine.generate_scale_notes(root, scale, 1)

        pattern = []
        bass_root = scale_notes[0]
        notes = []

        for i in range(length):
            note_idx = min(i % len(scale_notes), len(scale_notes) - 1)
            note = scale_notes[note_idx]

            if i % 4 == 0:
                note = bass_root
            elif i % 2 == 0:
                note = scale_notes[min(2, len(scale_notes) - 1)]

            notes.append({
                "midi": note,
                "velocity": 100 + random.randint(-10, 10),
                "timing": i * 0.5,
                "duration": 0.5,
                "track": "bass"
            })

        return {"root": root, "scale": scale, "notes": notes}

    @staticmethod
    def generate_melody(key: int = 60, scale: str = "minor", length: int = 16) -> dict:
        scale_notes = MusicEngine.generate_scale_notes(key, scale, 2)

        notes = []
        last_note = key

        for i in range(length):
            if random.random() > 0.3:
                direction = random.choice([-2, -1, 0, 1, 2])
                new_idx = scale_notes.index(last_note) + direction
                new_idx = max(0, min(len(scale_notes) - 1, new_idx))
                last_note = scale_notes[new_idx]

                notes.append({
                    "midi": last_note,
                    "velocity": 80 + random.randint(0, 30),
                    "timing": i * 0.5,
                    "duration": random.choice([0.5, 1]),
                    "track": "melody"
                })

        return {"key": key, "scale": scale, "notes": notes}

    @staticmethod
    def generate_chords(key: int = 60, style: str = "pop", bars: int = 8) -> dict:
        chords = MusicEngine.CHORD_PROGRESSIONS.get(style, ["I", "V", "vi", "IV"])
        chord_intervals = {"I": [0, 4, 7], "i": [0, 3, 7], "V": [0, 4, 7], "vi": [0, 3, 7], "IV": [0, 4, 7]}

        root_offset = {"I": 0, "i": 0, "V": 7, "vi": 9, "IV": 5}

        notes = []
        chord_seq = chords * (bars // 4 + 1)
        for i in range(bars):
            chord = chord_seq[i]
            root = key + root_offset.get(chord, 0)
            for interval in chord_intervals.get(chord, [0, 4, 7]):
                notes.append({
                    "midi": root + interval,
                    "velocity": 70,
                    "timing": i * 4,
                    "duration": 4,
                    "track": "chords"
                })

        return {"key": key, "style": style, "notes": notes}


# ==================== FL STUDIO CONTROLLER ====================

class FLStudioController:
    """Control FL Studio via keyboard shortcuts"""

    def __init__(self):
        self.last_track = None
        self.fl_running = False

    def _keypress(self, *keys):
        """Send keyboard shortcut"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press(keys)
                return True
            except:
                pass
        return False

    def _combo(self, *keys):
        """Send keyboard combo"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey(*keys)
                return True
            except:
                pass
        return False

    def play(self):
        self._keypress("space")
        return {"status": "played", "message": "Playback started"}

    def stop(self):
        self._keypress("space")
        return {"status": "stopped", "message": "Playback stopped"}

    def record(self):
        self._combo("r")
        return {"status": "recording", "message": "Recording enabled"}

    def new_pattern(self):
        self._combo("ctrl", "n")
        return {"status": "new_pattern", "message": "New pattern created"}

    def open_piano_roll(self):
        self._combo("f6")
        return {"status": "piano_roll", "message": "Piano roll opened"}

    def save_project(self):
        self._combo("ctrl", "s")
        return {"status": "saved", "message": "Project saved"}


# ==================== MCP TOOLS ====================

music_engine = MusicEngine()
fl_controller = FLStudioController()


# MCP Tool Definitions - Claude Code compatible
MCP_TOOLS = [
    {
        "name": "generate_track",
        "description": "Generate a complete music track with drums, bass, melody, and chords",
        "inputSchema": {
            "type": "object",
            "properties": {
                "style": {"type": "string", "enum": ["trap", "house", "hiphop", "dnb", "dubstep", "lofi", "techno", "ambient"], "default": "house"},
                "tempo": {"type": "integer", "minimum": 60, "maximum": 200, "default": 120},
                "key": {"type": "integer", "minimum": 24, "maximum": 84, "default": 60},
                "scale": {"type": "string", "enum": ["major", "minor", "dorian", "pentatonic"], "default": "minor"},
                "bars": {"type": "integer", "minimum": 4, "maximum": 64, "default": 16},
            },
        },
    },
    {
        "name": "generate_drums",
        "description": "Generate drum pattern (kick, snare, hihat)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "style": {"type": "string", "enum": ["trap", "house", "hiphop"], "default": "trap"},
                "bars": {"type": "integer", "minimum": 1, "maximum": 8, "default": 1},
            },
        },
    },
    {
        "name": "generate_bass",
        "description": "Generate bass line",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "integer", "minimum": 24, "maximum": 60, "default": 36},
                "scale": {"type": "string", "default": "minor"},
                "length": {"type": "integer", "minimum": 4, "maximum": 32, "default": 16},
            },
        },
    },
    {
        "name": "generate_melody",
        "description": "Generate melodic phrase",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "integer", "minimum": 36, "maximum": 84, "default": 60},
                "scale": {"type": "string", "default": "minor"},
                "length": {"type": "integer", "minimum": 4, "maximum": 32, "default": 16},
            },
        },
    },
    {
        "name": "generate_chords",
        "description": "Generate chord progression",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "integer", "minimum": 36, "maximum": 72, "default": 60},
                "style": {"type": "string", "enum": ["pop", "jazz", "sad", "trap"], "default": "pop"},
                "bars": {"type": "integer", "minimum": 4, "maximum": 16, "default": 8},
            },
        },
    },
    {
        "name": "flstudio_play",
        "description": "Start FL Studio playback",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "flstudio_stop",
        "description": "Stop FL Studio playback",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "flstudio_record",
        "description": "Toggle recording mode",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "flstudio_new_pattern",
        "description": "Create new pattern in FL Studio",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "flstudio_piano_roll",
        "description": "Open piano roll window",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_note_data",
        "description": "Get generated note data for manual input into FL Studio",
        "inputSchema": {
            "type": "object",
            "properties": {
                "track": {"type": "string", "enum": ["drums", "bass", "melody", "chords", "all"]},
            },
        },
    },
    {
        "name": "get_midi_notes",
        "description": "Get MIDI note numbers and timings for FL Studio piano roll",
        "inputSchema": {
            "type": "object",
            "properties": {
                "track_type": {"type": "string", "enum": ["drums", "bass", "melody", "chords"]},
            },
        },
    },
]


# ==================== MCP ENDPOINTS ====================

@app.route("/mcp/tools", methods=["GET"])
def mcp_tools():
    """List available MCP tools"""
    return jsonify({
        "tools": MCP_TOOLS,
        "server": "FL Studio AI MCP Server",
        "version": "1.0",
    })


@app.route("/mcp/call", methods=["POST"])
def mcp_call():
    """Call MCP tool"""
    data = request.get_json() or {}
    tool = data.get("tool")
    args = data.get("arguments", {})

    if tool == "generate_track":
        style = args.get("style", "house")
        tempo = args.get("tempo", 120)
        key = args.get("key", 60)
        scale = args.get("scale", "minor")
        bars = args.get("bars", 16)

        drums = MusicEngine.generate_drums(style, bars // 4)
        bass = MusicEngine.generate_bass(key - 24, scale, bars)
        melody = MusicEngine.generate_melody(key, scale, bars)
        chords = MusicEngine.generate_chords(key, args.get("chord_style", "pop"), bars)

        return jsonify({
            "status": "success",
            "track": {
                "style": style,
                "tempo": tempo,
                "key": key,
                "scale": scale,
                "bars": bars,
                "drums": drums,
                "bass": bass,
                "melody": melody,
                "chords": chords,
            },
            "message": f"Generated {style} track in {key} {scale}, {bars} bars at {tempo} BPM"
        })

    elif tool == "generate_drums":
        style = args.get("style", "trap")
        bars = args.get("bars", 1)
        result = MusicEngine.generate_drums(style, bars)
        return jsonify({
            "status": "success",
            "drums": result,
            "message": f"Generated {style} drum pattern ({bars} bars)"
        })

    elif tool == "generate_bass":
        root = args.get("root", 36)
        scale = args.get("scale", "minor")
        length = args.get("length", 16)
        result = MusicEngine.generate_bass(root, scale, length)
        return jsonify({
            "status": "success",
            "bass": result,
            "message": f"Generated bass line in {scale}"
        })

    elif tool == "generate_melody":
        key = args.get("key", 60)
        scale = args.get("scale", "minor")
        length = args.get("length", 16)
        result = MusicEngine.generate_melody(key, scale, length)
        return jsonify({
            "status": "success",
            "melody": result,
            "message": f"Generated melody in {key} {scale}"
        })

    elif tool == "generate_chords":
        key = args.get("key", 60)
        style = args.get("style", "pop")
        bars = args.get("bars", 8)
        result = MusicEngine.generate_chords(key, style, bars)
        return jsonify({
            "status": "success",
            "chords": result,
            "message": f"Generated {style} chord progression"
        })

    elif tool == "flstudio_play":
        return jsonify(fl_controller.play())

    elif tool == "flstudio_stop":
        return jsonify(fl_controller.stop())

    elif tool == "flstudio_record":
        return jsonify(fl_controller.record())

    elif tool == "flstudio_new_pattern":
        return jsonify(fl_controller.new_pattern())

    elif tool == "flstudio_piano_roll":
        return jsonify(fl_controller.open_piano_roll())

    elif tool == "get_note_data":
        track = args.get("track", "all")
        drums = MusicEngine.generate_drums("trap", 1)
        bass = MusicEngine.generate_bass(36, "minor", 8)
        melody = MusicEngine.generate_melody(60, "minor", 8)
        chords = MusicEngine.generate_chords(60, "pop", 8)

        return jsonify({
            "status": "success",
            "data": {
                "drums": drums["notes"],
                "bass": bass["notes"],
                "melody": melody["notes"],
                "chords": chords["notes"],
            },
            "instructions": "Copy notes to FL Studio piano roll manually or use with FL Studio Python API"
        })

    elif tool == "get_midi_notes":
        track_type = args.get("track_type", "melody")
        if track_type == "drums":
            result = MusicEngine.generate_drums("trap", 1)
        elif track_type == "bass":
            result = MusicEngine.generate_bass(36, "minor", 8)
        elif track_type == "chords":
            result = MusicEngine.generate_chords(60, "pop", 8)
        else:
            result = MusicEngine.generate_melody(60, "minor", 8)

        return jsonify({
            "status": "success",
            "notes": result["notes"],
            "format": "MIDI: pitch(0-127), velocity(1-127), timing(beats), duration(beats)"
        })

    return jsonify({"status": "error", "message": f"Unknown tool: {tool}"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "server": "FL Studio AI MCP",
        "version": "1.0",
        "tools_count": len(MCP_TOOLS),
    })


# ==================== MAIN ====================

if __name__ == "__main__":
    print("=" * 60)
    print("FL STUDIO AI - MCP Server for Claude Code/OpenCode")
    print("=" * 60)
    print(f"Server running at http://localhost:5000")
    print(f"MCP Tools available: {len(MCP_TOOLS)}")
    print("")
    print("Usage with Claude Code:")
    print('  Use MCP at http://localhost:5000')
    print('  Example: "Make a trap beat at 150 BPM"')
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)