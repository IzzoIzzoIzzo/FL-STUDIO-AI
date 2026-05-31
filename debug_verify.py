"""
COMPREHENSIVE DEBUG & VERIFICATION SCRIPT
==========================================
Motto: "Make sure everything works and is connected"
Level: Easiest to Hardest

Test Order:
1. Basic Imports (easiest)
2. Core Classes
3. Mid-Level Features
4. Advanced Features
5. Full Integration (hardest)
"""

import sys
import math

sys.path.insert(0, '.')

print("=" * 70)
print("  COMPREHENSIVE DEBUG - EASIEST TO HARDEST")
print("  Motto: Make sure everything works and is connected")
print("=" * 70)

results = []

# ============================================================
# TIER 1 - BASIC IMPORTS (EASIEST)
# ============================================================
print("\n[TIER 1] Basic Imports...")

basic_modules = [
    ('enhanced_synth_v2', 'EnhancedSynthesizer'),
    ('drum_machine_v2', 'SmartDrumGenerator'),
    ('mixer_v2', 'EnhancedMixer'),
    ('melody_v2', 'EnhancedMelodyAI'),
    ('arpeggiator_v2', 'ArpPro'),
    ('pattern_library_v2', 'PatternLibrary'),
    ('arrangement_ai', 'ArrangementAI'),
    ('web3_basics', 'Web3BeatManager'),
]

for module, classname in basic_modules:
    try:
        exec("from %s import %s" % (module, classname))
        print("  [OK] %s" % module)
        results.append((module, 'OK'))
    except Exception as e:
        print("  [FAIL] %s: %s" % (module, str(e)[:50]))
        results.append((module, str(e)[:30]))

# ============================================================
# TIER 2 - CORE CLASSES (EASY)
# ============================================================
print("\n[TIER 2] Core Classes...")

try:
    synth = EnhancedSynthesizer()
    audio = synth.play_note(440, 0.1)
    print("  [OK] Synth: play note")
    results.append(('Synth', 'OK'))
except Exception as e:
    print("  [FAIL] Synth: %s" % e)
    results.append(('Synth', str(e)[:30]))

try:
    drums = SmartDrumGenerator()
    pattern = drums.generate(2, 'trap')
    print("  [OK] Drums: generate pattern")
    results.append(('Drums', 'OK'))
except Exception as e:
    print("  [FAIL] Drums: %s" % e)
    results.append(('Drums', str(e)[:30]))

try:
    mixer = EnhancedMixer()
    processed = mixer.process_track([0.5]*4410, 'synth')
    print("  [OK] Mixer: process track")
    results.append(('Mixer', 'OK'))
except Exception as e:
    print("  [FAIL] Mixer: %s" % e)
    results.append(('Mixer', str(e)[:30]))

try:
    melody = EnhancedMelodyAI()
    m = melody.generate_emotional('happy', 60, 8)
    print("  [OK] Melody: generate")
    results.append(('Melody', 'OK'))
except Exception as e:
    print("  [FAIL] Melody: %s" % e)
    results.append(('Melody', str(e)[:30]))

# ============================================================
# TIER 3 - MID-LEVEL FEATURES
# ============================================================
print("\n[TIER 3] Mid-Level Features...")

try:
    arp = ArpPro()
    notes = arp.generate_from_chord(60, 'major', 1.0)
    print("  [OK] Arpeggiator: generate")
    results.append(('Arp', 'OK'))
except Exception as e:
    print("  [FAIL] Arp: %s" % e)
    results.append(('Arp', str(e)[:30]))

try:
    from analysis_tools_v2 import BPMDetector, KeyDetector
    audio = [math.sin(440*2*math.pi*i/44100) for i in range(44100)]
    bpm = BPMDetector.detect_bpm(audio)
    key = KeyDetector.detect_key(audio)
    print("  [OK] Analysis: BPM=%.1f Key=%s" % (bpm, key['key']))
    results.append(('Analysis', 'OK'))
except Exception as e:
    print("  [FAIL] Analysis: %s" % e)
    results.append(('Analysis', str(e)[:30]))

try:
    drum = PatternLibrary.get_drum_pattern('trap')
    print("  [OK] Pattern Library: get pattern")
    results.append(('Patterns', 'OK'))
except Exception as e:
    print("  [FAIL] Patterns: %s" % e)
    results.append(('Patterns', str(e)[:30]))

# ============================================================
# TIER 4 - ADVANCED FEATURES
# ============================================================
print("\n[TIER 4] Advanced Features...")

try:
    arranger = ArrangementAI()
    arr = arranger.generate_arrangement('pop', 120)
    print("  [OK] Arrangement: %d bars" % arr['total_bars'])
    results.append(('Arrangement', 'OK'))
except Exception as e:
    print("  [FAIL] Arrangement: %s" % e)
    results.append(('Arrangement', str(e)[:30]))

try:
    from ai_agents import MasteringAgent
    master = MasteringAgent()
    result = master.analyze([0.5]*44100)
    print("  [OK] AI Agents: analyze")
    results.append(('AIAgents', 'OK'))
except Exception as e:
    print("  [FAIL] AI Agents: %s" % e)
    results.append(('AIAgents', str(e)[:30]))

try:
    web3 = Web3BeatManager()
    reg = web3.register_beat([0.5]*44100, {'title': 'Test'})
    print("  [OK] Web3: register beat")
    results.append(('Web3', 'OK'))
except Exception as e:
    print("  [FAIL] Web3: %s" % e)
    results.append(('Web3', str(e)[:30]))

# ============================================================
# TIER 5 - LEVEL 5 MODULES
# ============================================================
print("\n[TIER 5] Level 5 Modules...")

try:
    from level_5_1 import AutomationCurve, SidechainCompressor
    auto = AutomationCurve('Test', 'volume')
    auto.add_point(0, 0.5)
    val = auto.get_value(2)
    print("  [OK] 5.1 Automation: value=%.2f" % val)
    results.append(('L5_Auto', 'OK'))
except Exception as e:
    print("  [FAIL] 5.1: %s" % e)
    results.append(('L5_Auto', str(e)[:30]))

try:
    from level_5_2 import FFTAnalyzer
    fft = FFTAnalyzer(1024)
    audio = [math.sin(440*2*math.pi*t/44100) for t in range(1024)]
    mags, _ = fft.transform(audio)
    print("  [OK] 5.2 FFT: %d bins" % len(mags))
    results.append(('L5_FFT', 'OK'))
except Exception as e:
    print("  [FAIL] 5.2: %s" % e)
    results.append(('L5_FFT', str(e)[:30]))

try:
    from level_5_3 import ProjectFile
    proj = ProjectFile('Test')
    proj.add_track('Drums', 'audio')
    print("  [OK] 5.3 Project: %d tracks" % len(proj.tracks))
    results.append(('L5_Project', 'OK'))
except Exception as e:
    print("  [FAIL] 5.3: %s" % e)
    results.append(('L5_Project', str(e)[:30]))

# ============================================================
# TIER 6 - MAIN API (HARDEST - FULL INTEGRATION)
# ============================================================
print("\n[TIER 6] Main API Integration...")

try:
    from flstudio_ai_api import FLStudioAI
    api = FLStudioAI()
    print("  [OK] API: init")
    results.append(('API_Init', 'OK'))
except Exception as e:
    print("  [FAIL] API: %s" % e)
    results.append(('API_Init', str(e)[:30]))

try:
    beat = api.generate_beat('trap', 2)
    if beat.get('success'):
        print("  [OK] API: generate beat")
        results.append(('API_Beat', 'OK'))
    else:
        print("  [FAIL] Beat: %s" % beat.get('error'))
        results.append(('API_Beat', 'FAIL'))
except Exception as e:
    print("  [FAIL] Beat: %s" % e)
    results.append(('API_Beat', str(e)[:30]))

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("  DEBUG SUMMARY")
print("=" * 70)

passed = sum(1 for _, s in results if s == 'OK')
total = len(results)

print("  Tests: %d/%d passed" % (passed, total))
print("  Status: %s" % ("ALL WORKING!" if passed == total else "ISSUES FOUND"))

for name, status in results:
    symbol = "OK" if status == "OK" else "FAIL"
    print("    [%s] %s" % (symbol, name))

print("\n" + "=" * 70)
if passed == total:
    print("  MOTTO VERIFIED: Everything works and is connected!")
else:
    print("  Some issues found - need debugging")
print("=" * 70)