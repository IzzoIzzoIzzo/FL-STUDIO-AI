"""
LEVEL 6.2 - ADVANCED MIXING & MASTERING
=======================================
- Parametric EQ
- Multi-band compression
- Stereo enhancement
- Loudness maximizer
- Spectrum analyzer

Pro mastering tools!
"""

import math
import random
from typing import List, Dict


class ParametricEQ:
    """8-band parametric EQ"""
    
    def __init__(self):
        self.bands = []
        self._init_bands()
    
    def _init_bands(self):
        """Initialize default bands"""
        frequencies = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        
        for freq in frequencies:
            self.bands.append({
                'frequency': freq,
                'gain': 0.0,
                'q': 1.0,
                'type': 'peaking',
                'active': True
            })
    
    def set_band(self, index: int, gain: float, q: float = 1.0):
        """Set band parameters"""
        if 0 <= index < len(self.bands):
            self.bands[index]['gain'] = gain
            self.bands[index]['q'] = q
    
    def process(self, audio: List[float]) -> List[float]:
        """Process audio through EQ"""
        
        output = list(audio)
        
        for band in self.bands:
            if not band['active'] or band['gain'] == 0:
                continue
            
            # Simple shelving/peaking filter
            # (simplified - real implementation would use proper biquads)
            gain = band['gain']
            
            # Apply gain
            for i in range(len(output)):
                output[i] *= (10 ** (gain / 20))
        
        return output
    
    def get_settings(self) -> Dict:
        """Get current EQ settings"""
        return {'bands': len(self.bands), 'active': sum(1 for b in self.bands if b['active'])}


class MultiBandCompressor:
    """4-band multi-band compressor"""
    
    def __init__(self):
        self.bands = [
            {'name': 'sub', 'freq_low': 20, 'freq_high': 60, 'threshold': -12, 'ratio': 4, 'attack': 10, 'release': 100},
            {'name': 'bass', 'freq_low': 60, 'freq_high': 250, 'threshold': -15, 'ratio': 3, 'attack': 15, 'release': 150},
            {'name': 'mid', 'freq_low': 250, 'freq_high': 4000, 'threshold': -18, 'ratio': 2, 'attack': 20, 'release': 200},
            {'name': 'high', 'freq_low': 4000, 'freq_high': 20000, 'threshold': -21, 'ratio': 1.5, 'attack': 5, 'release': 100}
        ]
    
    def set_band(self, name: str, threshold: float = None, ratio: float = None):
        """Set band parameters"""
        for band in self.bands:
            if band['name'] == name:
                if threshold is not None:
                    band['threshold'] = threshold
                if ratio is not None:
                    band['ratio'] = ratio
    
    def process(self, audio: List[float]) -> List[float]:
        """Process with multi-band compression"""
        # Simplified - would split into bands in real implementation
        output = []
        
        for sample in audio:
            # Apply gentle compression
            if abs(sample) > 0.3:
                sample = 0.3 + (abs(sample) - 0.3) * 0.8
            output.append(sample)
        
        return output


class StereoEnhancer:
    """Stereo width and enhancement"""
    
    MODES = ['mono', 'normal', 'wide', 'ultra']
    
    def __init__(self, mode: str = 'normal'):
        self.mode = mode
        self.width = 1.0
        self.mid_side = False
        
        if mode == 'mono':
            self.width = 0.0
        elif mode == 'wide':
            self.width = 1.5
        elif mode == 'ultra':
            self.width = 2.0
    
    def process(self, left: List[float], right: List[float]) -> tuple:
        """Process stereo enhancement"""
        
        if self.width == 0:
            # Mono
            mono = [(l + r) / 2 for l, r in zip(left, right)]
            return mono, mono
        
        output_left = []
        output_right = []
        
        for l, r in zip(left, right):
            mid = (l + r) / 2
            side = (l - r) / 2
            
            # Enhance width
            side *= self.width
            
            # Recombine
            output_left.append(mid + side)
            output_right.append(mid - side)
        
        return output_left, output_right


class LoudnessMaximizer:
    """Loudness maximizer/limiter"""
    
    def __init__(self):
        self.ceiling = -0.1  # dB
        self.lookahead = 10  # ms
        self.release = 100   # ms
    
    def process(self, audio: List[float]) -> List[float]:
        """Process with limiting"""
        
        output = []
        gain = 1.0
        
        for sample in audio:
            if abs(sample) > 0.9:
                # Soft clip
                sample = 0.9 + (abs(sample) - 0.9) * 0.1
                if sample > 0.9:
                    sample = 0.9
            
            output.append(sample * 0.95)  # Slight reduction for safety
        
        return output
    
    def set_ceiling(self, db: float):
        """Set ceiling in dB"""
        self.ceiling = db


class SpectrumAnalyzer:
    """Real-time spectrum analyzer"""
    
    def __init__(self, fft_size: int = 2048):
        self.fft_size = fft_size
        self.window = self._hann_window(fft_size)
        self.bands = ['31', '62', '125', '250', '500', '1k', '2k', '4k', '8k', '16k']
    
    def _hann_window(self, size: int) -> List[float]:
        """Create Hann window"""
        return [0.5 * (1 - math.cos(2 * math.pi * i / (size - 1))) for i in range(size)]
    
    def analyze(self, audio: List[float]) -> Dict:
        """Analyze spectrum"""
        
        if len(audio) < self.fft_size:
            audio = audio + [0] * (self.fft_size - len(audio))
        else:
            audio = audio[:self.fft_size]
        
        # Apply window
        windowed = [a * w for a, w in zip(audio, self.window)]
        
        # Simple magnitude calculation (not full FFT - simplified)
        magnitudes = []
        
        for i in range(10):
            start = i * (self.fft_size // 10)
            end = start + (self.fft_size // 10)
            band_samples = windowed[start:end]
            avg = sum(abs(s) for s in band_samples) / len(band_samples)
            magnitudes.append(avg)
        
        # Normalize to dB-like values
        db_values = [max(0, min(100, m * 100)) for m in magnitudes]
        
        return {
            'bands': self.bands,
            'magnitudes': magnitudes,
            'db': db_values,
            'peak': max(magnitudes) if magnitudes else 0
        }
    
    def get_visualization(self, analysis: Dict) -> str:
        """Get ASCII visualization"""
        chars = ' .:-=+*#'
        result = []
        
        for db in analysis['db']:
            level = int(db / 12.5)
            level = max(0, min(8, level))
            result.append(chars[level])
        
        return ''.join(result)


class MasteringChain:
    """Complete mastering chain"""
    
    def __init__(self):
        self.eq = ParametricEQ()
        self.compressor = MultiBandCompressor()
        self.stereo = StereoEnhancer()
        self.limiter = LoudnessMaximizer()
        self.analyzer = SpectrumAnalyzer()
    
    def process(self, audio: List[float]) -> Dict:
        """Process full mastering chain"""
        
        # Create stereo (duplicate mono to stereo)
        left = list(audio)
        right = list(audio)
        
        # Process
        left = self.eq.process(left)
        left = self.compressor.process(left)
        left, right = self.stereo.process(left, right)
        left = self.limiter.process(left)
        right = self.limiter.process(right)
        
        # Analyze
        analysis = self.analyzer.analyze(left)
        
        return {
            'left': left,
            'right': right,
            'analysis': analysis,
            'loudness': analysis['peak']
        }


def demo():
    print("=" * 60)
    print("  LEVEL 6.2 - ADVANCED MIXING & MASTERING")
    print("=" * 60)
    
    # Parametric EQ
    print("\n[Parametric EQ]")
    eq = ParametricEQ()
    eq.set_band(0, 3.0)  # Boost bass
    eq.set_band(5, -2.0)  # Cut mids
    audio = eq.process([0.5] * 4410)
    print("  Bands: %d" % len(eq.bands))
    
    # Multi-band Compressor
    print("\n[Multi-Band Compressor]")
    mbc = MultiBandCompressor()
    mbc.set_band('mid', threshold=-20, ratio=3)
    print("  Bands: %d" % len(mbc.bands))
    
    # Stereo Enhancer
    print("\n[Stereo Enhancer]")
    se = StereoEnhancer('wide')
    left = [0.5] * 100
    right = [0.3] * 100
    l, r = se.process(left, right)
    print("  Mode: %s, Width: %.1f" % (se.mode, se.width))
    
    # Loudness Maximizer
    print("\n[Loudness Maximizer]")
    lm = LoudnessMaximizer()
    audio = lm.process([0.8] * 4410)
    print("  Ceiling: %.1f dB" % lm.ceiling)
    
    # Spectrum Analyzer
    print("\n[Spectrum Analyzer]")
    sa = SpectrumAnalyzer()
    analysis = sa.analyze([math.sin(440 * 2 * math.pi * i / 44100) for i in range(2048)])
    viz = sa.get_visualization(analysis)
    print("  Peak: %.2f, Viz: %s" % (analysis['peak'], viz[:20]))
    
    # Mastering Chain
    print("\n[Mastering Chain]")
    mc = MasteringChain()
    result = mc.process([0.5] * 44100)
    print("  Loudness: %.2f" % result['loudness'])
    
    print("\n" + "=" * 60)
    print("  LEVEL 6.2 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()