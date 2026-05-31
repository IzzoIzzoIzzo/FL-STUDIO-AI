#!/usr/bin/env python3
"""SHADDAI - Quick Test"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from flstudio_ai_api import FLStudioAI
api = FLStudioAI()

# Just create the beat files - fast!
api.generate_beat("trap", 4)
api.generate_beat("house", 4)

print("BEATS CREATED!")
print("Check exports/ folder for .mid files")
print("Check audio/ folder for .wav files")
print("\nDONE!")