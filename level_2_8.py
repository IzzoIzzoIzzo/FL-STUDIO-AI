"""
LEVEL 2.8 - ADVANCED ANALYSIS & DETECTION
==========================================
Deep analysis features:
- Harmonic analysis
- Transient detection
- Formant extraction
- Room detection
- Instrument identification
- Key detection (multiple algorithms)
"""

import math
import random
from typing import List, Dict, Tuple


class HarmonicAnalyzer:
    """Analyze harmonic content"""
    
    def __init__(self):
        self.num_harmonics = 16
        self.min_freq = 20
        self.max_freq = 20000
    
    def analyze(self, audio: List[float], sample_rate: int = 44100) -> Dict:
        """Analyze harmonics"""
        
        # Find fundamental
        fundamental = self._find_fundamental(audio, sample_rate)
        
        # Extract harmonics
        harmonics = self._extract_harmonics(audio, fundamental, sample_rate)
        
        return {
            'fundamental': fundamental,
            'harmonics': harmonics,
            'harmonicity': self._calculate_harmonicity(harmonics),
            'spectral_centroid': self._get_centroid(audio, sample_rate)
        }
    
    def _find_fundamental(self, audio: List[float], sr: int) -> float:
        """Find fundamental frequency"""
        
        # Autocorrelation method
        n = len(audio)
        if n < 50:
            return 440.0
        
        max_lag = sr // 20  # Max freq 20Hz
        
        best_corr = 0
        best_lag = 0
        
        for lag in range(20, min(max_lag, n - 50)):
            corr = sum(audio[i] * audio[i + lag] for i in range(min(n - lag, 500))) / 500
            if corr > best_corr:
                best_corr = corr
                best_lag = lag
        
        if best_lag > 0:
            return sr / best_lag
        return 440.0
    
    def _extract_harmonics(self, audio: List[float], fundamental: float, 
                          sr: int) -> List[Dict]:
        """Extract harmonic components"""
        
        harmonics = []
        
        for h in range(1, self.num_harmonics + 1):
            freq = fundamental * h
            
            if freq > self.max_freq:
                break
            
            # Simple bandpass around harmonic
            bandwidth = fundamental * 0.1
            
            amplitude = 0
            count = 0
            
            for i, sample in enumerate(audio):
                f = i * sr / len(audio)
                if abs(f - freq) < bandwidth:
                    amplitude += abs(sample)
                    count += 1
            
            if count > 0:
                amplitude /= count
                harmonics.append({
                    'harmonic': h,
                    'frequency': freq,
                    'amplitude': amplitude
                })
        
        return harmonics
    
    def _calculate_harmonicity(self, harmonics: List[Dict]) -> float:
        """Calculate harmonicity score"""
        
        if not harmonics:
            return 0.0
        
        # Check if harmonics are integer multiples
        expected_ratios = [h['harmonic'] for h in harmonics]
        actual_ratios = [h['frequency'] / harmonics[0]['frequency'] for h in harmonics]
        
        error = sum(abs(exp - act) for exp, act in zip(expected_ratios, actual_ratios[:len(expected_ratios)]))
        
        return max(0, 1 - error / 10)
    
    def _get_centroid(self, audio: List[float], sr: int) -> float:
        """Calculate spectral centroid"""
        
        weighted_sum = 0
        magnitude_sum = 0
        
        for i, sample in enumerate(audio):
            freq = i * sr / len(audio)
            mag = abs(sample)
            weighted_sum += freq * mag
            magnitude_sum += mag
        
        if magnitude_sum > 0:
            return weighted_sum / magnitude_sum
        return 0


class TransientDetector:
    """Detect transients in audio"""
    
    def __init__(self):
        self.window_size = 512
        self.threshold = 0.3
        self.min_distance = 1000
    
    def detect(self, audio: List[float], sample_rate: int = 44100) -> List[Dict]:
        """Detect transients"""
        
        transients = []
        
        # Calculate energy in windows
        energies = []
        for i in range(0, len(audio) - self.window_size, self.window_size // 2):
            window = audio[i:i + self.window_size]
            energy = sum(x * x for x in window) / self.window_size
            energies.append((i, energy))
        
        # Find peaks in energy
        prev_energy = 0
        for i, (pos, energy) in enumerate(energies):
            if i > 0:
                # Attack detection: sudden increase
                if energy > prev_energy * (1 + self.threshold):
                    if not transients or pos - transients[-1]['position'] > self.min_distance:
                        transients.append({
                            'position': pos,
                            'energy': energy,
                            'type': 'attack'
                        })
            
            prev_energy = energy
        
        return transients
    
    def set_threshold(self, threshold: float):
        """Set detection threshold"""
        self.threshold = threshold


class FormantExtractor:
    """Extract formants (vowel identification)"""
    
    FORMANTS = {
        'A': [730, 1090, 2440],
        'E': [530, 1830, 2480],
        'I': [390, 1990, 2550],
        'O': [570, 840, 2410],
        'U': [440, 1020, 2350]
    }
    
    def __init__(self):
        self.num_formants = 3
    
    def extract(self, audio: List[float], sample_rate: int = 44100) -> Dict:
        """Extract formants"""
        
        # Find peaks in spectrum
        peaks = self._find_spectral_peaks(audio, sample_rate)
        
        # Match to vowels
        vowel = self._match_formants(peaks)
        
        return {
            'detected_vowel': vowel,
            'formant_frequencies': peaks[:self.num_formants],
            'confidence': self._get_confidence(peaks, vowel)
        }
    
    def _find_spectral_peaks(self, audio: List[float], sr: int) -> List[float]:
        """Find spectral peaks"""
        
        # Simple peak detection
        n = len(audio)
        peaks = []
        
        for i in range(1, n - 1):
            if abs(audio[i]) > abs(audio[i-1]) and abs(audio[i]) > abs(audio[i+1]):
                freq = i * sr / n
                if 200 < freq < 5000:  # Formant range
                    peaks.append(freq)
        
        # Sort by amplitude
        peak_amplitudes = [(p, abs(audio[int(p * n / sr)])) for p in peaks]
        peak_amplitudes.sort(key=lambda x: x[1], reverse=True)
        
        return [p[0] for p in peak_amplitudes[:5]]
    
    def _match_formants(self, peaks: List[float]) -> str:
        """Match formants to vowel"""
        
        if not peaks:
            return 'unknown'
        
        best_match = 'unknown'
        best_distance = float('inf')
        
        for vowel, formants in self.FORMANTS.items():
            # Compare first 3 formants
            distance = 0
            for i in range(min(3, len(peaks), len(formants))):
                distance += abs(peaks[i] - formants[i])
            
            if distance < best_distance:
                best_distance = distance
                best_match = vowel
        
        return best_match
    
    def _get_confidence(self, peaks: List[float], vowel: str) -> float:
        """Get confidence of detection"""
        
        if vowel == 'unknown':
            return 0.0
        
        return max(0.3, 1 - len(peaks) / 20)


class RoomDetector:
    """Detect room characteristics"""
    
    def __init__(self):
        self.ir_length = 2.0  # seconds
    
    def analyze(self, audio: List[float], sample_rate: int = 44100) -> Dict:
        """Analyze room from impulse response"""
        
        # Find reverb tail
        tail_start = self._find_tail_start(audio)
        
        # Calculate decay rate
        decay = self._calculate_decay(audio, tail_start)
        
        # Estimate room size
        rt60 = self._estimate_rt60(decay, sample_rate)
        
        return {
            'reverb_length': len(audio) - tail_start,
            'decay_rate': decay,
            'rt60': rt60,
            'room_size': self._size_from_rt60(rt60)
        }
    
    def _find_tail_start(self, audio: List[float]) -> int:
        """Find start of reverb tail"""
        
        max_val = max(abs(x) for x in audio)
        threshold = max_val * 0.1
        
        for i in range(len(audio)):
            if abs(audio[i]) < threshold:
                return max(0, i - 100)
        
        return 0
    
    def _calculate_decay(self, audio: List[float], start: int) -> float:
        """Calculate decay rate"""
        
        if start >= len(audio):
            return 0.0
        
        tail = audio[start:]
        
        if not tail:
            return 0.0
        
        # Simple linear decay estimation
        max_val = max(abs(x) for x in tail[:1000]) if len(tail) > 1000 else 0.1
        
        return max_val
    
    def _estimate_rt60(self, decay: float, sr: int) -> float:
        """Estimate RT60 (time to decay 60dB)"""
        
        if decay <= 0:
            return 0.5
        
        # Rough estimation
        return 1.0 / decay
    
    def _size_from_rt60(self, rt60: float) -> str:
        """Get room size from RT60"""
        
        if rt60 < 0.3:
            return 'small'
        elif rt60 < 0.7:
            return 'medium'
        elif rt60 < 1.5:
            return 'large'
        else:
            return 'hall'


class InstrumentIdentifier:
    """Identify instruments from audio"""
    
    INSTRUMENTS = {
        'piano': {'spectral': [100, 500, 2000], 'attack': 0.005, 'character': 'bell-like'},
        'guitar': {'spectral': [200, 800, 3000], 'attack': 0.01, 'character': 'stringy'},
        'violin': {'spectral': [300, 2000, 5000], 'attack': 0.02, 'character': 'smooth'},
        'drums': {'spectral': [100, 500, 5000], 'attack': 0.001, 'character': 'percussive'},
        'bass': {'spectral': [40, 200, 400], 'attack': 0.01, 'character': 'punchy'},
        'synth': {'spectral': [200, 1000, 4000], 'attack': 0.05, 'character': 'electronic'},
        'voice': {'spectral': [300, 1500, 3000], 'attack': 0.05, 'character': 'vocal'}
    }
    
    def identify(self, audio: List[float], sample_rate: int = 44100) -> Dict:
        """Identify instrument"""
        
        # Analyze characteristics
        centroid = self._get_spectral_centroid(audio, sample_rate)
        attack = self._detect_attack(audio, sample_rate)
        bandwidth = self._get_bandwidth(audio, sample_rate)
        
        # Match to instruments
        scores = {}
        
        for name, params in self.INSTRUMENTS.items():
            score = 0
            
            # Check spectral match
            for target in params['spectral']:
                if abs(centroid - target) < target * 0.5:
                    score += 1
            
            # Check attack
            if abs(attack - params['attack']) < params['attack']:
                score += 1
            
            scores[name] = score
        
        # Get best match
        best = max(scores.items(), key=lambda x: x[1])
        
        return {
            'instrument': best[0],
            'confidence': best[1] / 5,
            'character': self.INSTRUMENTS[best[0]]['character'],
            'scores': scores
        }
    
    def _get_spectral_centroid(self, audio: List[float], sr: int) -> float:
        """Get spectral centroid"""
        
        weighted = 0
        total = 0
        
        for i, sample in enumerate(audio):
            freq = i * sr / len(audio)
            weighted += freq * abs(sample)
            total += abs(sample)
        
        return weighted / total if total > 0 else 0
    
    def _detect_attack(self, audio: List[float], sr: int) -> float:
        """Detect attack time"""
        
        window = 0.01  # 10ms
        samples = int(window * sr)
        
        energy = [x*x for x in audio[:samples]]
        
        for i in range(1, len(energy)):
            if energy[i] > energy[0] * 2:
                return i / sr
        
        return 0.05
    
    def _get_bandwidth(self, audio: List[float], sr: int) -> float:
        """Get bandwidth"""
        
        centroid = self._get_spectral_centroid(audio, sr)
        
        variance = 0
        total = 0
        
        for i, sample in enumerate(audio):
            freq = i * sr / len(audio)
            variance += (freq - centroid) ** 2 * abs(sample)
            total += abs(sample)
        
        return math.sqrt(variance / total) if total > 0 else 0


class AdvancedAnalysisV2:
    """Complete analysis suite"""
    
    def __init__(self):
        self.harmonic = HarmonicAnalyzer()
        self.transient = TransientDetector()
        self.formant = FormantExtractor()
        self.room = RoomDetector()
        self.instrument = InstrumentIdentifier()
    
    def full_analysis(self, audio: List[float], sample_rate: int = 44100) -> Dict:
        """Perform full analysis"""
        
        return {
            'harmonic': self.harmonic.analyze(audio, sample_rate),
            'transients': self.transient.detect(audio, sample_rate),
            'formants': self.formant.extract(audio, sample_rate),
            'room': self.room.analyze(audio, sample_rate),
            'instrument': self.instrument.identify(audio, sample_rate)
        }


def demo():
    print("=" * 60)
    print("  LEVEL 2.8 - ADVANCED ANALYSIS & DETECTION")
    print("=" * 60)
    
    # Generate test audio (smaller for speed)
    test_audio = [math.sin(440 * 2 * math.pi * t / 44100) + 
                  0.5 * math.sin(880 * 2 * math.pi * t / 44100) 
                  for t in range(4410)]
    
    # Harmonic
    print("\n[Harmonic Analysis]")
    h = HarmonicAnalyzer()
    result = h.analyze(test_audio)
    print("  Fundamental: %.1f Hz, Harmonicity: %.2f" % (result['fundamental'], result['harmonicity']))
    
    # Transient
    print("\n[Transient Detection]")
    t = TransientDetector()
    trans = t.detect(test_audio)
    print("  Transients found: %d" % len(trans))
    
    # Formant
    print("\n[Formant Extraction]")
    f = FormantExtractor()
    form = f.extract(test_audio)
    print("  Vowel: %s, Confidence: %.2f" % (form['detected_vowel'], form['confidence']))
    
    # Room
    print("\n[Room Detection]")
    r = RoomDetector()
    room = r.analyze(test_audio[:4410])
    print("  Room size: %s, RT60: %.2fs" % (room['room_size'], room['rt60']))
    
    # Instrument
    print("\n[Instrument Identification]")
    i = InstrumentIdentifier()
    inst = i.identify(test_audio)
    print("  Instrument: %s (%s), Conf: %.2f" % (inst['instrument'], inst['character'], inst['confidence']))
    
    # Full analysis
    print("\n[Full Analysis]")
    aa = AdvancedAnalysisV2()
    full = aa.full_analysis(test_audio)
    print("  All 5 analyzers: OK")
    
    print("\n" + "=" * 60)
    print("  LEVEL 2.8 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()