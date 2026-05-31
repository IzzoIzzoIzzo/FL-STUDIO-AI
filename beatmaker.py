"""
FL STUDIO AI - Easy Beat Making CLI
=====================================
Simple command-line tool to generate beats
Can be called from Claude Code, OpenCode, or any AI assistant

Usage:
  python beatmaker.py generate trap
  python beatmaker.py make "trap beat 150 bpm"
  python beatmaker.py serve

Or use as a Python module:
  from beatmaker import generate_track
  track = generate_track(style="trap", tempo=150)
"""

import json
import random
import sys
import time
from datetime import datetime
from typing import Any, Optional

# Core music generation
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "pentatonic": [0, 2, 5, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
}

DRUM_STYLES = {
    "trap": [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    "house": [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
    "hiphop": [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    "techno": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    "dnb": [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    "dubstep": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    "lofi": [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "ambient": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

TEMPO_RANGES = {
    "trap": (140, 180),
    "house": (118, 130),
    "hiphop": (80, 110),
    "techno": (128, 150),
    "dnb": (160, 180),
    "dubstep": (138, 160),
    "lofi": (70, 90),
    "ambient": (60, 100),
}


def midi_to_note(midi: int) -> str:
    """Convert MIDI note to name"""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return f"{notes[midi % 12]}{(midi // 12) - 1}"


def generate_notes(root: int, scale: str, count: int) -> list:
    """Generate notes in a scale"""
    intervals = SCALES.get(scale, SCALES["minor"])
    notes = []
    for i in range(count):
        interval = intervals[i % len(intervals)]
        octave = i // len(intervals)
        note = root + interval + (octave * 12)
        if note <= 127:
            notes.append(note)
    return notes


def generate_drums(style: str = "trap", bars: int = 1) -> list:
    """Generate drum pattern"""
    pattern = DRUM_STYLES.get(style, DRUM_STYLES["trap"])
    pattern = pattern * bars

    notes = []
    for step, hit in enumerate(pattern):
        if hit:
            # Kick on 1, 5, 9, 13
            if step % 4 == 0:
                notes.append({"midi": 36, "velocity": 120, "start": step * 0.25, "track": "kick"})
            # Snare on 4, 12
            elif step % 8 == 4:
                notes.append({"midi": 38, "velocity": 100, "start": step * 0.25, "track": "snare"})
            # 808 for trap
            elif style == "trap" and step % 8 == 2:
                notes.append({"midi": 36, "velocity": 110, "start": step * 0.25, "track": "808"})

        # Hihat on every step for some styles
        if style in ["techno", "dnb"]:
            notes.append({"midi": 42, "velocity": 70, "start": step * 0.25, "track": "hihat"})

    # Add hihats for other styles
    if style not in ["techno", "dnb"]:
        for i in range(bars * 16):
            if i % 2 == 0:
                notes.append({"midi": 42, "velocity": 70, "start": i * 0.25, "track": "hihat"})

    return notes


def generate_bass(root: int = 36, scale: str = "minor", bars: int = 8) -> list:
    """Generate bass line"""
    notes = []
    scale_notes = generate_notes(root, scale, bars * 2)

    for i in range(bars):
        # Root on 1, octave on 5
        if i % 4 == 0:
            note = root
        elif i % 4 == 2:
            note = root + 12 if scale == "major" else scale_notes[min(2, len(scale_notes)-1)]
        else:
            note = scale_notes[min(i, len(scale_notes)-1)] if scale_notes else root

        notes.append({
            "midi": note,
            "velocity": 100,
            "start": i * 4,
            "duration": 2,
            "track": "bass"
        })

    return notes


def generate_melody(root: int = 60, scale: str = "minor", bars: int = 8) -> list:
    """Generate melody"""
    notes = []
    scale_notes = generate_notes(root + 12, scale, bars * 8)

    current = 60
    for i in range(bars * 4):
        if random.random() > 0.4:
            # Move in scale
            direction = random.choice([-1, -1, 0, 1, 1, 2])
            idx = scale_notes.index(current) if current in scale_notes else 0
            new_idx = max(0, min(len(scale_notes) - 1, idx + direction))
            current = scale_notes[new_idx]

            notes.append({
                "midi": current,
                "velocity": 80 + random.randint(0, 30),
                "start": i,
                "duration": random.choice([0.5, 1, 1.5]),
                "track": "melody"
            })

    return notes


def generate_chords(root: int = 60, style: str = "pop", bars: int = 8) -> list:
    """Generate chord progression"""
    progressions = {
        "pop": [0, 7, 9, 5],  # I, V, vi, IV
        "sad": [0, 9, 3, 7],  # i, VI, III, VII
        "trap": [0, 5, 10, 3],  # im, IVm, VII, III
        "jazz": [2, 7, 0, 9],  # IIm7, V7, Imaj7, VI7
    }

    offsets = progressions.get(style, progressions["pop"])
    intervals = [0, 4, 7]  # Major triad

    notes = []
    for i in range(bars):
        chord_offset = offsets[i % len(offsets)]
        chord_root = root + chord_offset

        for j, interval in enumerate(intervals):
            notes.append({
                "midi": chord_root + interval + (12 if j == 2 else 0),
                "velocity": 70,
                "start": i * 4,
                "duration": 4,
                "track": "chords"
            })

    return notes


def generate_track(style: str = "house", tempo: int = 120, key: int = 60,
                   scale: str = "minor", bars: int = 16) -> dict:
    """Generate complete track"""

    # Auto-set tempo from style if not provided
    if tempo is None or tempo == 120:
        tempo_range = TEMPO_RANGES.get(style, (120, 130))
        tempo = random.randint(*tempo_range)

    drums = generate_drums(style, bars // 4)
    bass = generate_bass(key - 24, scale, bars)
    melody = generate_melody(key, scale, bars)
    chords = generate_chords(key, style, bars)

    return {
        "metadata": {
            "style": style,
            "tempo": tempo,
            "key": key,
            "key_name": midi_to_note(key),
            "scale": scale,
            "bars": bars,
            "generated_at": datetime.now().isoformat(),
        },
        "tracks": {
            "drums": {"notes": drums, "count": len(drums)},
            "bass": {"notes": bass, "count": len(bass)},
            "melody": {"notes": melody, "count": len(melody)},
            "chords": {"notes": chords, "count": len(chords)},
        },
        "total_notes": len(drums) + len(bass) + len(melody) + len(chords),
    }


def format_for_fl_studio(track: dict) -> str:
    """Format track data for easy copy to FL Studio"""
    output = []
    output.append(f"=== TRACK: {track['metadata']['style'].upper()} | {track['metadata']['tempo']} BPM | {midi_to_note(track['metadata']['key'])} {track['metadata']['scale']} ===")
    output.append(f"Total notes: {track['total_notes']}")
    output.append("")

    # Show drum pattern
    output.append("DRUMS:")
    for note in track["tracks"]["drums"]["notes"][:8]:
        output.append(f"  {note['track'].upper()}: MIDI {note['midi']} @ beat {note['start']}")
    if len(track["tracks"]["drums"]["notes"]) > 8:
        output.append(f"  ... +{len(track['tracks']['drums']['notes']) - 8} more")

    # Show bass
    output.append("\nBASS:")
    for note in track["tracks"]["bass"]["notes"][:4]:
        output.append(f"  {midi_to_note(note['midi'])} (MIDI {note['midi']}) @ bar {note['start']//4 + 1}")

    # Show melody
    output.append("\nMELODY:")
    for note in track["tracks"]["melody"]["notes"][:4]:
        output.append(f"  {midi_to_note(note['midi'])} (MIDI {note['midi']}) @ beat {note['start']}")

    # Show chords
    output.append("\nCHORDS:")
    for note in track["tracks"]["chords"]["notes"][:4]:
        output.append(f"  {midi_to_note(note['midi'])} @ bar {note['start']//4 + 1}")

    return "\n".join(output)


def format_midi_data(track: dict) -> str:
    """Format as MIDI data for FL Studio"""
    lines = []

    for track_name, track_data in track["tracks"].items():
        lines.append(f"\n[{track_name.upper()}]")
        for note in track_data["notes"]:
            # FL Studio piano roll format
            lines.append(f"{note['midi']},{note['velocity']},{note.get('start', 0):.2f},{note.get('duration', 1):.2f}")

    return "\n".join(lines)


# ==================== CLI ====================

def main():
    args = sys.argv[1:]

    if not args:
        print("FL STUDIO AI - Beat Maker CLI")
        print("=" * 50)
        print("Usage:")
        print("  python beatmaker.py generate <style> [tempo]")
        print("  python beatmaker.py make '<description>'")
        print("  python beatmaker.py serve")
        print("")
        print("Examples:")
        print("  python beatmaker.py generate trap")
        print("  python beatmaker.py generate house 128")
        print("  python beatmaker.py make 'dark trap beat 160 bpm in a minor'")
        return

    command = args[0]

    if command == "generate":
        style = args[1] if len(args) > 1 else "house"
        tempo = int(args[2]) if len(args) > 2 else 120
        bars = int(args[3]) if len(args) > 3 else 16

        track = generate_track(style=style, tempo=tempo, bars=bars)
        print(format_for_fl_studio(track))

    elif command == "make":
        desc = " ".join(args[1:]).lower() if len(args) > 1 else ""

        # Parse description
        style = "house"
        for s in DRUM_STYLES.keys():
            if s in desc:
                style = s
                break

        tempo = 120
        for word in desc.split():
            if word.isdigit():
                tempo = int(word)
                break

        bars = 16
        if "short" in desc:
            bars = 8
        elif "long" in desc:
            bars = 32

        track = generate_track(style=style, tempo=tempo, bars=bars)
        print(format_for_fl_studio(track))

    elif command == "serve":
        print("Starting MCP server on http://localhost:5000...")
        print("Use with Claude Code/OpenCode")
        from flstudio_mcp_server_v2 import app
        app.run(host="0.0.0.0", port=5000, debug=False)

    elif command == "export":
        style = args[1] if len(args) > 1 else "house"
        track = generate_track(style=style)
        print(format_midi_data(track))

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()