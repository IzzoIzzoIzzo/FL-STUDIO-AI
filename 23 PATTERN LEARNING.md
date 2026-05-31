---
tags: [ai, pattern, learning]
---

# 🧠 AI Pattern Learning

## Learn Pattern

```json
POST /learn/pattern
{
  "name": "my_trap_beat",
  "notes": [
    {"midi": 36, "velocity": 120, "timing": 0},
    {"midi": 38, "velocity": 100, "timing": 1},
    {"midi": 42, "velocity": 80, "timing": 0.5}
  ]
}

Response:
{
  "status": "success",
  "learned": "my_trap_beat",
  "features": {
    "rhythm_type": "sixteenth",
    "density": 0.75,
    "range": 24,
    "avg_velocity": 100,
    "pitch_center": 38
  }
}
```

## Generate from Learned

```json
POST /learn/generate
{
  "name": "my_trap_beat",
  "variation": 0.2,
  "length": 16
}
```

Returns pattern with variations applied.

## Find Similar

```json
POST /learn/similar
{
  "features": {
    "rhythm_type": "eighth",
    "density": 0.5,
    "range": 24
  },
  "threshold": 0.7
}

Response:
{"similar": [...]}
```

## List Learned Patterns

```json
GET /learn/list

Response:
{"patterns": ["my_trap_beat", "bass_line_1", ...]}
```