---
tags: [mix, templates]
---

# 🎛️ Mix Templates

## Available Templates

| Template | Drums | Bass | Melody | Chords | Lead | Character |
|----------|-------|------|--------|--------|------|-----------|
| flat | 0.8 | 0.7 | 0.6 | 0.5 | 0.6 | Neutral |
| drums_heavy | 1.0 | 0.6 | 0.5 | 0.4 | 0.5 | Drums forward |
| bass_heavy | 0.7 | 1.0 | 0.5 | 0.4 | 0.5 | Bass forward |
| ambient | 0.4 | 0.5 | 0.7 | 0.8 | 0.6 | Ethereal |
| rock | 0.9 | 0.8 | 0.7 | 0.6 | 0.8 | Balanced |
| electronic | 0.9 | 0.8 | 0.6 | 0.5 | 0.7 | Punchy |
| lofi_mix | 0.6 | 0.7 | 0.5 | 0.5 | 0.4 | Warm |
| warm | 0.7 | 0.7 | 0.7 | 0.7 | 0.7 | Even |

## Apply Template

```json
POST /mix/template
{"template": "bass_heavy"}

Response:
{
  "template": "bass_heavy",
  "settings": {
    "drums": {"volume": 0.7, "pan": 0, "mute": false},
    "bass": {"volume": 1.0, "pan": 0, "mute": false},
    ...
  }
}
```

## Volume Scale

- 0.0 - 1.0 (0% - 100%)
- Default is roughly -12dB to 0dB range