"""
LEVEL 1.7 - ADDITIONAL CORE UPGRADES
====================================
- Multi-oscillator engine
-更多合成器预设
- Advanced drum variations
- Enhanced effects

Making Level 1 even better!
"""

import math
import random
from typing import List, Dict


class MultiOscillatorEngine:
    """Multiple oscillator types with stacking"""
    
    OSC_TYPES = [
        'standard', 'drift', 'spread', 'stack', 
        'thicken', 'harmonic', 'fm', 'am'
    ]
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def generate_stack(self, freq: float, duration: float, osc_type: str = 'standard') -> List[float]:
        """Generate with multiple oscillators"""
        
        samples = int(self.sample_rate * duration)
        result = []
        
        for i in range(samples):
            t = i / self.sample_rate
            sample = 0
            
            if osc_type == 'standard':
                # Standard saw
                sample = math.sin(2 * math.pi * freq * t)
                sample += math.sin(2 * math.pi * freq * 1.01 * t) * 0.5
                
            elif osc_type == 'drift':
                # Slight frequency drift
                drift = math.sin(t * 0.5) * 2
                sample = math.sin(2 * math.pi * (freq + drift) * t)
                
            elif osc_type == 'spread':
                # Wide stereo spread
                sample = math.sin(2 * math.pi * freq * t)
                sample += math.sin(2 * math.pi * freq * 1.03 * t) * 0.4
                sample += math.sin(2 * math.pi * freq * 0.97 * t) * 0.4
                
            elif osc_type == 'stack':
                # Stack harmonics
                for h in range(1, 5):
                    sample += math.sin(2 * math.pi * freq * h * t) / h
                    
            elif osc_type == 'thicken':
                # Dense thickening
                for detune in [-10, -5, 0, 5, 10]:
                    f = freq * (1 + detune/1200)
                    sample += math.sin(2 * math.pi * f * t) * 0.2
                    
            elif osc_type == 'harmonic':
                # Odd harmonics
                for h in [1, 3, 5, 7, 9]:
                    sample += math.sin(2 * math.pi * freq * h * t) / h
                    
            elif osc_type == 'fm':
                # FM synthesis
                mod = math.sin(2 * math.pi * freq * 2 * t) * 3
                sample = math.sin(2 * math.pi * freq * t + mod)
                
            elif osc_type == 'am':
                # AM synthesis
                carrier = math.sin(2 * math.pi * freq * t)
                mod = (math.sin(2 * math.pi * freq * 0.5 * t) + 1) / 2
                sample = carrier * mod
            
            result.append(sample * 0.3)
        
        return result


class EffectChain:
    """Multi-effect chain"""
    
    EFFECTS = ['distortion', 'saturation', 'bitcrush', 'tube', 'tape', 'vinyl']
    
    @staticmethod
    def apply_distortion(audio: List[float], amount: float = 0.5) -> List[float]:
        """Apply distortion"""
        return [math.tanh(s * (1 + amount * 5)) for s in audio]
    
    @staticmethod
    def apply_saturation(audio: List[float], drive: float = 0.5) -> List[float]:
        """Apply saturation"""
        return [s * (1 + drive * 0.5) + s**3 * drive * 0.3 for s in audio]
    
    @staticmethod
    def apply_bitcrush(audio: List[float], bits: int = 8) -> List[float]:
        """Apply bit crushing"""
        scale = 2 ** bits - 1
        return [round(s * scale) / scale for s in audio]
    
    @staticmethod
    def apply_tube(audio: List[float], warmth: float = 0.5) -> List[float]:
        """Apply tube warmth"""
        return [s * (1 - warmth * 0.2) + math.tanh(s * 2) * warmth * 0.3 for s in audio]
    
    @staticmethod
    def apply_tape(audio: List[float], wow: float = 0.3) -> List[float]:
        """Apply tape simulation"""
        result = []
        for i, s in enumerate(audio):
            wow_mod = 1 + math.sin(i / 1000 * wow) * 0.01
            result.append(s * wow_mod)
        return result
    
    @staticmethod
    def apply_vinyl(audio: List[float], crackle: float = 0.1) -> List[float]:
        """Apply vinyl crackle"""
        result = []
        for i, s in enumerate(audio):
            if random.random() < crackle * 0.01:
                s += random.random() * 0.1
            result.append(s * 0.99)
        return result


class EnhancedDrumEngine:
    """Enhanced drum synthesis"""
    
    @staticmethod
    def synth_kick(pitch: float = 60, decay: float = 0.3, sample_rate: int = 44100) -> List[float]:
        """Synthesize kick drum"""
        samples = int(sample_rate * decay)
        result = []
        
        for i in range(samples):
            t = i / sample_rate
            # Pitch envelope
            freq = pitch * (1 - t * 3)
            if freq < 30:
                freq = 30
            
            # Amplitude envelope
            env = math.exp(-t * 10)
            
            # Wave
            wave = math.sin(2 * math.pi * freq * t)
            
            result.append(wave * env)
        
        return result
    
    @staticmethod
    def synth_snare(tone: float = 200, snap: float = 0.5, sample_rate: int = 44100) -> List[float]:
        """Synthesize snare"""
        duration = 0.3
        samples = int(sample_rate * duration)
        result = []
        
        for i in range(samples):
            t = i / sample_rate
            # Tone
            tone_env = math.exp(-t * 15)
            tone_wave = math.sin(2 * math.pi * tone * t) * tone_env
            
            # Noise (snap)
            if t < 0.05:
                noise = (random.random() * 2 - 1) * (1 - t/0.05) * snap
            else:
                noise = 0
            
            result.append((tone_wave * 0.6 + noise * 0.4) * math.exp(-t * 8))
        
        return result
    
    @staticmethod
    def synth_hihat(tonal: float = 800, metallic: float = 0.3, sample_rate: int = 44100) -> List[float]:
        """Synthesize hi-hat"""
        duration = 0.1
        samples = int(sample_rate * duration)
        result = []
        
        for i in range(samples):
            t = i / sample_rate
            env = math.exp(-t * 30)
            
            # Metallic component
            metal = math.sin(2 * math.pi * tonal * t) * metallic
            
            # Noise component
            noise = (random.random() * 2 - 1) * (1 - metallic)
            
            result.append((metal + noise) * env * 0.5)
        
        return result


def demo():
    print("=" * 60)
    print("  LEVEL 1.7 - ADDITIONAL CORE UPGRADES")
    print("=" * 60)
    
    # Multi Oscillator
    print("\n[Multi-Oscillator Engine]")
    engine = MultiOscillatorEngine()
    for osc_type in ['standard', 'drift', 'fm', 'am']:
        audio = engine.generate_stack(440, 0.5, osc_type)
        print(f"  {osc_type}: {len(audio)} samples")
    
    # Effects
    print("\n[Effect Chain]")
    test_audio = [math.sin(440 * 2 * math.pi * i/44100) for i in range(4410)]
    distorted = EffectChain.apply_distortion(test_audio, 0.5)
    print(f"  Distortion: {len(distorted)} samples")
    crushed = EffectChain.apply_bitcrush(test_audio, 4)
    print(f"  Bitcrush: {len(crushed)} samples")
    
    # Drum synthesis
    print("\n[Enhanced Drum Engine]")
    kick = EnhancedDrumEngine.synth_kick(60, 0.3)
    print(f"  Kick: {len(kick)} samples")
    snare = EnhancedDrumEngine.synth_snare(200, 0.5)
    print(f"  Snare: {len(snare)} samples")
    hihat = EnhancedDrumEngine.synth_hihat(800, 0.3)
    print(f"  Hi-hat: {len(hihat)} samples")
    
    print("\n" + "=" * 60)
    print("  LEVEL 1.7 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()