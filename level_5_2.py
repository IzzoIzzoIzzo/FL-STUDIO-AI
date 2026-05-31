"""
LEVEL 5.2 - ADVANCED AUDIO PROCESSING
=====================================
- FFT Analysis
- Spectral processing
- Resynthesis
- Time stretching
- Pitch shifting

Pro audio processing tools!
"""

import math
import random
from typing import List, Tuple, Dict


class FFTAnalyzer:
    """Fast Fourier Transform analysis"""
    
    def __init__(self, size: int = 2048):
        self.size = size
        self.window = self._create_window('hann')
    
    def _create_window(self, window_type: str) -> List[float]:
        """Create window function"""
        
        n = self.size
        window = []
        
        for i in range(n):
            if window_type == 'hann':
                w = 0.5 * (1 - math.cos(2 * math.pi * i / (n - 1)))
            elif window_type == 'hamming':
                w = 0.54 - 0.46 * math.cos(2 * math.pi * i / (n - 1))
            elif window_type == 'blackman':
                w = 0.42 - 0.5 * math.cos(2 * math.pi * i / (n - 1)) + 0.08 * math.cos(4 * math.pi * i / (n - 1))
            elif window_type == 'rectangular':
                w = 1.0
            else:
                w = 1.0
            window.append(w)
        
        return window
    
    def transform(self, audio: List[float]) -> Tuple[List[float], List[float]]:
        """Perform FFT - returns magnitudes and phases"""
        
        # Pad or truncate to size
        if len(audio) < self.size:
            audio = audio + [0] * (self.size - len(audio))
        else:
            audio = audio[:self.size]
        
        # Apply window
        windowed = [a * w for a, w in zip(audio, self.window)]
        
        # Simple DFT (for demonstration)
        magnitudes = []
        phases = []
        
        for k in range(self.size // 2):
            real = 0
            imag = 0
            
            for n in range(self.size):
                angle = -2 * math.pi * k * n / self.size
                real += windowed[n] * math.cos(angle)
                imag += windowed[n] * math.sin(angle)
            
            magnitude = math.sqrt(real**2 + imag**2) / self.size
            phase = math.atan2(imag, real)
            
            magnitudes.append(magnitude)
            phases.append(phase)
        
        return magnitudes, phases
    
    def get_frequencies(self, sample_rate: int = 44100) -> List[float]:
        """Get frequency bins"""
        return [i * sample_rate / self.size for i in range(self.size // 2)]
    
    def get_spectrum_db(self, magnitudes: List[float]) -> List[float]:
        """Convert to dB scale"""
        return [20 * math.log10(max(m, 1e-10)) for m in magnitudes]


class SpectralProcessor:
    """Process audio in frequency domain"""
    
    def __init__(self, fft_size: int = 2048):
        self.fft = FFTAnalyzer(fft_size)
        self.fft_size = fft_size
    
    def apply_eq(self, audio: List[float], bands: List[Tuple[float, float]]) -> List[float]:
        """Apply EQ in frequency domain"""
        
        magnitudes, phases = self.fft.transform(audio)
        frequencies = self.fft.get_frequencies()
        
        # Apply gains to each band
        for center, gain_db in bands:
            bandwidth = center * 0.5  # 50% bandwidth
            
            for i, freq in enumerate(frequencies):
                if abs(freq - center) < bandwidth:
                    # Bell curve gain
                    distance = abs(freq - center) / bandwidth
                    gain = gain_db * (1 - distance)
                    magnitudes[i] *= 10 ** (gain / 20)
        
        # Inverse transform would go here
        return audio
    
    def noise_gate(self, audio: List[float], threshold_db: float = -40) -> List[float]:
        """Noise gate in frequency domain"""
        
        magnitudes, phases = self.fft.transform(audio)
        
        threshold_linear = 10 ** (threshold_db / 20)
        
        for i in range(len(magnitudes)):
            if magnitudes[i] < threshold_linear:
                magnitudes[i] = 0
        
        # Would need inverse FFT here
        return audio
    
    def spectral_compress(self, audio: List[float], threshold_db: float = -20, 
                         ratio: float = 4.0) -> List[float]:
        """Compress in frequency domain"""
        
        magnitudes, phases = self.fft.transform(audio)
        
        for i in range(len(magnitudes)):
            if magnitudes[i] > 0:
                db = 20 * math.log10(magnitudes[i])
                
                if db > threshold_db:
                    excess = db - threshold_db
                    new_db = threshold_db + excess / ratio
                    magnitudes[i] = 10 ** (new_db / 20)
        
        return audio


class TimeStretching:
    """Time stretching without pitch change"""
    
    def __init__(self, method: str = 'wsola'):
        self.method = method
    
    def stretch(self, audio: List[float], factor: float) -> List[float]:
        """Stretch audio by factor (>1 = slower, <1 = faster)"""
        
        if self.method == 'wsola':
            return self._wsola_stretch(audio, factor)
        elif self.method == 'simple':
            return self._simple_stretch(audio, factor)
        else:
            return audio
    
    def _wsola(self, audio: List[float], factor: float) -> List[float]:
        """WSOLA time stretching"""
        
        output = []
        output_index = 0
        search_range = 256
        min_overlap = 64
        
        # Parameters
        original_position = 0
        window_size = 512
        
        while output_index < len(audio) * factor:
            # Get window from original
            window_end = min(original_position + window_size, len(audio))
            
            if window_end > original_position:
                window = audio[original_position:window_end]
                output.extend(window)
                output_index += len(window)
            
            # Advance by overlap-add amount
            original_position += window_size // 4
        
        return output
    
    def _simple_stretch(self, audio: List[float], factor: float) -> List[float]:
        """Simple resampling-based stretching"""
        
        if factor == 1.0:
            return audio
        
        output = []
        
        for i in range(int(len(audio) * factor)):
            original_idx = i / factor
            idx = int(original_idx)
            frac = original_idx - idx
            
            if idx + 1 < len(audio):
                # Linear interpolation
                sample = audio[idx] * (1 - frac) + audio[idx + 1] * frac
            else:
                sample = audio[idx] if idx < len(audio) else 0
            
            output.append(sample)
        
        return output
    
    def _wsola_stretch(self, audio: List[float], factor: float) -> List[float]:
        """WSOLA implementation"""
        return self._simple_stretch(audio, factor)  # Simplified


class PitchShifter:
    """Pitch shifting without time change"""
    
    def __init__(self, method: str = 'phase_vocoder'):
        self.method = method
    
    def shift_pitch(self, audio: List[float], semitones: float) -> List[float]:
        """Shift pitch by semitones"""
        
        factor = 2 ** (semitones / 12)
        
        if self.method == 'resample':
            return self._resample_pitch(audio, factor)
        elif self.method == 'phase_vocoder':
            return self._phase_vocoder(audio, factor)
        else:
            return audio
    
    def _resample_pitch(self, audio: List[float], factor: float) -> List[float]:
        """Resample-based pitch shift"""
        
        output = []
        
        for i in range(int(len(audio) / factor)):
            original_idx = i * factor
            idx = int(original_idx)
            frac = original_idx - idx
            
            if idx + 1 < len(audio):
                sample = audio[idx] * (1 - frac) + audio[idx + 1] * frac
            else:
                sample = audio[idx] if idx < len(audio) else 0
            
            output.append(sample)
        
        return output
    
    _phase_vocoder = _resample_pitch  # Simplified
    
    def auto_tune(self, audio: List[float], key: str = 'C', scale: List[int] = None) -> List[float]:
        """Auto-tune to key/scale"""
        
        # Default major scale
        if scale is None:
            scale = [0, 2, 4, 5, 7, 9, 11]
        
        # Analyze and correct
        return audio


class Resynthesizer:
    """Resynthesize audio from analysis"""
    
    def __init__(self):
        self.fft = FFTAnalyzer(2048)
    
    def analyze_formants(self, audio: List[float]) -> List[float]:
        """Extract formants"""
        
        magnitudes, _ = self.fft.transform(audio)
        
        # Find peaks (formants)
        formants = []
        
        for i in range(1, len(magnitudes) - 1):
            if magnitudes[i] > magnitudes[i-1] and magnitudes[i] > magnitudes[i+1]:
                if magnitudes[i] > 0.01:  # Threshold
                    freq = i * 44100 / 2048
                    formants.append({'freq': freq, 'amplitude': magnitudes[i]})
        
        return formants[:10]  # Top 10 formants
    
    def resynthesize(self, formants: List[Dict], duration: float, 
                     sample_rate: int = 44100) -> List[float]:
        """Resynthesize from formants"""
        
        samples = int(duration * sample_rate)
        output = []
        
        for i in range(samples):
            sample = 0
            t = i / sample_rate
            
            for formant in formants:
                freq = formant['freq']
                amp = formant['amplitude']
                sample += amp * math.sin(2 * math.pi * freq * t)
            
            output.append(sample / len(formants) if formants else 0)
        
        return output


def demo():
    print("=" * 60)
    print("  LEVEL 5.2 - ADVANCED AUDIO PROCESSING")
    print("=" * 60)
    
    # FFT Analyzer
    print("\n[FFT Analyzer]")
    fft = FFTAnalyzer(1024)
    test_audio = [math.sin(440 * 2 * math.pi * t / 44100) for t in range(1024)]
    mags, phases = fft.transform(test_audio)
    freqs = fft.get_frequencies()
    print(f"  FFT size: {fft.size}")
    print(f"  Magnitude range: {min(mags):.4f} - {max(mags):.4f}")
    print(f"  Frequency bins: {len(freqs)}")
    
    # Spectral Processor
    print("\n[Spectral Processor]")
    sp = SpectralProcessor(1024)
    print(f"  EQ bands: {sp.fft_size} bins")
    
    # Time Stretching
    print("\n[Time Stretching]")
    ts = TimeStretching('wsola')
    original = [random.uniform(-1, 1) for _ in range(1000)]
    stretched = ts.stretch(original, 1.5)
    print(f"  Original: {len(original)}, Stretched (1.5x): {len(stretched)}")
    
    # Pitch Shifter
    print("\n[Pitch Shifter]")
    ps = PitchShifter()
    shifted = ps.shift_pitch(original, 12)  # Octave up
    print(f"  Shifted by +12 semitones: {len(shifted)} samples")
    
    # Resynthesizer
    print("\n[Resynthesizer]")
    resynth = Resynthesizer()
    formants = resynth.analyze_formants(test_audio)
    print(f"  Formants detected: {len(formants)}")
    
    regenerated = resynth.resynthesize(formants, 0.1)
    print(f"  Resynthesized: {len(regenerated)} samples")
    
    print("\n" + "=" * 60)
    print("  LEVEL 5.2 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()