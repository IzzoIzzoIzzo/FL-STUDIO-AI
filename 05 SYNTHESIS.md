---
tags: [synthesis, sound-design]
---

# 🔊 Synthesis Engine

## Oscillators

Waveforms available:
- `sine` - Pure tone
- `square` - Hollow sound
- `sawtooth` - Bright, rich
- `triangle` - Soft, mellow
- `pulse` - PWM sound
- `noise` - White noise

## Envelopes (ADSR)

```json
{
  "name": "amp",
  "attack": 0.01,
  "decay": 0.1,
  "sustain": 0.7,
  "release": 0.3
}
```

## Filters

Types:
- `lowpass` - Cut highs
- `highpass` - Cut lows
- `bandpass` - Cut both
- `notch` - Cut mid
- `peak` - Boost mid
- `lowshelf` - Shelf lows
- `highshelf` - Shelf highs

Parameters:
- `cutoff`: Frequency (Hz)
- `resonance`: Q factor (0-1)

## FM Synthesis

```json
{
  "carrier_ratio": 1,
  "modulator_ratio": 2,
  "modulation_index": 1
}
```

## Wavetables

- basic, square, saw, triangle, sine
- pulse_25, noise_white
- Morph between wavetables