---
tags: [audio, analysis, bpm, key]
---

# 🔍 Audio Analysis

## BPM Detection

### Style-based Estimation
```json
POST /analyze/bpm
{"style": "trap"}

Response:
{
  "min": 140, "max": 180, "typical": 150, "style": "trap"
}
```

### Styles & BPM Ranges

| Style | Min | Max | Typical |
|-------|-----|-----|----------|
| ambient | 60 | 90 | 75 |
| lofi | 70 | 90 | 80 |
| hiphop | 80 | 110 | 90 |
| house | 118 | 130 | 124 |
| techno | 128 | 150 | 135 |
| trance | 130 | 145 | 138 |
| dubstep | 138 | 160 | 140 |
| dnb | 160 | 180 | 170 |
| trap | 140 | 180 | 150 |
| electro | 120 | 140 | 128 |

## Key Detection

```json
POST /analyze/key
{"notes": [60, 62, 64, 67, 71, 74]}

Response:
{
  "root": 0,
  "mode": "major",
  "note": "C",
  "confidence": 0.85,
  "alternatives": [...]
}
```

## Track Analysis

```json
POST /creative/energy
{"track_data": {...}}

Response:
{
  "overall_energy": 0.75,
  "sections": [
    {"section": "drums", "energy": 0.9, "density": 45},
    {"section": "bass", "energy": 0.7, "density": 32}
  ],
  "dynamic_range": "high"
}
```

## Pitch Distribution

Returns distribution of notes across 12 pitch classes (0-11).