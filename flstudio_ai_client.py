"""
FL Studio AI Pro - Test & Demo Client
Demonstrates all features of the AI beat making system
"""

import json
import urllib.request
import urllib.error
import time


class FLStudioAIClient:
    def __init__(self, host="localhost", port=5000):
        self.base = f"http://{host}:{port}"

    def request(self, endpoint, data=None):
        url = f"{self.base}{endpoint}"
        headers = {"Content-Type": "application/json"}
        req_data = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST" if data else "GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def health(self):
        return self.request("/health")

    def generate_track(self, style="house", key=60, scale="minor", bars=16, tempo=120):
        return self.request("/generate/track", {
            "style": style, "key": key, "scale": scale, "bars": bars, "tempo": tempo,
            "elements": {"drums": True, "bass": True, "melody": True, "chords": True, "arps": True}
        })

    def generate_drums(self, style="trap", bars=2, complexity=4):
        return self.request("/generate/drums", {
            "style": style, "bars": bars, "complexity": complexity, "swing": 0.1, "humanize": 0.05
        })

    def generate_bass(self, root=36, scale="minor", length=8, pattern="rolling"):
        return self.request("/generate/bass", {"root": root, "scale": scale, "length": length, "pattern": pattern})

    def generate_melody(self, key=60, scale="dorian", length=8, contour="ascending"):
        return self.request("/generate/melody", {"key": key, "scale": scale, "length": length, "contour": contour})

    def generate_chords(self, key=60, style="neo_soul", bars=8, voicing="jazz"):
        return self.request("/generate/chords", {"key": key, "style": style, "bars": bars, "voicing": voicing})

    def generate_arps(self, root=60, chord_type="major", pattern="updown", octaves=3):
        return self.request("/generate/arps", {"root": root, "chord_type": chord_type, "pattern": pattern, "octaves": octaves})

    def generate_arrangement(self, style="house", bars=32):
        return self.request("/generate/arrangement", {"style": style, "bars": bars})

    def polyrhythm(self, primary=4, secondary=3, steps=12):
        return self.request("/generate/polyrhythm", {"primary": primary, "secondary": secondary, "steps": steps})

    def binary_pattern(self, bars=1, density=0.5):
        return self.request("/generate/binary", {"bars": bars, "density": density})

    def set_tempo(self, bpm):
        return self.request("/tempo", {"bpm": bpm})

    def tempo_ramp(self, start=100, end=160, bars=8, curve="exponential"):
        return self.request("/tempo/ramp", {"start": start, "end": end, "bars": bars, "curve": curve})

    def time_signature(self, num=4, denom=4):
        return self.request("/time_signature", {"numerator": num, "denominator": denom})

    def key_detect(self, notes):
        return self.request("/key/detect", {"notes": notes})

    def create_osc(self, name="lead", waveform="sawtooth", freq=440):
        return self.request("/synth/create_osc", {"name": name, "waveform": waveform, "frequency": freq})

    def create_envelope(self, name="amp", attack=0.01, decay=0.1, sustain=0.7, release=0.3):
        return self.request("/synth/create_envelope", {"name": name, "attack": attack, "decay": decay, "sustain": sustain, "release": release})

    def create_filter(self, name="main", ftype="lowpass", cutoff=1000, resonance=0.5):
        return self.request("/synth/create_filter", {"name": name, "type": ftype, "cutoff": cutoff, "resonance": resonance})

    def set_compressor(self, threshold=-20, ratio=4, attack=0.01, release=0.1):
        return self.request("/effects/compressor", {"threshold": threshold, "ratio": ratio, "attack": attack, "release": release})

    def set_reverb(self, size=0.5, decay=2, damping=0.5, wet=0.3):
        return self.request("/effects/reverb", {"size": size, "decay": decay, "damping": damping, "wet": wet})

    def set_delay(self, time=0.5, feedback=0.3, wet=0.3):
        return self.request("/effects/delay", {"time": time, "feedback": feedback, "wet": wet})

    def get_effects_chain(self):
        return self.request("/effects/chain")

    def export_midi(self, track_data, filename="export.mid", tempo=120):
        return self.request("/export/midi", {"track_data": track_data, "filename": filename, "tempo": tempo})


def demo():
    print("=" * 60)
    print("FL STUDIO AI PRO - Client Demo")
    print("=" * 60)

    client = FLStudioAIClient()

    print("\n[1] Health Check...")
    health = client.health()
    print(f"    Status: {health}")

    print("\n[2] Generating Full Track...")
    track = client.generate_track("trap", 60, "minor", 8, 140)
    print(f"    Style: {track['metadata']['style']}")
    print(f"    Key: {track['metadata']['key_name']} {track['metadata']['scale']}")
    print(f"    Tempo: {track['metadata']['tempo']} BPM")
    print(f"    Bars: {track['metadata']['bars']}")
    print(f"    Drums: {len(track['drums']['midi'])} events")
    print(f"    Bass: {len(track['bass']['notes'])} notes")
    print(f"    Melody: {len(track['melody']['notes'])} notes")
    print(f"    Chords: {len(track['chords']['chords'])} progressions")

    print("\n[3] Generating Drums...")
    drums = client.generate_drums("dnb", 2, 4)
    print(f"    Style: {drums['style']}")
    print(f"    Steps: {drums['steps']}")
    print(f"    Tracks: {list(drums['pattern'].keys())}")

    print("\n[4] Generating Bass...")
    bass = client.generate_bass(36, "phrygian", 16, "wobble")
    print(f"    Root: {bass['root_name']}")
    print(f"    Scale: {bass['scale']}")
    print(f"    Pattern: {bass['pattern']}")
    print(f"    Notes: {len(bass['notes'])}")

    print("\n[5] Generating Melody...")
    melody = client.generate_melody(60, "harmonic_minor", 12, "arch")
    print(f"    Key: {melody['key_name']}")
    print(f"    Scale: {melody['scale']}")
    print(f"    Contour: {melody['contour']}")
    print(f"    Phrases: {len(melody['phrases'])}")

    print("\n[6] Generating Chords...")
    chords = client.generate_chords(60, "jazz", 8, "piano")
    print(f"    Key: {chords['key_name']}")
    print(f"    Style: {chords['style']}")
    print(f"    Voicing: {chords['voicing']}")

    print("\n[7] Generating Arps...")
    arps = client.generate_arps(60, "minor", "roller", 3)
    print(f"    Chord: {arps['chord_root_name']} {arps['chord_type']}")
    print(f"    Pattern: {arps['pattern']}")
    print(f"    Notes: {len(arps['notes'])}")

    print("\n[8] Polyrhythm...")
    poly = client.polyrhythm(5, 3, 15)
    print(f"    Ratio: {poly['ratio']}")
    print(f"    Primary hits: {poly['primary_hits']}")
    print(f"    Secondary hits: {poly['secondary_hits']}")

    print("\n[9] Binary Pattern...")
    binary = client.binary_pattern(1, 0.6)
    print(f"    Binary: {binary['binary_string'][:48]}...")
    print(f"    Hex: {binary['hex']}")

    print("\n[10] Tempo Ramp...")
    ramp = client.tempo_ramp(100, 180, 8, "exponential")
    print(f"    Points: {len(ramp['ramp'])}")
    print(f"    Curve: {ramp['curve']}")

    print("\n[11] Key Detection...")
    key = client.key_detect([60, 62, 64, 67, 71, 74])
    print(f"    Detected: {key['note']} major")

    print("\n[12] Synth Creation...")
    osc = client.create_osc("lead_saw", "sawtooth", 220)
    env = client.create_envelope("pad_env", 0.5, 0.3, 0.6, 1.0)
    filt = client.create_filter("lowpass", "lowpass", 2000, 0.7)
    print(f"    Oscillator: {osc['waveform']} @ {osc['frequency']}Hz")
    print(f"    Envelope: A={env['attack']}s D={env['decay']}s S={env['sustain']} R={env['release']}s")
    print(f"    Filter: {filt['type']} @ {filt['cutoff']}Hz Q={filt['resonance']}")

    print("\n[13] Effects Chain...")
    comp = client.set_compressor(-18, 6, 0.005, 0.2)
    rev = client.set_reverb(0.7, 3, 0.4, 0.25)
    delay = client.set_delay(0.375, 0.4, 0.2)
    chain = client.get_effects_chain()
    print(f"    Compressor: {comp['compressor']['ratio']}:1, {comp['compressor']['threshold']}dB")
    print(f"    Reverb: {rev['reverb']['size']} size, {rev['reverb']['decay']}s decay")
    print(f"    Delay: {delay['delay']['time']}s, {delay['delay']['feedback']*100}% feedback")

    print("\n" + "=" * 60)
    print("ALL DEMO TESTS COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    demo()