---
tags: [effects, audio-processing]
---

# 🎛️ Effects Chain

## Compressor

```json
{
  "threshold": -20,
  "ratio": 4,
  "attack": 0.01,
  "release": 0.1,
  "makeup": 0
}
```

- Threshold: dB (-60 to 0)
- Ratio: 1:1 to 20:1
- Attack/Release: seconds

## Reverb

```json
{
  "size": 0.5,
  "decay": 2,
  "damping": 0.5,
  "wet": 0.3
}
```

- Size: 0-1 (room size)
- Decay: seconds
- Damping: 0-1 (high freq absorption)
- Wet: 0-1 (dry/wet mix)

## Delay

```json
{
  "time": 0.5,
  "feedback": 0.3,
  "wet": 0.3,
  "sync": false
}
```

- Time: seconds
- Feedback: 0-1
- Wet: dry/wet mix
- Sync: sync to tempo

## Parametric EQ

```json
{
  "bands": [
    {"freq": 100, "gain": 0, "q": 1},
    {"freq": 1000, "gain": 0, "q": 1},
    {"freq": 10000, "gain": 0, "q": 1}
  ]
}
```

- Freq: Hz (20-20000)
- Gain: dB (-12 to +12)
- Q: bandwidth (0.1-10)