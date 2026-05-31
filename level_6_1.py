"""
LEVEL 6.1 - ADVANCED SOUND DESIGN
=================================
- Sound design engine
- Preset generator
- Texture synthesizer
- Hybrid instruments

Advanced sound creation!
"""

import math
import random
from typing import List, Dict


class SoundDesignEngine:
    """Advanced sound design engine"""
    
    SYNTH_TYPES = ['subtractive', 'additive', 'fm', 'wavetable', 'granular', 'hybrid']
    
    def __init__(self):
        self.synth_type = 'subtractive'
        self.oscillators = []
        self.filters = []
        self.lfos = []
    
    def add_oscillator(self, waveform: str, freq: float, detune: float = 0):
        """Add oscillator"""
        osc = {
            'waveform': waveform,
            'frequency': freq,
            'detune': detune,
            'level': 1.0,
            'phase': 0
        }
        self.oscillators.append(osc)
        return osc
    
    def add_filter(self, filter_type: str, cutoff: float, resonance: float = 0):
        """Add filter"""
        filt = {
            'type': filter_type,  # lowpass, highpass, bandpass
            'cutoff': cutoff,
            'resonance': resonance,
            'env_amount': 0
        }
        self.filters.append(filt)
        return filt
    
    def generate(self, duration: float, sample_rate: int = 44100) -> List[float]:
        """Generate sound"""
        samples = int(duration * sample_rate)
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            sample = 0
            
            for osc in self.oscillators:
                freq = osc['frequency'] * (1 + osc['detune'] / 1000)
                
                if osc['waveform'] == 'sine':
                    val = math.sin(2 * math.pi * freq * t)
                elif osc['waveform'] == 'square':
                    val = 1 if (freq * t) % 1 < 0.5 else -1
                elif osc['waveform'] == 'saw':
                    val = 2 * ((freq * t) % 1) - 1
                elif osc['waveform'] == 'triangle':
                    val = 2 * abs((freq * t) % 1 - 0.5) - 1
                else:
                    val = math.sin(2 * math.pi * freq * t)
                
                sample += val * osc['level']
            
            # Apply filters
            for filt in self.filters:
                if filt['type'] == 'lowpass':
                    # Simple filter approximation
                    sample = sample * (1 - filt['cutoff'] / 20000)
            
            output.append(sample / max(len(self.oscillators), 1))
        
        return output


class PresetGenerator:
    """Generate synth presets"""
    
    CATEGORIES = ['bass', 'lead', 'pad', 'pluck', 'fx', 'keys', 'strings', 'brass']
    
    def __init__(self):
        self.presets = []
    
    def generate(self, category: str = 'lead') -> Dict:
        """Generate preset"""
        
        preset = {
            'name': '%s_%d' % (category, random.randint(100, 999)),
            'category': category,
            'oscillators': [],
            'filter': {},
            'envelope': {},
            'lfo': {}
        }
        
        # Generate based on category
        if category == 'bass':
            preset['oscillators'] = [
                {'waveform': 'saw', 'freq': 55, 'detune': 0},
                {'waveform': 'square', 'freq': 55, 'detune': -5}
            ]
            preset['filter'] = {'type': 'lowpass', 'cutoff': 800, 'resonance': 0.3}
            preset['envelope'] = {'attack': 0.01, 'decay': 0.2, 'sustain': 0.5, 'release': 0.3}
        
        elif category == 'lead':
            preset['oscillators'] = [
                {'waveform': 'saw', 'freq': 440, 'detune': 5},
                {'waveform': 'saw', 'freq': 440, 'detune': -5}
            ]
            preset['filter'] = {'type': 'lowpass', 'cutoff': 4000, 'resonance': 0.5}
            preset['envelope'] = {'attack': 0.05, 'decay': 0.1, 'sustain': 0.7, 'release': 0.2}
        
        elif category == 'pad':
            preset['oscillators'] = [
                {'waveform': 'sine', 'freq': 220, 'detune': 0},
                {'waveform': 'sine', 'freq': 222, 'detune': 0}
            ]
            preset['filter'] = {'type': 'lowpass', 'cutoff': 2000, 'resonance': 0.2}
            preset['envelope'] = {'attack': 0.5, 'decay': 0.3, 'sustain': 0.8, 'release': 1.0}
        
        elif category == 'pluck':
            preset['oscillators'] = [
                {'waveform': 'triangle', 'freq': 880, 'detune': 0}
            ]
            preset['filter'] = {'type': 'lowpass', 'cutoff': 6000, 'resonance': 0.4}
            preset['envelope'] = {'attack': 0.001, 'decay': 0.5, 'sustain': 0, 'release': 0.3}
        
        else:  # fx, keys, strings, brass
            preset['oscillators'] = [
                {'waveform': random.choice(['sine', 'saw', 'square']), 
                 'freq': random.randint(200, 800), 'detune': 0}
            ]
            preset['filter'] = {'type': 'lowpass', 'cutoff': 3000, 'resonance': 0.3}
            preset['envelope'] = {'attack': 0.1, 'decay': 0.2, 'sustain': 0.6, 'release': 0.5}
        
        self.presets.append(preset)
        return preset
    
    def generate_random(self) -> Dict:
        """Generate random preset"""
        category = random.choice(self.CATEGORIES)
        return self.generate(category)


class TextureSynthesizer:
    """Create textures and atmospheres"""
    
    TEXTURE_TYPES = ['drone', 'ambient', 'noise', 'granular', 'harmonic']
    
    def __init__(self):
        self.texture_type = 'ambient'
    
    def create_texture(self, texture_type: str, duration: float) -> List[float]:
        """Create texture"""
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        if texture_type == 'drone':
            return self._drone(samples, sample_rate)
        elif texture_type == 'ambient':
            return self._ambient(samples, sample_rate)
        elif texture_type == 'noise':
            return self._noise(samples)
        elif texture_type == 'granular':
            return self._granular(samples, sample_rate)
        else:
            return self._harmonic(samples, sample_rate)
    
    def _drone(self, samples: int, sr: int) -> List[float]:
        """Deep drone"""
        output = []
        for i in range(samples):
            t = i / sr
            val = (math.sin(2 * math.pi * 55 * t) + 
                   math.sin(2 * math.pi * 55.5 * t) * 0.5 +
                   math.sin(2 * math.pi * 110 * t) * 0.3) * 0.2
            output.append(val)
        return output
    
    def _ambient(self, samples: int, sr: int) -> List[float]:
        """Ambient texture"""
        output = []
        for i in range(samples):
            t = i / sr
            # Slow evolving texture
            env = 0.3 + 0.2 * math.sin(0.1 * t)
            val = random.uniform(-0.1, 0.1) * env
            val += math.sin(2 * math.pi * (200 + 50 * math.sin(0.5 * t)) * t) * 0.1
            output.append(val)
        return output
    
    def _noise(self, samples: int) -> List[float]:
        """Colored noise"""
        output = [random.uniform(-1, 1) * 0.1 for _ in range(samples)]
        return output
    
    def _granular(self, samples: int, sr: int) -> List[float]:
        """Granular texture"""
        output = []
        for i in range(samples):
            t = i / sr
            grain = random.uniform(-0.3, 0.3)
            env = math.exp(-((t % 0.1) * 10))
            output.append(grain * env)
        return output
    
    def _harmonic(self, samples: int, sr: int) -> List[float]:
        """Harmonic pad"""
        output = []
        for i in range(samples):
            t = i / sr
            val = sum(math.sin(2 * math.pi * (220 * (1 + h*0.01)) * t) / (h+1) 
                     for h in range(8)) * 0.05
            output.append(val)
        return output


class HybridInstrument:
    """Combine acoustic and synthetic"""
    
    def __init__(self):
        self.acoustic_part = None
        self.synth_part = None
    
    def create(self, acoustic_type: str, synth_type: str, ratio: float = 0.5) -> Dict:
        """Create hybrid instrument"""
        
        return {
            'acoustic': acoustic_type,  # piano, guitar, strings
            'synth': synth_type,  # saw, pad, fm
            'mix_ratio': ratio,
            'acoustic_params': self._get_acoustic_params(acoustic_type),
            'synth_params': self._get_synth_params(synth_type)
        }
    
    def _get_acoustic_params(self, atype: str) -> Dict:
        """Get acoustic params"""
        params = {
            'piano': {'decay': 0.8, 'brightness': 0.6},
            'guitar': {'decay': 0.5, 'brightness': 0.7},
            'strings': {'decay': 0.9, 'brightness': 0.4},
            'brass': {'decay': 0.3, 'brightness': 0.8}
        }
        return params.get(atype, {'decay': 0.5, 'brightness': 0.5})
    
    def _get_synth_params(self, stype: str) -> Dict:
        """Get synth params"""
        params = {
            'saw': {'filter': 2000, 'resonance': 0.4},
            'pad': {'filter': 1000, 'resonance': 0.2},
            'fm': {'mod_index': 2, 'ratio': 2},
            'wavetable': {'table': 'morph', 'position': 0.5}
        }
        return params.get(stype, {'filter': 1500, 'resonance': 0.3})


def demo():
    print("=" * 60)
    print("  LEVEL 6.1 - ADVANCED SOUND DESIGN")
    print("=" * 60)
    
    # Sound Design Engine
    print("\n[Sound Design Engine]")
    sde = SoundDesignEngine()
    sde.add_oscillator('saw', 220)
    sde.add_filter('lowpass', 2000, 0.5)
    audio = sde.generate(0.1)
    print("  Generated: %d samples" % len(audio))
    
    # Preset Generator
    print("\n[Preset Generator]")
    pg = PresetGenerator()
    for cat in ['bass', 'lead', 'pad', 'pluck']:
        p = pg.generate(cat)
        print("  %s: %s" % (cat, p['name']))
    
    # Texture Synthesizer
    print("\n[Texture Synthesizer]")
    ts = TextureSynthesizer()
    for tex in ['drone', 'ambient', 'noise']:
        audio = ts.create_texture(tex, 0.1)
        print("  %s: %d samples" % (tex, len(audio)))
    
    # Hybrid Instrument
    print("\n[Hybrid Instrument]")
    hi = HybridInstrument()
    hybrid = hi.create('piano', 'pad', 0.3)
    print("  Piano + Pad: ratio=%.1f" % hybrid['mix_ratio'])
    
    print("\n" + "=" * 60)
    print("  LEVEL 6.1 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()