# FL Studio AI Pro - Ultimate Beat Making Engine

## Version 2.0 - Production Ready

The most advanced AI-powered music production system for FL Studio integration.

---

## Quick Start

1. Run `START_FLSTUDIO_AI_PRO.bat`
2. Server runs on `http://localhost:5000`
3. Use client or HTTP calls to generate music

---

## What's New in 2.0

### Advanced Rhythm Engine
- **12+ Drum Styles**: trap, house, techno, dnb, hiphop, lofi, dubstep, garage, jungle, ambient, drift
- **Polyrhythms**: Generate complex polyrhythmic patterns (4:3, 5:4, 7:8, etc.)
- **Polymeter**: Different length patterns repeating
- **Binary Patterns**: Generate binary on/off patterns with hex output
- **Groove Templates**: shuffle, swing, bounce, lazy, jazzy
- **Humanization**: Add timing variations for organic feel
- **Swing Control**: 0-100% swing amount

### Sound Synthesis Engine
- **Oscillators**: sine, square, sawtooth, triangle, pulse, noise, sampler
- **ADSR Envelopes**: Full control over attack, decay, sustain, release
- **Filters**: lowpass, highpass, bandpass, notch, peak, lowshelf, highshelf
- **LFO Modulation**: Rate, depth, waveform, sync options

### FM & Wavetable Synthesis
- **FM Synthesis**: Carrier/modulator ratios, modulation index
- **Operator Creation**: Create custom FM operators
- **Algorithms**: Configure carrier/modulator routing
- **Wavetables**: basic, square, saw, triangle, sine, pulse, noise
- **Wavetable Morphing**: Smooth transitions between wavetables

### Melody & Harmony AI
- **15+ Scale Types**: major, minor, harmonic/minor, dorian, phrygian, lydian, mixolydian, pentatonic, blues, bebop, whole tone, etc.
- **Phrase-based Generation**: Generate coherent musical phrases
- **Contour Control**: random, ascending, descending, wave, arch, jumps, scalar
- **Variation System**: Generate variations of existing melodies
- **Auto-harmonization**: Add chords underneath melodies based on key

### Bass AI
- **12+ Patterns**: walking, rolling, driving, syncopated, plucks, offbeat, drone, groove, figure, wobble, slap, finger
- **Octave Shifting**: Move bass between octaves
- **Sync to Drums**: Rhythmically match drum patterns

### Chord AI
- **15+ Progression Styles**: pop, jazz, neo_soul, cinematic, edm, rock, blues, reggae, trap, lofi, boogie, spanish, vintage
- **Voicing Options**: root, spread, block, jazz, piano, guitar, inversions
- **Chord Extensions**: 7ths, 9ths, 11ths, 13ths, add9, sus4, etc.
- **Auto inversions**: Add chord inversions for smoother progressions

### Arpeggiator
- **10+ Patterns**: up, down, updown, downup, random, pingpong, roller, converge, diverge, random_up
- **Octave Range**: 1-4 octaves
- **Speed Options**: 16ths, 8ths, quarters, half, whole
- **Gate Control**: Note length percentage

### Arrangement Engine
- **10+ Song Structures**: simple, ab, abab, verse_chorus, electronic, trap, lofi, pop, ambient, minimal
- **Auto Section Sizing**: Intro, verse, chorus, bridge, outro with proper lengths
- **Full Song Builder**: Generate complete tracks with all elements

### Effects Chain
- **Parametric EQ**: Multi-band EQ with frequency, gain, Q control
- **Compressor**: Threshold, ratio, attack, release, makeup gain, knee
- **Reverb**: Size, decay, damping, wet/dry mix
- **Delay**: Time, feedback, wet/dry, optional sync

### Tempo & Time Control
- **Tempo Range**: 20-300 BPM
- **Time Signatures**: Any numerator/denominator (4/4, 3/4, 6/8, 5/4, 7/8, etc.)
- **Tempo Automation**: Create ramps with linear, exponential, logarithmic curves
- **Bar-level Control**: Get tempo at any bar point

### MIDI Export
- **Standard MIDI Files**: Export to .mid format
- **Multi-track Support**: Drums, bass, melody, chords, arps on separate channels
- **Tempo Preservation**: Export includes tempo data
- **Compatible**: Works with FL Studio, Ableton, Logic, Pro Tools

### Key Detection
- **Auto Key Detection**: Analyze notes to find key
- **Confidence Score**: Know how confident the detection is

---

## HTTP API Endpoints

### Generation

```bash
# Generate full track
POST /generate/track
{"style": "house", "key": 60, "scale": "minor", "bars": 32, "tempo": 128}

# Generate drums
POST /generate/drums
{"style": "trap", "bars": 2, "complexity": 4, "swing": 0.1, "humanize": 0.05}

# Generate bass
POST /generate/bass
{"root": 36, "scale": "minor", "length": 16, "pattern": "rolling"}

# Generate melody
POST /generate/melody
{"key": 60, "scale": "dorian", "length": 12, "contour": "ascending"}

# Generate chords
POST /generate/chords
{"key": 60, "style": "neo_soul", "bars": 8, "voicing": "jazz"}

# Generate arps
POST /generate/arps
{"root": 60, "chord_type": "major", "pattern": "updown", "octaves": 3}

# Generate arrangement structure
POST /generate/arrangement
{"style": "house", "bars": 32}
```

### Advanced Rhythm

```bash
# Polyrhythm (4 against 3)
POST /generate/polyrhythm
{"primary": 4, "secondary": 3, "steps": 12}

# Binary pattern
POST /generate/binary
{"bars": 1, "density": 0.5, "seed": 12345}
```

### Tempo Control

```bash
# Set tempo
POST /tempo
{"bpm": 140}

# Tempo ramp over 8 bars, 100 to 160 BPM, exponential curve
POST /tempo/ramp
{"start": 100, "end": 160, "bars": 8, "curve": "exponential"}

# Time signature
POST /time_signature
{"numerator": 4, "denominator": 4}
```

### Synthesis

```bash
# Create oscillator
POST /synth/create_osc
{"name": "lead", "waveform": "sawtooth", "frequency": 440}

# Create envelope
POST /synth/create_envelope
{"name": "amp", "attack": 0.01, "decay": 0.1, "sustain": 0.7, "release": 0.3}

# Create filter
POST /synth/create_filter
{"name": "main", "type": "lowpass", "cutoff": 2000, "resonance": 0.5}
```

### Effects

```bash
# Compressor
POST /effects/compressor
{"threshold": -20, "ratio": 4, "attack": 0.01, "release": 0.1}

# Reverb
POST /effects/reverb
{"size": 0.5, "decay": 2, "damping": 0.5, "wet": 0.3}

# Delay
POST /effects/delay
{"time": 0.5, "feedback": 0.3, "wet": 0.3}

# Get full chain
GET /effects/chain
```

### Export

```bash
# Export to MIDI
POST /export/midi
{"track_data": {...}, "filename": "beat.mid", "tempo": 120}
```

---

## Example Usage

### Generate a Trap Track

```json
{
  "style": "trap",
  "key": 60,
  "scale": "harmonic_minor",
  "bars": 16,
  "tempo": 142,
  "elements": {
    "drums": true,
    "bass": true,
    "melody": true,
    "chords": false,
    "arps": false
  }
}
```

### Generate a Lo-Fi Track

```json
{
  "style": "lofi",
  "key": 58,
  "scale": "pentatonic_minor",
  "bars": 12,
  "tempo": 80
}
```

### Generate Drum Pattern Only

```json
{
  "style": "dnb",
  "bars": 2,
  "complexity": 5,
  "swing": 0.15,
  "humanize": 0.1
}
```

---

## Style Reference

### Drum Styles
| Style | Tempo Range | Character |
|-------|-------------|-----------|
| trap | 140-180 | Hard 808s, fast hats |
| house | 120-130 | Four-on-floor, rolling hats |
| techno | 130-150 | Industrial, repetitive |
| dnb | 160-180 | Fast, breakbeat |
| hiphop | 80-110 | Boom-bap, laid back |
| lofi | 70-90 | Dusty, vinyl crackle |
| dubstep | 140-160 | Wobble bass, heavy |
| ambient | 60-100 | Sparse, atmospheric |

### Scale Reference
| Scale | Mood | Example |
|--------|------|---------|
| major | Happy, bright | C major |
| minor | Sad, dark | A minor |
| harmonic_minor | Exotic, dramatic | A harmonic minor |
| dorian | Jazzy, cool | D dorian |
| phrygian | Spanish, mysterious | E phrygian |
| mixolydian | Bluesy, rock | G mixolydian |
| pentatonic | General, safe | C pentatonic |
| blues | Classic blues | C blues |

---

## Files

- `flstudio_ai_pro.py` - Main server
- `flstudio_ai_client.py` - Python client with demo
- `START_FLSTUDIO_AI_PRO.bat` - Launcher
- `FLSTUDIO_AI_PRO_README.md` - This file

---

## Future Roadmap

- [ ] Direct FL Studio plugin integration
- [ ] Real-time audio analysis
- [ ] Machine learning model training on your patterns
- [ ] Cloud rendering
- [ ] Plugin presets for popular VSTs
- [ ] Stem export (separate tracks)
- [ ] Mixdown automation

---

## Support

The server accepts OSC commands to FL Studio when available, with keyboard shortcut fallback.

For issues or questions, check the HTTP response status in each API call.