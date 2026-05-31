---
tags: [arrangement, structure]
---

# 🎼 Smart Arrangement

## Patterns

| Pattern | Sections | Best For |
|---------|----------|----------|
| classic | 8 | General pop |
| ab | 8 | Rock |
| verse_pre_chorus | 10 | Pop/rock |
| electronic_drop | 8 | EDM |
| trap_verse | 8 | Trap |
| minimal | 4 | Loops |
| ambient | 6 | Atmospheric |
| pop | 10 | Pop hits |

## Generate Arrangement

```json
POST /arrangement/smart
{"pattern": "trap_verse", "total_bars": 24}

Response:
{
  "pattern": "trap_verse",
  "total_bars": 24,
  "arrangement": [
    {"section": "intro", "start": 0, "bars": 4, "type": "structural"},
    {"section": "verse", "start": 4, "bars": 4, "type": "verse"},
    ...
  ],
  "duration_seconds": 360
}
```

## Section Types

- `structural` - intro, outro
- `main` - drop, chorus, peak, hook
- `verse` - verse, a, b
- `transition` - build, break

## Section Lengths (default bars)

| Section | Bars |
|---------|------|
| intro | 4 |
| verse | 8 |
| pre_chorus | 4 |
| chorus | 8 |
| bridge | 8 |
| drop | 8 |
| build | 4 |
| break | 4 |
| outro | 4 |

## Suggest Variations

```json
POST /arrangement/variations
{"arrangement": {...}}

Response:
{
  "variations": [
    {"name": "extended", "description": "Add 2 bars to each section"},
    {"name": "shortened", "description": "Radio edit"},
    {"name": "drop_heavy", "description": "More drops"}
  ]
}
```