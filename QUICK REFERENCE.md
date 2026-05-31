# ⚡ Quick Reference - FL Studio AI

## Run Server
```bash
START_FLSTUDIO_AI_PRO.bat        # v2.0 Pro
# or
python flstudio_ai_extreme.py     # v3.0 Extreme
```

## Quick Generate

```bash
# Full track
curl -X POST http://localhost:5000/generate/track -H "Content-Type: application/json" -d '{"style":"trap","key":60,"scale":"minor","bars":16,"tempo":140}'

# Drums only
curl -X POST http://localhost:5000/generate/drums -H "Content-Type: application/json" -d '{"style":"trap","bars":2}'

# Bass only
curl -X POST http://localhost:5000/generate/bass -H "Content-Type: application/json" -d '{"root":36,"scale":"minor","length":16}'
```

## Key Parameters

| Parameter | Values |
|-----------|--------|
| style | trap, house, techno, dnb, hiphop, lofi, dubstep, etc. |
| scale | major, minor, harmonic_minor, dorian, phrygian, etc. |
| pattern (bass) | walking, rolling, driving, syncopated, wobble, etc. |
| voicing | root, spread, block, jazz, piano, guitar |
| curve | linear, ease_in, ease_out, sigmoid, bounce |

## Common MIDI Notes

| Note | MIDI |
|------|------|
| C2 | 36 |
| C3 | 48 |
| C4 (Middle C) | 60 |
| C5 | 72 |
| Kick | 36 |
| Snare | 38 |
| Hihat | 42 |

## Styles & BPM

| Style | BPM Range |
|-------|-----------|
| lofi | 70-90 |
| hiphop | 80-110 |
| house | 118-130 |
| techno | 128-150 |
| dubstep | 138-160 |
| dnb | 160-180 |
| trap | 140-180 |

## Endpoints Summary

- `/generate/track` - Full track
- `/generate/drums` - Drums
- `/generate/bass` - Bass
- `/generate/melody` - Melody
- `/generate/chords` - Chords
- `/generate/arps` - Arpeggios
- `/generate/polyrhythm` - Polyrhythm
- `/analyze/key` - Key detection
- `/analyze/bpm` - BPM estimation
- `/automation/volume` - Volume automation
- `/samples/search` - Sample search
- `/master/suggest` - Master chain
- `/creative/variations` - Pattern variations
- `/creative/fills` - Drum fills
- `/generate/extreme` - Full extreme generation