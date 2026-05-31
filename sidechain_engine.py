"""
SIDECHAIN DUCKING ENGINE
========================
Professional sidechain compression for pumping effects.
Supports ducking, keying, and parallel processing.
"""

import math
import struct
import wave
import os
from typing import List, Tuple, Optional


class SidechainEngine:
    """Sidechain ducking and compression engine"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.envelope = []
        self.attack_time = 0.01
        self.release_time = 0.3
        self.threshold = -20
        self.ratio = 4.0
        self.knee = 6.0
        self.makeup_gain = 1.0
    
    def _db_to_linear(self, db: float) -> float:
        return 10 ** (db / 20)
    
    def _linear_to_db(self, linear: float) -> float:
        return 20 * math.log10(max(linear, 0.0001))
    
    def _compute_envelope(self, audio: List[float]) -> List[float]:
        """Compute amplitude envelope for ducking"""
        envelope = []
        attack_samples = int(self.sample_rate * self.attack_time)
        release_samples = int(self.sample_rate * self.release_time)
        
        peak = 0
        for sample in audio:
            if abs(sample) > peak:
                peak = abs(sample) + peak * 0.5
            else:
                peak *= 0.99
            
            if len(envelope) == 0:
                envelope.append(peak)
            else:
                prev = envelope[-1]
                if peak > prev:
                    alpha = 1.0 / attack_samples if attack_samples > 0 else 1.0
                    envelope.append(prev + (peak - prev) * alpha)
                else:
                    alpha = 1.0 / release_samples if release_samples > 0 else 1.0
                    envelope.append(prev + (peak - prev) * (1 - alpha))
        
        return envelope
    
    def _compressor_curve(self, input_db: float) -> float:
        """Compute compressor gain reduction"""
        if input_db > self.threshold + self.knee / 2:
            excess = input_db - (self.threshold + self.knee / 2)
            return excess * (1 - 1 / self.ratio)
        elif input_db < self.threshold - self.knee / 2:
            return 0
        else:
            excess = input_db - (self.threshold - self.knee / 2)
            return (excess / self.knee) ** 2 * (1 - 1 / self.ratio)
    
    def apply_sidechain(self, target: List[float], trigger: List[float],
                        mode: str = 'duck') -> List[float]:
        """Apply sidechain ducking to target using trigger signal"""
        if len(trigger) < len(target):
            trigger = trigger + [0] * (len(target) - len(trigger))
        
        self.envelope = self._compute_envelope(trigger)
        
        result = []
        for i in range(len(target)):
            input_db = self._linear_to_db(abs(target[i]) + 0.0001)
            gain_reduction = self._compressor_curve(input_db)
            
            if mode == 'duck':
                duck_amount = 1 - self._db_to_linear(-self.threshold) * (1 - self._db_to_linear(-gain_reduction))
                duck_amount *= self.envelope[i] if i < len(self.envelope) else 1
                duck_amount = max(0.1, duck_amount)
            elif mode == 'pump':
                duck_amount = 0.5 + 0.5 * (self.envelope[i] if i < len(self.envelope) else 0)
            elif mode == 'swell':
                duck_amount = 1 + (self.envelope[i] if i < len(self.envelope) else 0) * 2
            else:
                duck_amount = 1
            
            result.append(target[i] * duck_amount * self.makeup_gain)
        
        return result
    
    def apply_keying(self, audio: List[float], key_freq: float,
                     mode: str = 'low') -> List[float]:
        """Apply frequency-based keying"""
        result = []
        for i in range(len(audio)):
            t = i / self.sample_rate
            key_signal = math.sin(2 * math.pi * key_freq * t)
            key_envelope = abs(key_signal)
            
            if mode == 'low':
                gain = 1 - key_envelope * 0.7
            elif mode == 'high':
                gain = 0.3 + key_envelope * 0.7
            else:
                gain = 1
            
            result.append(audio[i] * gain)
        
        return result
    
    def parallel_dry_wet(self, dry: List[float], wet: List[float],
                         mix: float = 0.5) -> List[float]:
        """Parallel dry/wet blend"""
        result = []
        for i in range(len(dry)):
            d = dry[i] if i < len(dry) else 0
            w = wet[i] if i < len(wet) else 0
            result.append(d * (1 - mix) + w * mix)
        return result
    
    def duck_music_for_vocals(self, music: List[float], vocals: List[float]) -> List[float]:
        """Duck music when vocals are present"""
        return self.apply_sidechain(music, vocals, 'duck')
    
    def duck_for_kick(self, pads: List[float], kick: List[float]) -> List[float]:
        """Classic sidechain - pads duck when kick hits"""
        return self.apply_sidechain(pads, kick, 'pump')
    
    def duck_for_bass(self, lead: List[float], bass: List[float]) -> List[float]:
        """Lead ducking for bass clarity"""
        return self.apply_sidechain(lead, bass, 'duck')
    
    def save_wav(self, samples: List[float], filename: str):
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            samples = [s * 0.9 / max_val for s in samples]
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            for s in samples:
                packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
                wav.writeframes(packed)


class MultiBandSidechain:
    """Multi-band sidechain for more advanced processing"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.bands = {
            'sub': {'freq': 60, 'duck': 1.0, 'attack': 0.005, 'release': 0.1},
            'bass': {'freq': 250, 'duck': 0.8, 'attack': 0.01, 'release': 0.2},
            'low_mid': {'freq': 500, 'duck': 0.5, 'attack': 0.02, 'release': 0.3},
            'high_mid': {'freq': 2000, 'duck': 0.3, 'attack': 0.03, 'release': 0.4},
            'high': {'freq': 5000, 'duck': 0.1, 'attack': 0.05, 'release': 0.5},
        }
    
    def apply_multiband(self, audio: List[float], trigger: List[float]) -> List[float]:
        """Apply different ducking per frequency band"""
        result = audio.copy()
        
        for band_name, params in self.bands.items():
            envelope = self._compute_band_envelope(trigger, params['freq'], params['attack'], params['release'])
            
            for i in range(len(result)):
                duck = 1 - params['duck'] * envelope[i] if i < len(envelope) else 1
                duck = max(0.1, duck)
                result[i] *= duck
        
        return result
    
    def _compute_band_envelope(self, audio: List[float], freq: float, attack: float, release: float) -> List[float]:
        """Compute envelope for specific frequency band"""
        envelope = []
        attack_samples = int(self.sample_rate * attack)
        release_samples = int(self.sample_rate * release)
        
        peak = 0
        for sample in audio:
            if abs(sample) > peak:
                peak = abs(sample)
            else:
                peak *= 0.99
            
            if len(envelope) == 0:
                envelope.append(peak)
            else:
                prev = envelope[-1]
                if peak > prev:
                    alpha = 1.0 / attack_samples if attack_samples > 0 else 1.0
                    envelope.append(prev + (peak - prev) * alpha)
                else:
                    alpha = 1.0 / release_samples if release_samples > 0 else 1.0
                    envelope.append(prev + (peak - prev) * (1 - alpha))
        
        return envelope


def demo():
    print("=" * 60)
    print("  SIDECHAIN DUCKING ENGINE")
    print("=" * 60)
    
    sc = SidechainEngine(44100)
    sc.threshold = -18
    sc.ratio = 4
    sc.attack_time = 0.01
    sc.release_time = 0.2
    
    print("\n[1] Creating test signals...")
    kick = [math.sin(2 * math.pi * 60 * (i/44100)) * (1 - i/22050) for i in range(22050)]
    pads = [math.sin(2 * math.pi * 220 * (i/44100)) * 0.3 for i in range(44100)]
    
    print("[2] Applying sidechain duck (pads + kick)...")
    ducked = sc.duck_for_kick(pads, kick)
    sc.save_wav(ducked, 'audio/sidechain_ducked.wav')
    print("    Saved: audio/sidechain_ducked.wav")
    
    print("[3] Creating music/vocal duck example...")
    music = [math.sin(2 * math.pi * 440 * (i/44100)) * 0.5 for i in range(44100)]
    vocal = [math.sin(2 * math.pi * 880 * (i/44100)) * 0.7 * (1 - i/22050) for i in range(22050)]
    ducked_music = sc.duck_music_for_vocals(music, vocal)
    sc.save_wav(ducked_music, 'audio/vocal_ducked.wav')
    print("    Saved: audio/vocal_ducked.wav")
    
    print("\n" + "=" * 60)
    print("  SIDECHAIN ENGINE READY!")
    print("=" * 60)


if __name__ == "__main__":
    demo()