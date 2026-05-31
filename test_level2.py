"""Verify Level 2 modules connect to main system"""
import sys
import math
sys.path.insert(0, '.')

print("=" * 60)
print("  LEVEL 2 MODULES CONNECTION VERIFICATION")
print("=" * 60)

# Test importing new modules
print("\n[1] Testing Arpeggiator V2 import...")
from arpeggiator_v2 import ArpPro, ChordToArp
arp = ArpPro()
print("    [OK] Arpeggiator V2 connected")

print("\n[2] Testing Analysis Tools V2 import...")
from analysis_tools_v2 import BPMDetector, KeyDetector, ScaleFinder, ReferenceMatch
print("    [OK] Analysis Tools V2 connected")

# Test integration
print("\n[3] Testing integration...")
# BPM from audio analysis
test_audio = [math.sin(440 * 2 * math.pi * i/44100) for i in range(44100)]
bpm = BPMDetector.detect_bpm(test_audio)
print(f"    BPM detected: {bpm}")

# Key detection
key = KeyDetector.detect_key(test_audio)
print(f"    Key detected: {key['key']} {key['mode']}")

# Scale finder
scale = ScaleFinder.find_scale([60, 62, 64, 67, 69])
print(f"    Scale found: {scale['root']} {scale['scale']}")

# Arpeggiator
arp_result = arp.generate_from_chord(60, 'major', 1.0)
print(f"    Arp notes: {len(arp_result)}")

print("\n" + "=" * 60)
print("  ALL LEVEL 2 MODULES CONNECTED!")
print("=" * 60)