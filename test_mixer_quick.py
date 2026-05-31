"""Test auto_mixer quick"""
import sys
sys.path.insert(0, '.')
import math

print("[1] Importing auto_mixer...")
from auto_mixer import AutoMixer

print("[2] Creating mixer...")
mixer = AutoMixer()

print("[3] Creating test audio...")
test_audio = [math.sin(2 * math.pi * 440 * (i/44100)) * 0.5 for i in range(44100)]

print("[4] Testing auto_mix...")
result = mixer.auto_mix(test_audio, 'club', True, "audio/debug_mix")

print(f"  Mix file: {result['mix_file']}")
print(f"  Stems: {len(result['stems'])}")

print("\nAll tests passed!")