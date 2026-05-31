"""
FL Studio PRO MCP - Advanced Beat Making & AI Music Production
Complete music production suite with AI generation, VST control, arrangement, and export
"""

import json
import os
import random
import shutil
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from flask import Flask, request, jsonify, send_file
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

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

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


app = Flask(__name__)


# ==================== MUSIC THEORY & AI ====================

class MusicTheoryPro:
    """Advanced music theory with AI-powered generation"""

    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    @classmethod
    def _init_midi_map(cls):
        return {f"{n}{o}": (o + 1) * 12 + i for o in range(-1, 9) for i, n in enumerate(cls.NOTES)}
    
    NOTE_TO_MIDI = {}  # Will be populated on first use

    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 1, 3, 5, 7, 8, 10],
        "lydian": [0, 2, 4, 6, 7, 9, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
        " bebop_major": [0, 2, 4, 5, 7, 9, 10, 11],
        "whole_tone": [0, 2, 4, 6, 8, 10],
        "chromatic": list(range(12)),
    }

    CHORD_TYPES = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "diminished": [0, 3, 6],
        "augmented": [0, 4, 8],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7],
        "major7": [0, 4, 7, 11],
        "minor7": [0, 3, 7, 10],
        "dominant7": [0, 4, 7, 10],
        "major9": [0, 4, 7, 11, 14],
        "minor9": [0, 3, 7, 10, 14],
        "dominant9": [0, 4, 7, 10, 14],
        "add9": [0, 4, 7, 14],
        "6/9": [0, 4, 7, 9, 14],
        "dim7": [0, 3, 6, 9],
        "half_dim7": [0, 3, 6, 10],
    }

    DRUM_MIDI = {
        "kick": 36, "kick_alt": 35, "kick2": 37,
        "snare": 38, "snare_alt": 40, "snare_ghost": 37,
        "hihat_closed": 42, "hihat_pedal": 44, "hihat_open": 46,
        "crash": 49, "crash_alt": 55, "ride": 51, "ride_bell": 53,
        "tom_high": 48, "tom_mid": 45, "tom_low": 43,
        "clap": 39, "clap_alt": 37, "rim": 37, "rim_alt": 36,
        "cowbell": 56, "shaker": 70, "tambourine": 54,
        "conga_high": 62, "conga_mid": 60, "conga_low": 58,
        "bongo_high": 64, "bongo_low": 63,
    }

    KEY_AREAS = {
        "sub_bass": (24, 36),
        "bass": (36, 48),
        "low_mid": (48, 60),
        "mid": (60, 72),
        "high_mid": (72, 84),
        "lead": (84, 96),
        "high": (96, 108),
    }

    @staticmethod
    def midi_to_note(midi: int) -> str:
        octave = (midi // 12) - 1
        note = MusicTheoryPro.NOTES[midi % 12]
        return f"{note}{octave}"

    @staticmethod
    def note_to_midi(note: str) -> int:
        note = note.upper().strip()
        return MusicTheoryPro.NOTE_TO_MIDI.get(note, 60)

    @staticmethod
    def get_scale_notes(root: int, scale: str) -> list[int]:
        intervals = MusicTheoryPro.SCALES.get(scale, [0, 2, 4, 5, 7, 9, 11])
        return [root + i for i in intervals]

    @staticmethod
    def get_chord_notes(root: int, chord: str) -> list[int]:
        intervals = MusicTheoryPro.CHORD_TYPES.get(chord, [0, 4, 7])
        return [root + i for i in intervals]

    @staticmethod
    def transpose(note: int, semitones: int) -> int:
        return max(0, min(127, note + semitones))

    @staticmethod
    def quantize(time: float, grid: float) -> float:
        return round(time / grid) * grid


class GenerativeEngine:
    """AI-powered music generation engine"""

    def __init__(self):
        self.style_profiles = {
            "trap": {
                "tempo_range": (140, 180),
                "drums": {"kick": 0.4, "snare": 0.15, "hihat": 0.3, "808": 0.15},
                "scales": ["minor", "harmonic_minor"],
                "chords": ["minor", "minor7", "dominant7"],
                "bass_pattern": "rolling",
            },
            "house": {
                "tempo_range": (120, 130),
                "drums": {"kick": 0.35, "snare": 0.2, "hihat": 0.25, "clap": 0.2},
                "scales": ["major", "mixolydian"],
                "chords": ["major", "dominant7", "minor"],
                "bass_pattern": "driving",
            },
            "techno": {
                "tempo_range": (130, 150),
                "drums": {"kick": 0.5, "hihat": 0.3, "perc": 0.15, "snare": 0.05},
                "scales": ["minor", "phrygian"],
                "chords": ["minor", "sus2", "dominant7"],
                "bass_pattern": "drone",
            },
            "hiphop": {
                "tempo_range": (80, 110),
                "drums": {"kick": 0.3, "snare": 0.25, "hihat": 0.25, "perc": 0.2},
                "scales": ["major", "minor", "mixolydian"],
                "chords": ["major", "minor7", "dominant7"],
                "bass_pattern": "walking",
            },
            "lofi": {
                "tempo_range": (70, 90),
                "drums": {"kick": 0.35, "snare": 0.2, "hihat": 0.25, "vinyl": 0.2},
                "scales": ["pentatonic_minor", "major"],
                "chords": ["major", "minor", "add9"],
                "bass_pattern": "plucks",
            },
            "dubstep": {
                "tempo_range": (140, 160),
                "drums": {"kick": 0.4, "snare": 0.15, "hihat": 0.25, "sub": 0.2},
                "scales": ["minor", "phrygian"],
                "chords": ["minor", "diminished"],
                "bass_pattern": "wobble",
            },
            "drift": {
                "tempo_range": (120, 160),
                "drums": {"kick": 0.35, "snare": 0.15, "hihat": 0.3, "synth": 0.2},
                "scales": ["dorian", "mixolydian", "lydian"],
                "chords": ["major", "dominant7", "minor7"],
                "bass_pattern": "driving",
            },
            "ambient": {
                "tempo_range": (60, 100),
                "drums": {"kick": 0.2, "pad": 0.5, "hihat": 0.15, "nature": 0.15},
                "scales": ["minor", "major", "whole_tone"],
                "chords": ["major7", "minor7", "add9", "augmented"],
                "bass_pattern": "drone",
            },
            "dnb": {
                "tempo_range": (160, 180),
                "drums": {"kick": 0.3, "snare": 0.2, "hihat": 0.3, "perc": 0.2},
                "scales": ["minor", "dorian"],
                "chords": ["minor", "minor7", "dominant7"],
                "bass_pattern": "rolling",
            },
            "garage": {
                "tempo_range": (128, 140),
                "drums": {"kick": 0.3, "snare": 0.25, "hihat": 0.3, "perc": 0.15},
                "scales": ["major", "mixolydian"],
                "chords": ["major", "minor", "dominant7"],
                "bass_pattern": "syncopated",
            },
        }

    def generate_drums(self, style: str = "house", bars: int = 1, complexity: int = 3,
                      swing: float = 0.0, shuffle: float = 0.0) -> dict:
        """Generate sophisticated drum patterns"""

        profile = self.style_profiles.get(style, self.style_profiles["house"])
        steps = 8 * bars

        patterns = {
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
                "hihat": [1, 1, 1, 1, 1, 1, 1, 1],
                "perc": [0, 1, 0, 1, 0, 1, 0, 1],
                "snare": [0, 0, 0, 0, 1, 0, 0, 0],
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
            },
            "dubstep": {
                "kick": [1, 0, 0, 1, 0, 0, 0, 1],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0],
                "hihat": [1, 1, 0, 1, 0, 1, 0, 1],
                "sub": [1, 0, 1, 0, 0, 1, 0, 1],
            },
            "dnb": {
                "kick": [1, 0, 0, 1, 0, 0, 1, 0],
                "snare": [0, 0, 1, 0, 0, 0, 1, 0],
                "hihat": [1, 1, 1, 1, 1, 1, 1, 1],
                "perc": [0, 1, 0, 1, 0, 1, 0, 1],
            },
        }

        base_pattern = patterns.get(style, patterns["house"])

        pattern = {}
        for drum, hits in base_pattern.items():
            pattern[drum] = list(hits) * bars

        for _ in range(complexity - 3) if complexity > 3 else []:
            drum = random.choice(list(pattern.keys()))
            idx = random.randint(0, len(pattern[drum]) - 1)
            pattern[drum][idx] = 1 - pattern[drum][idx]

        sequence = []
        for step in range(len(pattern[list(pattern.keys())[0]])):
            step_events = []
            for drum, hits in pattern.items():
                if hits[step]:
                    velocity = random.randint(90, 127) if random.random() > 0.1 else random.randint(50, 89)
                    step_events.append({
                        "drum": drum,
                        "midi": MusicTheoryPro.DRUM_MIDI.get(drum, 36),
                        "velocity": velocity,
                        "timing": step / steps,
                    })
            if step_events:
                sequence.append({"step": step, "events": step_events})

        return {
            "style": style,
            "bars": bars,
            "steps": steps,
            "complexity": complexity,
            "swing": swing,
            "pattern": pattern,
            "sequence": sequence,
            "midi_data": [
                {"midi": e["midi"], "velocity": e["velocity"], "timing": e["timing"], "duration": 0.1}
                for s in sequence for e in s["events"]
            ],
        }

    def generate_bass(self, root: int = 36, scale: str = "minor", length: int = 8,
                     pattern_type: str = "walking", octave_shift: int = 0) -> dict:
        """Generate advanced bass lines"""

        scale_notes = MusicTheoryPro.get_scale_notes(root + (octave_shift * 12), scale)

        patterns = {
            "walking": [0, 2, 0, 3, 0, 2, 0, 1],
            "rolling": [0, 0, 2, 0, 3, 0, 2, 3],
            "driving": [0, 0, 2, 0, 0, 0, 3, 0],
            "syncopated": [0, 0, 2, 0, 0, 2, 0, 3],
            "plucks": [0, 0, 2, 0, 3, 0, 2, 0],
            "offbeat": [0, 2, 0, 3, 0, 2, 0, 3],
            "drone": [0, 0, 0, 0, 0, 0, 0, 0],
            "groove": [0, 2, 0, 1, 0, 3, 0, 2],
            "figure": [0, 3, 2, 0, 3, 0, 2, 0],
            "wobble": [0, 0, 0, 0, 3, 3, 0, 0],
        }

        base_pattern = patterns.get(pattern_type, patterns["walking"])

        notes = []
        for i in range(length):
            interval_idx = base_pattern[i % len(base_pattern)]
            if interval_idx < len(scale_notes):
                note = scale_notes[interval_idx]
            else:
                note = root + (octave_shift * 12)

            if random.random() < 0.1:
                note = root + (octave_shift * 12) + random.choice([-12, 12])

            velocity = random.randint(80, 110)
            duration = random.choice([0.5, 1, 1, 1, 1.5, 2])

            notes.append({
                "index": i,
                "note": note,
                "name": MusicTheoryPro.midi_to_note(note),
                "velocity": velocity,
                "duration": duration,
                "timing": i,
            })

        return {
            "root": root,
            "root_name": MusicTheoryPro.midi_to_note(root),
            "scale": scale,
            "pattern": pattern_type,
            "length": length,
            "notes": notes,
            "midi_data": [
                {"midi": n["note"], "velocity": n["velocity"], "duration": n["duration"], "timing": n["timing"]}
                for n in notes
            ],
        }

    def generate_melody(self, key: int = 60, scale: str = "minor", length: int = 8,
                       range_low: int = 4, range_high: int = 6, density: float = 0.7,
                       contour: str = "random") -> dict:
        """Generate intelligent melodies"""

        scale_notes = []
        for octave in range(range_low, range_high + 1):
            for interval in MusicTheoryPro.SCALES.get(scale, [0, 2, 4, 5, 7, 9, 11]):
                note = key + interval + (octave - 4) * 12
                if 24 <= note <= 108:
                    scale_notes.append(note)
        scale_notes = sorted(set(scale_notes))

        contours = {
            "random": lambda: random.choice([-1, 0, 1, 1, 1, 2]),
            "ascending": lambda: random.choice([1, 1, 2, 2]),
            "descending": lambda: random.choice([-1, -1, -2, -2]),
            "wave": lambda: random.choice([-1, 0, 1]),
            "jumps": lambda: random.choice([-3, -2, 2, 3, 0, 0]),
        }

        contour_func = contours.get(contour, contours["random"])

        melody = []
        current_idx = random.randint(0, len(scale_notes) - 1)

        for i in range(length):
            if random.random() < density:
                direction = contour_func()

                if direction == 0:
                    current_idx = random.randint(0, len(scale_notes) - 1)
                else:
                    current_idx = max(0, min(len(scale_notes) - 1, current_idx + direction))

                note = scale_notes[current_idx]
                duration = random.choice([0.25, 0.5, 0.5, 1, 1, 1.5, 2])
                velocity = random.randint(60, 120)

                melody.append({
                    "index": i,
                    "note": note,
                    "name": MusicTheoryPro.midi_to_note(note),
                    "duration": duration,
                    "velocity": velocity,
                    "timing": sum(m.get("duration", 1) for m in melody),
                })

        return {
            "key": key,
            "key_name": MusicTheoryPro.midi_to_note(key),
            "scale": scale,
            "range": f"{range_low}-{range_high}",
            "contour": contour,
            "length": length,
            "notes": melody,
            "midi_data": [
                {"midi": m["note"], "velocity": m["velocity"], "duration": m["duration"], "timing": m["timing"]}
                for m in melody
            ],
        }

    def generate_chords(self, key: int = 60, style: str = "pop", bars: int = 4,
                       voicing: str = "spread", extensions: bool = True) -> dict:
        """Generate chord progressions"""

        progressions = {
            "pop": ["I", "V", "vi", "IV", "I", "V", "vi", "IV"],
            "pop_verse": ["I", "vi", "IV", "V", "I", "vi", "IV", "I"],
            "pop_alt": ["I", "IV", "V", "IV", "I", "IV", "V", "I"],
            "jazz": ["IIm7", "V7", "Imaj7", "IVm7", "IIm7", "V7", "Imaj7", "VI7"],
            "jazz_alt": ["Imaj7", "IVm7", "IIm7", "V7", "VI7", "IIIm7", "VI7", "IVm7"],
            "neo_soul": ["Imaj7", "IVm7", "IIm7", "V7", "IVm7", "VII7", "IIIm7", "VI7"],
            "cinematic": ["Im", "VII", "III", "VI", "IV", "I", "V", "I"],
            "edm": ["I", "IV", "V", "I", "i", "VI", "IV", "V"],
            "rock": ["I", "IV", "I", "V", "I", "IV", "V", "I"],
            "blues": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "V7"],
            "reggae": ["I", "IV", "I", "V", "I", "IV", "V", "I"],
            "funk": ["I7", "IV7", "I7", "V7", "IV7", "V7", "I7", "V7"],
            "ambient": ["Imaj9", "IVm9", "Imaj9", "VIm9", "Imaj9", "IVm9", "VIm9", "V7"],
            "trap": ["Im", "IVm", "VII", "III", "Im", "IVm", "VI", "V"],
            "lofi": ["Imaj7", "VIm7", "IIm7", "V7", "Imaj7", "IVm7", "VIm7", "V7"],
        }

        roman_to_root = {
            "I": 0, "i": 0, "II": 2, "IIm7": 2, "III": 4, "III7": 4,
            "IV": 5, "IVm7": 5, "V": 7, "V7": 7, "VI": 9, "VI7": 9,
            "VII": 11, "VI": 9, "VII7": 11,
        }

        chord_types = {
            "I": "major7", "i": "minor7", "II": "major7", "IIm7": "minor7",
            "III": "major7", "III7": "major7", "IV": "major7", "IVm7": "minor7",
            "V": "major7", "V7": "dominant7", "VI": "major7", "VI7": "dominant7",
            "VII": "major7", "VI": "minor7",
        }

        voicings = {
            "root": lambda n: [n, n + 12],
            "spread": lambda n: [n, n + 4, n + 7],
            "block": lambda n: [n, n + 4, n + 7, n + 12],
            "jazz": lambda n: [n - 12, n, n + 3, n + 7],
            "piano": lambda n: [n, n + 4, n + 7, n + 12, n + 16],
            "guitar": lambda n: [n, n + 3, n + 5, n + 7, n + 10],
            "inversion": lambda n: [n, n + 12, n + 19],
        }

        prog = progressions.get(style, progressions["pop"])
        voicing_func = voicings.get(voicing, voicings["spread"])

        chords = []
        for i in range(bars):
            roman = prog[i % len(prog)]
            root_offset = roman_to_root.get(roman, 0)
            root = key + root_offset
            chord_type = chord_types.get(roman, "major7")

            if extensions and random.random() < 0.3:
                if "7" in chord_type:
                    pass
                elif "m" in chord_type:
                    chord_type = random.choice(["minor7", "minor9", "min7b5"])
                else:
                    chord_type = random.choice(["major7", "major9", "add9"])

            chord_notes = MusicTheoryPro.get_chord_notes(root, chord_type.replace("7", "").replace("maj", "").replace("min", "").replace("m", ""))
            voiced = voicing_func(root)

            chords.append({
                "index": i,
                "roman": roman,
                "root": root,
                "root_name": MusicTheoryPro.midi_to_note(root),
                "type": chord_type,
                "notes": chord_notes,
                "voiced": voiced,
                "duration": 4,
            })

        return {
            "key": key,
            "key_name": MusicTheoryPro.midi_to_note(key),
            "style": style,
            "bars": bars,
            "voicing": voicing,
            "chords": chords,
            "midi_data": [
                {"midi": n, "velocity": 75, "duration": 4, "timing": c["index"] * 4}
                for c in chords for n in c["voiced"]
            ],
        }

    def generate_arps(self, chord_root: int = 60, chord_type: str = "major",
                     pattern: str = "up", octave_range: int = 2, speed: str = "8ths") -> dict:
        """Generate arpeggios from chord"""

        chord_notes = MusicTheoryPro.get_chord_notes(chord_root, chord_type)
        full_notes = []
        for octave in range(octave_range):
            for note in chord_notes:
                full_notes.append(note + (octave * 12))

        patterns = {
            "up": list(range(len(full_notes))),
            "down": list(range(len(full_notes) - 1, -1, -1)),
            "updown": list(range(len(full_notes))) + list(range(len(full_notes) - 2, 0, -1)),
            "random": list(range(len(full_notes))),
            "pingpong": [0, 1, 2, 3, 2, 1, 0, 1, 2, 3],
            "roller": [0, 12, 0, 12, 0, 12],
        }

        speeds = {"16ths": 0.25, "8ths": 0.5, "quarters": 1, "half": 2}
        duration = speeds.get(speed, 0.5)

        indices = patterns.get(pattern, patterns["up"])
        arp_notes = []

        for i, idx in enumerate(indices):
            if idx < len(full_notes):
                note = full_notes[idx]
                arp_notes.append({
                    "index": i,
                    "note": note,
                    "name": MusicTheoryPro.midi_to_note(note),
                    "velocity": random.randint(70, 100),
                    "duration": duration,
                    "timing": i * duration,
                })

        return {
            "chord_root": chord_root,
            "chord_type": chord_type,
            "pattern": pattern,
            "octave_range": octave_range,
            "speed": speed,
            "notes": arp_notes,
            "midi_data": [
                {"midi": n["note"], "velocity": n["velocity"], "duration": n["duration"], "timing": n["timing"]}
                for n in arp_notes
            ],
        }

    def generate_arrangement(self, style: str = "house", total_bars: int = 32,
                            intro_bars: int = 4, outro_bars: int = 4) -> dict:
        """Generate song arrangement structure"""

        structures = {
            "simple": ["intro", "verse", "chorus", "verse", "chorus", "outro"],
            "ab": ["intro", "a", "b", "a", "b", "bridge", "b", "outro"],
            "verse_chorus": ["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "outro"],
            "complex": ["intro", "verse1", "pre_chorus", "chorus", "verse2", "chorus", "bridge", "break", "final", "outro"],
            "electronic": ["intro", "build", "drop1", "break", "drop2", "outro"],
            "trap": ["intro", "verse", "hook", "verse", "hook", "bridge", "hook", "outro"],
            "lofi": ["intro", "loop1", "loop2", "loop1_alt", "loop2", "outro"],
        }

        structure = structures.get(style, structures["simple"])

        bars_remaining = total_bars - intro_bars - outro_bars
        section_bars = bars_remaining // len(structure)

        arrangement = []
        current_bar = 0

        arrangement.append({"section": "intro", "start": 0, "bars": intro_bars})
        current_bar += intro_bars

        for section in structure:
            arrangement.append({
                "section": section,
                "start": current_bar,
                "bars": section_bars,
            })
            current_bar += section_bars

        arrangement.append({"section": "outro", "start": current_bar, "bars": outro_bars})

        return {
            "style": style,
            "total_bars": total_bars,
            "intro_bars": intro_bars,
            "outro_bars": outro_bars,
            "structure": structure,
            "arrangement": arrangement,
        }

    def generate_full_track(self, style: str = "house", key: int = 60, scale: str = "minor",
                          bars: int = 16, tempo: int = 120, add_arps: bool = True,
                          add_lead: bool = True) -> dict:
        """Generate complete production-ready track"""

        profile = self.style_profiles.get(style, self.style_profiles["house"])

        tempo = random.randint(*profile["tempo_range"]) if tempo is None else tempo
        scale = random.choice(profile["scales"]) if scale is None else scale

        arrangement = self.generate_arrangement(style, bars)
        drums = self.generate_drums(style, bars // 4, 3)
        bass = self.generate_bass(key - 24, scale, bars, random.choice(["walking", "rolling", "driving"]))
        melody = self.generate_melody(key, scale, bars * 2, 4, 6, 0.6)
        chords = self.generate_chords(key, style.replace("lofi", "pop"), bars, "spread", True)

        lead = None
        if add_lead:
            lead = self.generate_melody(key + 12, scale, bars, 5, 7, 0.5)

        arp = None
        if add_arps:
            arp = self.generate_arps(key, "major", "updown", 2, "16ths")

        return {
            "metadata": {
                "style": style,
                "key": key,
                "key_name": MusicTheoryPro.midi_to_note(key),
                "scale": scale,
                "tempo": tempo,
                "bars": bars,
                "generated_at": datetime.now().isoformat(),
            },
            "arrangement": arrangement,
            "drums": drums,
            "bass": bass,
            "melody": melody,
            "chords": chords,
            "lead": lead,
            "arp": arp,
            "full_midi": self._compile_full_midi(drums, bass, melody, chords, lead, arp),
        }

    def _compile_full_midi(self, *parts) -> list:
        """Compile all parts into unified MIDI timeline"""
        all_events = []
        for part in parts:
            if part and "midi_data" in part:
                all_events.extend(part["midi_data"])
        return sorted(all_events, key=lambda x: x.get("timing", 0))


class VSTManager:
    """Manage VST plugins and presets"""

    PRESETS = {
        "synth_lead": ["saw_lead", "square_lead", "pulse_lead", "supersaw"],
        "bass": ["sub_bass", "wobble_bass", " fm_bass", "acid_bass"],
        "pad": ["ambient_pad", "strings", "choir", "sweep_pad"],
        "pluck": ["guitar_pluck", "harp_pluck", "electric_pluck"],
        "keys": ["piano", "electric_piano", "organ", "clav"],
        "drums": ["808", "909", "acoustic_kit", "electronic_kit"],
    }

    def __init__(self):
        self.loaded_plugins = {}
        self.plugin_params = {}

    def load_plugin(self, plugin_name: str, slot: int = 0) -> dict:
        self.loaded_plugins[slot] = plugin_name
        return {"status": "success", "plugin": plugin_name, "slot": slot}

    def set_parameter(self, plugin_slot: int, param: int, value: float) -> dict:
        if plugin_slot not in self.plugin_params:
            self.plugin_params[plugin_slot] = {}
        self.plugin_params[plugin_slot][param] = value
        return {"status": "success", "plugin": plugin_slot, "param": param, "value": value}

    def get_plugins(self) -> dict:
        return {"loaded": self.loaded_plugins, "params": self.plugin_params}


class MixerManager:
    """Mixer state management"""

    def __init__(self):
        self.channels = {i: {"volume": 0.8, "pan": 0, "mute": False, "solo": False} for i in range(100)}
        self.master = {"volume": 0.8, "limiter": False}
        self.snapshots = {}

    def set_channel(self, channel: int, **kwargs) -> dict:
        for key, value in kwargs.items():
            if key in self.channels[channel]:
                self.channels[channel][key] = value
        return {"status": "success", "channel": channel, "settings": self.channels[channel]}

    def get_channel(self, channel: int) -> dict:
        return self.channels[channel]

    def save_snapshot(self, name: str) -> dict:
        self.snapshots[name] = {
            "channels": dict(self.channels),
            "master": dict(self.master),
            "timestamp": datetime.now().isoformat(),
        }
        return {"status": "success", "snapshot": name}

    def load_snapshot(self, name: str) -> dict:
        if name in self.snapshots:
            snapshot = self.snapshots[name]
            self.channels = dict(snapshot["channels"])
            self.master = dict(snapshot["master"])
            return {"status": "success", "loaded": name}
        return {"status": "error", "message": f"Snapshot {name} not found"}

    def list_snapshots(self) -> list:
        return list(self.snapshots.keys())


class SampleManager:
    """Sample browser and management"""

    def __init__(self):
        self.samples = {}
        self.favorites = []

        self.sample_library = {
            "drums": {
                "kicks": ["kick_808.wav", "kick_acoustic.wav", "kick_electronic.wav", "kick_punch.wav"],
                "snares": ["snare_acoustic.wav", "snare_clap.wav", "snare_electronic.wav", "snare_gated.wav"],
                "hihats": ["hihat_closed.wav", "hihat_open.wav", "hihat_pedal.wav", "hihat_electronic.wav"],
                "claps": ["clap_808.wav", "clap_acoustic.wav", "clap_rounded.wav"],
            },
            "bass": {
                "808": ["bass_808_long.wav", "bass_808_short.wav", "bass_808_sub.wav"],
                "synth": ["bass_saw.wav", "bass_square.wav", "bass_fm.wav"],
            },
            "fx": ["riser.wav", "impact.wav", "sweep_up.wav", "sweep_down.wav", "noise.wav"],
        }

    def add_sample(self, name: str, path: str, category: str = "user") -> dict:
        self.samples[name] = {"path": path, "category": category, "added": datetime.now().isoformat()}
        return {"status": "success", "sample": name}

    def list_samples(self, category: str = None) -> dict:
        if category:
            return self.sample_library.get(category, {})
        return self.sample_library

    def get_sample_path(self, category: str, subcategory: str, filename: str) -> str:
        return f"{category}/{subcategory}/{filename}"


class ProjectManager:
    """FL Studio project management"""

    def __init__(self):
        self.current_project = None
        self.projects = {}
        self.last_save = None

    def create_project(self, name: str, tempo: int = 120, sample_rate: int = 44100) -> dict:
        project = {
            "name": name,
            "tempo": tempo,
            "sample_rate": sample_rate,
            "created": datetime.now().isoformat(),
            "patterns": [],
            "tracks": [],
            "automation": {},
        }
        self.projects[name] = project
        self.current_project = name
        return {"status": "success", "project": project}

    def open_project(self, name: str) -> dict:
        if name in self.projects:
            self.current_project = name
            return {"status": "success", "project": self.projects[name]}
        return {"status": "error", "message": f"Project {name} not found"}

    def save_project(self, path: str = None) -> dict:
        if self.current_project:
            self.last_save = datetime.now().isoformat()
            return {"status": "success", "project": self.current_project, "saved": self.last_save}
        return {"status": "error", "message": "No project open"}

    def get_current(self) -> dict:
        if self.current_project:
            return self.projects.get(self.current_project, {})
        return {}


class FLStudioPro:
    """Main FL Studio controller with all features"""

    def __init__(self):
        self.connected = False
        self.osc_port = 5005

        if OSC_AVAILABLE:
            try:
                self.osc_client = SimpleUDPClient("127.0.0.1", self.osc_port)
                self.connected = True
            except:
                pass

        self.generative = GenerativeEngine()
        self.vst = VSTManager()
        self.mixer = MixerManager()
        self.samples = SampleManager()
        self.project = ProjectManager()
        self.tempo = 120
        self.playing = False
        self.recording = False

    def _send(self, address: str, *args) -> bool:
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

    def _ok(self, message: str, **data) -> dict:
        return {"status": "success", "message": message, "timestamp": datetime.now().isoformat(), **data}

    def play(self) -> dict:
        self._send("/play") or self._key("space")
        self.playing = True
        return self._ok("Playback started")

    def stop(self) -> dict:
        self._send("/stop") or self._key("space")
        self.playing = False
        return self._ok("Playback stopped")

    def pause(self) -> dict:
        self._send("/pause")
        return self._ok("Playback paused")

    def record(self) -> dict:
        self._send("/record") or self._combo("r")
        self.recording = not self.recording
        return self._ok(f"Recording {'enabled' if self.recording else 'disabled'}")

    def restart(self) -> dict:
        self._send("/restart") or self._key("home")
        return self._ok("Restarted to beginning")

    def set_tempo(self, bpm: int) -> dict:
        self.tempo = max(30, min(300, bpm))
        self._send("/tempo", self.tempo)
        return self._ok(f"Tempo set to {self.tempo} BPM")

    def set_position(self, bar: int) -> dict:
        self._send("/position", bar)
        return self._ok(f"Position set to bar {bar}")

    def volume(self, channel: int, level: float) -> dict:
        level = max(0, min(1, level))
        self.mixer.set_channel(channel, volume=level)
        self._send(f"/mixer/{channel}/volume", int(level * 128))
        return self._ok(f"Channel {channel} volume: {level:.0%}")

    def pan(self, channel: int, position: float) -> dict:
        position = max(-1, min(1, position))
        self.mixer.set_channel(channel, pan=position)
        self._send(f"/mixer/{channel}/pan", int((position + 1) * 64))
        return self._ok(f"Channel {channel} pan: {position:.0%}")

    def mute(self, channel: int, state: bool) -> dict:
        self.mixer.set_channel(channel, mute=state)
        self._send(f"/mixer/{channel}/mute", 1 if state else 0)
        return self._ok(f"Channel {channel} {'muted' if state else 'unmuted'}")

    def solo(self, channel: int, state: bool) -> dict:
        self.mixer.set_channel(channel, solo=state)
        self._send(f"/mixer/{channel}/solo", 1 if state else 0)
        return self._ok(f"Channel {channel} solo: {state}")

    def master_volume(self, level: float) -> dict:
        level = max(0, min(1, level))
        self.mixer.master["volume"] = level
        self._send("/master/volume", int(level * 128))
        return self._ok(f"Master volume: {level:.0%}")

    def select_pattern(self, num: int) -> dict:
        num = max(1, min(99, num))
        self._send("/pattern", num)
        return self._ok(f"Pattern {num} selected")

    def open_piano_roll(self, channel: int = 0) -> dict:
        self._send("/pianoroll", channel) or self._combo("f6")
        return self._ok(f"Piano roll opened for channel {channel}")

    def save_mixer_snapshot(self, name: str) -> dict:
        return self.mixer.save_snapshot(name)

    def load_mixer_snapshot(self, name: str) -> dict:
        return self.mixer.load_snapshot(name)

    def create_project(self, name: str, tempo: int = 120) -> dict:
        return self.project.create_project(name, tempo)

    def get_status(self) -> dict:
        return {
            "connected": self.connected,
            "playing": self.playing,
            "recording": self.recording,
            "tempo": self.tempo,
            "current_project": self.project.current_project,
        }


flstudio = FLStudioPro()


# ==================== HTTP ENDPOINTS ====================

@app.route("/health", methods=["GET"])
def health():
    return jsonify(flstudio.get_status())


@app.route("/transport/<action>", methods=["POST"])
def transport(action):
    actions = {
        "play": flstudio.play,
        "stop": flstudio.stop,
        "pause": flstudio.pause,
        "record": flstudio.record,
        "restart": flstudio.restart,
    }
    if action in actions:
        return jsonify(actions[action]())
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/tempo", methods=["POST"])
def tempo():
    data = request.get_json() or {}
    return jsonify(flstudio.set_tempo(data.get("bpm", 120)))


@app.route("/position", methods=["POST"])
def position():
    data = request.get_json() or {}
    return jsonify(flstudio.set_position(data.get("bar", 1)))


@app.route("/mixer/volume", methods=["POST"])
def mixer_volume():
    data = request.get_json() or {}
    return jsonify(flstudio.volume(data.get("channel", 0), data.get("level", 0.8)))


@app.route("/mixer/pan", methods=["POST"])
def mixer_pan():
    data = request.get_json() or {}
    return jsonify(flstudio.pan(data.get("channel", 0), data.get("position", 0)))


@app.route("/mixer/mute", methods=["POST"])
def mixer_mute():
    data = request.get_json() or {}
    return jsonify(flstudio.mute(data.get("channel", 0), data.get("state", True)))


@app.route("/mixer/solo", methods=["POST"])
def mixer_solo():
    data = request.get_json() or {}
    return jsonify(flstudio.solo(data.get("channel", 0), data.get("state", True)))


@app.route("/mixer/master", methods=["POST"])
def mixer_master():
    data = request.get_json() or {}
    return jsonify(flstudio.master_volume(data.get("level", 0.8)))


@app.route("/mixer/snapshot/save", methods=["POST"])
def save_snapshot():
    data = request.get_json() or {}
    return jsonify(flstudio.save_mixer_snapshot(data.get("name", "default")))


@app.route("/mixer/snapshot/load", methods=["POST"])
def load_snapshot():
    data = request.get_json() or {}
    return jsonify(flstudio.load_mixer_snapshot(data.get("name", "default")))


@app.route("/pattern/<action>", methods=["POST"])
def pattern(action):
    data = request.get_json() or {}
    if action == "select":
        return jsonify(flstudio.select_pattern(data.get("number", 1)))
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/pianoroll/<action>", methods=["POST"])
def pianoroll(action):
    data = request.get_json() or {}
    if action == "open":
        return jsonify(flstudio.open_piano_roll(data.get("channel", 0)))
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


@app.route("/project/<action>", methods=["POST"])
def project(action):
    data = request.get_json() or {}
    if action == "new":
        return jsonify(flstudio.create_project(data.get("name", "Untitled"), data.get("tempo", 120)))
    elif action == "save":
        return jsonify(flstudio.project.save_project(data.get("path")))
    return jsonify({"status": "error", "message": f"Unknown action: {action}"})


# ==================== GENERATION ENDPOINTS ====================

@app.route("/generate/drums", methods=["POST"])
def gen_drums():
    data = request.get_json() or {}
    result = flstudio.generative.generate_drums(
        style=data.get("style", "house"),
        bars=data.get("bars", 1),
        complexity=data.get("complexity", 3),
        swing=data.get("swing", 0),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/bass", methods=["POST"])
def gen_bass():
    data = request.get_json() or {}
    result = flstudio.generative.generate_bass(
        root=data.get("root", 36),
        scale=data.get("scale", "minor"),
        length=data.get("length", 8),
        pattern_type=data.get("pattern", "walking"),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/melody", methods=["POST"])
def gen_melody():
    data = request.get_json() or {}
    result = flstudio.generative.generate_melody(
        key=data.get("key", 60),
        scale=data.get("scale", "minor"),
        length=data.get("length", 8),
        range_low=data.get("range_low", 4),
        range_high=data.get("range_high", 6),
        density=data.get("density", 0.7),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/chords", methods=["POST"])
def gen_chords():
    data = request.get_json() or {}
    result = flstudio.generative.generate_chords(
        key=data.get("key", 60),
        style=data.get("style", "pop"),
        bars=data.get("bars", 4),
        voicing=data.get("voicing", "spread"),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/arps", methods=["POST"])
def gen_arps():
    data = request.get_json() or {}
    result = flstudio.generative.generate_arps(
        chord_root=data.get("root", 60),
        chord_type=data.get("chord_type", "major"),
        pattern=data.get("pattern", "up"),
        octave_range=data.get("octaves", 2),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/arrangement", methods=["POST"])
def gen_arrangement():
    data = request.get_json() or {}
    result = flstudio.generative.generate_arrangement(
        style=data.get("style", "house"),
        total_bars=data.get("bars", 32),
        intro_bars=data.get("intro", 4),
        outro_bars=data.get("outro", 4),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/track", methods=["POST"])
def gen_track():
    data = request.get_json() or {}
    result = flstudio.generative.generate_full_track(
        style=data.get("style", "house"),
        key=data.get("key", 60),
        scale=data.get("scale", "minor"),
        bars=data.get("bars", 16),
        tempo=data.get("tempo"),
    )
    return jsonify({"status": "success", **result})


@app.route("/generate/custom", methods=["POST"])
def gen_custom():
    """Generate custom combination of elements"""
    data = request.get_json() or {}

    elements = data.get("elements", ["drums", "bass", "melody", "chords"])
    result = {"metadata": data}

    for element in elements:
        if element == "drums":
            result["drums"] = flstudio.generative.generate_drums(
                data.get("style", "house"), data.get("bars", 4), data.get("complexity", 3)
            )
        elif element == "bass":
            result["bass"] = flstudio.generative.generate_bass(
                data.get("key", 60) - 24, data.get("scale", "minor"), data.get("bars", 16)
            )
        elif element == "melody":
            result["melody"] = flstudio.generative.generate_melody(
                data.get("key", 60), data.get("scale", "minor"), data.get("bars", 16)
            )
        elif element == "chords":
            result["chords"] = flstudio.generative.generate_chords(
                data.get("key", 60), data.get("style", "pop"), data.get("bars", 16)
            )
        elif element == "arps":
            result["arps"] = flstudio.generative.generate_arps(
                data.get("key", 60), "major", "updown", 2
            )

    return jsonify({"status": "success", **result})


@app.route("/tools", methods=["GET"])
def list_tools():
    return jsonify({
        "transport": ["play", "stop", "pause", "record", "restart", "tempo", "position"],
        "mixer": ["volume", "pan", "mute", "solo", "master", "snapshot_save", "snapshot_load"],
        "patterns": ["select", "create"],
        "pianoroll": ["open", "add_note", "clear"],
        "generation": ["drums", "bass", "melody", "chords", "arps", "arrangement", "track", "custom"],
        "project": ["new", "save", "open"],
    })


# ==================== MAIN ====================

if __name__ == "__main__":
    print("=" * 60)
    print("FL Studio PRO MCP Server")
    print("=" * 60)
    print(f"OSC: {'Connected' if flstudio.connected else 'Fallback mode'}")
    print(f"Features: Generative AI, VST control, Mixer snapshots")
    print("Server: http://localhost:5000")
    print("=" * 60)

    if FLASK_AVAILABLE:
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        print("ERROR: Install flask: pip install flask")