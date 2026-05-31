---
tags: [genre, templates]
---

# 🎸 Genre Templates

## Available Genres (8 complete templates)

| Genre | Tempo Range | Character |
|-------|-------------|-----------|
| trap | 140-180 | Heavy 808s, fast hats |
| house | 120-130 | Four-on-floor, rolling |
| hiphop | 80-110 | Boom-bap, melodic |
| dubstep | 138-160 | Wobble bass, drops |
| dnb | 160-180 | Fast, breakbeat |
| lofi | 70-90 | Dusty, warm, vinyl |
| techno | 128-150 | Industrial, driving |
| ambient | 60-100 | Atmospheric, sparse |

## Get Template

```json
GET /genre/templates

Response:
[
  {"name": "Trap", "tempo": (140, 180), "signature": "4/4"},
  ...
]
```

## Generate from Template

```json
POST /genre/generate
{"genre": "trap"}

Returns complete track with:
- Mix settings per track
- Effect chains
- Instrument routing
- Drum/bass/chord patterns
```

## Template Contents

Each template includes:
- Tempo range
- Time signature
- Mix levels with EQ per track
- Effect settings
- Instrument routing
- Default patterns