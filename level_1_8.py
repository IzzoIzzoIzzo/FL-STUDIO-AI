"""
LEVEL 1.8 - ADVANCED SYNTH ENGINE V3
====================================
Deep synthesis features:
- Wavetable synthesis
- Physical modeling
- Vector synthesis
- Sample playback
- Hybrid mode

Ultimate synth engine!
"""

import math
import random
from typing import List, Dict, Optional


class WavetableSynthesizer:
    """Advanced wavetable synthesis"""
    
    TABLES = ['saw', 'square', 'triangle', 'sine', 'noise', 'morph1', 'morph2', 'custom']
    
    def __init__(self):
        self.current_table = 'saw'
        self.position = 0.0
        self.morph_speed = 0.0
        self.tables = self._init_tables()
    
    def _init_tables(self) -> Dict:
        """Initialize wavetables"""
        tables = {}
        
        # Create 256-point wavetables
        for name in self.TABLES:
            table = []
            for i in range(256):
                t = i / 256
                if name == 'saw':
                    val = 2 * t - 1
                elif name == 'square':
                    val = 1 if t < 0.5 else -1
                elif name == 'triangle':
                    val = 4 * t - 2 if t < 0.5 else 4 * (1 - t) - 2
                elif name == 'sine':
                    val = math.sin(2 * math.pi * t)
                elif name == 'noise':
                    val = random.uniform(-1, 1)
                else:  # morph
                    val = math.sin(2 * math.pi * t) * (0.5 + 0.5 * math.sin(4 * math.pi * t))
                table.append(val)
            tables[name] = table
        
        return tables
    
    def set_table(self, name: str):
        """Set wavetable"""
        if name in self.TABLES:
            self.current_table = name
    
    def set_morph(self, speed: float):
        """Set morph speed"""
        self.morph_speed = speed
    
    def play(self, freq: float, duration: float, sample_rate: int = 44100) -> List[float]:
        """Play wavetable"""
        
        table = self.tables[self.current_table]
        samples = int(duration * sample_rate)
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Calculate position in table
            pos = (freq * t * 256) % 256
            idx = int(pos)
            frac = pos - idx
            
            # Interpolate
            if idx < 255:
                val = table[idx] * (1 - frac) + table[idx + 1] * frac
            else:
                val = table[idx]
            
            # Apply morph
            if self.morph_speed > 0:
                morph_pos = (self.morph_speed * t * 256) % 256
                m_idx = int(morph_pos)
                m_frac = morph_pos - m_idx
                if m_idx < 255:
                    morph_val = table[m_idx] * (1 - m_frac) + table[m_idx + 1] * m_frac
                    val = val * (1 + self.morph_speed * 0.5) + morph_val * 0.2
            
            output.append(val * 0.3)
        
        return output


class PhysicalModelingSynth:
    """Physical modeling synthesis"""
    
    MODELS = ['pluck', 'bow', 'blast', 'string', 'drum', 'pipe']
    
    def __init__(self, model: str = 'string'):
        self.model = model
        self.excitation = 0.5
        self.decay = 0.8
        self.tension = 0.5
        self._init_model()
    
    def _init_model(self):
        """Initialize model parameters"""
        
        presets = {
            'pluck': {'excitation': 0.8, 'decay': 0.6, 'tension': 0.5},
            'bow': {'excitation': 0.3, 'decay': 0.9, 'tension': 0.7},
            'blast': {'excitation': 1.0, 'decay': 0.3, 'tension': 0.2},
            'string': {'excitation': 0.4, 'decay': 0.8, 'tension': 0.6},
            'drum': {'excitation': 0.9, 'decay': 0.4, 'tension': 0.8},
            'pipe': {'excitation': 0.2, 'decay': 0.95, 'tension': 0.3}
        }
        
        if self.model in presets:
            p = presets[self.model]
            self.excitation = p['excitation']
            self.decay = p['decay']
            self.tension = p['tension']
    
    def play(self, freq: float, duration: float, sample_rate: int = 44100) -> List[float]:
        """Play physical model"""
        
        samples = int(duration * sample_rate)
        output = []
        
        # Karplus-Strong algorithm for string/pluck
        if self.model in ['pluck', 'string']:
            delay = int(sample_rate / freq)
            buffer = [random.uniform(-1, 1) * self.excitation for _ in range(delay)]
            
            for i in range(samples):
                out = buffer[i % delay]
                buffer[i % delay] = out * 0.996 + buffer[(i + 1) % delay] * 0.004
                output.append(out * self.decay)
        
        # Simple drum model
        elif self.model == 'drum':
            for i in range(samples):
                t = i / sample_rate
                env = math.exp(-t * (5 - self.excitation * 3))
                tone = math.sin(2 * math.pi * freq * t) + math.sin(4 * math.pi * freq * t) * 0.3
                output.append(tone * env * 0.5)
        
        # Pipe model
        elif self.model == 'pipe':
            for i in range(samples):
                t = i / sample_rate
                env = math.exp(-t * (1 - self.decay * 0.5))
                tone = math.sin(2 * math.pi * freq * t) * (1 + 0.1 * random.uniform(-1, 1))
                output.append(tone * env * 0.4)
        
        # Generic
        else:
            for i in range(samples):
                t = i / sample_rate
                env = math.exp(-t * (3 - self.decay * 2))
                tone = math.sin(2 * math.pi * freq * t) * self.excitation
                output.append(tone * env * 0.5)
        
        return output


class VectorSynthesizer:
    """Vector synthesis (like Sequential Circuits Prophet VS)"""
    
    def __init__(self):
        self.oscillators = 4
        self.levels = [0.25] * 4
        self.positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
    
    def set_oscillator(self, index: int, level: float, x: float, y: float):
        """Set oscillator level and position"""
        if 0 <= index < 4:
            self.levels[index] = level
            self.positions[index] = (x, y)
    
    def get_mix(self, x: float, y: float) -> float:
        """Get mix at position"""
        
        mix = 0
        
        for i, (ox, oy) in enumerate(self.positions):
            # Distance-based mixing
            dist = math.sqrt((x - ox) ** 2 + (y - oy) ** 2)
            weight = max(0, 1 - dist)
            mix += self.levels[i] * weight
        
        return mix / sum(self.levels) if sum(self.levels) > 0 else 0
    
    def play(self, freq: float, duration: float, sample_rate: int = 44100) -> List[float]:
        """Play vector synthesis"""
        
        samples = int(duration * sample_rate)
        output = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Move around the vector space
            x = (math.sin(2 * math.pi * freq * 0.5 * t) + 1) / 2
            y = (math.cos(2 * math.pi * freq * 0.3 * t) + 1) / 2
            
            mix = self.get_mix(x, y)
            
            # Generate oscillators
            sample = 0
            for j in range(self.oscillators):
                phase = j * 0.25
                wave = math.sin(2 * math.pi * (freq * (j + 1)) * t + phase)
                sample += wave * self.levels[j]
            
            output.append(sample * mix * 0.2)
        
        return output


class SamplePlaybackEngine:
    """Advanced sample playback with time stretching"""
    
    def __init__(self):
        self.samples = {}
        self.pitch = 1.0
        self.start = 0.0
        self.end = 1.0
        self.loop = False
    
    def load_sample(self, name: str, audio: List[float]):
        """Load sample"""
        self.samples[name] = audio
    
    def set_pitch(self, semitones: float):
        """Set pitch in semitones"""
        self.pitch = 2 ** (semitones / 12)
    
    def set_loop(self, start: float, end: float):
        """Set loop points"""
        self.start = start
        self.end = end
        self.loop = True
    
    def play(self, name: str, duration: float, sample_rate: int = 44100) -> List[float]:
        """Play sample with pitch/time adjustment"""
        
        if name not in self.samples:
            return [0] * int(duration * sample_rate)
        
        source = self.samples[name]
        target_samples = int(duration * sample_rate)
        output = []
        
        source_pos = 0
        pos_increment = self.pitch
        
        for i in range(target_samples):
            if int(source_pos) < len(source):
                output.append(source[int(source_pos)])
            else:
                output.append(0)
            
            source_pos += pos_increment
            
            # Handle loop
            if self.loop and source_pos >= len(source) * self.end:
                source_pos = len(source) * self.start
        
        return output


class HybridSynthEngine:
    """Hybrid synthesizer combining all methods"""
    
    def __init__(self):
        self.wavetable = WavetableSynthesizer()
        self.physical = PhysicalModelingSynth('string')
        self.vector = VectorSynthesizer()
        self.sample = SamplePlaybackEngine()
        
        self.mix = {
            'wavetable': 0.4,
            'physical': 0.3,
            'vector': 0.2,
            'sample': 0.1
        }
    
    def set_mix(self, wavetable: float = None, physical: float = None, 
                vector: float = None, sample: float = None):
        """Set mix levels"""
        
        if wavetable is not None:
            self.mix['wavetable'] = wavetable
        if physical is not None:
            self.mix['physical'] = physical
        if vector is not None:
            self.mix['vector'] = vector
        if sample is not None:
            self.mix['sample'] = sample
    
    def play(self, freq: float, duration: float, sample_rate: int = 44100) -> List[float]:
        """Play hybrid synth"""
        
        wt = self.wavetable.play(freq, duration, sample_rate)
        phys = self.physical.play(freq, duration, sample_rate)
        vec = self.vector.play(freq, duration, sample_rate)
        samp = self.sample.play('default', duration, sample_rate)
        
        # Mix all sources
        output = []
        for i in range(len(wt)):
            sample = (wt[i] * self.mix['wavetable'] +
                     phys[i] * self.mix['physical'] +
                     vec[i] * self.mix['vector'] +
                     samp[i] * self.mix['sample'])
            output.append(sample)
        
        return output


class AdvancedSynthV3:
    """Complete V3 synth with all features"""
    
    def __init__(self):
        self.oscillator = HybridSynthEngine()
        self.filter = self._create_filter()
        self.lfo = {'freq': 1.0, 'depth': 0.0}
        self.amp_envelope = {'attack': 0.01, 'decay': 0.2, 'sustain': 0.7, 'release': 0.3}
        self.filter_envelope = {'attack': 0.02, 'decay': 0.3, 'sustain': 0.5, 'release': 0.4}
    
    def _create_filter(self):
        """Create filter"""
        return {'type': 'lowpass', 'cutoff': 2000, 'resonance': 0.5}
    
    def set_filter(self, filter_type: str, cutoff: float, resonance: float = 0.5):
        """Set filter"""
        self.filter['type'] = filter_type
        self.filter['cutoff'] = cutoff
        self.filter['resonance'] = resonance
    
    def set_lfo(self, freq: float, depth: float):
        """Set LFO"""
        self.lfo['freq'] = freq
        self.lfo['depth'] = depth
    
    def play(self, freq: float, duration: float, sample_rate: int = 44100) -> List[float]:
        """Play complete synth"""
        
        # Generate base audio
        audio = self.oscillator.play(freq, duration, sample_rate)
        
        # Apply filter
        cutoff = self.filter['cutoff']
        for i in range(len(audio)):
            # LFO modulation
            t = i / sample_rate
            lfo_mod = 1 + math.sin(2 * math.pi * self.lfo['freq'] * t) * self.lfo['depth']
            
            # Simple filter
            eff_cutoff = cutoff * lfo_mod
            audio[i] *= max(0, 1 - eff_cutoff / 40000)
        
        return audio


def demo():
    print("=" * 60)
    print("  LEVEL 1.8 - ADVANCED SYNTH ENGINE V3")
    print("=" * 60)
    
    # Wavetable
    print("\n[Wavetable Synth]")
    wt = WavetableSynthesizer()
    for table in ['saw', 'square', 'triangle']:
        wt.set_table(table)
        audio = wt.play(440, 0.1)
        print("  %s: %d samples" % (table, len(audio)))
    
    # Physical Modeling
    print("\n[Physical Modeling]")
    for model in ['pluck', 'string', 'drum']:
        pm = PhysicalModelingSynth(model)
        audio = pm.play(220, 0.2)
        print("  %s: %d samples" % (model, len(audio)))
    
    # Vector
    print("\n[Vector Synthesis]")
    vec = VectorSynthesizer()
    vec.set_oscillator(0, 0.5, 0, 0)
    vec.set_oscillator(1, 0.5, 1, 1)
    audio = vec.play(330, 0.1)
    print("  Vector: %d samples" % len(audio))
    
    # Hybrid
    print("\n[Hybrid Engine]")
    hybrid = HybridSynthEngine()
    hybrid.set_mix(wavetable=0.5, physical=0.3, vector=0.1, sample=0.1)
    audio = hybrid.play(440, 0.1)
    print("  Hybrid: %d samples" % len(audio))
    
    # Advanced V3
    print("\n[Advanced Synth V3]")
    synth = AdvancedSynthV3()
    synth.set_filter('lowpass', 3000, 0.6)
    synth.set_lfo(2.0, 0.3)
    audio = synth.play(440, 0.2)
    print("  V3 Synth: %d samples" % len(audio))
    
    print("\n" + "=" * 60)
    print("  LEVEL 1.8 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()