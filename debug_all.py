"""COMPREHENSIVE DEBUG - TEST ALL MODULES"""
import sys
import os
import traceback
import math

sys.path.insert(0, '.')
os.chdir(r'C:\Users\Brittany\OneDrive\Desktop\AI FL STUDIO BUILD')

results = []

def test_module(name, test_func):
    """Test a module and track results"""
    print(f"\n{'='*50}")
    print(f"TESTING: {name}")
    print('='*50)
    try:
        result = test_func()
        results.append((name, "PASS", result))
        print(f"[PASS] {name}")
        return result
    except Exception as e:
        results.append((name, "FAIL", str(e)))
        print(f"[FAIL] {name}: {e}")
        traceback.print_exc()
        return None

# ============================================================
# CORE MODULES
# ============================================================

def test_api():
    """Test flstudio_ai_api.py"""
    from flstudio_ai_api import FLStudioAI
    ai = FLStudioAI()
    print("  - API initialized")
    return "OK"

def test_super_engine():
    """Test super_engine.py"""
    from super_engine import BeatGenerator
    gen = BeatGenerator()
    beat = gen.generate('trap', 2)
    print(f"  - Generated beat: {beat.get('style', 'unknown')}")
    return "OK"

def test_drum_machine():
    """Test drum_machine.py"""
    from drum_machine import DrumSequencer
    seq = DrumSequencer('808')
    audio = seq.generate(2)
    print(f"  - Generated {len(audio)} samples")
    return "OK"

def test_advanced_synth():
    """Test advanced_synth.py"""
    from advanced_synth import AdvancedSynthesizer
    synth = AdvancedSynthesizer()
    audio = synth.play_note(440, 0.1, 0.8)
    print(f"  - Generated {len(audio)} samples")
    return "OK"

def test_instrument_emulator():
    """Test instrument_emulator.py"""
    from instrument_emulator import PadSynth, LeadSynth, BassSynth
    pad = PadSynth()
    chord = pad.play_chord('C', 'major', 1.0, 'ambient')
    print(f"  - Generated chord: {len(chord)} samples")
    return "OK"

def test_ai_melody():
    """Test ai_melody_engine.py"""
    from ai_melody_engine import AIMelodyComposer
    composer = AIMelodyComposer()
    melody = composer.compose_melody('electronic', 'dreamy')
    print(f"  - Generated melody: {len(melody)} notes")
    return "OK"

def test_audio_analyzer():
    """Test audio_analysis_engine.py"""
    from audio_analysis_engine import AudioAnalyzer
    analyzer = AudioAnalyzer()
    test_audio = [math.sin(2 * math.pi * 440 * (i/44100)) for i in range(22050)]
    bpm = analyzer.detect_bpm(test_audio)
    print(f"  - Detected BPM: {bpm}")
    return "OK"

def test_beatmaker():
    """Test beatmaker.py"""
    from beatmaker import generate_track
    track = generate_track('trap', 140, 4)
    print(f"  - Created track: {track.get('style', 'unknown')}")
    return "OK"

def test_automation():
    """Test automation_timeline.py"""
    from automation_timeline import Timeline
    timeline = Timeline(120)
    track = timeline.add_track('test_track', 'audio')
    track.add_automation('volume', 0, 1)
    print(f"  - Created track with automation")
    return "OK"

def test_sampler():
    """Test sampler_system.py"""
    from sampler_system import AudioSample, SampleChopper
    samples = [math.sin(i*0.1) for i in range(44100)]
    sample = AudioSample(samples=samples, sample_rate=44100, name='test')
    chopper = SampleChopper()
    slices = chopper.chop_by_transients(sample)
    print(f"  - Created {len(slices)} slices")
    return "OK"

def test_complete_sampler():
    """Test complete_sampler.py"""
    from complete_sampler import CompleteSampler
    sampler = CompleteSampler()
    print(f"  - Created CompleteSampler")
    return "OK"

def test_midi_pattern():
    """Test midi_pattern_generator.py"""
    from midi_pattern_generator import MIDIPatternGenerator
    gen = MIDIPatternGenerator(120)
    drums = gen.generate_drum_pattern('808')
    print(f"  - Generated {len(drums)} drum events")
    return "OK"

def test_sidechain():
    """Test sidechain_engine.py"""
    from sidechain_engine import SidechainEngine
    sc = SidechainEngine()
    kick = [math.sin(2 * math.pi * 60 * (i/44100)) * (1 - i/22050) for i in range(22050)]
    pads = [math.sin(2 * math.pi * 220 * (i/44100)) * 0.3 for i in range(44100)]
    ducked_audio = sc.duck_for_kick(pads, kick)
    print(f"  - Ducked {len(ducked_audio)} samples")
    return "OK"

def test_exporter():
    """Test audio_exporter.py"""
    from audio_exporter import AudioExporter
    exp = AudioExporter()
    test_audio = [math.sin(2 * math.pi * 440 * (i/44100)) for i in range(44100)]
    wav_file = exp.export_wav(test_audio, 'audio/debug_all_test.wav')
    print(f"  - Exported WAV: {wav_file}")
    return "OK"

def test_preset_manager():
    """Test preset_manager.py"""
    from preset_manager import PresetManager
    pm = PresetManager('presets')
    pm.save_synth_preset('debug_test', {'attack': 0.01, 'decay': 0.1})
    loaded = pm.load_synth_preset('debug_test')
    print(f"  - Preset loaded: {loaded.get('name', 'unknown')}")
    return "OK"

def test_audio_track():
    """Test audio_track.py - minimal"""
    from audio_track import TrackGenerator
    gen = TrackGenerator()
    # Don't run full generation, just check it can be created
    print("  - TrackGenerator created")
    return "OK"

def test_live_performance():
    """Test live_performance.py - check import only"""
    from live_performance import LivePerformance
    perf = LivePerformance()
    print("  - LivePerformance created")
    return "OK"

def test_beat_visualizer():
    """Test beat_visualizer.py"""
    from beat_visualizer import VisualBeatGenerator
    gen = VisualBeatGenerator(400, 300)
    audio = [math.sin(i * 0.1) for i in range(1000)]
    viz = gen.generate_visualization_json(audio)
    print(f"  - Generated {len(viz.get('visualizations', []))} visualizations")
    return "OK"

def test_advanced_audio():
    """Test advanced_audio.py"""
    from advanced_audio import AdvancedOscillator
    osc = AdvancedOscillator(44100)
    audio = osc.generate('sine', 440, 0.1)
    print(f"  - Generated {len(audio)} samples")
    return "OK"

def test_auto_mixer():
    """Test auto_mixer.py"""
    from auto_mixer import AutoMixer
    mixer = AutoMixer()
    test_audio = [math.sin(2 * math.pi * 440 * (i/44100)) for i in range(22050)]
    result = mixer.auto_mix(test_audio, 'club', False, 'audio/debug_mixer')
    print(f"  - Mixed audio, stems: {len(result.get('stems', []))}")
    return "OK"

# ============================================================
# MAIN DEBUG RUN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  COMPREHENSIVE DEBUG - ALL MODULES")
    print("=" * 70)
    
    # Test all modules
    test_module("flstudio_ai_api", test_api)
    test_module("super_engine", test_super_engine)
    test_module("drum_machine", test_drum_machine)
    test_module("advanced_synth", test_advanced_synth)
    test_module("instrument_emulator", test_instrument_emulator)
    test_module("ai_melody_engine", test_ai_melody)
    test_module("audio_analysis_engine", test_audio_analyzer)
    test_module("beatmaker", test_beatmaker)
    test_module("automation_timeline", test_automation)
    test_module("sampler_system", test_sampler)
    test_module("complete_sampler", test_complete_sampler)
    test_module("midi_pattern_generator", test_midi_pattern)
    test_module("sidechain_engine", test_sidechain)
    test_module("audio_exporter", test_exporter)
    test_module("preset_manager", test_preset_manager)
    test_module("audio_track", test_audio_track)
    test_module("live_performance", test_live_performance)
    test_module("beat_visualizer", test_beat_visualizer)
    test_module("advanced_audio", test_advanced_audio)
    test_module("auto_mixer", test_auto_mixer)
    
    # Summary
    print("\n" + "=" * 70)
    print("  DEBUG SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, status, _ in results if status == "PASS")
    failed = sum(1 for _, status, _ in results if status == "FAIL")
    
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    if failed > 0:
        print("\nFAILED MODULES:")
        for name, status, error in results:
            if status == "FAIL":
                print(f"  - {name}: {error}")
    
    print("\n" + "=" * 70)