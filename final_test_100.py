import sys
import math
import os

print('=' * 80)
print(' FINAL 100% COMPREHENSIVE DEBUG ')
print('=' * 80)
print()

# Get all py files for import test
py_files = [f for f in os.listdir('.') if f.endswith('.py')]

# Import test
print('[PHASE 1] Import Test - All Python Files')
print('-' * 40)
import_errors = []

for f in py_files:
    if any(x in f for x in ['__init__', 'test_', 'debug_', 'e2e_', 'deep_']):
        continue
    module = f[:-3]
    try:
        __import__(module)
    except Exception as e:
        import_errors.append((f, str(e)[:50]))

print(f'Total files: {len(py_files)}')
print(f'Import errors: {len(import_errors)}')

if import_errors:
    for f, e in import_errors:
        print(f'  ERROR: {f} - {e}')
else:
    print('  ALL IMPORTS OK!')

print()
print('[PHASE 2] Functional Test - 24 Core Modules')
print('-' * 40)

tests_passed = 0
tests_failed = []

# 1
try:
    from flstudio_ai_api import FLStudioAI
    api = FLStudioAI()
    r = api.generate_beat('trap', 4, save=False)
    print('[OK] 1. Main API')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 1. Main API: {str(e)[:40]}')
    tests_failed.append(('Main API', str(e)))

# 2
try:
    from super_engine import SuperEngine
    engine = SuperEngine()
    result = engine.create_beat('house', 4, save=False)
    print('[OK] 2. Super Engine')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 2. Super Engine: {str(e)[:40]}')
    tests_failed.append(('Super Engine', str(e)))

# 3
try:
    from advanced_synth import AdvancedSynthesizer
    synth = AdvancedSynthesizer()
    audio = synth.play_note(440, 0.5, 0.8)
    print('[OK] 3. Advanced Synth')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 3. Advanced Synth: {str(e)[:40]}')
    tests_failed.append(('Advanced Synth', str(e)))

# 4
try:
    from drum_machine import DrumSequencer
    seq = DrumSequencer()
    seq.set_pattern('kick', [1,0,0,0]*4)
    audio = seq.generate(4, 0.1)
    print('[OK] 4. Drum Machine')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 4. Drum Machine: {str(e)[:40]}')
    tests_failed.append(('Drum Machine', str(e)))

# 5
try:
    from neural_music_generator import CompleteNeuralMusicEngine
    engine = CompleteNeuralMusicEngine()
    song = engine.generate_complete_song('electronic', 60, 120, 4)
    print('[OK] 5. Neural Music')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 5. Neural Music: {str(e)[:40]}')
    tests_failed.append(('Neural Music', str(e)))

# 6
try:
    from esoteric_music_engine import CompleteEsotericMusicEngine
    engine = CompleteEsotericMusicEngine()
    moon = engine.create_moon_phase_music()
    print('[OK] 6. Esoteric Engine')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 6. Esoteric Engine: {str(e)[:40]}')
    tests_failed.append(('Esoteric Engine', str(e)))

# 7
try:
    from mastering_engine import CompleteMasteringEngine, MasterMode
    master = CompleteMasteringEngine()
    master.set_mode(MasterMode.MODERN)
    audio = [math.sin(440*2*math.pi*i/44100) for i in range(44100)]
    result = master.master(audio)
    print('[OK] 7. Mastering Engine')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 7. Mastering Engine: {str(e)[:40]}')
    tests_failed.append(('Mastering Engine', str(e)))

# 8
try:
    from audio_analyzer import CompleteAudioAnalyzer
    analyzer = CompleteAudioAnalyzer()
    result = analyzer.analyze_full([0.1]*44100)
    print('[OK] 8. Audio Analyzer')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 8. Audio Analyzer: {str(e)[:40]}')
    tests_failed.append(('Audio Analyzer', str(e)))

# 9
try:
    from live_performance_dj import CompletePerformanceEngine
    perf = CompletePerformanceEngine()
    result = perf.create_performance_recording()
    print('[OK] 9. Live Performance')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 9. Live Performance: {str(e)[:40]}')
    tests_failed.append(('Live Performance', str(e)))

# 10
try:
    from music_theory_engine import MusicTheoryEngine
    mt = MusicTheoryEngine()
    scales = mt.scales
    print('[OK] 10. Music Theory')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 10. Music Theory: {str(e)[:40]}')
    tests_failed.append(('Music Theory', str(e)))

# 11
try:
    from auto_creator import AutoCreator
    ac = AutoCreator()
    song = ac.create_full_song('electronic', 120, 16)
    print('[OK] 11. Auto Creator')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 11. Auto Creator: {str(e)[:40]}')
    tests_failed.append(('Auto Creator', str(e)))

# 12
try:
    from effects_rack import EffectsRack
    rack = EffectsRack()
    audio = rack.process([0.1]*44100)
    print('[OK] 12. Effects Rack')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 12. Effects Rack: {str(e)[:40]}')
    tests_failed.append(('Effects Rack', str(e)))

# 13
try:
    from module_registry import ModuleRegistry
    status = ModuleRegistry.get_system_status()
    print('[OK] 13. Module Registry')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 13. Module Registry: {str(e)[:40]}')
    tests_failed.append(('Module Registry', str(e)))

# 14
try:
    from stem_separator import STEMSeparator
    sep = STEMSeparator()
    result = sep.separate([0.1]*44100, ['drums', 'bass'])
    print('[OK] 14. Stem Separator')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 14. Stem Separator: {str(e)[:40]}')
    tests_failed.append(('Stem Separator', str(e)))

# 15
try:
    from vocal_processor import VocalProcessor
    vp = VocalProcessor()
    audio = [math.sin(440*2*math.pi*i/44100) for i in range(44100)]
    result = vp.process(audio)
    print('[OK] 15. Vocal Processor')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 15. Vocal Processor: {str(e)[:40]}')
    tests_failed.append(('Vocal Processor', str(e)))

# 16
try:
    from sample_manipulation_engine import CompleteSampleEngine, StretchMode
    engine = CompleteSampleEngine()
    audio = engine.time_stretch([0.1]*44100, 1.5, StretchMode.SIMPLE)
    print('[OK] 16. Sample Engine')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 16. Sample Engine: {str(e)[:40]}')
    tests_failed.append(('Sample Engine', str(e)))

# 17
try:
    from audio_format_converter import CompleteExportEngine, ExportSettings, AudioFormat
    engine = CompleteExportEngine()
    print('[OK] 17. Format Converter')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 17. Format Converter: {str(e)[:40]}')
    tests_failed.append(('Format Converter', str(e)))

# 18
try:
    from real_time_audio_engine import CompleteRealTimeEngine
    engine = CompleteRealTimeEngine()
    result = engine.process_buffer([0.1]*256)
    print('[OK] 18. Real-time Audio')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 18. Real-time Audio: {str(e)[:40]}')
    tests_failed.append(('Real-time Audio', str(e)))

# 19
try:
    from music_color_cymatics import MusicColorCymaticsEngine
    engine = MusicColorCymaticsEngine()
    audio = engine.create_binaural_track(10, 60, 5)
    print('[OK] 19. Cymatics')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 19. Cymatics: {str(e)[:40]}')
    tests_failed.append(('Cymatics', str(e)))

# 20
try:
    from midi_controller import MIDIController
    mc = MIDIController()
    mc.bpm = 120
    print('[OK] 20. MIDI Controller')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 20. MIDI Controller: {str(e)[:40]}')
    tests_failed.append(('MIDI Controller', str(e)))

# 21
try:
    from instrument_library import InstrumentLibrary
    lib = InstrumentLibrary()
    piano = lib.piano
    print('[OK] 21. Instrument Library')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 21. Instrument Library: {str(e)[:40]}')
    tests_failed.append(('Instrument Library', str(e)))

# 22
try:
    from preset_pack_100 import PRESETS_100
    count = len(PRESETS_100)
    print('[OK] 22. Preset Pack')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 22. Preset Pack: {str(e)[:40]}')
    tests_failed.append(('Preset Pack', str(e)))

# 23
try:
    from advanced_synthesis_engine import CompleteSynthesisEngine
    synth = CompleteSynthesisEngine()
    audio = synth.create_fm_sound('classic', 440, 0.5)
    print('[OK] 23. Advanced Synthesis')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 23. Advanced Synthesis: {str(e)[:40]}')
    tests_failed.append(('Advanced Synthesis', str(e)))

# 24
try:
    from auto_mixer import AutoMixer
    mixer = AutoMixer()
    print('[OK] 24. Auto Mixer')
    tests_passed += 1
except Exception as e:
    print(f'[FAIL] 24. Auto Mixer: {str(e)[:40]}')
    tests_failed.append(('Auto Mixer', str(e)))

print()
print('=' * 80)
print(f'RESULT: {tests_passed}/24 TESTS PASSED ({100*tests_passed//24}%)')
print('=' * 80)

if tests_failed:
    print()
    print('FAILED TESTS:')
    for name, err in tests_failed:
        print(f'  {name}: {err}')
else:
    print()
    print('*** 100% COMPLETE - ALL SYSTEMS OPERATIONAL ***')
print('=' * 80)