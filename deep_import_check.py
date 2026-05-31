"""Deep import check - all modules"""
import sys
import importlib
sys.path.insert(0, '.')

print("=" * 60)
print("  DEEP IMPORT CHECK")
print("=" * 60)

modules = [
    'flstudio_ai_api', 'super_engine', 'drum_machine', 
    'advanced_synth', 'instrument_emulator', 'ai_melody_engine',
    'audio_analysis_engine', 'beatmaker', 'automation_timeline',
    'sampler_system', 'complete_sampler', 'midi_pattern_generator',
    'sidechain_engine', 'audio_exporter', 'preset_manager',
    'audio_track', 'live_performance', 'beat_visualizer',
    'advanced_audio', 'auto_mixer', 'flstudio_ai_master',
    'flstudio_ai_pro', 'flstudio_ai_supreme', 'flstudio_ai_ultra',
    'flstudio_ai_extreme'
]

errors = []
for mod in modules:
    try:
        m = importlib.import_module(mod)
        print(f"  [OK] {mod}")
    except Exception as e:
        print(f"  [FAIL] {mod}: {e}")
        errors.append((mod, str(e)))

print(f"\nTotal: {len(modules)} | Passed: {len(modules)-len(errors)} | Failed: {len(errors)}")

if errors:
    print("\nFAILED MODULES:")
    for name, err in errors:
        print(f"  - {name}: {err}")

print("\n" + "=" * 60)