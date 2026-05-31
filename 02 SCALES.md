---
tags: [scales, melody, music-theory]
---

# 🎼 Scales & Keys

## Available Scales

| Scale | Mood | Intervals |
|-------|------|-----------|
| `major` | Happy | 0,2,4,5,7,9,11 |
| `minor` | Sad | 0,2,3,5,7,8,10 |
| `harmonic_minor` | Exotic | 0,2,3,5,7,8,11 |
| `melodic_minor` | Jazzy | 0,2,3,5,7,9,11 |
| `dorian` | Cool | 0,2,3,5,7,9,10 |
| `phrygian` | Spanish | 0,1,3,5,7,8,10 |
| `lydian` | Dreamy | 0,2,4,6,7,9,11 |
| `mixolydian` | Bluesy | 0,2,4,5,7,9,10 |
| `pentatonic_major` | Safe | 0,2,4,7,9 |
| `pentatonic_minor` | Rock | 0,3,5,7,10 |
| `blues` | Classic | 0,3,5,6,7,10 |
| `bebop_major` | Jazz | 0,2,4,5,7,9,10,11 |
| `whole_tone` | Dreamy | 0,2,4,6,8,10 |
| `chromatic` | All notes | 0-11 |
| `enigmatic` | Mystery | 0,1,4,6,8,10,11 |
| `hirajoshi` | Japanese | 0,2,3,7,8 |
| `in_sen` | Japanese | 0,1,5,7,10 |

## Melodic Contours

- `random` - Any direction
- `ascending` - Mostly up
- `descending` - Mostly down
- `wave` - Up and down
- `arch` - Up then down
- `jumps` - Large intervals
- `scalar` - Stepwise

## Usage

```json
{
  "key": 60,
  "scale": "dorian",
  "length": 8,
  "contour": "ascending"
}
```

Key = MIDI note (60 = C4)