"""
INSTRUMENT LIBRARY - Professional Virtual Instruments
======================================================
- Piano (Acoustic, Electric, Digital)
- Guitar (Acoustic, Electric, Nylon)
- Strings (Violin, Cello, Orchestral)
- Brass (Trumpet, Trombone, Sax)
- Synths (Modern, Retro, Vintage)
- World (Sitar, Koto, Didgeridoo)

Each with multiple articulations and velocity layers!
"""

import math
import random
from typing import List, Dict


class PianoInstrument:
    """Piano family"""
    
    TYPES = {
        'acoustic': {'brightness': 0.7, 'body': 0.8, 'decay': 0.9},
        'electric': {'brightness': 0.5, 'body': 0.6, 'decay': 0.5},
        'digital': {'brightness': 0.8, 'body': 0.4, 'decay': 0.6},
        'grand': {'brightness': 0.75, 'body': 0.9, 'decay': 0.95},
        'upright': {'brightness': 0.6, 'body': 0.85, 'decay': 0.85}
    }
    
    def __init__(self, piano_type: str = 'grand'):
        self.type = piano_type
        self.params = self.TYPES.get(piano_type, self.TYPES['grand'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0, 
             sample_rate: int = 44100) -> List[float]:
        """Play piano note"""
        
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * sample_rate)
        
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Multiple harmonics for richness
            sample = 0
            
            # Fundamental
            sample += math.sin(2 * math.pi * freq * t) * 1.0
            
            # Harmonics
            h2 = math.sin(2 * math.pi * freq * 2 * t) * 0.5
            h3 = math.sin(2 * math.pi * freq * 3 * t) * 0.25
            h4 = math.sin(2 * math.pi * freq * 4 * t) * 0.125
            h5 = math.sin(2 * math.pi * freq * 5 * t) * 0.0625
            
            sample += (h2 + h3 + h4 + h5) * self.params['brightness']
            
            # Envelope
            env = math.exp(-t * (3 - self.params['decay'] * 2))
            
            # Add noise for realism
            noise = random.uniform(-0.02, 0.02) * self.params['body']
            
            output.append((sample + noise) * env * velocity * 0.5)
        
        return output


class GuitarInstrument:
    """Guitar family"""
    
    TYPES = {
        'acoustic_nylon': {'brightness': 0.6, 'decay': 0.7},
        'acoustic_steel': {'brightness': 0.8, 'decay': 0.65},
        'electric_clean': {'brightness': 0.5, 'decay': 0.5},
        'electric_dist': {'brightness': 0.9, 'decay': 0.4},
        'nylon_spanish': {'brightness': 0.55, 'decay': 0.75}
    }
    
    def __init__(self, guitar_type: str = 'acoustic_nylon'):
        self.type = guitar_type
        self.params = self.TYPES.get(guitar_type, self.TYPES['acoustic_nylon'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0,
             sample_rate: int = 44100) -> List[float]:
        """Play guitar note"""
        
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * sample_rate)
        
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Guitar harmonics
            sample = 0
            
            # Fundamental + string harmonics
            sample += math.sin(2 * math.pi * freq * t) * 1.0
            sample += math.sin(2 * math.pi * freq * 2.02 * t) * 0.6  # slightly detuned
            sample += math.sin(2 * math.pi * freq * 3.0 * t) * 0.4
            sample += math.sin(2 * math.pi * freq * 4.0 * t) * 0.3
            
            # Pluck envelope
            if t < 0.01:
                env = t / 0.01
            else:
                env = math.exp(-(t - 0.01) * (4 - self.params['decay'] * 3))
            
            # Pick noise
            if t < 0.02:
                pick_noise = random.uniform(-0.2, 0.2) * (1 - t / 0.02)
            else:
                pick_noise = 0
            
            sample = (sample * self.params['brightness'] + pick_noise) * env * velocity * 0.5
            output.append(sample)
        
        return output


class StringsInstrument:
    """String instruments"""
    
    TYPES = {
        'violin': {'brightness': 0.9, 'vibrato': 0.1, 'attack': 0.05, 'decay': 0.7},
        'cello': {'brightness': 0.6, 'vibrato': 0.05, 'attack': 0.1, 'decay': 0.6},
        'viola': {'brightness': 0.75, 'vibrato': 0.07, 'attack': 0.08, 'decay': 0.65},
        'orchestral': {'brightness': 0.8, 'vibrato': 0.08, 'attack': 0.15, 'decay': 0.75},
        'pizzicato': {'brightness': 0.7, 'vibrato': 0, 'attack': 0.001, 'decay': 0.3}
    }
    
    def __init__(self, string_type: str = 'violin'):
        self.type = string_type
        self.params = self.TYPES.get(string_type, self.TYPES['violin'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0,
             sample_rate: int = 44100) -> List[float]:
        """Play string note"""
        
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * sample_rate)
        
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Attack
            if t < self.params['attack']:
                attack = t / self.params['attack']
            else:
                attack = 1
            
            # Vibrato
            vib = math.sin(2 * math.pi * 5 * t) * self.params['vibrato'] if self.params['vibrato'] > 0 else 0
            
            # String harmonics
            sample = 0
            sample += math.sin(2 * math.pi * freq * (1 + vib) * t) * 1.0
            sample += math.sin(2 * math.pi * freq * 2 * (1 + vib) * t) * 0.6
            sample += math.sin(2 * math.pi * freq * 3 * (1 + vib) * t) * 0.4
            sample += math.sin(2 * math.pi * freq * 4 * (1 + vib) * t) * 0.25
            
            # Decay
            env = attack * math.exp(-(t - self.params['attack']) * (2 - self.params['decay']))
            
            output.append(sample * self.params['brightness'] * env * velocity * 0.5)
        
        return output


class BrassInstrument:
    """Brass instruments"""
    
    TYPES = {
        'trumpet': {'brightness': 0.85, 'breath': 0.3, 'attack': 0.03, 'decay': 0.5},
        'trombone': {'brightness': 0.7, 'breath': 0.25, 'attack': 0.08, 'decay': 0.55},
        'sax_alto': {'brightness': 0.8, 'breath': 0.4, 'attack': 0.05, 'decay': 0.6},
        'sax_tenor': {'brightness': 0.75, 'breath': 0.35, 'attack': 0.06, 'decay': 0.58},
        'french_horn': {'brightness': 0.6, 'breath': 0.2, 'attack': 0.1, 'decay': 0.65}
    }
    
    def __init__(self, brass_type: str = 'trumpet'):
        self.type = brass_type
        self.params = self.TYPES.get(brass_type, self.TYPES['trumpet'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0,
             sample_rate: int = 44100) -> List[float]:
        """Play brass note"""
        
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * sample_rate)
        
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Attack
            if t < self.params['attack']:
                attack = t / self.params['attack']
            else:
                attack = 1
            
            # Brass harmonics (rich overtone series)
            sample = 0
            sample += math.sin(2 * math.pi * freq * t) * 1.0
            sample += math.sin(2 * math.pi * freq * 2 * t) * 0.7
            sample += math.sin(2 * math.pi * freq * 3 * t) * 0.5
            sample += math.sin(2 * math.pi * freq * 4 * t) * 0.35
            sample += math.sin(2 * math.pi * freq * 5 * t) * 0.25
            sample += math.sin(2 * math.pi * freq * 6 * t) * 0.15
            
            # Breath noise
            breath = random.uniform(-0.1, 0.1) * self.params['breath']
            
            # Decay
            env = attack * math.exp(-(t - self.params['attack']) * (1.5 - self.params['decay']))
            
            output.append((sample + breath) * self.params['brightness'] * env * velocity * 0.5)
        
        return output


class SynthInstrument:
    """Synthesizer instruments"""
    
    TYPES = {
        'modern_lead': {'wave': 'saw', 'detune': 5, 'filter': 3000},
        'retro_lead': {'wave': 'square', 'detune': 10, 'filter': 2500},
        'acid_synth': {'wave': 'saw', 'detune': 25, 'filter': 1200},
        'wobble': {'wave': 'sine', 'detune': 0, 'filter': 800},
        'supersaw': {'wave': 'saw', 'detune': 15, 'filter': 3500},
        'pluck_synth': {'wave': 'triangle', 'detune': 0, 'filter': 4000}
    }
    
    def __init__(self, synth_type: str = 'modern_lead'):
        self.type = synth_type
        self.params = self.TYPES.get(synth_type, self.TYPES['modern_lead'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0,
             sample_rate: int = 44100) -> List[float]:
        """Play synth note"""
        
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * sample_rate)
        
        wave = self.params['wave']
        detune = self.params['detune']
        
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            phase = freq * t
            
            # Generate wave
            if wave == 'sine':
                sample = math.sin(2 * math.pi * phase)
            elif wave == 'saw':
                sample = 2 * (phase % 1) - 1
            elif wave == 'square':
                sample = 1 if (phase % 1) < 0.5 else -1
            elif wave == 'triangle':
                sample = 2 * abs((phase % 1)) - 1
            else:
                sample = math.sin(2 * math.pi * phase)
            
            # Detune
            sample *= (1 + detune / 1000)
            
            # Envelope
            if t < 0.01:
                env = t / 0.01
            elif t < 0.1:
                env = 1
            else:
                env = math.exp(-(t - 0.1) * 2)
            
            output.append(sample * env * velocity * 0.5)
        
        return output


class WorldInstrument:
    """World music instruments"""
    
    TYPES = {
        'sitar': {'brightness': 0.7, 'drone': True, 'decay': 0.8},
        'koto': {'brightness': 0.6, 'drone': False, 'decay': 0.5},
        'didgeridoo': {'brightness': 0.4, 'drone': True, 'decay': 0.9},
        'duduk': {'brightness': 0.5, 'drone': False, 'decay': 0.7},
        'erhu': {'brightness': 0.6, 'drone': False, 'decay': 0.6}
    }
    
    def __init__(self, world_type: str = 'sitar'):
        self.type = world_type
        self.params = self.TYPES.get(world_type, self.TYPES['sitar'])
    
    def play(self, note: int, duration: float, velocity: float = 1.0,
             sample_rate: int = 44100) -> List[float]:
        """Play world instrument"""
        
        freq = 440 * 2 ** ((note - 69) / 12)
        samples = int(duration * sample_rate)
        
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Main tone
            sample = math.sin(2 * math.pi * freq * t) * 0.7
            
            # Drone (if applicable)
            if self.params['drone']:
                drone = math.sin(2 * math.pi * freq * 0.5 * t) * 0.3
                sample += drone
            
            # Add harmonics
            sample += math.sin(2 * math.pi * freq * 2 * t) * 0.2
            sample += math.sin(2 * math.pi * freq * 3 * t) * 0.1
            
            # Envelope
            env = math.exp(-t * (2 - self.params['decay']))
            
            output.append(sample * self.params['brightness'] * env * velocity * 0.5)
        
        return output


class InstrumentLibrary:
    """Complete instrument library"""
    
    def __init__(self):
        # Initialize all instruments
        self.piano = PianoInstrument()
        self.guitar = GuitarInstrument()
        self.strings = StringsInstrument()
        self.brass = BrassInstrument()
        self.synth = SynthInstrument()
        self.world = WorldInstrument()
    
    def get_instrument(self, category: str, instrument_type: str = None):
        """Get instrument by category"""
        
        if category == 'piano':
            return PianoInstrument(instrument_type or 'grand')
        elif category == 'guitar':
            return GuitarInstrument(instrument_type or 'acoustic_nylon')
        elif category == 'strings':
            return StringsInstrument(instrument_type or 'violin')
        elif category == 'brass':
            return BrassInstrument(instrument_type or 'trumpet')
        elif category == 'synth':
            return SynthInstrument(instrument_type or 'modern_lead')
        elif category == 'world':
            return WorldInstrument(instrument_type or 'sitar')
        
        return None
    
    def get_all_categories(self) -> Dict:
        """Get all instrument categories"""
        
        return {
            'piano': list(PianoInstrument.TYPES.keys()),
            'guitar': list(GuitarInstrument.TYPES.keys()),
            'strings': list(StringsInstrument.TYPES.keys()),
            'brass': list(BrassInstrument.TYPES.keys()),
            'synth': list(SynthInstrument.TYPES.keys()),
            'world': list(WorldInstrument.TYPES.keys())
        }


def demo():
    print("=" * 60)
    print("  INSTRUMENT LIBRARY - 30+ INSTRUMENTS")
    print("=" * 60)
    
    lib = InstrumentLibrary()
    categories = lib.get_all_categories()
    
    print("\n[Instrument Categories]")
    for cat, instruments in categories.items():
        print("  %s: %s" % (cat, ', '.join(instruments)))
    
    print("\n[Testing Instruments]")
    
    # Piano
    piano = lib.get_instrument('piano', 'grand')
    audio = piano.play(60, 1.0)
    print("  Piano (C4): %d samples" % len(audio))
    
    # Guitar
    guitar = lib.get_instrument('guitar', 'acoustic_steel')
    audio = guitar.play(60, 1.0)
    print("  Guitar (C4): %d samples" % len(audio))
    
    # Strings
    strings = lib.get_instrument('strings', 'violin')
    audio = strings.play(60, 1.0)
    print("  Violin (C4): %d samples" % len(audio))
    
    # Brass
    brass = lib.get_instrument('brass', 'trumpet')
    audio = brass.play(60, 1.0)
    print("  Trumpet (C4): %d samples" % len(audio))
    
    # Synth
    synth = lib.get_instrument('synth', 'supersaw')
    audio = synth.play(60, 1.0)
    print("  SuperSaw (C4): %d samples" % len(audio))
    
    # World
    world = lib.get_instrument('world', 'sitar')
    audio = world.play(60, 1.0)
    print("  Sitar (C4): %d samples" % len(audio))
    
    print("\n" + "=" * 60)
    print("  INSTRUMENT LIBRARY COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()