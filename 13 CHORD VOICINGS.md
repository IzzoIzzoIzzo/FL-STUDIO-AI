---
tags: [chords, voicings, voice-leading]
---

# 🎹 Chord Voicings & Voice Leading

## Voicing Types

| Type | Description | Best For |
|------|-------------|----------|
| `root` | Root position | Basic |
| `spread` | Triad spread | Pop |
| `block` | Block chords | Jazz |
| `jazz` | Jazz voicings | Ballads |
| `piano` | Piano style | Solo piano |
| `guitar` | Guitar style | Band context |
| `drop2` | Drop 2 voicing | 4-note chords |
| `drop3` | Drop 3 voicing | Big sound |
| `shell` | Shell voicing | Sparse arrangement |
| `quartal` | Stack of 4ths | Modern jazz |
| `clusters` | Close clusters | Avant-garde |
| `pad` | Full pad sound | Ambient |

## Generate Voicing

```json
POST /voicing/generate
{
  "root": 60,
  "chord_type": "major7",
  "voicing_type": "drop2"
}

Response:
{
  "root": 60,
  "chord_type": "major7",
  "voicing_type": "drop2",
  "voiced_notes": [60, 64, 67, 72],
  "note_names": ["C4", "E4", "G4", "C5"]
}
```

## Progression with Voice Leading

```json
POST /voicing/progression
{
  "progression": [
    {"root": 60, "type": "major7", "voicing": "jazz"},
    {"root": 65, "type": "minor7", "voicing": "spread"},
    {"root": 67, "type": "dominant7", "voicing": "shell"},
    {"root": 72, "type": "major7", "voicing": "block"}
  ]
}
```

Returns smooth voice leading between all chords.

## Voice Leading Metrics

- `total_movement` - Total semitones moved
- `average_movement` - Avg per voice
- `smoothness_score` - 0-100 (higher = smoother)
- `parallel_motion` - True if all voices move same direction
- `contrary_motion` - True if voices move opposite