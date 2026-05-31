"""
FL Studio MCP Server - AI Beat Making Integration
Provides tools for AI assistants to control FL Studio for music production

Communication: OSC (Open Sound Control) + Keyboard Shortcuts
"""

import asyncio
import json
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any

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


class FLStudioMCP:
    """MCP Server for FL Studio beat-making control"""

    def __init__(self, osc_port: int = 5005, fl_port: int = 5006):
        self.osc_port = osc_port
        self.fl_port = fl_port
        self.connected = False

        if OSC_AVAILABLE:
            try:
                self.osc_client = SimpleUDPClient("127.0.0.1", self.fl_port)
                self.connected = True
                print(f"FL Studio MCP: Connected to FL Studio on port {fl_port}")
            except Exception as e:
                print(f"FL Studio MCP: OSC connection failed - {e}")
                self.connected = False
        else:
            print("FL Studio MCP: OSC not available, using keyboard shortcuts")

        self.current_project = "Untitled"
        self.pattern_count = 0
        self.channels = []

    def _send_osc(self, address: str, *args):
        """Send OSC message to FL Studio"""
        if self.connected:
            try:
                self.osc_client.send_message(address, list(args))
                return True
            except Exception as e:
                print(f"OSC send error: {e}")
                return False
        return False

    def _keyboard_shortcut(self, *keys):
        """Fallback keyboard shortcut automation"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press(keys)
                return True
            except Exception as e:
                print(f"Keyboard shortcut error: {e}")
                return False
        return False

    def _keyboard_combo(self, *keys):
        """Execute keyboard combo"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.hotkey(*keys)
                return True
            except Exception as e:
                print(f"Keyboard combo error: {e}")
                return False
        return False

    # ==================== TRANSPORT CONTROLS ====================

    def play(self) -> dict:
        """Start playback"""
        if not self._send_osc("/play", 1):
            self._keyboard_shortcut("space")
        return {"status": "success", "action": "play", "timestamp": datetime.now().isoformat()}

    def stop(self) -> dict:
        """Stop playback"""
        if not self._send_osc("/stop", 1):
            self._keyboard_shortcut("space")
        return {"status": "success", "action": "stop", "timestamp": datetime.now().isoformat()}

    def pause(self) -> dict:
        """Pause playback"""
        if not self._send_osc("/pause", 1):
            self._keyboard_combo("space")
        return {"status": "success", "action": "pause", "timestamp": datetime.now().isoformat()}

    def record(self) -> dict:
        """Toggle recording mode"""
        if not self._send_osc("/record", 1):
            self._keyboard_combo("r")
        return {"status": "success", "action": "record", "timestamp": datetime.now().isoformat()}

    def restart(self) -> dict:
        """Restart from beginning"""
        if not self._send_osc("/restart", 1):
            self._keyboard_shortcut("home")
        return {"status": "success", "action": "restart", "timestamp": datetime.now().isoformat()}

    def set_position(self, bar: int = 1) -> dict:
        """Set playback position to specific bar"""
        if not self._send_osc("/position", bar):
            for _ in range(bar):
                self._keyboard_shortcut("down")
        return {"status": "success", "position": f"bar {bar}", "timestamp": datetime.now().isoformat()}

    # ==================== MIXER CONTROLS ====================

    def set_volume(self, channel: int, volume: float) -> dict:
        """
        Set channel volume (0.0 to 1.0)
        channel: 0-99
        volume: 0.0 to 1.0
        """
        volume_int = int(volume * 128)
        if not self._send_osc(f"/mixer/{channel}/volume", volume_int):
            pass
        return {"status": "success", "channel": channel, "volume": volume, "timestamp": datetime.now().isoformat()}

    def set_pan(self, channel: int, pan: float) -> dict:
        """
        Set channel pan (-1.0 left to 1.0 right)
        """
        pan_int = int((pan + 1) * 64)
        if not self._send_osc(f"/mixer/{channel}/pan", pan_int):
            pass
        return {"status": "success", "channel": channel, "pan": pan, "timestamp": datetime.now().isoformat()}

    def set_mute(self, channel: int, muted: bool) -> dict:
        """Toggle channel mute"""
        if not self._send_osc(f"/mixer/{channel}/mute", 1 if muted else 0):
            pass
        return {"status": "success", "channel": channel, "muted": muted, "timestamp": datetime.now().isoformat()}

    def set_solo(self, channel: int, solo: bool) -> dict:
        """Toggle channel solo"""
        if not self._send_osc(f"/mixer/{channel}/solo", 1 if solo else 0):
            pass
        return {"status": "success", "channel": channel, "solo": solo, "timestamp": datetime.now().isoformat()}

    def master_volume(self, volume: float) -> dict:
        """Set master volume (0.0 to 1.0)"""
        volume_int = int(volume * 128)
        if not self._send_osc("/master/volume", volume_int):
            pass
        return {"status": "success", "master_volume": volume, "timestamp": datetime.now().isoformat()}

    # ==================== PATTERN/SEQUENCER ====================

    def select_pattern(self, pattern: int) -> dict:
        """Select pattern number (1-99)"""
        if not self._send_osc("/pattern/select", pattern):
            self._keyboard_shortcut(str(pattern))
        self.current_pattern = pattern
        return {"status": "success", "pattern": pattern, "timestamp": datetime.now().isoformat()}

    def create_pattern(self, name: str = None) -> dict:
        """Create new pattern"""
        self.pattern_count += 1
        if not self._send_osc("/pattern/create", self.pattern_count):
            self._keyboard_combo("ctrl", "n")
        return {"status": "success", "pattern": self.pattern_count, "name": name or f"Pattern {self.pattern_count}", "timestamp": datetime.now().isoformat()}

    def duplicate_pattern(self, from_pattern: int, to_pattern: int) -> dict:
        """Duplicate pattern to new slot"""
        if not self._send_osc("/pattern/duplicate", from_pattern, to_pattern):
            self._keyboard_combo("ctrl", "d")
        return {"status": "success", "from": from_pattern, "to": to_pattern, "timestamp": datetime.now().isoformat()}

    def set_step(self, step: int, velocity: int = 100) -> dict:
        """Set step in step sequencer"""
        if not self._send_osc("/step", step, velocity):
            pass
        return {"status": "success", "step": step, "velocity": velocity, "timestamp": datetime.now().isoformat()}

    # ==================== PIANO ROLL ====================

    def open_piano_roll(self, channel: int = None) -> dict:
        """Open piano roll for channel"""
        if not self._send_osc("/pianoroll/open", channel or 0):
            self._keyboard_combo("f6")
        return {"status": "success", "channel": channel, "timestamp": datetime.now().isoformat()}

    def close_piano_roll(self) -> dict:
        """Close piano roll"""
        if not self._send_osc("/pianoroll/close", 1):
            self._keyboard_shortcut("escape")
        return {"status": "success", "action": "close_piano_roll", "timestamp": datetime.now().isoformat()}

    def add_note(self, pitch: int, start_beat: float, duration: float, velocity: int = 100) -> dict:
        """
        Add note to piano roll
        pitch: 0-127 (C-1 = 0, C4 = 60)
        start_beat: 0.0 to end
        duration: in beats
        velocity: 0-127
        """
        if not self._send_osc("/note/add", pitch, start_beat, duration, velocity):
            pass
        return {"status": "success", "note": {"pitch": pitch, "start": start_beat, "duration": duration, "velocity": velocity}, "timestamp": datetime.now().isoformat()}

    def add_chord(self, root: int, chord_type: str, start_beat: float, duration: float, velocity: int = 100) -> dict:
        """
        Add chord to piano roll
        chord_type: major, minor, diminished, augmented, 7, maj7, min7
        """
        chords = {
            "major": [0, 4, 7],
            "minor": [0, 3, 7],
            "diminished": [0, 3, 6],
            "augmented": [0, 4, 8],
            "7": [0, 4, 7, 10],
            "maj7": [0, 4, 7, 11],
            "min7": [0, 3, 7, 10],
        }
        intervals = chords.get(chord_type, [0, 4, 7])
        notes = [root + interval for interval in intervals]
        for note in notes:
            self.add_note(note, start_beat, duration, velocity)
        return {"status": "success", "chord": chord_type, "root": root, "notes": notes, "timestamp": datetime.now().isoformat()}

    def clear_piano_roll(self) -> dict:
        """Clear all notes in piano roll"""
        if not self._send_osc("/pianoroll/clear", 1):
            self._keyboard_combo("ctrl", "a", "backspace")
        return {"status": "success", "action": "clear_piano_roll", "timestamp": datetime.now().isoformat()}

    # ==================== GENERATIVE BEAT TOOLS ====================

    def generate_drum_pattern(self, style: str = "basic", complexity: int = 3) -> dict:
        """
        Generate drum pattern
        style: basic, trap, house, techno, hiphop, lofi
        complexity: 1-5
        """
        drum_patterns = {
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
        }

        pattern = drum_patterns.get(style, drum_patterns["basic"])

        if complexity > 3:
            for drum in pattern:
                for i in range(len(pattern[drum])):
                    if random.random() < (complexity - 3) * 0.15:
                        pattern[drum][i] = 1 - pattern[drum][i]

        self.last_drum_pattern = pattern
        return {
            "status": "success",
            "style": style,
            "complexity": complexity,
            "pattern": pattern,
            "timestamp": datetime.now().isoformat()
        }

    def generate_bass_line(self, root_note: int = 36, scale: str = "minor", length: int = 8) -> dict:
        """
        Generate bass line
        root_note: MIDI note (36 = C2)
        scale: major, minor, pentatonic, blues
        length: number of beats
        """
        scale_patterns = {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "minor": [0, 2, 3, 5, 7, 8, 10],
            "pentatonic": [0, 2, 5, 7, 10],
            "blues": [0, 3, 5, 6, 10],
        }

        scale_notes = scale_patterns.get(scale, scale_patterns["minor"])
        bass_pattern = []

        root = root_note
        patterns = [
            [0, 0, 2, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 3],
            [0, -2, 0, 0],
        ]

        selected_pattern = random.choice(patterns)
        for beat in range(length):
            interval = selected_pattern[beat % len(selected_pattern)]
            if interval < 0:
                interval = scale_notes[random.randint(0, len(scale_notes)-1)]
            note = root + interval
            bass_pattern.append({"note": note, "duration": 1})

        self.last_bass_line = bass_pattern
        return {
            "status": "success",
            "root": root_note,
            "scale": scale,
            "length": length,
            "bass_line": bass_pattern,
            "timestamp": datetime.now().isoformat()
        }

    def generate_melody(self, key: int = 60, scale: str = "minor", length: int = 8, octave_range: tuple = (4, 5)) -> dict:
        """
        Generate melodic phrase
        key: MIDI root note
        scale: major, minor, pentatonic, dorian, mixolydian
        length: number of notes
        """
        scale_patterns = {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "minor": [0, 2, 3, 5, 7, 8, 10],
            "pentatonic": [0, 2, 5, 7, 10],
            "dorian": [0, 2, 3, 5, 7, 9, 10],
            "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        }

        scale_notes = scale_patterns.get(scale, scale_patterns["minor"])

        melody = []
        current_octave = random.randint(octave_range[0], octave_range[1])
        current_note = key + (current_octave - 4) * 12

        for i in range(length):
            direction = random.choice([-1, 1, 1, 1])
            if direction != 0:
                step = random.choice(scale_notes)
                current_note = key + step + (current_octave - 4) * 12

            if random.random() < 0.2:
                current_octave += random.choice([-1, 1])
                current_octave = max(octave_range[0], min(octave_range[1], current_octave))

            duration = random.choice([0.5, 1, 1, 1.5, 2])
            velocity = random.randint(80, 120)

            melody.append({
                "note": current_note,
                "start": i,
                "duration": duration,
                "velocity": velocity
            })

        self.last_melody = melody
        return {
            "status": "success",
            "key": key,
            "scale": scale,
            "melody": melody,
            "timestamp": datetime.now().isoformat()
        }

    def generate_chord_progression(self, key: int = 60, style: str = "pop", length: int = 4) -> dict:
        """
        Generate chord progression
        key: MIDI root note
        style: pop, jazz, cinematic, edm
        """
        progressions = {
            "pop": ["I", "V", "vi", "IV"],
            "jazz": ["IIm7", "V7", "Imaj7", "IVm7"],
            "cinematic": ["Im", "VII", "III", "VI"],
            "edm": ["I", "IV", "V", "I"],
        }

        prog = progressions.get(style, progressions["pop"])

        chord_map = {
            "I": [0, 4, 7],
            "II": [2, 5, 9],
            "III": [4, 7, 11],
            "IV": [5, 9, 12],
            "V": [7, 11, 14],
            "VI": [9, 12, 16],
            "VII": [11, 14, 17],
            "IIm7": [2, 5, 9, 12],
            "V7": [7, 11, 14, 17],
            "Imaj7": [0, 4, 7, 11],
            "IVm7": [5, 9, 12, 16],
            "IIIm": [4, 7, 10],
        }

        chords = []
        for i in range(length):
            chord_name = prog[i % len(prog)]
            intervals = chord_map.get(chord_name, [0, 4, 7])
            chord_notes = [key + interval for interval in intervals]
            chords.append({"name": chord_name, "notes": chord_notes, "duration": 4})

        self.last_chord_progression = chords
        return {
            "status": "success",
            "key": key,
            "style": style,
            "progression": chords,
            "timestamp": datetime.now().isoformat()
        }

    # ==================== ARRANGEMENT ====================

    def add_to_arrangement(self, pattern: int, position: int, length: int = 4) -> dict:
        """Add pattern to arrangement at position"""
        if not self._send_osc("/arrangement/add", pattern, position, length):
            pass
        return {"status": "success", "pattern": pattern, "position": position, "length": length, "timestamp": datetime.now().isoformat()}

    def set_tempo(self, bpm: int) -> dict:
        """Set tempo (BPM)"""
        if not self._send_osc("/tempo", bpm):
            pass
        return {"status": "success", "bpm": bpm, "timestamp": datetime.now().isoformat()}

    def set_time_signature(self, numerator: int = 4, denominator: int = 4) -> dict:
        """Set time signature"""
        if not self._send_osc("/timesig", numerator, denominator):
            pass
        return {"status": "success", "time_signature": f"{numerator}/{denominator}", "timestamp": datetime.now().isoformat()}

    # ==================== PROJECT MANAGEMENT ====================

    def save_project(self, path: str) -> dict:
        """Save FL Studio project"""
        if not self._send_osc("/project/save", path):
            self._keyboard_combo("ctrl", "s")
        self.current_project = path
        return {"status": "success", "path": path, "timestamp": datetime.now().isoformat()}

    def new_project(self) -> dict:
        """Create new project"""
        if not self._send_osc("/project/new", 1):
            self._keyboard_combo("ctrl", "n")
        return {"status": "success", "action": "new_project", "timestamp": datetime.now().isoformat()}

    # ==================== PLUGINS ====================

    def load_plugin(self, plugin_name: str, slot: int = 0) -> dict:
        """Load plugin in slot"""
        if not self._send_osc(f"/plugin/load/{slot}", plugin_name):
            pass
        return {"status": "success", "plugin": plugin_name, "slot": slot, "timestamp": datetime.now().isoformat()}

    def set_plugin_param(self, plugin_slot: int, param: int, value: float) -> dict:
        """Set plugin parameter"""
        value_int = int(value * 127)
        if not self._send_osc(f"/plugin/{plugin_slot}/param/{param}", value_int):
            pass
        return {"status": "success", "plugin": plugin_slot, "parameter": param, "value": value, "timestamp": datetime.now().isoformat()}

    # ==================== STATUS ====================

    def get_status(self) -> dict:
        """Get current FL Studio status"""
        return {
            "status": "connected" if self.connected else "disconnected",
            "osc_port": self.fl_port,
            "current_project": self.current_project,
            "pattern_count": self.pattern_count,
            "timestamp": datetime.now().isoformat()
        }


flstudio = FLStudioMCP()

TOOLS = [
    {
        "name": "flstudio_play",
        "description": "Start FL Studio playback",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "flstudio_stop",
        "description": "Stop FL Studio playback",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "flstudio_pause",
        "description": "Pause FL Studio playback",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "flstudio_record",
        "description": "Toggle recording mode",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "flstudio_restart",
        "description": "Restart playback from beginning",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "flstudio_set_position",
        "description": "Set playback position to specific bar",
        "inputSchema": {
            "type": "object",
            "properties": {"bar": {"type": "integer", "minimum": 1, "default": 1}}
        }
    },
    {
        "name": "flstudio_set_volume",
        "description": "Set mixer channel volume (0.0 to 1.0)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel": {"type": "integer", "minimum": 0, "maximum": 99},
                "volume": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["channel", "volume"]
        }
    },
    {
        "name": "flstudio_set_pan",
        "description": "Set mixer channel pan (-1.0 left to 1.0 right)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel": {"type": "integer", "minimum": 0, "maximum": 99},
                "pan": {"type": "number", "minimum": -1, "maximum": 1}
            },
            "required": ["channel", "pan"]
        }
    },
    {
        "name": "flstudio_set_mute",
        "description": "Toggle channel mute",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel": {"type": "integer", "minimum": 0, "maximum": 99},
                "muted": {"type": "boolean"}
            },
            "required": ["channel", "muted"]
        }
    },
    {
        "name": "flstudio_set_solo",
        "description": "Toggle channel solo",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel": {"type": "integer", "minimum": 0, "maximum": 99},
                "solo": {"type": "boolean"}
            },
            "required": ["channel", "solo"]
        }
    },
    {
        "name": "flstudio_master_volume",
        "description": "Set master output volume",
        "inputSchema": {
            "type": "object",
            "properties": {"volume": {"type": "number", "minimum": 0, "maximum": 1}},
            "required": ["volume"]
        }
    },
    {
        "name": "flstudio_select_pattern",
        "description": "Select pattern in step sequencer",
        "inputSchema": {
            "type": "object",
            "properties": {"pattern": {"type": "integer", "minimum": 1, "maximum": 99}},
            "required": ["pattern"]
        }
    },
    {
        "name": "flstudio_create_pattern",
        "description": "Create new pattern",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string"}}
        }
    },
    {
        "name": "flstudio_open_piano_roll",
        "description": "Open piano roll for channel",
        "inputSchema": {
            "type": "object",
            "properties": {"channel": {"type": "integer", "minimum": 0}}
        }
    },
    {
        "name": "flstudio_add_note",
        "description": "Add note to piano roll",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pitch": {"type": "integer", "minimum": 0, "maximum": 127},
                "start_beat": {"type": "number", "minimum": 0},
                "duration": {"type": "number", "minimum": 0.25},
                "velocity": {"type": "integer", "minimum": 0, "maximum": 127}
            },
            "required": ["pitch", "start_beat", "duration"]
        }
    },
    {
        "name": "flstudio_add_chord",
        "description": "Add chord to piano roll",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "integer", "minimum": 0, "maximum": 127},
                "chord_type": {"type": "enum", "enum": ["major", "minor", "diminished", "augmented", "7", "maj7", "min7"]},
                "start_beat": {"type": "number", "minimum": 0},
                "duration": {"type": "number", "minimum": 0.25}
            },
            "required": ["root", "chord_type", "start_beat", "duration"]
        }
    },
    {
        "name": "flstudio_clear_piano_roll",
        "description": "Clear all notes in piano roll",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "flstudio_generate_drum_pattern",
        "description": "Generate drum pattern - returns pattern data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "style": {"type": "enum", "enum": ["basic", "trap", "house", "techno", "hiphop", "lofi"], "default": "basic"},
                "complexity": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3}
            }
        }
    },
    {
        "name": "flstudio_generate_bass_line",
        "description": "Generate bass line - returns note data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root_note": {"type": "integer", "minimum": 24, "maximum": 60, "default": 36},
                "scale": {"type": "enum", "enum": ["major", "minor", "pentatonic", "blues"], "default": "minor"},
                "length": {"type": "integer", "minimum": 4, "maximum": 32, "default": 8}
            }
        }
    },
    {
        "name": "flstudio_generate_melody",
        "description": "Generate melodic phrase - returns note data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "integer", "minimum": 24, "maximum": 84, "default": 60},
                "scale": {"type": "enum", "enum": ["major", "minor", "pentatonic", "dorian", "mixolydian"], "default": "minor"},
                "length": {"type": "integer", "minimum": 4, "maximum": 32, "default": 8}
            }
        }
    },
    {
        "name": "flstudio_generate_chord_progression",
        "description": "Generate chord progression - returns chord data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "integer", "minimum": 24, "maximum": 84, "default": 60},
                "style": {"type": "enum", "enum": ["pop", "jazz", "cinematic", "edm"], "default": "pop"},
                "length": {"type": "integer", "minimum": 2, "maximum": 8, "default": 4}
            }
        }
    },
    {
        "name": "flstudio_set_tempo",
        "description": "Set project tempo in BPM",
        "inputSchema": {
            "type": "object",
            "properties": {"bpm": {"type": "integer", "minimum": 40, "maximum": 300, "default": 120}},
            "required": ["bpm"]
        }
    },
    {
        "name": "flstudio_save_project",
        "description": "Save FL Studio project",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "flstudio_get_status",
        "description": "Get FL Studio connection status and info",
        "inputSchema": {"type": "object", "properties": {}}
    },
]


def handle_tool(name: str, args: dict = None) -> dict:
    """Handle tool calls"""
    args = args or {}

    handlers = {
        "flstudio_play": lambda: flstudio.play(),
        "flstudio_stop": lambda: flstudio.stop(),
        "flstudio_pause": lambda: flstudio.pause(),
        "flstudio_record": lambda: flstudio.record(),
        "flstudio_restart": lambda: flstudio.restart(),
        "flstudio_set_position": lambda: flstudio.set_position(args.get("bar", 1)),
        "flstudio_set_volume": lambda: flstudio.set_volume(args["channel"], args["volume"]),
        "flstudio_set_pan": lambda: flstudio.set_pan(args["channel"], args["pan"]),
        "flstudio_set_mute": lambda: flstudio.set_mute(args["channel"], args["muted"]),
        "flstudio_set_solo": lambda: flstudio.set_solo(args["channel"], args["solo"]),
        "flstudio_master_volume": lambda: flstudio.master_volume(args["volume"]),
        "flstudio_select_pattern": lambda: flstudio.select_pattern(args["pattern"]),
        "flstudio_create_pattern": lambda: flstudio.create_pattern(args.get("name")),
        "flstudio_open_piano_roll": lambda: flstudio.open_piano_roll(args.get("channel")),
        "flstudio_add_note": lambda: flstudio.add_note(
            args["pitch"], args["start_beat"], args["duration"], args.get("velocity", 100)
        ),
        "flstudio_add_chord": lambda: flstudio.add_chord(
            args["root"], args["chord_type"], args["start_beat"], args["duration"], args.get("velocity", 100)
        ),
        "flstudio_clear_piano_roll": lambda: flstudio.clear_piano_roll(),
        "flstudio_generate_drum_pattern": lambda: flstudio.generate_drum_pattern(
            args.get("style", "basic"), args.get("complexity", 3)
        ),
        "flstudio_generate_bass_line": lambda: flstudio.generate_bass_line(
            args.get("root_note", 36), args.get("scale", "minor"), args.get("length", 8)
        ),
        "flstudio_generate_melody": lambda: flstudio.generate_melody(
            args.get("key", 60), args.get("scale", "minor"), args.get("length", 8)
        ),
        "flstudio_generate_chord_progression": lambda: flstudio.generate_chord_progression(
            args.get("key", 60), args.get("style", "pop"), args.get("length", 4)
        ),
        "flstudio_set_tempo": lambda: flstudio.set_tempo(args["bpm"]),
        "flstudio_save_project": lambda: flstudio.save_project(args["path"]),
        "flstudio_get_status": lambda: flstudio.get_status(),
    }

    if name in handlers:
        return handlers[name]()

    return {"error": f"Unknown tool: {name}"}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        tool_name = sys.argv[1]
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        result = handle_tool(tool_name, args)
        print(json.dumps(result))
    else:
        print("FL Studio MCP Server running...")
        print(f"Tools available: {len(TOOLS)}")
        status = flstudio.get_status()
        print(f"Status: {status}")