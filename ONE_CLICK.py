#!/usr/bin/env python3
"""
SHADDAI MUSIC ENGINE - ONE CLICK SYSTEM
Just double click this file to run!
Motto: Everything works and is connected!
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print(" SHADDAI MUSIC ENGINE v8.0")
print("="*60)
print("Motto: Everything works and is connected!")
print()

try:
    from flstudio_ai_api import FLStudioAI
    api = FLStudioAI()
    print("[OK] All modules loaded!")
except Exception as e:
    print(f"[ERROR] {e}")
    input("Press Enter to exit...")
    exit()

print("")
print("="*60)
print("  WHAT TO DO - Type a number and press Enter:")
print("="*60)
print("  1 - Generate TRAP beat")
print("  2 - Generate HOUSE beat")  
print("  3 - Generate HIPHOP beat")
print("  4 - Play SYNTH (real audio)")
print("  5 - Play PIANO (real audio)")
print("  6 - Play DRUMS (real audio)")
print("  7 - Generate FULL SONG")
print("  8 - List ALL presets")
print("  9 - Demo - do everything")
print("  0 - Exit")
print("="*60)

while True:
    choice = input("\nEnter choice: ").strip()
    
    if choice == "1":
        print("\nGenerating TRAP beat...")
        api.generate_beat("trap", 4)
        print("Done! File: exports/super_trap.mid")
    
    elif choice == "2":
        print("\nGenerating HOUSE beat...")
        api.generate_beat("house", 4)
        print("Done! File: exports/super_house.mid")
    
    elif choice == "3":
        print("\nGenerating HIPHOP beat...")
        api.generate_beat("hiphop", 4)
        print("Done! File: exports/super_hiphop.mid")
    
    elif choice == "4":
        print("\nPlaying SYNTH (real audio)...")
        api.real_synth.load_preset("lead")
        audio = api.real_synth.play(440, 1.0)
        print(f"Generated {len(audio)} samples!")
    
    elif choice == "5":
        print("\nPlaying PIANO (real audio)...")
        audio = api.extensive_instruments.generate_note("grand_piano", 60, 1.0, 1.0)
        print(f"Generated {len(audio)} samples!")
    
    elif choice == "6":
        print("\nPlaying DRUMS (real audio)...")
        kick = api.real_drums.play("kick")
        snare = api.real_drums.play("snare")
        hihat = api.real_drums.play("hihat")
        print(f"Kick: {len(kick)}, Snare: {len(snare)}, HiHat: {len(hihat)} samples!")
    
    elif choice == "7":
        print("\nGenerating FULL SONG...")
        api.generate_full_track("house", True, True)
        print("Done! Check audio/full_house_track.wav")
    
    elif choice == "8":
        print("\nAvailable Presets:")
        print(f"Extensive Synth: {len(api.extensive_synth.presets)} presets")
        print(f"Instruments: {len(api.extensive_instruments.instruments)} instruments")
        print("Some: " + ", ".join(list(api.extensive_synth.presets.keys())[:10]))
    
    elif choice == "9":
        print("\n=== DEMO ===")
        print("1. Beat...")
        api.generate_beat("trap", 4)
        print("2. Synth...")
        api.real_synth.load_preset("supersaw")
        api.real_synth.play(440, 1.0)
        print("3. Drums...")
        api.real_drums.play("kick")
        print("All done!")
    
    elif choice == "0":
        print("\nThanks!")
        break
    
    else:
        print("Invalid!")