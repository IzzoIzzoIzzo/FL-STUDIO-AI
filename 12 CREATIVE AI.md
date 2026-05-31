---
tags: [creative, variations, fills]
---

# ✨ Creative AI

## Variations

Generate variations of patterns with transformations:

```json
POST /creative/variations
{
  "original": {"midi": [...]},
  "count": 4
}

Response:
[
  {"variation_id": 1, "transformations": ["pitch_shift_2", "velocity_mod"]},
  {"variation_id": 2, "transformations": ["timing_offset"]},
  ...
]
```

### Transformation Types

- `pitch_shift_{±n}` - Shift pitch
- `velocity_mod` - Vary velocity
- `timing_offset` - Shift timing

## Drum Fills

```json
POST /creative/fills
{"bars": 2, "style": "techno"}

Response:
[
  {"step": 0, "hit": 1, "velocity": 100},
  {"step": 5, "hit": 1, "velocity": 95},
  ...
]
```

### Fill Styles

- `simple` - Basic fills
- `triplet` - Triplet-based
- `linear` - Linear patterns
- `orchestral` - Complex
- `techno` - Driving
- `breakbeat` - Broken patterns

## Transitions

Suggest transitions between sections:

```python
transitions = creative.suggest_transitions("verse", "chorus")
# ["riser", "drum_fill", "filter_sweep"]
```

## Energy Analysis

```json
POST /creative/energy
{"track_data": {...}}

Response:
{
  "overall_energy": 0.75,
  "sections": [
    {"section": "drums", "energy": 0.9, "density": 45},
    {"section": "bass", "energy": 0.7, "density": 32},
    {"section": "melody", "energy": 0.6, "density": 18}
  ],
  "dynamic_range": "high"
}
```

### Energy Levels
- 0.0 - 0.3: Low/ambient
- 0.3 - 0.6: Medium
- 0.6 - 0.8: High
- 0.8 - 1.0: Maximum