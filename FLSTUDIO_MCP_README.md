# FL Studio MCP - AI Beat Making Integration

## Quick Start

1. **Start FL Studio** (make sure it's running)
2. **Start the MCP Server**: Run `START_FLSTUDIO_MCP.bat`
3. **Use with Claude Code/OpenCode**: The MCP is now available at `http://localhost:5000`

## Installation

Required packages (already installed):
```
pip install python-osc pyautogui flask
```

## How It Works

The MCP server provides HTTP endpoints that AI assistants can call to:
- Control transport (play, stop, pause, record)
- Control mixer (volume, pan, mute, solo)
- Control patterns and piano roll
- **Generate music elements** (drums, bass, melody, chords, full tracks)

## Example AI Commands

### Transport Control
```
"FL Studio, play the beat"
"Stop the playback"
"Set tempo to 140 BPM"
"Jump to bar 8"

```

### Mixer Control
```
"Set channel 1 volume to 80%"
"Pan channel 3 to the left"
"Mute channel 2"
"Solo on channel 4"

```

### Pattern & Piano Roll
```
"Select pattern 3"
"Open piano roll for channel 1"
"Add a C4 note at beat 0, lasting 1 beat"
"Clear the piano roll"

```

### Generate Music (AI creates music for you!)
```
"Generate a trap drum pattern"
"Create a bass line in A minor, 8 beats"
"Generate a melody in G minor"
"Generate a chord progression in C major, 4 bars"
"Create a full house track in D minor, 8 bars"

```

### Generate with Specific Styles
```python
# Drums: basic, trap, house, techno, hiphop, lofi, dubstep, jungle
# Scales: major, minor, pentatonic, dorian, phrygian, lydian, mixolydian
# Chord styles: pop, jazz, cinematic, edm, soul, rock, blues, reggae
# Bass patterns: walking, drone, driving, syncopated, plucks, offbeat
```

## HTTP API Examples

```bash
# Check health
curl http://localhost:5000/health

# Start playback
curl -X POST http://localhost:5000/transport/play

# Set tempo
curl -X POST -H "Content-Type: application/json" -d '{"bpm": 140}' http://localhost:5000/tempo

# Generate trap drums
curl -X POST -H "Content-Type: application/json" -d '{"style": "trap", "bars": 2, "complexity": 4}' http://localhost:5000/generate/drums

# Generate full track
curl -X POST -H "Content-Type: application/json" -d '{"style": "house", "key": 60, "scale": "minor", "bars": 8}' http://localhost:5000/generate/track
```

## Using with Claude Code / OpenCode

### Option 1: Direct HTTP calls from Claude Code

Create a skill or use direct HTTP calls:

```python
import urllib.request
import json

def flstudio_call(endpoint, data=None):
    url = f"http://localhost:5000{endpoint}"
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                  headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

# Example: Generate and play a beat
result = flstudio_call("/generate/track", {"style": "trap", "key": 60, "scale": "minor", "bars": 8})
print(result)
```

### Option 2: Python Script Runner

```bash
python flstudio_client.py generate track
python flstudio_client.py tempo 140
```

### Option 3: Add to your agent prompts

```
You have access to FL Studio via MCP at localhost:5000.
Available tools:
- Transport: play, stop, pause, record, restart
- Mixer: volume, pan, mute, solo
- Generators: generate_drums, generate_bass, generate_melody, generate_chords, generate_track
- Piano roll: add_note, open_piano_roll, clear_piano_roll
- Patterns: select_pattern, create_pattern

Example: "Create a trap beat with 140 BPM"
```

## Generative Music Features

### Drum Generation
Returns full pattern with MIDI events ready to send to FL Studio:
- 8 drum types: kick, snare, hihat, clap, 808, perc, crash, ride
- Styles: trap, house, techno, hiphop, lofi, dubstep, jungle
- Complexity: 1-5 (adds more variations)
- Swing: 0-1 (adds groove)

### Bass Generation
- Root note: any MIDI note (36=C2)
- Scales: major, minor, pentatonic, blues
- Patterns: walking, drone, driving, syncopated, plucks, offbeat

### Melody Generation
- Key: any MIDI note (60=C4)
- Scales: major, minor, pentatonic, dorian, phrygian, lydian, mixolydian
- Octave range: configurable
- Rhythm density: controls note density

### Chord Progression
- Styles: pop, jazz, cinematic, edm, soul, rock, blues, reggae
- Voicings: root, spread, block, jazz, inversions
- Chord types: major, minor, dim, aug, 7, maj7, min7, 9

### Full Track Generation
Combines all elements into a complete structure:
- Intro, verse, chorus, outro arrangement
- Tempo, key, scale, style all configurable

## Troubleshooting

1. **Server won't start**: Make sure port 5000 is free
2. **FL Studio not responding**: Check if OSC is enabled in FL Studio (Options > General > OSC)
3. **Keyboard shortcuts not working**: Make sure FL Studio window is focused

## Future: AI Agent Beat Making

The long-term vision:
- AI agents can compose complete tracks
- Generate melodies based on mood/style
- Auto-arrange songs
- Learn from your preferences
- Create variations of existing beats

Currently: You can ask AI to generate patterns, then manually input into FL Studio.

## Files

- `flstudio_mcp_server.py` - Main MCP server
- `flstudio_client.py` - Python client library
- `flstudio_mcp_manifest.json` - Tool definitions
- `START_FLSTUDIO_MCP.bat` - Launch server