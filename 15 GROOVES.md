---
tags: [groove, swing, timing]
---

# 🎚️ Groove Extraction & Application

## Available Grooves

| Groove | Swing | Velocity | Character |
|--------|-------|----------|-----------|
| basic_swing | 0.55 | 0 | Standard swing |
| jazzy_swing | 0.60 | 10 | Classic jazz |
| lofi_swing | 0.52 | -5 | Lo-fi feel |
| house_groove | 0.50 | 5 | Straight house |
| shuffle | 0.58 | 8 | 12/8 feel |
| bounce | 0.56 | 3 | Upbeat bounce |
| breakbeat | 0.50 | 15 | Broken feel |
| hiphop_groove | 0.52 | 0 | Hip hop pocket |

## Apply Groove

```json
POST /groove/apply
{
  "notes": [
    {"midi": 36, "velocity": 100, "timing": 0},
    {"midi": 38, "velocity": 90, "timing": 1},
    ...
  ],
  "groove": "jazzy_swing"
}
```

## Extract Groove

```json
POST /groove/extract
{"notes": [...]}

Response:
{
  "extracted_groove": "basic_swing",
  "confidence": 0.75,
  "swing_estimate": 0.52,
  "velocity_offset_estimate": -5
}
```

## Create Custom Groove

```json
POST /groove/create
{
  "name": "my_groove",
  "swing": 0.58,
  "velocity": 5,
  "timing": [0, 0.1, 0, -0.1, 0, 0.1, 0, -0.1]
}
```

## List Grooves

```json
GET /groove/list

Response:
{"grooves": [...]}
```