"""Test advanced_synth basic functions"""
import sys
sys.path.insert(0, '.')

from advanced_synth import AdvancedSynthesizer, SynthesizerPreset

print("[1] Testing preset list...")
presets = SynthesizerPreset.list_presets()
print(f"  Found {len(presets)} presets: {presets}")

print("\n[2] Testing synth creation...")
synth = AdvancedSynthesizer()
print("  OK")

print("\n[3] Testing note generation (short)...")
audio = synth.play_note(440, 0.1, 0.8)  # Short 0.1s note
print(f"  Generated {len(audio)} samples")

print("\n[4] Saving test...")
synth.save_wav(audio, 'audio/debug_synth_test.wav')
print("  Saved: audio/debug_synth_test.wav")

print("\nAll tests passed!")