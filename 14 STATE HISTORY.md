---
tags: [state, history, versioning]
---

# 💾 State Manager & History

## State Manager

### Save State
```json
POST /state/save
{"name": "verse_section", "data": {"tempo": 140, "style": "trap"}}
```

### Undo
```json
POST /state/undo
```

### Redo
```json
POST /state/redo
```

### Save Snapshot
```json
POST /state/snapshot
{"name": "my_saved_state", "data": {...}}
```

### Load Snapshot
```json
POST /state/load
{"name": "my_saved_state"}
```

## Project History

### Create Project
```json
POST /history/create
{"name": "My Track", "metadata": {"tempo": 140}}
```

### Save Version
```json
POST /history/save
{
  "project": "My Track",
  "data": {"track_data": {...}},
  "label": "Added bass line"
}
```

### List Versions
```json
POST /history/versions
{"project": "My Track"}

Response:
[
  {"version": 1, "timestamp": "2026-01-01...", "label": "Initial"},
  {"version": 2, "timestamp": "2026-01-01...", "label": "Added bass"}
]
```

### Load Version
```json
POST /history/load
{"project": "My Track", "version": 2}
```

## Undo/Redo Stack

- Max history: 50 states
- Each save pushes to history
- Undo moves to history, pushes to redo stack
- Redo reverses the process
- New action clears redo stack