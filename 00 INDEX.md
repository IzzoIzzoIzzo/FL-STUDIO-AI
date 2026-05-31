---
alias: "AI FL Studio Build"
tags:
  - [flstudio, ai, music-production, mcp, beat-making]
  - project/active
---

# AI FL STUDIO BUILD - Complete Beat Making System

## Quick Start

### Basic Generation
```
python flstudio_ai.py generate trap 150 16
python flstudio_ai.py make "dark trap in a minor 160 bpm"
python flstudio_ai.py full trap 150 16
```

### Advanced Commands
```
python flstudio_ai.py arp up 60 minor      # Generate arpeggio
python flstudio_ai.py effects radio        # Effects chain
python flstudio_ai.py mixer balanced        # Mixer settings
python flstudio_ai.py patterns              # List patterns
python flstudio_ai.py minimal house         # Quick 4-bar
```

---

## All Files

### Main Toolkit
| File | Purpose |
|------|---------|
| `flstudio_ai.py` | **Complete toolkit** - All-in-one beat maker |
| `flstudio_mcp_server_v2.py` | MCP server for AI integration |
| `beatmaker.py` | Simple CLI beat generator |
| `START_MCP_SERVER.bat` | Launch MCP server |

### Full Servers (Progressive features)
- `START_FLSTUDIO_AI_SUPREME.bat` - v5.0 (all features)
- `START_FLSTUDIO_AI_ULTRA.bat` - v4.0
- `START_FLSTUDIO_AI_EXTREME.bat` - v3.0
- `START_FLSTUDIO_AI_PRO.bat` - v2.0

---

## CLI Commands

```bash
# Basic Generation
python flstudio_ai.py generate <style> [tempo] [bars]   # Generate track
python flstudio_ai.py make '<description>'              # Natural language
python flstudio_ai.py full <style> [tempo] [bars]        # Full production
python flstudio_ai.py minimal <style>                    # Quick 4-bar

# Advanced Features
python flstudio_ai.py arp <pattern> [root] [scale]      # Arpeggiator
python flstudio_ai.py effects <style>                   # Effects chain
python flstudio_ai.py mixer [style]                     # Mixer settings
python flstudio_ai.py patterns                          # List patterns
python flstudio_ai.py piano <style>                     # Piano roll data
python flstudio_ai.py export <style> [filename]         # Export MIDI
python flstudio_ai.py text <style>                      # Text output
python flstudio_ai.py serve                             # Start MCP server
```

### Styles Available
trap, house, hiphop, techno, dnb, dubstep, lofi, ambient

---

## MCP Server Tools

When running `START_MCP_SERVER.bat`:

1. **generate_track** - Complete track generation
2. **generate_drums** - Drums only
3. **generate_bass** - Bass only
4. **generate_melody** - Melody only
5. **generate_chords** - Chords only
6. **flstudio_play** - Start playback
7. **flstudio_stop** - Stop playback
8. **flstudio_record** - Toggle recording
9. **flstudio_new_pattern** - New pattern
10. **flstudio_piano_roll** - Open piano roll
11. **get_note_data** - All notes data
12. **get_midi_notes** - MIDI format

---

## Usage Examples

### CLI
```bash
# Basic generation
python flstudio_ai.py generate house 128 16

# Natural language
python flstudio_ai.py make "dark lofi beat in a minor"

# Piano roll data for manual entry
python flstudio_ai.py piano trap
```

### MCP with Claude
```
User: "Make a trap beat at 160 BPM"
Claude calls: POST /generate {"style": "trap", "tempo": 160}
```

---

## Documentation

- `CLAUDE_INTEGRATION.md` - Complete integration guide
- `QUICK REFERENCE.md` - Quick commands
- `01-23` - Feature documentation

## Features Included

- Drums (8 styles with patterns)
- Bass (6 patterns, multiple scales)
- Melody (8 scales, octave range)
- Chords (5 progressions, multiple keys)
- MIDI output for FL Studio
- Piano roll format
- CSV export
- Natural language parsing

Run `python flstudio_ai.py` without args for help.