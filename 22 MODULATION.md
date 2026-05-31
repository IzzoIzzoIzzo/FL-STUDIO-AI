---
tags: [modulation, lfo]
---

# 🌊 Modulation & LFO

## LFO Shapes

| Shape | Character |
|-------|-----------|
| sine | Smooth, classic |
| triangle | Softer peaks |
| square | Pulsing |
| saw_up | Rising |
| saw_down | Falling |
| s&h | Random stepped |
| random | Smooth random |

## Create LFO

```json
POST /modulation/lfo
{
  "name": "filter_lfo",
  "rate": 0.5,
  "shape": "sine",
  "depth": 1,
  "offset": 0
}
```

Parameters:
- `rate`: Hz (or 1/n for beat sync)
- `shape`: from table above
- `depth`: 0-1 (intensity)
- `offset`: 0-1 (phase)

## Create Modulation

```json
POST /modulation/create
{
  "source": "lfo1",
  "target": "filter_cutoff",
  "amount": 1,
  "lfo": "filter_lfo"
}
```

## Get Waveform

```json
POST /modulation/waveform
{
  "lfo": "filter_lfo",
  "samples": 64
}

Response:
{"waveform": [0.0, 0.1, 0.3, ...]}
```