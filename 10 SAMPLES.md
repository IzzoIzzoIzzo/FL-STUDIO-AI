---
tags: [samples, library]
---

# 🎚️ Sample Library

## Categories

### Drums
- kicks (4 variants)
- snares (4 variants)
- hihats (3 variants)
- claps (3 variants)
- toms (3 variants)
- cymbals (3 variants)

### Bass
- 808 (3 variants)
- synth (4 variants)
- acoustic (3 variants)

### Synth
- leads (4 variants)
- pads (4 variants)
- plucks (3 variants)

### FX
- rises (3 variants)
- impacts (3 variants)
- fills (3 variants)

### Vocals
- phrases (2 variants)
- one_shots (2 variants)

## Search Samples

```json
POST /samples/search
{"query": "kick", "category": "drums"}

Response:
[
  {"name": "kick_808", "category": "drums", "tags": ["drums", "kicks"], ...},
  ...
]
```

## Get Random Sample

```json
POST /samples/random
{"category": "drums", "tags": ["kicks"]}
```

## Get by Style

```json
POST /samples/style
{"style": "trap"}

Response:
[{"name": "kick_808", ...}, {"name": "snare_clap", ...}, ...]
```

## Tagging

```python
samples.add_tag("kick_808", "hard")
samples.toggle_favorite("kick_808")
```