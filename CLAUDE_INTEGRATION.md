# FL STUDIO AI - Integration Guide for Claude Code / OpenCode

## Quick Start

### Option 1: MCP Server (Recommended for AI Integration)

1. Run `START_MCP_SERVER.bat` or:
   ```bash
   python flstudio_mcp_server_v2.py
   ```

2. Server runs at `http://localhost:5000`

3. Use in Claude Code/OpenCode by calling MCP tools

### Option 2: CLI Tool (Quick Generation)

```bash
# Generate a trap beat at 150 BPM
python beatmaker.py generate trap 150

# Generate house at 128 BPM
python beatmaker.py generate house 128

# Natural language
python beatmaker.py make "dark trap beat in a minor 160 bpm"
```

---

## Using with Claude Code / OpenCode

### MCP Tools Available

When the MCP server is running, you can ask Claude to:

#### Generate Complete Tracks
```
"Make a trap beat at 150 BPM in A minor"
"Create a house track at 128 BPM"
"Generate a lofi hiphop beat"
```

#### Generate Individual Elements
```
"Generate trap drums"
"Create a bass line in C minor"
"Make a melody in G major"
"Generate chord progression in D minor"
```

#### Control FL Studio
```
"Start playback in FL Studio"
"Stop playback"
"Toggle recording mode"
"Open piano roll"
```

#### Get Note Data
```
"Get the MIDI notes for the drums"
"Show me the bass line data"
```

---

## MCP Endpoint Details

### Base URL
```
http://localhost:5000
```

### Tools Endpoint
```
GET /mcp/tools
```

### Call Tool
```
POST /mcp/call
```

#### Example: Generate Track
```json
{
  "tool": "generate_track",
  "arguments": {
    "style": "trap",
    "tempo": 150,
    "key": 57,
    "scale": "minor",
    "bars": 16
  }
}
```

#### Example: Get Notes for FL Studio
```json
{
  "tool": "get_note_data",
  "arguments": {
    "track": "all"
  }
}
```

---

## CLI Commands Reference

### beatmaker.py

```bash
# Generate with style, tempo, bars
python beatmaker.py generate <style> [tempo] [bars]

# Styles: trap, house, hiphop, techno, dnb, dubstep, lofi, ambient
python beatmaker.py generate trap 150 16

# Natural language
python beatmaker.py make '<description>'

# Start MCP server
python beatmaker.py serve

# Export MIDI data
python beatmaker.py export <style>
```

---

## Output Formats

### Track Summary
```
=== TRACK: TRAP | 150 BPM | C4 minor ===
Total notes: 70

DRUMS:
  KICK: MIDI 36 @ beat 0.0
  HIHAT: MIDI 42 @ beat 0.0
  ...

BASS:
  C2 (MIDI 36) @ bar 1
  ...

MELODY:
  D#5 (MIDI 75) @ beat 0
  ...
```

### MIDI Data Format (for FL Studio piano roll)
```
[drums]
36,120,0.00,0.10
42,70,0.00,0.05
...

[bass]
36,100,0.00,2.00
...

[melody]
75,100,0.00,1.00
...

[chords]
60,70,0.00,4.00
...
```

---

## Troubleshooting

### MCP Server Not Starting
- Check if port 5000 is available
- Install dependencies: `pip install flask`

### Claude Not Connecting
- Ensure MCP server is running first
- Check server URL is correct: `http://localhost:5000`

### Keyboard Shortcuts Not Working
- Install pyautogui: `pip install pyautogui`
- Make sure FL Studio window is focused

---

## File Structure

```
AI FL STUDIO BUILD/
├── beatmaker.py              - CLI beat generator
├── flstudio_mcp_server_v2.py - MCP server for AI integration
├── START_MCP_SERVER.bat      - Launch MCP server
├── START_FLSTUDIO_AI_*.bat  - Full version launchers
├── flstudio_ai_supreme.py  - Supreme version (all features)
└── [documentation files]
```

---

## Quick Examples

### From Claude Code:
```
User: "Make a trap beat at 160 BPM"
Claude calls MCP: POST /mcp/call {tool: "generate_track", arguments: {style: "trap", tempo: 160}}
Returns: Track data with drums, bass, melody, chords

User: "Show me the bass notes"
Claude calls MCP: POST /mcp/call {tool: "get_midi_notes", arguments: {track_type: "bass"}}
Returns: MIDI note numbers, velocities, timings

User: "Start playback"
Claude calls MCP: POST /mcp/call {tool: "flstudio_play"}
FL Studio: Starts playing
```

### From Terminal:
```bash
python beatmaker.py generate trap 150 16
# Output: Complete track data ready for FL Studio
```