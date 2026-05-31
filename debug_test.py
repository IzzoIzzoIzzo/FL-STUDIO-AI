"""Quick debug test for modules that hang"""
import sys
import traceback

# Test advanced_synth imports
print("[TEST] Importing advanced_synth...")
try:
    import advanced_synth
    print("  OK - imports work")
except Exception as e:
    print(f"  ERROR: {e}")
    traceback.print_exc()

# Test audio_analysis imports  
print("\n[TEST] Importing audio_analysis_engine...")
try:
    import audio_analysis_engine
    print("  OK - imports work")
except Exception as e:
    print(f"  ERROR: {e}")
    traceback.print_exc()

# Test auto_mixer imports
print("\n[TEST] Importing auto_mixer...")
try:
    import auto_mixer
    print("  OK - imports work")
except Exception as e:
    print(f"  ERROR: {e}")
    traceback.print_exc()

print("\n[TEST] Done!")