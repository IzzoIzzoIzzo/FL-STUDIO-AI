#!/usr/bin/env python3
"""
SHADDAI - AUTO RUN ON DOUBLE CLICK
This runs automatically - no typing needed!
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from flstudio_ai_api import FLStudioAI
    api = FLStudioAI()
    print("OK - Modules loaded")
except Exception as e:
    print(f"ERROR: {e}")
    exit()

# Auto run everything
print("1. Generating TRAP beat...")
api.generate_beat("trap", 4)

print("2. Generating HOUSE beat...")
api.generate_beat("house", 4)

print("3. Playing Synth...")
api.real_synth.load_preset("lead")
api.real_synth.play(440, 1.0)

print("4. Playing Piano...")
api.extensive_instruments.generate_note("grand_piano", 60, 1.0, 1.0)

print("5. Playing Drums...")
api.real_drums.play("kick")

print("\n" + "="*50)
print("ALL DONE!")
print("Files are in exports/ and audio/ folders")
print("="*50)