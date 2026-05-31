import os
os.chdir(r"C:\Users\Brittany\OneDrive\Desktop\AI FL STUDIO BUILD")

print("SHADDAI Music Engine Starting...")
print("Motto: Everything works and is connected!")
print()

from flstudio_ai_api import FLStudioAI
api = FLStudioAI()

print("Generating TRAP beat...")
api.generate_beat("trap", 4)
print("Saved: exports/super_trap.mid")

print("Generating HOUSE beat...")
api.generate_beat("house", 4)
print("Saved: exports/super_house.mid")

print("Playing Synth note...")
api.real_synth.load_preset("lead")
api.real_synth.play(440, 1.0)
print("Generated audio!")

print()
print("=" * 50)
print("ALL DONE! Check these folders:")
print("  C:\\Users\\Brittany\\OneDrive\\Desktop\\AI FL STUDIO BUILD\\exports")
print("  C:\\Users\\Brittany\\OneDrive\\Desktop\\AI FL STUDIO BUILD\\audio")
print("=" * 50)