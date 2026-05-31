---
tags: [automation, mixer, curves]
---

# 🤖 Automation Builder

## Curve Types

| Type | Description |
|------|-------------|
| `linear` | Straight line |
| `ease_in` | Slow start, fast end |
| `ease_out` | Fast start, slow end |
| `ease_in_out` | Slow start/end, fast middle |
| `exponential` | Rapid change |
| `logarithmic` | Gradual change |
| `sigmoid` | S-curve |
| `bounce` | Bouncy feel |
| `zigzag` | Up-down pattern |

## Volume Automation

```json
POST /automation/volume
{
  "start": 0.3,
  "end": 0.8,
  "bars": 8,
  "curve": "ease_in_out"
}

Response:
[
  {"bar": 0.0, "value": 0.3, "type": "volume"},
  {"bar": 0.25, "value": 0.35, "type": "volume"},
  ...
]
```

## Pan Automation

```json
POST /automation/pan
{
  "start": -1,
  "end": 1,
  "bars": 4,
  "curve": "sigmoid"
}
```

## Filter Automation

```json
POST /automation/filter
{
  "cutoff_start": 200,
  "cutoff_end": 8000,
  "bars": 4,
  "curve": "sigmoid"
}
```

## Full Mixer Setup

```python
automation = AutomationBuilder()
full_auto = automation.create_full_mixer_automation([
    {"id": 0, "volume": {"start": 0, "end": 0.8, "curve": "ease_in"}},
    {"id": 1, "volume": {"start": 0, "end": 0.7, "curve": "linear"}},
    {"id": 2, "pan": {"start": -1, "end": 1, "curve": "linear"}},
], duration_bars=16)
```