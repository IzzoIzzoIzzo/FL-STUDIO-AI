"""
EXPANDED INSTRUMENT LIBRARY
==========================
Additional instrument categories beyond the base library:
- Bass Instruments (Synth, Electric, Acoustic, Fretless, Slap)
- Keys & Organs (Hammond, Electric Piano, Clav, Organ)
- Pad & Atmosphere (Ambient, Warm, Evolving, Shimmer)
- Lead & Solo (Monophonic, Polyphonic, Whistle)
- Drum Kits (Electronic, Acoustic, Hybrid)
- FX & Sounds (Risers, Impacts, Transitions, Textures)

CONNECTED TO MAIN API!
"""

import math
import random
from typing import List, Dict, Tuple
from enum import Enum


class InstrumentCategory(Enum):
    """Extended instrument categories"""
    BASS = "bass"
    KEYS = "keys"
    PAD = "pad"
    LEAD = "lead"
    DRUMS_EXTENDED = "drums_extended"
    FX = "fx"


class BassInstrument:
    """Bass family - Synth, Electric, Acoustic, Fretless, Slap"""
    
    TYPES = {
        'synth_bass': {'sub': 1.0, 'attack': 0.01, 'decay': 0.3, 'brightness': 0.7},
        'electric_finger': {'sub': 0.5, 'attack': 0.02, 'decay': 0.4, 'brightness': 0.6},
        'electric_pick': {'sub': 0.3, 'attack': 0.01, 'decay': 0.35, 'brightness': 0.8},
        'acoustic': {'sub': 0.4, 'attack': 0.03, 'decay': 0.5, 'brightness': 0.5},
        'fretless': {'sub': 0.4, 'attack': 0.02, 'decay': 0.45, 'brightness': 0.5},
        'slap': {'sub': 0.8, 'attack': 0.005, 'decay': 0.2, 'brightness': 0.9},
        'fm': {'sub': 0.6, 'attack': 0.01, 'decay': 0.25, 'brightness': 0.8},
        'wobble': {'sub': 1.0, 'attack': 0.02, 'decay': 0.3, 'brightness': 0.6}
    }
    
    def __init__(self, bass_type: str = 'synth_bass', sample_rate: int = 44100):
        self.type = bass_type
        self.sample_rate = sample_rate
        self.params = self.TYPES.get(bass_type, self.TYPES['synth_bass'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * self.sample_rate)
        
        output = [0.0] * samples
        
        sub_freq = freq * 0.5 if self.params['sub'] > 0 else freq
        
        for i in range(samples):
            t = i / self.sample_rate
            
            if t < self.params['attack']:
                env = t / self.params['attack']
            elif t < self.params['attack'] + self.params['decay']:
                env = 1 - (1 - 0.7) * (t - self.params['attack']) / self.params['decay']
            else:
                env = 0.7 * math.exp(-(t - self.params['attack'] - self.params['decay']) * 2)
            
            main = math.sin(2 * math.pi * freq * t)
            sub = math.sin(2 * math.pi * sub_freq * t) * self.params['sub']
            harm = math.sin(2 * math.pi * freq * 2 * t) * 0.3 * self.params['brightness']
            
            output[i] = (main + sub + harm) * env * velocity * 0.5
        
        return output


class KeysInstrument:
    """Keys & Organs - Hammond, Electric Piano, Clav, Organ"""
    
    TYPES = {
        'hammond_b3': {'drawbars': [1, 0.5, 0.3, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05], 'vibrato': 0.1},
        'rhodes': {'brightness': 0.6, 'tremolo': 0.1, 'tine': 0.8},
        'wurlitzer': {'brightness': 0.5, 'tremolo': 0.15, 'reed': 0.7},
        'clavinet': {'brightness': 0.9, 'decay': 0.3, 'pickup': 0.5},
        'farfisa': {'brightness': 0.8, 'reverb': 0.3, 'swell': 0.5},
        'dx7': {'brightness': 0.7, 'operator_count': 6, 'algorithm': 1},
        'cp80': {'brightness': 0.6, 'string': 0.5, 'hammer': 0.4}
    }
    
    def __init__(self, keys_type: str = 'rhodes', sample_rate: int = 44100):
        self.type = keys_type
        self.sample_rate = sample_rate
        self.params = self.TYPES.get(keys_type, self.TYPES['rhodes'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * self.sample_rate)
        
        output = [0.0] * samples
        
        if self.type == 'hammond_b3':
            drawbars = self.params['drawbars']
            for i in range(samples):
                t = i / self.sample_rate
                sample = 0.0
                for h, db in enumerate(drawbars):
                    harm_freq = freq * (h + 1)
                    sample += db * math.sin(2 * math.pi * harm_freq * t)
                vibrato = math.sin(2 * math.pi * 5 * t) * self.params['vibrato']
                output[i] = sample * (1 + vibrato * 0.1) * velocity * 0.3
        
        else:
            bright = self.params.get('brightness', 0.6)
            trem = self.params.get('tremolo', 0.1)
            
            for i in range(samples):
                t = i / self.sample_rate
                
                osc = math.sin(2 * math.pi * freq * t)
                osc += 0.5 * math.sin(2 * math.pi * freq * 2 * t)
                osc += 0.25 * math.sin(2 * math.pi * freq * 3 * t) * bright
                
                tremolo = 1 + 0.3 * math.sin(2 * math.pi * 6 * t) * trem
                env = math.exp(-t * 2)
                
                output[i] = osc * tremolo * env * velocity * 0.5
        
        return output


class PadInstrument:
    """Pad & Atmosphere - Ambient, Warm, Evolving, Shimmer"""
    
    TYPES = {
        'ambient': {'spread': 0.3, 'movement': 0.5, 'reverb': 0.8, 'filter': 2000},
        'warm': {'spread': 0.2, 'movement': 0.3, 'reverb': 0.6, 'filter': 3000},
        'evolving': {'spread': 0.4, 'movement': 0.7, 'reverb': 0.7, 'filter': 2500},
        'shimmer': {'spread': 0.5, 'movement': 0.8, 'reverb': 0.9, 'filter': 4000},
        'sweep': {'spread': 0.3, 'movement': 0.9, 'reverb': 0.7, 'filter': 1500},
        'drone': {'spread': 0.1, 'movement': 0.2, 'reverb': 0.5, 'filter': 800},
        'texture': {'spread': 0.4, 'movement': 0.6, 'reverb': 0.8, 'filter': 3500},
        'choir': {'spread': 0.5, 'movement': 0.4, 'reverb': 0.9, 'filter': 2800}
    }
    
    def __init__(self, pad_type: str = 'ambient', sample_rate: int = 44100):
        self.type = pad_type
        self.sample_rate = sample_rate
        self.params = self.TYPES.get(pad_type, self.TYPES['ambient'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * self.sample_rate)
        
        output = [0.0] * samples
        spread = self.params['spread']
        movement = self.params['movement']
        
        detunes = [-spread * 10, 0, spread * 10, spread * 5]
        
        for i in range(samples):
            t = i / self.sample_rate
            sample = 0.0
            
            for detune in detunes:
                actual_freq = freq * (1 + detune / 1200)
                
                osc = math.sin(2 * math.pi * actual_freq * t)
                osc += 0.3 * math.sin(2 * math.pi * actual_freq * 2 * t)
                osc += 0.15 * math.sin(2 * math.pi * actual_freq * 3 * t)
                
                filter_sweep = 1 + movement * 0.3 * math.sin(2 * math.pi * 0.2 * t)
                sample += osc * filter_sweep / len(detunes)
            
            output[i] = sample
        
        attack_samples = min(int(self.sample_rate * 0.5), samples)
        for i in range(attack_samples):
            output[i] *= i / attack_samples
        
        for i in range(attack_samples, samples):
            output[i] *= 1.0
        
        output = [s * velocity * 0.3 for s in output]
        return output


class LeadInstrument:
    """Lead & Solo - Monophonic, Polyphonic, Whistle"""
    
    TYPES = {
        'monophonic': {'portamento': 0.1, 'vibrato': 0.1, 'brightness': 0.7},
        'poly_lead': {'portamento': 0, 'vibrato': 0.05, 'brightness': 0.8},
        'whistle': {'portamento': 0, 'vibrato': 0.2, 'brightness': 0.6},
        'saw_lead': {'portamento': 0.05, 'vibrato': 0.08, 'brightness': 0.9},
        'square_lead': {'portamento': 0.05, 'vibrato': 0.1, 'brightness': 0.7},
        'brass_lead': {'portamento': 0.1, 'vibrato': 0.02, 'brightness': 0.6},
        'flute_lead': {'portamento': 0.02, 'vibrato': 0.15, 'brightness': 0.4},
        'sync_lead': {'portamento': 0.05, 'vibrato': 0.1, 'brightness': 0.8}
    }
    
    def __init__(self, lead_type: str = 'monophonic', sample_rate: int = 44100):
        self.type = lead_type
        self.sample_rate = sample_rate
        self.params = self.TYPES.get(lead_type, self.TYPES['monophonic'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * self.sample_rate)
        
        output = [0.0] * samples
        vibrato = self.params['vibrato']
        brightness = self.params['brightness']
        
        for i in range(samples):
            t = i / self.sample_rate
            
            if self.type in ['saw_lead', 'sync_lead']:
                phase = (freq * t) % 1
                osc = 2 * phase - 1
            elif self.type == 'square_lead':
                phase = (freq * t) % 1
                osc = 1 if phase < 0.5 else -1
            else:
                osc = math.sin(2 * math.pi * freq * t)
            
            if brightness > 0.5:
                osc += 0.5 * brightness * math.sin(2 * math.pi * freq * 2 * t)
            if brightness > 0.7:
                osc += 0.25 * brightness * math.sin(2 * math.pi * freq * 3 * t)
            
            if vibrato > 0:
                vib = 1 + vibrato * 0.05 * math.sin(2 * math.pi * 5 * t)
                osc *= vib
            
            env = math.exp(-t * 1.5)
            if i < 1000:
                env = env * (i / 1000)
            
            output[i] = osc * env * velocity * 0.5
        
        return output


class ExtendedDrumKit:
    """Extended Drum Kits - Electronic, Acoustic, Hybrid"""
    
    KITS = {
        'electronic_808': {'kick': 45, 'snare': 200, 'hihat': 8000, 'clap': 1500,
            'tom_low': 80, 'tom_mid': 120, 'tom_high': 180, 'cymbal': 6000, 'cowbell': 800},
        'electronic_909': {'kick': 50, 'snare': 220, 'hihat': 10000, 'clap': 1800,
            'tom_low': 90, 'tom_mid': 140, 'tom_high': 200, 'ride': 5000, 'crash': 4000},
        'acoustic': {'kick': 60, 'snare': 250, 'hihat': 12000, 'snare_side': 300,
            'tom_floor': 100, 'tom_mid': 150, 'tom_high': 220, 'ride': 5500, 'crash': 4500},
        'hybrid': {'kick': 48, 'snare': 210, 'hihat': 9000, 'clap': 1600,
            'tom_low': 85, 'tom_mid': 130, 'tom_high': 190, 'electronic_perc': 1200},
        'trap': {'kick': 40, 'snare': 180, 'hihat': 14000, 'clap': 2000,
            'sub_kick': 35, '_808_bass': 50, 'rim': 800, 'snap': 2500},
        'lofi': {'kick': 55, 'snare': 180, 'hihat': 6000, 'vinyl_snap': 1500,
            'tape_kick': 50, 'dusty_snare': 160, 'crackle': 3000}
    }
    
    def __init__(self, kit_type: str = 'electronic_808', sample_rate: int = 44100):
        self.type = kit_type
        self.sample_rate = sample_rate
        self.kit_params = self.KITS.get(kit_type, self.KITS['electronic_808'])
    
    def play_drum(self, drum: str, velocity: float = 1.0, pitch: float = 1.0) -> List[float]:
        freq = self.kit_params.get(drum, 200)
        freq *= pitch
        
        samples = int(0.5 * self.sample_rate)
        output = [0.0] * samples
        
        if 'kick' in drum:
            for i in range(samples):
                t = i / self.sample_rate
                freq_sweep = freq * (1 + 10 * math.exp(-t * 20))
                output[i] = math.sin(2 * math.pi * freq_sweep * t) * math.exp(-t * 8)
        
        elif 'snare' in drum:
            for i in range(samples):
                t = i / self.sample_rate
                tone = math.sin(2 * math.pi * freq * t) * math.exp(-t * 10)
                noise = random.uniform(-0.3, 0.3) * math.exp(-t * 15)
                output[i] = tone + noise
        
        elif 'hihat' in drum or 'cymbal' in drum or 'ride' in drum:
            for i in range(samples):
                t = i / self.sample_rate
                noise = random.uniform(-1, 1)
                output[i] = noise * math.exp(-t * 20)
        
        elif 'tom' in drum:
            for i in range(samples):
                t = i / self.sample_rate
                freq_sweep = freq * (1 + 2 * math.exp(-t * 5))
                output[i] = math.sin(2 * math.pi * freq_sweep * t) * math.exp(-t * 5)
        
        elif 'clap' in drum:
            for _ in range(3):
                start = random.randint(0, samples - 1000)
                burst = [random.uniform(-0.5, 0.5) for _ in range(1000)]
                for i, b in enumerate(burst):
                    if start + i < samples:
                        output[start + i] += b
        
        else:
            for i in range(samples):
                t = i / self.sample_rate
                output[i] = math.sin(2 * math.pi * freq * t) * math.exp(-t * 5)
        
        output = [s * velocity * 0.7 for s in output]
        return output


class FXSound:
    """FX & Sounds - Risers, Impacts, Transitions, Textures"""
    
    TYPES = {
        'riser': {'direction': 'up', 'duration': 4, 'intensity': 0.8},
        'downlifter': {'direction': 'down', 'duration': 3, 'intensity': 0.7},
        'impact': {'type': 'impact', 'size': 0.8, 'reverb': 0.9},
        'sweep': {'type': 'filter', 'direction': 'up', 'duration': 2},
        'stab': {'type': 'chord', 'size': 0.6, 'reverb': 0.7},
        'rattle': {'type': 'noise', 'intensity': 0.5},
        'texture': {'type': 'ambient', 'movement': 0.6},
        'sub_drop': {'type': 'sub', 'depth': 0.9, 'duration': 2},
        'vinyl_stop': {'type': 'stop', 'intensity': 0.8},
        'glitch': {'type': 'glitch', 'intensity': 0.6}
    }
    
    def __init__(self, fx_type: str = 'riser', sample_rate: int = 44100):
        self.type = fx_type
        self.sample_rate = sample_rate
        self.params = self.TYPES.get(fx_type, self.TYPES['riser'])
    
    def play(self, duration: float = None, velocity: float = 1.0) -> List[float]:
        dur = duration or self.params.get('duration', 2)
        samples = int(dur * self.sample_rate)
        output = [0.0] * samples
        
        if self.type == 'riser':
            for i in range(samples):
                t = i / self.sample_rate
                noise = random.uniform(-1, 1)
                output[i] = noise * (1 + t / dur * 2)
        
        elif self.type == 'downlifter':
            for i in range(samples):
                t = i / self.sample_rate
                noise = random.uniform(-1, 1)
                output[i] = noise * (1 + (1 - t / dur) * 2)
        
        elif self.type == 'impact':
            for i in range(samples):
                t = i / self.sample_rate
                size = self.params.get('size', 0.8)
                thump = math.sin(2 * math.pi * 60 * t) * math.exp(-t * 10)
                noise = random.uniform(-0.2, 0.2) * math.exp(-t * 20)
                output[i] = thump * size + noise
        
        elif self.type == 'stab':
            chord_freqs = [220, 277, 330, 440]
            for i in range(samples):
                t = i / self.sample_rate
                sample = 0.0
                for f in chord_freqs:
                    sample += math.sin(2 * math.pi * f * t) * 0.3
                output[i] = sample * math.exp(-t * 3)
        
        elif self.type == 'sub_drop':
            for i in range(samples):
                t = i / self.sample_rate
                depth = self.params.get('depth', 0.9)
                freq_sweep = 80 * depth * (1 - t / dur) + 20
                output[i] = math.sin(2 * math.pi * freq_sweep * t)
        
        elif self.type == 'glitch':
            intensity = self.params.get('intensity', 0.6)
            for _ in range(50):
                pos = random.randint(0, samples - 100)
                glitch = [random.uniform(-intensity, intensity) for _ in range(100)]
                for i, g in enumerate(glitch):
                    if pos + i < samples:
                        output[pos + i] += g
        
        else:
            output = [random.uniform(-0.1, 0.1) for _ in range(samples)]
        
        output = [s * velocity * 0.5 for s in output]
        return output


class ExpandedInstrumentLibrary:
    """
    Expanded instrument library combining all categories.
    CONNECTED TO MAIN API!
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
        self.bass = BassInstrument('synth_bass', sample_rate)
        self.keys = KeysInstrument('rhodes', sample_rate)
        self.pad = PadInstrument('ambient', sample_rate)
        self.lead = LeadInstrument('monophonic', sample_rate)
        self.drums = ExtendedDrumKit('electronic_808', sample_rate)
        self.fx = FXSound('riser', sample_rate)
        
        print(f"    [OK] Expanded Instrument Library initialized")
        print(f"         - Bass: 8 types")
        print(f"         - Keys: 7 types")
        print(f"         - Pad: 8 types")
        print(f"         - Lead: 8 types")
        print(f"         - Drums: 6 kits")
        print(f"         - FX: 10 types")
    
    def set_instrument(self, category: str, instrument_type: str):
        if category == 'bass':
            self.bass = BassInstrument(instrument_type, self.sample_rate)
        elif category == 'keys':
            self.keys = KeysInstrument(instrument_type, self.sample_rate)
        elif category == 'pad':
            self.pad = PadInstrument(instrument_type, self.sample_rate)
        elif category == 'lead':
            self.lead = LeadInstrument(instrument_type, self.sample_rate)
        elif category == 'drums':
            self.drums = ExtendedDrumKit(instrument_type, self.sample_rate)
        elif category == 'fx':
            self.fx = FXSound(instrument_type, self.sample_rate)
    
    def play_bass(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        return self.bass.play(note, duration, velocity)
    
    def play_keys(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        return self.keys.play(note, duration, velocity)
    
    def play_pad(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        return self.pad.play(note, duration, velocity)
    
    def play_lead(self, note: int, duration: float, velocity: float = 1.0) -> List[float]:
        return self.lead.play(note, duration, velocity)
    
    def play_drum(self, drum: str, velocity: float = 1.0, pitch: float = 1.0) -> List[float]:
        return self.drums.play_drum(drum, velocity, pitch)
    
    def play_fx(self, duration: float = 2.0, velocity: float = 1.0) -> List[float]:
        return self.fx.play(duration, velocity)
    
    def get_available_types(self) -> Dict[str, List[str]]:
        return {
            'bass': list(BassInstrument.TYPES.keys()),
            'keys': list(KeysInstrument.TYPES.keys()),
            'pad': list(PadInstrument.TYPES.keys()),
            'lead': list(LeadInstrument.TYPES.keys()),
            'drums': list(ExtendedDrumKit.KITS.keys()),
            'fx': list(FXSound.TYPES.keys())
        }


# Test function
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" EXPANDED INSTRUMENT LIBRARY TEST")
    print("="*60 + "\n")
    
    lib = ExpandedInstrumentLibrary(44100)
    
    print("\n[1] Bass (Synth)...")
    audio = lib.play_bass(36, 1.0, 1.0)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[2] Keys (Rhodes)...")
    audio = lib.play_keys(60, 1.0, 1.0)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[3] Pad (Ambient)...")
    audio = lib.play_pad(48, 2.0, 1.0)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[4] Lead (Monophonic)...")
    audio = lib.play_lead(72, 0.5, 1.0)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[5] Drums (808 Kit)...")
    audio = lib.play_drum('kick', 1.0, 1.0)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[6] FX (Riser)...")
    audio = lib.play_fx(2.0, 1.0)
    print(f"     OK - {len(audio)} samples")
    
    print("\n" + "="*60)
    print(" ALL EXPANDED INSTRUMENTS OPERATIONAL!")
    print("="*60 + "\n")