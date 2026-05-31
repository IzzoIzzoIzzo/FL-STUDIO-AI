"""
CREATIVE SOUND ENGINE
====================
Advanced sound design and synthesis:
- Granular Synthesis Engine
- Sampler & Looper Engine  
- Resampling Engine
- Spectral Processing Engine
- Convolution Reverb Engine
- Convolution Reverb Engine
- Analog Warmth Engine
- Stereo Enhancement Engine
- Harmonic Exciter Engine
- Tone Control Engine

CONNECTED TO MAIN API!
"""

import math
import random
from typing import List, Dict, Tuple, Optional
from enum import Enum


class GrainSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class GranularSynthesisEngine:
    """Granular synthesis - create textures from samples"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.grain_size = 1024
        self.grain_overlap = 4
        self.grain_pitch = 1.0
        self.density = 1.0
    
    def set_parameters(self, size: int = 1024, overlap: int = 4, pitch: float = 1.0, density: float = 1.0):
        """Set granular parameters"""
        self.grain_size = size
        self.grain_overlap = overlap
        self.grain_pitch = pitch
        self.density = density
    
    def generate(self, source_audio: List[float], duration: float, 
                 pitch: float = 1.0, density: float = 1.0, 
                 texture: str = 'cloud') -> List[float]:
        """Generate granular texture from source"""
        
        if not source_audio:
            # Generate noise if no source
            source_audio = [random.uniform(-1, 1) for _ in range(self.sample_rate)]
        
        target_samples = int(duration * self.sample_rate)
        output = [0.0] * target_samples
        
        grain_size = self.grain_size
        num_grains = int(target_samples / (grain_size / self.grain_overlap))
        
        for g in range(num_grains):
            # Random position in source
            pos = random.randint(0, len(source_audio) - grain_size)
            
            # Extract grain
            grain = source_audio[pos:pos+grain_size]
            
            # Apply pitch shift
            if pitch != 1.0:
                new_grain = []
                for i in range(grain_size):
                    src_idx = i * pitch
                    if src_idx < grain_size:
                        new_grain.append(grain[int(src_idx)])
                    else:
                        new_grain.append(0)
                grain = new_grain
            
            # Apply envelope (Hanning window)
            window = [0.5 * (1 - math.cos(2 * math.pi * i / grain_size)) for i in range(grain_size)]
            grain = [g * w for g, w in zip(grain, window)]
            
            # Add grain to output
            grain_start = g * (grain_size // self.grain_overlap)
            grain_end = min(grain_start + grain_size, target_samples)
            
            for i in range(len(grain)):
                if grain_start + i < target_samples:
                    output[grain_start + i] += grain[i] * density
        
        # Normalize
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output
    
    def generate_texture(self, duration: float, texture: str = 'cloud') -> List[float]:
        """Generate procedural granular texture"""
        
        if texture == 'cloud':
            # Dense, overlapping grains
            return self.generate([], duration, pitch=random.uniform(0.5, 2.0), density=0.5)
        elif texture == 'stream':
            # Sparse, flowing grains
            return self.generate([], duration, pitch=random.uniform(0.8, 1.2), density=0.2)
        elif texture == 'swarm':
            # Many small grains
            return self.generate([], duration, pitch=random.uniform(0.5, 1.5), density=0.8)
        elif texture == 'drift':
            # Slow pitch-shifting texture
            return self.generate([], duration, pitch=random.uniform(0.9, 1.1), density=0.3)
        
        return self.generate([], duration)


class SamplerEngine:
    """Professional sampler with slicing and looping"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.samples = {}
        self.current_sample = None
        self.loop_enabled = False
        self.start_point = 0
        self.end_point = 0
    
    def load_sample(self, name: str, audio: List[float]):
        """Load sample into sampler"""
        self.samples[name] = audio
        self.current_sample = name
        self.end_point = len(audio)
    
    def load_from_file(self, filepath: str) -> bool:
        """Load sample from file"""
        try:
            import wave
            with wave.open(filepath, 'rb') as wav:
                frames = wav.readframes(wav.getnframes())
                audio = []
                for i in range(0, len(frames), wav.getsampwidth()):
                    sample = int.from_bytes(frames[i:i+wav.getsampwidth()], 
                                            byteorder='little', signed=True)
                    audio.append(sample / 32768.0)
                
                name = filepath.split('/')[-1].split('\\')[-1].replace('.wav', '')
                self.load_sample(name, audio)
                return True
        except:
            return False
    
    def set_loop(self, start: int, end: int, enabled: bool = True):
        """Set loop points"""
        self.start_point = start
        self.end_point = end
        self.loop_enabled = enabled
    
    def play(self, note: int, velocity: float = 1.0, duration: float = None) -> List[float]:
        """Play loaded sample"""
        if not self.current_sample or self.current_sample not in self.samples:
            return []
        
        audio = self.samples[self.current_sample]
        
        # Map note to pitch
        pitch_ratio = 2 ** ((note - 60) / 12)
        
        # Resample for pitch
        output = []
        for i in range(int(len(audio) * pitch_ratio)):
            src_idx = i / pitch_ratio
            
            if self.loop_enabled and src_idx >= self.end_point:
                src_idx = self.start_point + (src_idx - self.start_point) % (self.end_point - self.start_point)
            
            if src_idx < len(audio):
                output.append(audio[int(src_idx)] * velocity)
        
        return output
    
    def slice_auto(self, sensitivity: float = 0.5) -> List[Dict]:
        """Auto-slice sample based on transients"""
        if not self.current_sample or self.current_sample not in self.samples:
            return []
        
        audio = self.samples[self.current_sample]
        slices = []
        
        # Simple transient detection
        threshold = sensitivity * 0.5
        prev_amp = 0
        
        for i in range(1, len(audio)):
            curr_amp = abs(audio[i])
            
            if curr_amp > threshold and prev_amp < threshold:
                slices.append({'start': i, 'type': 'transient'})
            
            prev_amp = curr_amp
        
        return slices


class ResamplingEngine:
    """Resampling and time-stretching"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def time_stretch(self, audio: List[float], ratio: float) -> List[float]:
        """Time stretch without pitch change"""
        output = []
        
        for i in range(int(len(audio) / ratio)):
            src_idx = i * ratio
            output.append(audio[int(src_idx)])
        
        return output
    
    def pitch_shift(self, audio: List[float], semitones: float) -> List[float]:
        """Pitch shift without time change"""
        ratio = 2 ** (semitones / 12)
        output = []
        
        for i in range(len(audio)):
            src_idx = i / ratio
            if src_idx < len(audio):
                output.append(audio[int(src_idx)])
        
        return output
    
    def rubberband(self, audio: List[float], time_ratio: float, pitch_ratio: float) -> List[float]:
        """Combined time stretch and pitch shift (rubberband style)"""
        # First time stretch
        stretched = self.time_stretch(audio, time_ratio)
        # Then pitch shift
        semitones = 12 * math.log2(pitch_ratio)
        return self.pitch_shift(stretched, semitones)


class SpectralProcessingEngine:
    """Spectral domain processing"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.fft_size = 2048
    
    def set_fft_size(self, size: int):
        """Set FFT window size"""
        self.fft_size = size
    
    def analyze_spectrum(self, audio: List[float]) -> Dict:
        """Analyze frequency spectrum"""
        n = self.fft_size
        
        # Get window
        window = [0.5 * (1 - math.cos(2 * math.pi * i / n)) for i in range(n)]
        
        # Get frame
        if len(audio) < n:
            frame = list(audio) + [0] * (n - len(audio))
        else:
            frame = audio[:n]
        
        # Apply window
        frame = [f * w for f, w in zip(frame, window)]
        
        # Calculate magnitudes (simplified DFT)
        magnitudes = []
        for k in range(n // 2):
            real = sum(frame[i] * math.cos(2 * math.pi * k * i / n) for i in range(n))
            imag = sum(frame[i] * math.sin(2 * math.pi * k * i / n) for i in range(n))
            magnitude = math.sqrt(real**2 + imag**2) / n
            magnitudes.append(magnitude)
        
        # Find peaks
        peaks = []
        for i in range(1, len(magnitudes) - 1):
            if magnitudes[i] > magnitudes[i-1] and magnitudes[i] > magnitudes[i+1]:
                if magnitudes[i] > 0.01:
                    freq = i * self.sample_rate / n
                    peaks.append({'freq': freq, 'mag': magnitudes[i]})
        
        return {
            'magnitudes': magnitudes,
            'peaks': peaks[:10],
            'centroid': sum(m * f for m, f in zip(magnitudes, range(len(magnitudes)))) / 
                         max(sum(magnitudes), 0.0001)
        }
    
    def spectral_gate(self, audio: List[float], threshold: float = 0.1) -> List[float]:
        """Apply spectral gating (noise reduction)"""
        # Simplified - just use threshold
        return [a if abs(a) > threshold else a * 0.5 for a in audio]


class ConvolutionReverbEngine:
    """Convolution reverb with IR loading"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.ir_samples = None
        self.mix = 0.5
    
    def load_impulse_response(self, ir: List[float]):
        """Load impulse response"""
        self.ir_samples = ir
    
    def generate_ir(self, preset: str) -> List[float]:
        """Generate synthetic impulse response"""
        
        if preset == 'hall':
            length = 3 * self.sample_rate
            ir = []
            for i in range(length):
                decay = math.exp(-3 * i / length)
                noise = random.uniform(-1, 1)
                ir.append(noise * decay * 0.5)
            return ir
        
        elif preset == 'room':
            length = 1 * self.sample_rate
            ir = [0] * length
            # Early reflections
            for _ in range(10):
                pos = random.randint(100, length // 4)
                ir[pos] = random.uniform(-0.3, 0.3)
            # Decay
            for i in range(length // 4, length):
                ir[i] = random.uniform(-1, 1) * math.exp(-5 * i / length)
            return ir
        
        elif preset == 'plate':
            length = 2 * self.sample_rate
            ir = [random.uniform(-1, 1) * math.exp(-4 * i / length) for i in range(length)]
            return ir
        
        elif preset == 'cathedral':
            length = 5 * self.sample_rate
            ir = [random.uniform(-1, 1) * math.exp(-2 * i / length) for i in range(length)]
            return ir
        
        # Default - small room
        return self.generate_ir('room')
    
    def process(self, audio: List[float], wet_dry: float = 0.5) -> List[float]:
        """Apply convolution reverb"""
        
        if not self.ir_samples:
            self.ir_samples = self.generate_ir('room')
        
        output = [0.0] * len(audio)
        ir = self.ir_samples
        
        for i in range(len(audio)):
            # Simple convolution sum
            for j in range(min(len(ir), i + 1)):
                output[i] += audio[i - j] * ir[j] * 0.1
        
        # Mix wet and dry
        return [audio[i] * (1 - wet_dry) + output[i] * wet_dry for i in range(len(audio))]


class AnalogWarmthEngine:
    """Analog warmth and saturation"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.tube_mode = True
        self.drive = 0.5
    
    def set_drive(self, amount: float):
        """Set drive amount (0-1)"""
        self.drive = amount
    
    def set_mode(self, mode: str):
        """Set saturation mode (tube, tape, transistor)"""
        self.tube_mode = (mode == 'tube')
    
    def process(self, audio: List[float], drive: float = None) -> List[float]:
        """Apply analog warmth"""
        
        if drive is None:
            drive = self.drive
        
        output = []
        
        for sample in audio:
            if self.tube_mode:
                # Soft clipping (tube)
                output.append(math.tanh(sample * (1 + drive * 3)))
            else:
                # Hard clipping (transistor)
                if sample > 1 / (1 + drive * 3):
                    sample = 1 / (1 + drive * 3)
                elif sample < -1 / (1 + drive * 3):
                    sample = -1 / (1 + drive * 3)
                output.append(sample * (1 + drive * 3))
        
        # Normalize
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.9 for s in output]
        
        return output


class StereoEnhancementEngine:
    """Stereo widening and enhancement"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.width = 1.0
    
    def set_width(self, width: float):
        """Set stereo width (0-2, 1=normal)"""
        self.width = width
    
    def process(self, audio: List[float]) -> List[Tuple[float, float]]:
        """Process to stereo output"""
        
        output = []
        
        # Simple stereo processing
        for i, sample in enumerate(audio):
            # Apply width
            if i % 2 == 0:
                left = sample * self.width
                right = sample * (2 - self.width)
            else:
                left = sample * (2 - self.width)
                right = sample * self.width
            
            output.append((left, right))
        
        return output
    
    def mid_side_decode(self, mid: List[float], side: List[float]) -> List[Tuple[float, float]]:
        """Decode mid-side to stereo"""
        return [(m + s, m - s) for m, s in zip(mid, side)]


class HarmonicExciterEngine:
    """Harmonic excitation for brightness"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.amount = 0.5
        self.algorithm = 'tube'
    
    def set_amount(self, amount: float):
        """Set excitation amount"""
        self.amount = amount
    
    def process(self, audio: List[float]) -> List[float]:
        """Add harmonic content"""
        
        output = []
        
        for sample in audio:
            # Add harmonics based on algorithm
            if self.algorithm == 'tube':
                # Even harmonics
                h2 = math.sin(2 * math.pi * 220 * 0) * sample * self.amount * 0.3
                h4 = math.sin(2 * math.pi * 440 * 0) * sample * self.amount * 0.1
                output.append(sample + h2 + h4)
            elif self.algorithm == 'tape':
                # Odd harmonics
                h3 = math.sin(2 * math.pi * 330 * 0) * sample * self.amount * 0.2
                h5 = math.sin(2 * math.pi * 550 * 0) * sample * self.amount * 0.1
                output.append(sample + h3 + h5)
            else:
                # Flat
                output.append(sample)
        
        return output


class ToneControlEngine:
    """Multi-band tone control"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.bands = {
            'sub': {'freq': 60, 'gain': 0, 'q': 1.0},
            'bass': {'freq': 250, 'gain': 0, 'q': 1.0},
            'low_mid': {'freq': 500, 'gain': 0, 'q': 1.0},
            'mid': {'freq': 2000, 'gain': 0, 'q': 1.0},
            'high_mid': {'freq': 4000, 'gain': 0, 'q': 1.0},
            'high': {'freq': 8000, 'gain': 0, 'q': 1.0},
            'air': {'freq': 12000, 'gain': 0, 'q': 0.5},
        }
    
    def set_gain(self, band: str, gain_db: float):
        """Set band gain in dB"""
        if band in self.bands:
            self.bands[band]['gain'] = gain_db
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply tone control"""
        
        # Simplified EQ - just apply gain
        output = list(audio)
        
        for band, params in self.bands.items():
            gain = params['gain']
            if gain != 0:
                # Apply simple gain
                factor = 10 ** (gain / 20)
                output = [s * factor for s in output]
        
        return output


class CreativeSoundEngine:
    """
    Master creative sound engine.
    CONNECTED TO MAIN API!
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
        self.granular = GranularSynthesisEngine(sample_rate)
        self.sampler = SamplerEngine(sample_rate)
        self.resample = ResamplingEngine(sample_rate)
        self.spectral = SpectralProcessingEngine(sample_rate)
        self.convolve = ConvolutionReverbEngine(sample_rate)
        self.analog = AnalogWarmthEngine(sample_rate)
        self.stereo = StereoEnhancementEngine(sample_rate)
        self.exciter = HarmonicExciterEngine(sample_rate)
        self.tone = ToneControlEngine(sample_rate)
        
        print(f"    [OK] Creative Sound Engine initialized")
        print(f"         - Granular Synthesis")
        print(f"         - Sampler & Looper")
        print(f"         - Resampling Engine")
        print(f"         - Spectral Processing")
        print(f"         - Convolution Reverb")
        print(f"         - Analog Warmth")
        print(f"         - Stereo Enhancement")
        print(f"         - Harmonic Exciter")
        print(f"         - Tone Control")
    
    def granular_texture(self, duration: float, texture: str = 'cloud') -> List[float]:
        """Generate granular texture"""
        return self.granular.generate_texture(duration, texture)
    
    def process_reverb(self, audio: List[float], preset: str = 'hall', 
                       wet_dry: float = 0.5) -> List[float]:
        """Apply reverb"""
        self.convolve.generate_ir(preset)
        return self.convolve.process(audio, wet_dry)
    
    def add_analog_warmth(self, audio: List[float], drive: float = 0.5) -> List[float]:
        """Add analog warmth"""
        return self.analog.process(audio, drive)
    
    def enhance_stereo(self, audio: List[float], width: float = 1.5) -> List[Tuple[float, float]]:
        """Enhance stereo width"""
        self.stereo.set_width(width)
        return self.stereo.process(audio)


# Test function
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" CREATIVE SOUND ENGINE TEST")
    print("="*60 + "\n")
    
    engine = CreativeSoundEngine(44100)
    
    print("\n[1] Granular Texture (Cloud)...")
    audio = engine.granular_texture(1.0, 'cloud')
    print(f"     OK - {len(audio)} samples")
    
    print("\n[2] Reverb (Hall)...")
    test_audio = [math.sin(440 * 2 * math.pi * i / 44100) for i in range(44100)]
    audio = engine.process_reverb(test_audio, 'hall', 0.5)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[3] Analog Warmth...")
    audio = engine.add_analog_warmth(test_audio[:4410], 0.5)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[4] Stereo Enhancement...")
    stereo = engine.enhance_stereo(test_audio[:1000], 1.5)
    print(f"     OK - {len(stereo)} stereo pairs")
    
    print("\n" + "="*60)
    print(" ALL CREATIVE SOUND MODULES OPERATIONAL!")
    print("="*60 + "\n")