---
tags: [scales, modes]
---

# 🎼 Custom Scales & Modes

## Generate Scale

### From Template
```json
POST /scales/generate
{"root": 60, "template": "whole_tone"}

Response:
{
  "root": 60,
  "intervals": [0, 2, 4, 6, 8, 10],
  "notes": [60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82],
  "note_names": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", ...]
}
```

### Custom Intervals
```json
POST /scales/generate
{"root": 60, "intervals": [0, 3, 5, 6, 8, 10]}
```

### Random Scale
```json
POST /scales/generate
{"root": 60, "num_notes": 7}
```

## Generate All Modes

```json
POST /scales/modes
{"root": 60}

Response:
{
  "root": 60,
  "modes": [
    {"mode": "Ionian", "intervals": [0, 2, 4, 5, 7, 9, 11], "notes": [...]},
    {"mode": "Dorian", "intervals": [0, 2, 3, 5, 7, 9, 10], "notes": [...]},
    ...
  ]
}
```

## Available Templates

- `ionian` - Major
- `dorian` - Minor (raised 6th)
- `phrygian` - Minor (flat 2)
- `lydian` - Major (raised 4)
- `mixolydian` - Major (flat 7)
- `aeolian` - Natural minor
- `locrian` - Diminished (flat 2, 5)
- `whole_tone` - Whole tone
- `diminished` - Diminished
- `chromatic` - All 12 notes
- ` bebop_dorian` - Bebop major