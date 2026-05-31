---
tags: [api, http, endpoints]
---

# 📡 API Reference

## Base URL

```
http://localhost:5000
```

## Endpoints

### Generation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate/track` | Full track |
| POST | `/generate/drums` | Drum pattern |
| POST | `/generate/bass` | Bass line |
| POST | `/generate/melody` | Melody |
| POST | `/generate/chords` | Chord progression |
| POST | `/generate/arps` | Arpeggios |
| POST | `/generate/arrangement` | Song structure |

### Advanced
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate/polyrhythm` | Polyrhythm |
| POST | `/generate/binary` | Binary pattern |

### Control
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tempo` | Set tempo |
| POST | `/tempo/ramp` | Tempo ramp |
| POST | `/time_signature` | Time sig |
| POST | `/key/detect` | Detect key |

### Synthesis
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/synth/create_osc` | Oscillator |
| POST | `/synth/create_envelope` | Envelope |
| POST | `/synth/create_filter` | Filter |

### Effects
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/effects/compressor` | Compressor |
| POST | `/effects/reverb` | Reverb |
| POST | `/effects/delay` | Delay |
| GET | `/effects/chain` | Full chain |

### Export
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/export/midi` | Export MIDI |

### Info
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server status |
| GET | `/tools` | Available tools |