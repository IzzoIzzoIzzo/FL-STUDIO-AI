"""
TEST SUITE V2 - Level 1.6
==========================
Comprehensive tests for all modules
Auto-test runner
Coverage tracking
Regression prevention

Building on what we have - making it stable!
"""

import sys
import os
import importlib
import math
from typing import Dict, List, Tuple, Callable


# Add parent dir to path
sys.path.insert(0, '.')


class TestResult:
    """Store test result"""
    def __init__(self, name: str, passed: bool, message: str = "", time: float = 0):
        self.name = name
        self.passed = passed
        self.message = message
        self.time = time


class TestSuite:
    """Test suite runner"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, name: str, test_func: Callable) -> TestResult:
        """Run a single test"""
        import time
        start = time.time()
        
        try:
            result = test_func()
            elapsed = time.time() - start
            
            if result:
                self.passed += 1
                return TestResult(name, True, "OK", elapsed)
            else:
                self.failed += 1
                return TestResult(name, False, "Test returned False", elapsed)
                
        except Exception as e:
            elapsed = time.time() - start
            self.failed += 1
            return TestResult(name, False, str(e), elapsed)
    
    def summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("  TEST SUITE RESULTS")
        print("=" * 60)
        
        total = self.passed + self.failed
        percent = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {percent:.1f}%")
        
        if self.failed > 0:
            print("\n" + "=" * 60)
            print("  FAILED TESTS")
            print("=" * 60)
            for r in self.results:
                if not r.passed:
                    print(f"  [X] {r.name}: {r.message}")
        
        return self.failed == 0


# ===== MODULE TESTS =====

def test_synth_v2_import():
    """Test synth v2 imports"""
    from enhanced_synth_v2 import EnhancedSynthesizer, EnhancedOscillatorBank
    synth = EnhancedSynthesizer()
    return synth is not None


def test_synth_v2_presets():
    """Test synth v2 presets load"""
    from enhanced_synth_v2 import EnhancedSynthesizer
    synth = EnhancedSynthesizer()
    synth.load_preset('lead_superSaw')
    return synth.current_preset == 'lead_superSaw'


def test_synth_v2_generate():
    """Test synth v2 generates audio"""
    from enhanced_synth_v2 import EnhancedSynthesizer
    synth = EnhancedSynthesizer()
    audio = synth.play_note(440, 0.1)
    return len(audio) > 0 and abs(sum(audio)) > 0


def test_drums_v2_import():
    """Test drums v2 imports"""
    from drum_machine_v2 import SmartDrumGenerator, Humanizer
    gen = SmartDrumGenerator()
    return gen is not None


def test_drums_v2_humanize():
    """Test humanization"""
    from drum_machine_v2 import Humanizer
    vel = Humanizer.humanize_velocity(100, 0.1)
    return 70 <= vel <= 130


def test_drums_v2_generate():
    """Test drum generation"""
    from drum_machine_v2 import SmartDrumGenerator
    gen = SmartDrumGenerator()
    pattern = gen.generate(2, 'trap')
    return len(pattern) > 0


def test_drums_v2_groove():
    """Test groove templates"""
    from drum_machine_v2 import SmartDrumGenerator
    gen = SmartDrumGenerator()
    pattern = gen.generate_with_groove(2, 'trap', 'funk')
    return len(pattern) > 0


def test_mixer_v2_import():
    """Test mixer v2 imports"""
    from mixer_v2 import EnhancedMixer, SmartEQ
    mixer = EnhancedMixer()
    return mixer is not None


def test_mixer_v2_eq():
    """Test EQ presets"""
    from mixer_v2 import SmartEQ
    eq = SmartEQ()
    kick_settings = eq.get_settings('kick')
    return kick_settings['low'] == 4


def test_mixer_v2_process():
    """Test track processing"""
    from mixer_v2 import EnhancedMixer
    mixer = EnhancedMixer()
    audio = [0.5] * 4410
    processed = mixer.process_track(audio, 'synth')
    return len(processed) == len(audio)


def test_mixer_v2_limiter():
    """Test limiter"""
    from mixer_v2 import EnhancedMixer
    mixer = EnhancedMixer()
    audio = [1.0] * 4410
    limited = mixer.limiter.apply(audio)
    return max(abs(s) for s in limited) <= 1.0


def test_melody_v2_import():
    """Test melody v2 imports"""
    from melody_v2 import EnhancedMelodyAI, MusicalScale
    ai = EnhancedMelodyAI()
    return ai is not None


def test_melody_v2_scales():
    """Test scale generation"""
    from melody_v2 import MusicalScale
    notes = MusicalScale.get_notes('major', 60)
    return len(notes) == 14  # 2 octaves


def test_melody_v2_emotions():
    """Test emotion profiles"""
    from melody_v2 import EmotionGenerator
    melody = EmotionGenerator.generate('happy', 8, 60)
    return len(melody) == 8


def test_melody_v2_phrase():
    """Test phrase generation"""
    from melody_v2 import PhraseGenerator
    phrase = PhraseGenerator.generate_phrase(60, 'minor', 'verse')
    return len(phrase) > 0


def test_melody_v2_full():
    """Test full melody generation"""
    from melody_v2 import EnhancedMelodyAI
    ai = EnhancedMelodyAI()
    full = ai.generate_full_melody(60, 'dorian', 'dreamy', 'structured')
    return full['note_count'] > 0


def test_cli_v2_import():
    """Test CLI v2 imports"""
    from cli_v2 import MenuSystem, HelpSystem, InteractiveCLI
    return MenuSystem is not None


def test_cli_v2_help():
    """Test help system"""
    from cli_v2 import HelpSystem
    help_text = HelpSystem.COMMANDS
    return 'generate' in help_text


def test_cli_v2_suggest():
    """Test command suggestions"""
    from cli_v2 import CommandSuggestions
    sugs = CommandSuggestions.suggest('gen')
    return 'generate' in sugs


# ===== MAIN TEST RUNNER =====

def run_all_tests():
    """Run all tests"""
    
    suite = TestSuite()
    
    # Synth V2 Tests
    print("\n[1] Testing Synth V2...")
    suite.run_test("synth_v2_import", test_synth_v2_import)
    suite.run_test("synth_v2_presets", test_synth_v2_presets)
    suite.run_test("synth_v2_generate", test_synth_v2_generate)
    
    # Drums V2 Tests
    print("[2] Testing Drums V2...")
    suite.run_test("drums_v2_import", test_drums_v2_import)
    suite.run_test("drums_v2_humanize", test_drums_v2_humanize)
    suite.run_test("drums_v2_generate", test_drums_v2_generate)
    suite.run_test("drums_v2_groove", test_drums_v2_groove)
    
    # Mixer V2 Tests
    print("[3] Testing Mixer V2...")
    suite.run_test("mixer_v2_import", test_mixer_v2_import)
    suite.run_test("mixer_v2_eq", test_mixer_v2_eq)
    suite.run_test("mixer_v2_process", test_mixer_v2_process)
    suite.run_test("mixer_v2_limiter", test_mixer_v2_limiter)
    
    # Melody V2 Tests
    print("[4] Testing Melody V2...")
    suite.run_test("melody_v2_import", test_melody_v2_import)
    suite.run_test("melody_v2_scales", test_melody_v2_scales)
    suite.run_test("melody_v2_emotions", test_melody_v2_emotions)
    suite.run_test("melody_v2_phrase", test_melody_v2_phrase)
    suite.run_test("melody_v2_full", test_melody_v2_full)
    
    # CLI V2 Tests
    print("[5] Testing CLI V2...")
    suite.run_test("cli_v2_import", test_cli_v2_import)
    suite.run_test("cli_v2_help", test_cli_v2_help)
    suite.run_test("cli_v2_suggest", test_cli_v2_suggest)
    
    # Print results
    return suite.summary()


# ===== REGRESSION CHECK =====

def check_original_modules():
    """Verify original modules still work"""
    print("\n" + "=" * 60)
    print("  REGRESSION CHECK - Original Modules")
    print("=" * 60)
    
    modules = [
        ('flstudio_ai_api', 'FLStudioAI'),
        ('super_engine', 'BeatGenerator'),
        ('drum_machine', 'DrumSequencer'),
        ('advanced_synth', 'AdvancedSynthesizer'),
        ('ai_melody_engine', 'AIMelodyComposer'),
        ('auto_mixer', 'AutoMixer'),
    ]
    
    all_ok = True
    for module, class_name in modules:
        try:
            mod = __import__(module, fromlist=[class_name])
            cls = getattr(mod, class_name)
            print(f"  [OK] {module}.{class_name}")
        except Exception as e:
            print(f"  ✗ {module}.{class_name}: {e}")
            all_ok = False
    
    return all_ok


if __name__ == "__main__":
    print("=" * 60)
    print("  TEST SUITE V2 - Level 1.6")
    print("=" * 60)
    
    # Run new module tests
    all_passed = run_all_tests()
    
    # Check regressions
    regression_ok = check_original_modules()
    
    # Final summary
    print("\n" + "=" * 60)
    if all_passed and regression_ok:
        print("  [OK] ALL TESTS PASSED - Level 1 Complete!")
    else:
        print("  [X] Some tests failed - needs attention")
    print("=" * 60)