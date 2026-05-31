---
tags: [bass, patterns]
---

# 🎸 Bass Patterns

## Pattern Types

| Pattern | Character |
|---------|-----------|
| `walking` | Classic walking bass |
| `rolling` | Continuous 16th notes |
| `driving` | Punchy, relentless |
| `syncopated` | Off-beat emphasis |
| `plucks` | Staccato plucks |
| `offbeat` | Off-beat notes |
| `drone` | Sustained root |
| `groove` | Funky groove |
| `figure` | Melodic figure |
| `wobble` | Dubstep wobble |
| `slap` | Slap bass |
| `finger` | Fingerstyle |

## Parameters

```json
{
  "root": 36,
  "scale": "minor",
  "length": 16,
  "pattern": "rolling"
}
```

- `root`: MIDI note (36 = C2)
- `scale`: any scale from [[02 SCALES]]
- `length`: number of beats
- `pattern`: from table above

## Octave Shift

Use `octave_shift` to move bass up/down octaves:
- 0 = C2 (root)
- 1 = C3 (one octave up)
- -1 = C1 (one octave down)