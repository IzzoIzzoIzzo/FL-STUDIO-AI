---
tags: [export, mastering]
---

# 📤 Export Presets

## Available Presets

| Preset | Format | Sample Rate | Bit Depth | Target LUFS |
|--------|--------|------------|-----------|-------------|
| streaming | WAV | 44.1k | 24 | -14 |
| cd | WAV | 44.1k | 16 | -9 |
| broadcast | WAV | 48k | 24 | -24 |
| mp3_320 | MP3 | - | 320kbps | -14 |
| mp3_128 | MP3 | - | 128kbps | -16 |
| stems | WAV | 44.1k | 24 | -14 |
| midi_only | MIDI | - | - | - |
| stems_drum | WAV | 44.1k | 24 | -14 |
| stems_bass | WAV | 44.1k | 24 | -14 |

## Generate Export Config

```json
POST /export/config
{
  "preset": "stems",
  "project": {"name": "my_beat"}
}

Response:
{
  "preset": "stems",
  "output": {"filename": "my_beat_stems", "extension": "wav"},
  "processing": {"sample_rate": 44100, "bit_depth": 24},
  "loudness": {"target_lufs": -14, "true_peak_db": -1}
}
```

## List Presets

```json
GET /export/presets

Response:
{"presets": ["streaming", "cd", "broadcast", "mp3_320", "stems", ...]}
```