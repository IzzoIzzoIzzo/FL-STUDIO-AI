"""CONNECTION TEST - Verify all modules connected to API"""
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("  TESTING ALL MODULES CONNECTED TO UNIFIED API")
print("=" * 60)

# Test main API imports all modules
from flstudio_ai_api import FLStudioAI
ai = FLStudioAI()

print("\n[1] API imports connected modules:")
print(f"  - Beat Generator: {hasattr(ai, 'generate_beat')}")
print(f"  - Synthesizer: {hasattr(ai, 'synth')}")
print(f"  - Drum Machine: {hasattr(ai, 'drums')}")
print(f"  - Melody Engine: {hasattr(ai, 'melody')}")
print(f"  - Mixer: {hasattr(ai, 'mixer')}")
print(f"  - Visualizer: {hasattr(ai, 'visualizer')}")
print(f"  - Exporter: {hasattr(ai, 'exporter')}")

# Test actual generation using multiple modules
print("\n[2] Generating full track with all modules connected...")

# Generate beat
beat = ai.generate_beat('trap', 4)
print(f"  - Beat generated: {beat.get('audio', 'N/A')[:50]}...")

# Test synth connection
synth_audio = ai.synth.play_note(440, 0.5)
print(f"  - Synth connected: {len(synth_audio)} samples")

# Test drums
drums_audio = ai.drums.generate(4)
print(f"  - Drums connected: {len(drums_audio)} samples")

# Test melody
melody = ai.melody.compose_melody('electronic', 'happy')
print(f"  - Melody connected: {len(melody)} notes")

# Test mixer
mix_result = ai.mixer.auto_mix([0.5]*44100, 'club')
print(f"  - Mixer connected: {mix_result.get('mix_file', 'N/A')}")

# Test exporter
test_audio = [0.5] * 44100
wav_file = ai.exporter.export_wav(test_audio, 'audio/connection_test.wav')
print(f"  - Exporter connected: {wav_file}")

# Test visualizer
viz = ai.visualizer.generate_visualization_json([0.5]*1000)
print(f"  - Visualizer connected: {len(viz.get('visualizations', []))} viz")

print("\n" + "=" * 60)
print("  ALL MODULES CONNECTED AND WORKING!")
print("=" * 60)