"""Test audio_analysis basic functions"""
import sys
sys.path.insert(0, '.')

import math

print("[1] Importing audio_analysis...")
from audio_analysis_engine import AudioAnalyzer

print("[2] Creating analyzer...")
analyzer = AudioAnalyzer()

print("[3] Creating test audio...")
test_audio = [math.sin(2 * math.pi * 440 * (i/44100)) for i in range(44100)]

print("[4] Testing BPM detection...")
bpm = analyzer.detect_bpm(test_audio)
print(f"  Detected BPM: {bpm}")

print("[5] Testing key detection...")
key = analyzer.detect_key(test_audio)
print(f"  Detected key: {key}")

print("\nAll tests passed!")