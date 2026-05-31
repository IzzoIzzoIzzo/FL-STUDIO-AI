# FL STUDIO AI — Ultimate Beat Making Engine

> **Status:** In Progress — Core systems operational, actively building
> **Version:** v8.0 (Pre-Release)
> **Motto:** *"Everything works and is connected"*

An AI-powered music production system with 100+ Python modules for beat generation, synthesis, mixing, mastering, and creative sound design. Designed for integration with FL Studio via MCP protocol, REST API, and CLI.

---

## Architecture

```
flstudio_ai_api.py         — Main REST API (port 5000)
flstudio_mcp_server_v2.py  — MCP protocol server for AI IDE integration
├── Super Engine           — Beat generation (15+ styles)
├── Advanced Synth         — 47+ presets, 5 synthesis methods
├── Drum Machine           — 5 kits with patterns & fills
├── Mixer                  — 8-channel with EQ, compression
├── Mastering Engine       — 6 mastering modes
├── AI Melody Engine       — Neural composition
├── Effects Rack           — 9-effect chain
└── Stem Separator         — Extract drums/bass/vocals/melody
```

### How It Works

The system is modular by design. Every component can run standalone or through the unified API:

1. **REST API** (`flstudio_ai_api.py`) — All features accessible via HTTP on `localhost:5000`. Used by web interfaces and external integrations.
2. **MCP Server** (`flstudio_mcp_server_v2.py`) — Model Context Protocol server that lets AI coding assistants (Claude Code, OpenCode) generate music directly by calling tools like `generate_beat`, `synthesize_sound`, `mix_track`.
3. **CLI** — Direct Python invocations for power users and automation.
4. **Web Interfaces** — HTML dashboards for visual control.

---

## Core Components

### Generation Engine
| Module | What It Does |
|--------|-------------|
| `super_engine.py` | Beat generation in 15+ styles (trap, house, hiphop, techno, lofi, dubstep, dnb, garage, etc.) |
| `ai_melody_engine.py` | AI-powered melody and chord generation with emotion profiles |
| `neural_music_generator.py` | LSTM-style composition with style transfer |
| `music_theory_engine.py` | 50+ scales, 100+ chord types, progressions, voice leading |
| `auto_creator.py` | Full song generation from scratch with structure, mixing, mastering |

### Synthesis
| Module | What It Does |
|--------|-------------|
| `advanced_synth.py` | 47+ presets across 11 categories (leads, bass, pads, plucks, keys, strings, brass, FX, bells, SFX, special) |
| `advanced_synthesis_engine.py` | 5 methods: Wavetable, FM, Granular, Additive, Physical Modeling |
| `enhanced_synth_v4.py` | Real-time modulation, arpeggiator, filter bank |
| `instrument_library.py` | 31 virtual instruments (piano, guitar, strings, brass, synth, world) |

### Production & Mixing
| Module | What It Does |
|--------|-------------|
| `mixer_v3.py` | 8-channel strip with EQ, compression, sends/returns, metering |
| `auto_mixer.py` | Stem separation, vocal processing, auto-EQ |
| `mastering_engine.py` | 6 modes: analog, modern, vinyl, cassette, tape, digital. LUFS normalization |
| `effects_rack.py` | EQ, compressor, saturator, delay, reverb, chorus, flanger, phaser, distortion |
| `sidechain_engine.py` | Sidechain compression with envelope shaping |

### Creative & Esoteric
| Module | What It Does |
|--------|-------------|
| `esoteric_music_engine.py` | Sacred geometry, 528Hz Solfeggio healing, planetary frequencies, binaural beats |
| `music_color_cymatics.py` | Frequency-to-color mapping, cymatic visual patterns |
| `creative_sound_engine.py` | Granular, spectral, convolution reverb, analog warmth, stereo widening |

### Analysis & AI
| Module | What It Does |
|--------|-------------|
| `audio_analyzer.py` | FFT spectrum, BPM detection, key detection, pitch tracking |
| `advanced_ai_composer.py` | 8 AI models: Markov Chain, LSTM, Style Transfer, Arrangement, etc. |
| `ai_agents.py` | AI mastering, mixing, and sound design agents |
| `stem_separator.py` | Extract drums, bass, vocals, melody from audio files |

### Integration
| Module | What It Does |
|--------|-------------|
| `flstudio_mcp_server_v2.py` | MCP protocol for Claude Code / OpenCode integration |
| `flstudio_ai_api.py` | Flask REST API — single endpoint for all features |
| `web_dashboard_backend.py` | Backend for HTML visual dashboards |
| `midi_controller.py` | MIDI I/O, CC mapping, clock sync |
| `live_performance_dj.py` | DJ decks, beatmatching, hot cues, loops |

---

## SHADDAI Orchestration Layer (In Development)

> **SOL** — Shaddai Orchestration Layer

A token-saving graph-native orchestration layer being built to connect the 7 SHADDAI agents across local LLM (Ollama) and multi-provider cloud fallbacks (AceDataCloud, Groq, Gemini, OpenAI, Anthropic, DeepSeek).

| Agent | Port | Role |
|-------|------|------|
| SHADDAI | 8000 | Supreme Orchestrator |
| ZEROX | 8001 | Markets & Finance |
| ORACLE | 8002 | Research & Esoteric |
| NEXUS | 8003 | Routing & Architecture |
| TURTLE | 8004 | Creative & UI/UX |
| QUILL | 8005 | Writing & Documentation |
| PIKADON | 8008 | Security & Compliance |

SOL uses 5 primitives (STORE, FETCH, QUERY, COMPUTE, LOGIC) to minimize API costs by routing simple tasks to local processing and reserving paid LLM calls for complex operations only.

---

## HTML Interfaces

| File | What It Does |
|------|-------------|
| `SHADDAI_OPENCORE_V1.html` | Graph-based dashboard with 7 agents, AINL primitives, memory panel |
| `SHADDAI_ENGINE.html` | Unified music creation engine |
| `UNIFIED.html` | Music engine with beats/synth/piano/healing/AI/export |
| `LAUNCHER.html` | Main music engine launcher |
| `flstudio_ai_interface.html` | Web GUI for FL Studio AI |
| `system_architecture.html` | Interactive 3D visualization of all modules |
| `beat_visualizer.html` | Beat visualization |

---

## Quick Start

```bash
# Start the API server
python flstudio_ai_api.py

# Generate a trap beat via CLI
python beatmaker.py generate trap 150

# Complete verification test
python debug_verify.py

# Run all levels (1-6) test
python final_test_100.py
```

### Starting the MCP Server (for AI IDE integration)
```bash
python flstudio_mcp_server_v2.py
```

This exposes tools like `generate_beat`, `synthesize_sound`, `mix_track`, `master_track` to any MCP-compatible AI assistant.

---

## Debug & Verification

The system includes multiple verification scripts:

```bash
python debug_verify.py          # Quick test all 19 modules
python final_test_100.py        # Comprehensive test suite
python e2e_test.py              # End-to-end production test
python test_suite_v2.py         # Extended test suite
```

Each module also has standalone tests:
```bash
python test_synth_quick.py      # Test synthesizer
python test_mixer_quick.py      # Test mixer
python test_analysis_quick.py   # Test analysis tools
```

---

## File Index (200+ Files)

The build is organized into:

- **~/ (root)** — Core Python modules, APIs, servers
- **audio/** — Audio assets and samples
- **exports/** — Generated MIDI and audio exports
- **presets/** — Sound presets and configurations
- **js/** — JavaScript assets for web interfaces
- **data/** — Data files and pattern libraries
- **Level-based** — `level_1_7.py` through `level_6_3.py` — Progressive feature layers

Complete documentation at `00 INDEX.md` through `22 MODULATION.md` (22 reference docs).

---

## License

MIT — Use freely. Build legacy.
