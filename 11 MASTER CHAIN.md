---
tags: [master, loudness, mixing]
---

# 📊 Master Chain & Loudness

## Processors

Available:
- `eq` - Parametric EQ
- `compressor` - Dynamics
- `limiter` - Brick wall
- `multiband` - Band compression
- `clipper` - Soft clip
- `maximizer` - Loudness maximizer

## Style Suggestions

```json
POST /master/suggest
{"style": "edm"}

Response:
{
  "eq": {"low": 3, "mid": 1, "high": 2},
  "compressor": {"threshold": -20, "ratio": 3, "makeup": 5},
  "limiter": {"ceiling": -0.5}
}
```

## Style-Specific Settings

| Style | Comp Ratio | Limiter Ceiling | Target |
|-------|------------|-----------------|--------|
| pop | 4:1 | -0.8 dB | -14 LUFS |
| hiphop | 6:1 | -1.0 dB | -14 LUFS |
| edm | 3:1 | -0.5 dB | -14 LUFS |
| lofi | 2:1 | -3.0 dB | -16 LUFS |
| rock | 4:1 | -0.8 dB | -12 LUFS |

## Loudness Targets

- **Streaming**: -14 LUFS (Spotify, Apple, YouTube)
- **Broadcast**: -24 LUFS (EBU R128)
- **CD**: -9 LUFS (Red Book)

## Limiter Settings

```python
master.configure_limiter(
    threshold=-0.5,
    release=0.3,
    ceiling=-0.3
)
```

## Calculate Loudness

```python
result = master.calculate_loudness(
    integrated=-12.5,
    true_peak=-1.2
)
# Returns gain adjustment needed
```