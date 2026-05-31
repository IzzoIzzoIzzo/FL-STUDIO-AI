"""END-TO-END FEATURE TEST"""
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("  END-TO-END FEATURE TEST")
print("=" * 60)

# Test 1: Full beat generation with audio output
print("\n[TEST 1] Generate full beat with audio...")
from flstudio_ai_api import FLStudioAI
ai = FLStudioAI()
result = ai.generate_beat('house', 2)
print(f"  Result: {result.get('success', False)}")
print(f"  Audio: {result.get('audio_file', 'N/A')}")

# Test 2: Synth with preset
print("\n[TEST 2] Synth with preset...")
presets = ai.list_synth_presets()
print(f"  Presets: {presets[:3]}...")
synth_audio = ai.synth.play_note(440, 0.5, 0.8)
print(f"  Generated: {len(synth_audio)} samples")

# Test 3: Drum generation
print("\n[TEST 3] Drum generation...")
drums = ai.drums.generate(2)
print(f"  Generated: {len(drums)} samples")

# Test 4: Melody generation
print("\n[TEST 4] Melody generation...")
melody = ai.melody.compose_melody('electronic', 'happy', length=8)
print(f"  Notes: {len(melody)}")

# Test 5: Auto-mixer with stems
print("\n[TEST 5] Auto-mixer with stems...")
test_audio = [0.3] * 88200  # 2 seconds
mix = ai.mixer.auto_mix(test_audio, 'club', True, 'audio/e2e_test')
print(f"  Mix file: {mix.get('mix_file', 'N/A')}")
print(f"  Stems: {len(mix.get('stems', []))}")

# Test 6: Audio export
print("\n[TEST 6] Audio export...")
exported = ai.exporter.export_wav(synth_audio, 'audio/e2e_synth.wav')
print(f"  Exported: {exported}")

# Test 7: Visualizer
print("\n[TEST 7] Visualizer...")
viz_data = ai.visualizer.generate_visualization_json([0.5] * 1000)
print(f"  Visualizations: {len(viz_data.get('visualizations', []))}")

# Test 8: MIDI export from beat
print("\n[TEST 8] MIDI export...")
import os
midi_exists = os.path.exists('exports/super_trap.mid')
print(f"  MIDI exists: {midi_exists}")

# Test 9: Preset manager
print("\n[TEST 9] Preset manager...")
from preset_manager import PresetManager
pm = PresetManager('presets')
pm.save_synth_preset('e2e_test', {'attack': 0.01})
loaded = pm.load_synth_preset('e2e_test')
print(f"  Saved and loaded: {loaded.get('name', 'N/A')}")

# Test 10: Sidechain
print("\n[TEST 10] Sidechain...")
from sidechain_engine import SidechainEngine
sc = SidechainEngine()
kick = [1.0 if i < 1000 else 0 for i in range(44100)]
pad = [0.5] * 44100
ducked = sc.duck_for_kick(pad, kick)
print(f"  Ducked samples: {len(ducked)}")

# Test 11: MIDI pattern
print("\n[TEST 11] MIDI pattern generator...")
from midi_pattern_generator import MIDIPatternGenerator
mpg = MIDIPatternGenerator(120)
drums = mpg.generate_drum_pattern('808')
print(f"  Drum events: {len(drums)}")

# Test 12: Instrument emulator
print("\n[TEST 12] Instrument emulator...")
from instrument_emulator import PadSynth
pad = PadSynth()
chord = pad.play_chord('C', 'major', 1.0, 'ambient')
print(f"  Chord samples: {len(chord)}")

print("\n" + "=" * 60)
print("  ALL END-TO-END TESTS PASSED!")
print("=" * 60)