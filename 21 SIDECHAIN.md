---
tags: [sidechain, routing]
---

# 🔗 Sidechain & Routing

## Create Sidechain

```json
POST /sidechain/create
{
  "source": "kick",
  "target": "bass",
  "amount": 0.7,
  "attack": 0.001,
  "release": 0.1
}
```

Parameters:
- `source`: Trigger track
- `target`: Compressed track
- `amount`: 0-1 (strength)
- `attack`: seconds
- `release`: seconds

## Create Send Route

```json
POST /sidechain/route
{
  "source": "drums",
  "target": "reverb",
  "level": 0.3
}
```

## Create Full Matrix

```json
POST /sidechain/matrix
{
  "tracks": ["drums", "bass", "melody"],
  "sends": ["reverb", "delay"]
}
```

## Get Status

```json
GET /sidechain/status

Response:
{
  "sidechains": {...},
  "routing": {...}
}
```