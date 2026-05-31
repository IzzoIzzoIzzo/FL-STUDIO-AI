---
tags: [drums, rhythm, generation]
---

# 🥁 Drum Styles

## Available Styles

| Style | Tempo | Character |
|-------|-------|-----------|
| `trap` | 140-180 | Hard 808s, fast hats |
| `house` | 120-130 | Four-on-floor |
| `techno` | 130-150 | Industrial, repetitive |
| `dnb` | 160-180 | Fast, breakbeat |
| `hiphop` | 80-110 | Boom-bap |
| `lofi` | 70-90 | Dusty, vinyl |
| `dubstep` | 140-160 | Wobble bass |
| `garage` | 128-140 | UK Garage |
| `jungle` | 160-180 | Breakbeat |
| `ambient` | 60-100 | Sparse |
| `drift` | 120-160 | Drift/wave |
| `jungle_terror` | 140-160 | Trap + Dnb |

## Parameters

```json
{
  "style": "trap",
  "bars": 2,
  "complexity": 4,
  "swing": 0.1,
  "humanize": 0.05
}
```

- `complexity`: 1-5 (add variations)
- `swing`: 0-1 (groove amount)
- `humanize`: 0-1 (timing variations)

## Tracks Generated

- kick, kick2, kick3
- snare, snare2
- hihat, hihat_open
- clap, perc
- 808, sub
- ride, cowbell