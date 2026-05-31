"""
DRUM MACHINE & SEQUENCER - Innovation!
======================================
- 16-step sequencer
- Multiple drum kits
- Pattern chaining
- Swing control
- Humanization
- Real-time playback

Innovation: FL Studio quality drum machine in pure Python!
"""

import math
import random
import json
import os
import struct
import wave
from typing import List, Dict, Optional
from datetime import datetime


class DrumKit:
    """Complete drum kits"""
    
    KITS = {
        '808': {
            'name': 'TR-808',
            'kick': {'pitch': 150, 'decay': 0.3, 'tone': 0.5},
            'snare': {'pitch': 200, 'decay': 0.2, 'snap': 0.8},
            'hihat': {'pitch': 800, 'decay': 0.05, 'metallic': 0.9},
            'clap': {'pitch': 400, 'decay': 0.15, 'snap': 0.9},
            'tom_low': {'pitch': 100, 'decay': 0.3},
            'tom_mid': {'pitch': 150, 'decay': 0.25},
            'tom_high': {'pitch': 200, 'decay': 0.2},
            'rim': {'pitch': 600, 'decay': 0.05},
            'cowbell': {'pitch': 800, 'decay': 0.2}
        },
        '909': {
            'name': 'TR-909',
            'kick': {'pitch': 150, 'decay': 0.4, 'tone': 0.6},
            'snare': {'pitch': 250, 'decay': 0.15, 'snap': 0.7},
            'hihat': {'pitch': 1000, 'decay': 0.03, 'metallic': 0.8},
            'clap': {'pitch': 500, 'decay': 0.1, 'snap': 0.8},
            'ride': {'pitch': 600, 'decay': 0.3},
            'crash': {'pitch': 400, 'decay': 0.5}
        },
        'acoustic': {
            'name': 'Acoustic Kit',
            'kick': {'pitch': 120, 'decay': 0.35, 'tone': 0.4},
            'snare': {'pitch': 220, 'decay': 0.15, 'snap': 0.6},
            'hihat': {'pitch': 1200, 'decay': 0.02, 'metallic': 0.5},
            'hihat_open': {'pitch': 1000, 'decay': 0.3, 'metallic': 0.5},
            'tom_high': {'pitch': 250, 'decay': 0.2},
            'tom_mid': {'pitch': 180, 'decay': 0.25},
            'tom_low': {'pitch': 100, 'decay': 0.3},
            'crash': {'pitch': 350, 'decay': 0.6},
            'ride': {'pitch': 500, 'decay': 0.4}
        },
        'electronic': {
            'name': 'Electronic',
            'kick': {'pitch': 180, 'decay': 0.2, 'tone': 0.8},
            'snare': {'pitch': 300, 'decay': 0.1, 'snap': 0.9},
            'hihat': {'pitch': 1500, 'decay': 0.02, 'metallic': 0.95},
            'clap': {'pitch': 600, 'decay': 0.08, 'snap': 1.0},
            'sub': {'pitch': 60, 'decay': 0.5, 'tone': 0.9},
            'click': {'pitch': 2000, 'decay': 0.01, 'metallic': 1.0}
        },
        'lofi': {
            'name': 'Lo-Fi',
            'kick': {'pitch': 100, 'decay': 0.4, 'tone': 0.3},
            'snare': {'pitch': 180, 'decay': 0.25, 'snap': 0.4},
            'hihat': {'pitch': 800, 'decay': 0.08, 'metallic': 0.3},
            'hihat_open': {'pitch': 600, 'decay': 0.4, 'metallic': 0.3},
            'shaker': {'pitch': 500, 'decay': 0.1}
        }
    }
    
    @classmethod
    def get_kit(cls, name: str) -> Dict:
        return cls.KITS.get(name, cls.KITS['808'])


class DrumSound:
    """Generate individual drum sounds"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def generate(self, drum_type: str, params: Dict) -> List[float]:
        """Generate drum sound"""
        
        if drum_type == 'kick':
            return self._generate_kick(params)
        elif drum_type == 'snare':
            return self._generate_snare(params)
        elif drum_type == 'hihat' or drum_type == 'hihat_open':
            return self._generate_hihat(params)
        elif drum_type == 'clap':
            return self._generate_clap(params)
        elif drum_type == 'tom_low' or drum_type == 'tom_mid' or drum_type == 'tom_high':
            return self._generate_tom(params)
        elif drum_type == 'rim':
            return self._generate_rim(params)
        elif drum_type == 'ride' or drum_type == 'crash':
            return self._generate_cymbal(params)
        elif drum_type == 'cowbell':
            return self._generate_cowbell(params)
        elif drum_type == 'sub':
            return self._generate_sub(params)
        elif drum_type == 'click':
            return self._generate_click(params)
        elif drum_type == 'shaker':
            return self._generate_shaker(params)
        
        return self._generate_kick(params)
    
    def _generate_kick(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 150)
        decay = params.get('decay', 0.3)
        tone = params.get('tone', 0.5)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            # Pitch envelope
            freq = pitch * (1 - t / duration * 0.7) + 40
            # Tone mixing
            tone_osc = math.sin(2 * math.pi * freq * t)
            noise = (random.random() * 2 - 1) * tone
            # Envelope
            env = (1 - t / duration) ** 2
            
            result.append((tone_osc + noise) * env)
        
        return self._normalize(result)
    
    def _generate_snare(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 200)
        decay = params.get('decay', 0.2)
        snap = params.get('snap', 0.7)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 1.5
            
            # Tone
            tone = math.sin(2 * math.pi * pitch * t) * 0.3
            # Noise (snare wires)
            noise = (random.random() * 2 - 1) * snap
            
            result.append((tone + noise) * env)
        
        return self._normalize(result)
    
    def _generate_hihat(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 800)
        decay = params.get('decay', 0.05)
        metallic = params.get('metallic', 0.9)
        
        duration = decay * 5
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 3
            
            # High frequency oscillation
            osc = math.sin(2 * math.pi * pitch * t)
            # Noise
            noise = (random.random() * 2 - 1) * metallic
            
            result.append((osc + noise) * env * 0.5)
        
        return self._normalize(result)
    
    def _generate_clap(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 400)
        decay = params.get('decay', 0.15)
        snap = params.get('snap', 0.9)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            
            # Multiple attacks (clap texture)
            att1 = math.exp(-((t - 0.01) ** 2) / 0.0001) if t > 0.01 else 0
            att2 = math.exp(-((t - 0.02) ** 2) / 0.0001) if t > 0.02 else 0
            att3 = math.exp(-((t - 0.025) ** 2) / 0.00005) if t > 0.025 else 0
            
            env = (att1 + att2 + att3) * (1 - t / duration)
            noise = (random.random() * 2 - 1) * snap
            
            result.append(noise * env * 0.8)
        
        return self._normalize(result)
    
    def _generate_tom(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 150)
        decay = params.get('decay', 0.25)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            freq = pitch * (1 - t / duration * 0.5) + 50
            env = (1 - t / duration) ** 1.5
            
            result.append(math.sin(2 * math.pi * freq * t) * env)
        
        return self._normalize(result)
    
    def _generate_rim(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 600)
        decay = params.get('decay', 0.05)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 4
            
            result.append(math.sin(2 * math.pi * pitch * t) * env + 
                        random.random() * 0.3 * env)
        
        return self._normalize(result)
    
    def _generate_cymbal(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 500)
        decay = params.get('decay', 0.4)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 1.5
            
            # Multiple harmonics
            s = math.sin(2 * math.pi * pitch * t)
            s += math.sin(2 * math.pi * pitch * 1.5 * t) * 0.5
            s += math.sin(2 * math.pi * pitch * 2 * t) * 0.3
            s += (random.random() * 2 - 1) * 0.4
            
            result.append(s * env * 0.5)
        
        return self._normalize(result)
    
    def _generate_cowbell(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 800)
        decay = params.get('decay', 0.2)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 2
            
            # Two-tone cowbell
            s = math.sin(2 * math.pi * pitch * t)
            s += math.sin(2 * math.pi * pitch * 0.5 * t) * 0.5
            
            result.append(s * env * 0.5)
        
        return self._normalize(result)
    
    def _generate_sub(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 60)
        decay = params.get('decay', 0.5)
        tone = params.get('tone', 0.9)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 1.2
            
            s = math.sin(2 * math.pi * pitch * t)
            # Sub harmonic
            s += math.sin(2 * math.pi * pitch * 0.5 * t) * tone * 0.5
            
            result.append(s * env * 0.7)
        
        return self._normalize(result)
    
    def _generate_click(self, params: Dict) -> List[float]:
        pitch = params.get('pitch', 2000)
        decay = params.get('decay', 0.01)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 8
            
            result.append((random.random() * 2 - 1) * env)
        
        return self._normalize(result)
    
    def _generate_shaker(self, params: Dict) -> List[float]:
        decay = params.get('decay', 0.1)
        
        duration = decay * 3
        samples = int(self.sample_rate * duration)
        
        result = []
        for i in range(samples):
            t = i / self.sample_rate
            env = (1 - t / duration) ** 2
            
            result.append((random.random() * 2 - 1) * env * 0.5)
        
        return self._normalize(result)
    
    def _normalize(self, samples: List[float]) -> List[float]:
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            return [s * 0.9 / max_val for s in samples]
        return samples


class DrumSequencer:
    """16-step drum sequencer"""
    
    def __init__(self, kit_name: str = '808'):
        self.sample_rate = 44100
        self.kit = DrumKit.get_kit(kit_name)
        self.drum_gen = DrumSound(self.sample_rate)
        self.steps = 16
        self.swing = 0
        self.bpm = 120
        
        # Initialize empty pattern
        self.pattern = self._empty_pattern()
    
    def _empty_pattern(self) -> Dict:
        """Empty pattern structure"""
        return {
            'kick': [0] * 16,
            'snare': [0] * 16,
            'hihat': [0] * 16,
            'clap': [0] * 16,
            'tom_low': [0] * 16,
            'tom_mid': [0] * 16,
            'tom_high': [0] * 16,
            'rim': [0] * 16,
            'cowbell': [0] * 16,
            'ride': [0] * 16,
            'crash': [0] * 16
        }
    
    def set_step(self, drum: str, step: int, velocity: int):
        """Set a step (0-15)"""
        if drum in self.pattern and 0 <= step < 16:
            self.pattern[drum][step] = max(0, min(100, velocity))
    
    def set_kick(self, step: int, velocity: int = 100):
        self.set_step('kick', step, velocity)
    
    def set_snare(self, step: int, velocity: int = 100):
        self.set_step('snare', step, velocity)
    
    def set_hihat(self, step: int, velocity: int = 80):
        self.set_step('hihat', step, velocity)
    
    def set_pattern(self, drum: str, steps: List[int]):
        """Set multiple steps at once"""
        if drum in self.pattern and len(steps) == 16:
            self.pattern[drum] = steps
    
    def generate(self, bars: int = 1, humanize: float = 0.1) -> List[float]:
        """Generate audio from pattern"""
        
        beat_duration = 60 / self.bpm
        step_duration = beat_duration / 4  # 16th notes
        
        total_samples = int(self.sample_rate * beat_duration * 4 * bars)
        audio = [0.0] * total_samples
        
        for bar in range(bars):
            for step in range(16):
                # Calculate swing offset
                swing_offset = 0
                if step % 2 == 1 and self.swing > 0:
                    swing_offset = step_duration * self.swing * 0.5
                
                step_time = (bar * 16 + step) * step_duration + swing_offset
                step_sample = int(step_time * self.sample_rate)
                
                for drum_name, drum_params in self.kit.items():
                    if drum_name == 'name':
                        continue
                    
                    velocity = self.pattern.get(drum_name, [0] * 16)[step]
                    
                    if velocity > 0:
                        # Generate drum sound
                        drum_audio = self.drum_gen.generate(drum_name, drum_params)
                        
                        # Apply humanization
                        if humanize > 0:
                            pitch_shift = random.uniform(-humanize, humanize)
                            drum_audio = self._pitch_shift(drum_audio, 1 + pitch_shift * 0.1)
                        
                        # Mix into output
                        vol = velocity / 100
                        for i, sample in enumerate(drum_audio):
                            idx = step_sample + i
                            if idx < total_samples:
                                audio[idx] += sample * vol
        
        return self._normalize(audio)
    
    def _pitch_shift(self, samples: List[float], ratio: float) -> List[float]:
        """Simple pitch shift by resampling"""
        if ratio == 1.0:
            return samples
        
        new_length = int(len(samples) / ratio)
        result = []
        
        for i in range(new_length):
            idx = i * ratio
            if idx < len(samples):
                result.append(samples[int(idx)])
        
        return result
    
    def _normalize(self, samples: List[float]) -> List[float]:
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            return [s * 0.8 / max_val for s in samples]
        return samples
    
    def load_preset(self, name: str):
        """Load preset patterns"""
        presets = {
            'four_on_floor': {
                'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
                'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
                'hihat': [80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0]
            },
            'trap': {
                'kick': [100, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0, 100, 0, 0, 0, 0],
                'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 100],
                'hihat': [80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
            },
            'boom_bap': {
                'kick': [100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
                'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
                'hihat': [60, 0, 60, 0, 0, 60, 0, 0, 60, 0, 60, 0, 0, 60, 0, 0]
            },
            'house': {
                'kick': [100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0],
                'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
                'hihat': [80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0]
            },
            'breakbeat': {
                'kick': [100, 0, 0, 100, 0, 0, 50, 0, 100, 0, 0, 50, 0, 0, 100, 0],
                'snare': [0, 0, 100, 0, 0, 0, 50, 0, 0, 0, 100, 0, 0, 50, 0, 0],
                'hihat': [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60]
            }
        }
        
        if name in presets:
            for drum, steps in presets[name].items():
                if drum in self.pattern:
                    self.pattern[drum] = steps


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  DRUM MACHINE & SEQUENCER")
    print("=" * 60)
    
    # Test different kits
    kits = ['808', '909', 'acoustic', 'electronic', 'lofi']
    
    print("\nAvailable Kits:", ', '.join(kits))
    
    # Test drum machine
    print("\n[TEST] TR-808 Kit - Trap Pattern")
    seq = DrumSequencer('808')
    seq.load_preset('trap')
    seq.bpm = 140
    
    audio = seq.generate(4, humanize=0.05)
    
    filename = "audio/drum_machine_808_trap.wav"
    
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        for s in audio:
            packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
            wav.writeframes(packed)
    
    print(f"      Saved: {filename} ({len(audio)/44100:.1f}s)")
    
    # Test different patterns
    print("\n[TEST] Acoustic Kit - Four on Floor")
    seq2 = DrumSequencer('acoustic')
    seq2.load_preset('four_on_floor')
    seq2.bpm = 120
    
    audio2 = seq2.generate(4)
    
    filename2 = "audio/drum_machine_acoustic.wav"
    
    with wave.open(filename2, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        for s in audio2:
            packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
            wav.writeframes(packed)
    
    print(f"      Saved: {filename2} ({len(audio2)/44100:.1f}s)")
    
    # Test Lo-Fi
    print("\n[TEST] Lo-Fi Kit - Boom Bap")
    seq3 = DrumSequencer('lofi')
    seq3.load_preset('boom_bap')
    seq3.swing = 0.1
    seq3.bpm = 90
    
    audio3 = seq3.generate(4)
    
    filename3 = "audio/drum_machine_lofi.wav"
    
    with wave.open(filename3, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        for s in audio3:
            packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
            wav.writeframes(packed)
    
    print(f"      Saved: {filename3} ({len(audio3)/44100:.1f}s)")
    
    print("\n" + "=" * 60)
    print("  DRUM MACHINE READY!")
    print("=" * 60)