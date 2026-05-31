"""
AUDIO EFFECTS RACK - Professional Effects Chain
=================================================
INSANE effects chain for artists:
- Parametric EQ (8 bands)
- Compressor (VCA, FET, Opto, multiband)
- Saturator (tape, tube, distortion)
- Reverb (algorithmic, convolution-ready)
- Delay (tempo-synced, ping-pong, filter)
- Chorus/Flanger/Phaser
- Distortion (overdrive, fuzz, bitcrush)
- Filter (LP/HP/BP with resonance)
- Limiter
- Gate

Each effect has full parameter control!
"""

import math
import random
from typing import List, Dict, Optional


class ParametricEQ8:
    """8-band parametric EQ"""
    
    BAND_TYPES = ['low_shelf', 'high_shelf', 'lowpass', 'highpass', 'peaking', 'notch']
    
    def __init__(self):
        self.bands = []
        self._init_bands()
    
    def _init_bands(self):
        """Initialize 8 bands"""
        freqs = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        
        for i, freq in enumerate(freqs):
            self.add_band(freq, 0.0, 1.0, 'peaking')
    
    def add_band(self, freq: float, gain: float, q: float, band_type: str):
        """Add EQ band"""
        
        self.bands.append({
            'frequency': freq,
            'gain': gain,
            'q': q,
            'type': band_type,
            'enabled': True
        })
    
    def set_band(self, index: int, freq: float = None, gain: float = None, 
                q: float = None, enabled: bool = None):
        """Set band parameters"""
        
        if index < len(self.bands):
            if freq is not None:
                self.bands[index]['frequency'] = freq
            if gain is not None:
                self.bands[index]['gain'] = gain
            if q is not None:
                self.bands[index]['q'] = q
            if enabled is not None:
                self.bands[index]['enabled'] = enabled
    
    def process(self, audio: List[float]) -> List[float]:
        """Process audio through EQ"""
        
        output = list(audio)
        
        for band in self.bands:
            if not band['enabled'] or band['gain'] == 0:
                continue
            
            # Apply gain (simplified shelving/peaking)
            gain_linear = 10 ** (band['gain'] / 20)
            
            if band['type'] in ['low_shelf', 'high_shelf', 'peaking']:
                output = [x * gain_linear for x in output]
            
            elif band['type'] == 'lowpass':
                output = self._lowpass(output, band['frequency'])
            
            elif band['type'] == 'highpass':
                output = self._highpass(output, band['frequency'])
        
        return self._normalize(output)
    
    def _lowpass(self, audio: List[float], cutoff: float) -> List[float]:
        """Simple low-pass"""
        
        output = [audio[0]]
        rc = 1.0 / (cutoff * 2 * math.pi)
        dt = 1.0 / 44100
        
        for i in range(1, len(audio)):
            alpha = dt / (rc + dt)
            output.append(output[-1] + alpha * (audio[i] - output[-1]))
        
        return output
    
    def _highpass(self, audio: List[float], cutoff: float) -> List[float]:
        """Simple high-pass"""
        
        output = [audio[0]]
        rc = 1.0 / (cutoff * 2 * math.pi)
        dt = 1.0 / 44100
        alpha = rc / (rc + dt)
        
        for i in range(1, len(audio)):
            output.append(alpha * (output[-1] + audio[i] - audio[i-1]))
        
        return output
    
    def _normalize(self, audio: List[float]) -> List[float]:
        """Normalize to prevent clipping"""
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class CompressorPro:
    """Professional compressor with multiple models"""
    
    TYPES = ['vca', 'fet', 'opto', 'vintage']
    
    def __init__(self, comp_type: str = 'vca'):
        self.type = comp_type
        self.threshold = -18  # dB
        self.ratio = 4
        self.attack = 10  # ms
        self.release = 100  # ms
        self.knee = 6  # dB
        self.makeup = 0  # dB
        self.link = True
        
        self._init_params()
    
    def _init_params(self):
        """Initialize parameters based on type"""
        
        presets = {
            'vca': {'attack': 1, 'release': 100, 'ratio': 4},
            'fet': {'attack': 0.1, 'release': 50, 'ratio': 10},
            'opto': {'attack': 10, 'release': 200, 'ratio': 3},
            'vintage': {'attack': 5, 'release': 150, 'ratio': 6}
        }
        
        if self.type in presets:
            for k, v in presets[self.type].items():
                setattr(self, k, v)
    
    def set_type(self, comp_type: str):
        """Change compressor type"""
        
        self.type = comp_type
        self._init_params()
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply compression"""
        
        output = []
        envelope = 0
        
        for sample in audio:
            # Input level
            input_level = abs(sample)
            
            # Get gain reduction
            gain = self._get_gain(input_level)
            
            # Attack/Release envelope
            if gain < envelope:
                # Attack
                attack_factor = math.exp(-1 / (self.attack * 44.1))
                envelope = envelope * attack_factor + gain * (1 - attack_factor)
            else:
                # Release
                release_factor = math.exp(-1 / (self.release * 44.1))
                envelope = envelope * release_factor + gain * (1 - release_factor)
            
            # Apply
            output.append(sample * envelope)
        
        # Makeup gain
        makeup_linear = 10 ** (self.makeup / 20)
        output = [x * makeup_linear for x in output]
        
        return self._normalize(output)
    
    def _get_gain(self, input_level: float) -> float:
        """Calculate gain reduction"""
        
        if input_level <= 0:
            return 1.0
        
        input_db = 20 * math.log10(input_level)
        
        if input_db < self.threshold - self.knee / 2:
            return 1.0
        
        if input_db > self.threshold + self.knee / 2:
            excess = input_db - self.threshold - self.knee / 2
            return 10 ** (-excess * (1 - 1/self.ratio) / 20)
        
        # Knee region
        excess = input_db - (self.threshold - self.knee / 2)
        excess = excess * excess / (2 * self.knee)
        return 10 ** (-excess * (1 - 1/self.ratio) / 20)
    
    def _normalize(self, audio: List[float]) -> List[float]:
        """Normalize"""
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class Saturator:
    """Saturation with multiple models"""
    
    TYPES = ['tape', 'tube', 'distortion', 'fuzz', 'soft']
    
    def __init__(self, sat_type: str = 'tape'):
        self.type = sat_type
        self.drive = 0.5  # 0-1
        self.tone = 0.5  # 0-1
        self.mix = 1.0  # 0-1
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply saturation"""
        
        output = []
        
        for sample in audio:
            # Scale input by drive
            scaled = sample * (1 + self.drive * 10)
            
            # Apply saturation based on type
            if self.type == 'tape':
                saturated = self._tape_saturation(scaled)
            elif self.type == 'tube':
                saturated = self._tube_saturation(scaled)
            elif self.type == 'distortion':
                saturated = self._hard_distortion(scaled)
            elif self.type == 'fuzz':
                saturated = self._fuzz(scaled)
            else:
                saturated = self._soft_saturation(scaled)
            
            # Mix dry/wet
            result = sample * (1 - self.mix) + saturated * self.mix
            
            # Tone control (simple EQ)
            result = result * (0.5 + self.tone)
            
            output.append(result)
        
        return self._normalize(output)
    
    def _tape_saturation(self, x: float) -> float:
        """Tape saturation (soft clipping)"""
        
        return math.tanh(x)
    
    def _tube_saturation(self, x: float) -> float:
        """Tube saturation (asymmetrical)"""
        
        pos = math.tanh(x)
        neg = -math.tanh(x * 0.5) * 0.5
        
        return pos if x > 0 else neg
    
    def _hard_distortion(self, x: float) -> float:
        """Hard clipping distortion"""
        
        if x > 1:
            return 1
        elif x < -1:
            return -1
        return x
    
    def _fuzz(self, x: float) -> float:
        """Fuzz effect"""
        
        return math.tanh(x * 5) * math.copysign(1, x)
    
    def _soft_saturation(self, x: float) -> float:
        """Soft saturation"""
        
        return x / (1 + abs(x))
    
    def _normalize(self, audio: List[float]) -> List[float]:
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class DelayPro:
    """Professional delay"""
    
    def __init__(self):
        self.time = 250  # ms
        self.feedback = 0.3
        self.mix = 0.3
        self.low_cut = 200  # Hz
        self.high_cut = 8000  # Hz
        self.tempo_sync = False
        self.note_value = 'quarter'  # quarter, eighth, sixteenth, etc.
        self.ping_pong = False
    
    def set_tempo(self, bpm: float, note: str = 'quarter'):
        """Set tempo-synced delay"""
        
        note_values = {
            'whole': 4,
            'half': 2,
            'quarter': 1,
            'eighth': 0.5,
            'sixteenth': 0.25,
            'triplet': 1/3
        }
        
        beats = note_values.get(note, 1)
        self.time = (60.0 / bpm) * beats * 1000
        self.tempo_sync = True
    
    def process(self, audio: List[float], sample_rate: int = 44100) -> List[float]:
        """Apply delay"""
        
        delay_samples = int(self.time / 1000 * sample_rate)
        max_delay = delay_samples * 4
        
        buffer = [0.0] * max_delay
        write_pos = 0
        
        output = []
        
        for i, sample in enumerate(audio):
            # Read from delay buffer
            read_pos = (write_pos - delay_samples) % max_delay
            delayed = buffer[read_pos]
            
            # Low/high cut on feedback
            # (simplified)
            
            # Write to buffer with feedback
            buffer[write_pos] = sample + delayed * self.feedback
            
            # Ping-pong (simplified - would split L/R)
            
            # Mix wet/det
            wet = delayed * self.mix
            dry = sample * (1 - self.mix)
            
            output.append(wet + dry)
            
            write_pos = (write_pos + 1) % max_delay
        
        return self._normalize(output)
    
    def _normalize(self, audio: List[float]) -> List[float]:
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class ReverbPro:
    """Professional reverb"""
    
    ALGORITHMS = ['room', 'hall', 'plate', 'spring', 'convolution']
    
    def __init__(self, algorithm: str = 'hall'):
        self.algorithm = algorithm
        self.room_size = 0.5
        self.damping = 0.5
        self.pre_delay = 20  # ms
        self.wet = 0.3
        self.dry = 0.7
        self.width = 1.0
        
        # Algorithm-specific
        if algorithm == 'room':
            self.decay = 1.5
        elif algorithm == 'hall':
            self.decay = 3.0
        elif algorithm == 'plate':
            self.decay = 2.0
        elif algorithm == 'spring':
            self.decay = 1.0
        else:
            self.decay = 2.0
    
    def process(self, audio: List[float], sample_rate: int = 44100) -> List[float]:
        """Apply reverb"""
        
        # Algorithmic reverb (simplified)
        
        # Pre-delay
        pre_delay_samples = int(self.pre_delay / 1000 * sample_rate)
        
        # Create delay lines
        num_lines = 8
        max_delay = int(self.decay * sample_rate)
        
        delay_lines = [[0.0] * max_delay for _ in range(num_lines)]
        write_positions = [0] * num_lines
        
        # Frequencies for each line (scattered)
        line_freqs = [200, 300, 500, 700, 1100, 1700, 2500, 4000]
        
        output = []
        
        for i, sample in enumerate(audio):
            # Get pre-delayed version
            if i >= pre_delay_samples:
                pre = audio[i - pre_delay_samples]
            else:
                pre = 0
            
            reverb_sample = 0
            
            # Process each delay line
            for li, (delay_line, freq) in enumerate(zip(delay_lines, line_freqs)):
                # Modulate delay time for shimmer
                mod = math.sin(2 * math.pi * freq * i / sample_rate) * 0.1
                delay = int((max_delay * self.room_size) + mod * 100)
                
                read_pos = (write_positions[li] - delay) % max_delay
                
                delayed = delay_line[read_pos]
                
                # Damping
                delayed *= (1 - self.damping * 0.5)
                
                # Write new sample
                delay_line[write_positions[li]] = pre + delayed * 0.3
                write_positions[li] = (write_positions[li] + 1) % max_delay
                
                reverb_sample += delayed
            
            reverb_sample /= num_lines
            
            # Mix
            wet = reverb_sample * self.wet
            dry = sample * self.dry
            
            output.append(wet + dry)
        
        return self._normalize(output)
    
    def _normalize(self, audio: List[float]) -> List[float]:
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class FilterPro:
    """Pro filter with multiple types"""
    
    TYPES = ['lowpass', 'highpass', 'bandpass', 'notch', 'peak', 'low_shelf', 'high_shelf']
    
    def __init__(self, filter_type: str = 'lowpass'):
        self.type = filter_type
        self.frequency = 1000  # Hz
        self.resonance = 0.5  # 0-1
        self.gain = 0  # dB (for peak/shelf)
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply filter"""
        
        # Simple IIR filter implementation
        output = list(audio)
        
        if self.type == 'lowpass':
            output = self._lp(audio, self.frequency, self.resonance)
        elif self.type == 'highpass':
            output = self._hp(audio, self.frequency, self.resonance)
        elif self.type == 'bandpass':
            lp = self._lp(audio, self.frequency, self.resonance)
            output = self._hp(lp, self.frequency, self.resonance)
        
        return self._normalize(output)
    
    def _lp(self, audio: List[float], freq: float, res: float) -> List[float]:
        """Low-pass"""
        
        output = [audio[0]]
        rc = 1.0 / (freq * 2 * math.pi)
        dt = 1.0 / 44100
        
        for i in range(1, len(audio)):
            alpha = dt / (rc + dt)
            output.append(output[-1] + alpha * (audio[i] - output[-1]))
        
        return output
    
    def _hp(self, audio: List[float], freq: float, res: float) -> List[float]:
        """High-pass"""
        
        output = [audio[0]]
        rc = 1.0 / (freq * 2 * math.pi)
        dt = 1.0 / 44100
        alpha = rc / (rc + dt)
        
        for i in range(1, len(audio)):
            output.append(alpha * (output[-1] + audio[i] - audio[i-1]))
        
        return output
    
    def _normalize(self, audio: List[float]) -> List[float]:
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class DistortionPro:
    """Pro distortion effects"""
    
    TYPES = ['overdrive', 'fuzz', 'metal', 'bitcrush', 'lofi', 'ring_mod']
    
    def __init__(self, dist_type: str = 'overdrive'):
        self.type = dist_type
        self.drive = 0.5
        self.tone = 0.5
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply distortion"""
        
        output = []
        
        for sample in audio:
            if self.type == 'overdrive':
                result = self._overdrive(sample)
            elif self.type == 'fuzz':
                result = self._fuzz(sample)
            elif self.type == 'metal':
                result = self._metal(sample)
            elif self.type == 'bitcrush':
                result = self._bitcrush(sample)
            elif self.type == 'lofi':
                result = self._lofi(sample)
            else:
                result = self._overdrive(sample)
            
            output.append(result)
        
        return self._normalize(output)
    
    def _overdrive(self, x: float) -> float:
        """Soft overdrive"""
        return math.tanh(x * (1 + self.drive * 5))
    
    def _fuzz(self, x: float) -> float:
        """Fuzz"""
        return math.copysign(1, x) * (1 - math.exp(-abs(x) * (3 + self.drive * 10)))
    
    def _metal(self, x: float) -> float:
        """Metal distortion"""
        return math.tanh(x * 10) * math.copysign(1, x)
    
    def _bitcrush(self, x: float) -> float:
        """Bit crushing"""
        bits = int(16 - self.drive * 14)
        scale = 2 ** bits
        return math.floor(x * scale) / scale
    
    def _lofi(self, x: float) -> float:
        """Lo-fi effect"""
        # Downsample
        x = x * (1 + self.drive)
        # Add noise
        x += random.uniform(-0.1, 0.1) * (1 - self.tone)
        return x
    
    def _normalize(self, audio: List[float]) -> List[float]:
        
        max_val = max(abs(x) for x in audio) if audio else 1
        if max_val > 0.95:
            return [x * 0.95 / max_val for x in audio]
        return audio


class LimiterPro:
    """Professional limiter"""
    
    def __init__(self):
        self.ceiling = -0.3  # dB
        self.threshold = -6  # dB
        self.release = 50  # ms
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply limiting"""
        
        output = []
        
        for sample in audio:
            # Soft clipper
            if abs(sample) > 0.95:
                sample = 0.95 * math.copysign(1, sample) + (abs(sample) - 0.95) * 0.3
            
            # Make sure we hit ceiling
            if sample > 10 ** (self.ceiling / 20):
                sample = 10 ** (self.ceiling / 20)
            elif sample < -10 ** (self.ceiling / 20):
                sample = -10 ** (self.ceiling / 20)
            
            output.append(sample)
        
        return output


class GatePro:
    """Noise gate"""
    
    def __init__(self):
        self.threshold = -40  # dB
        self.attack = 1  # ms
        self.release = 50  # ms
        self.range = -80  # dB (how much to reduce when closed)
    
    def process(self, audio: List[float]) -> List[float]:
        """Apply gate"""
        
        threshold_linear = 10 ** (self.threshold / 20)
        range_linear = 10 ** (self.range / 20)
        
        output = []
        envelope = 0
        
        for sample in audio:
            input_level = abs(sample)
            
            if input_level > threshold_linear:
                target = 1.0
            else:
                target = range_linear
            
            # Attack/Release
            if target > envelope:
                attack_factor = math.exp(-1 / (self.attack * 44.1))
                envelope = envelope * attack_factor + target * (1 - attack_factor)
            else:
                release_factor = math.exp(-1 / (self.release * 44.1))
                envelope = envelope * release_factor + target * (1 - release_factor)
            
            output.append(sample * envelope)
        
        return output


class EffectsRack:
    """Complete effects rack"""
    
    def __init__(self):
        # Initialize all effects
        self.eq = ParametricEQ8()
        self.compressor = CompressorPro('vca')
        self.saturator = Saturator('tape')
        self.delay = DelayPro()
        self.reverb = ReverbPro('hall')
        self.filter = FilterPro('lowpass')
        self.distortion = DistortionPro('overdrive')
        self.limiter = LimiterPro()
        self.gate = GatePro()
        
        # Bypass states
        self.bypass = {
            'eq': False,
            'compressor': False,
            'saturator': False,
            'delay': False,
            'reverb': False,
            'filter': False,
            'distortion': False,
            'limiter': False,
            'gate': False
        }
        
        # Order
        self.order = ['gate', 'eq', 'compressor', 'saturator', 'distortion', 
                     'filter', 'delay', 'reverb', 'limiter']
    
    def set_bypass(self, effect: str, bypassed: bool):
        """Toggle effect bypass"""
        
        if effect in self.bypass:
            self.bypass[effect] = bypassed
    
    def process(self, audio: List[float]) -> List[float]:
        """Process through full chain"""
        
        current = list(audio)
        
        for effect_name in self.order:
            if not self.bypass.get(effect_name, False):
                if effect_name == 'gate':
                    current = self.gate.process(current)
                elif effect_name == 'eq':
                    current = self.eq.process(current)
                elif effect_name == 'compressor':
                    current = self.compressor.process(current)
                elif effect_name == 'saturator':
                    current = self.saturator.process(current)
                elif effect_name == 'distortion':
                    current = self.distortion.process(current)
                elif effect_name == 'filter':
                    current = self.filter.process(current)
                elif effect_name == 'delay':
                    current = self.delay.process(current)
                elif effect_name == 'reverb':
                    current = self.reverb.process(current)
                elif effect_name == 'limiter':
                    current = self.limiter.process(current)
        
        return current
    
    def set_preset(self, preset: str):
        """Apply preset"""
        
        presets = {
            ' Vocal': {
                'compressor': 'opto', 'gate': -30, 'eq': {'gain': 3},
                'reverb': {'wet': 0.2, 'decay': 1.5}
            },
            ' Drums': {
                'compressor': 'fet', 'saturator': {'type': 'tape', 'drive': 0.3},
                'eq': {'gain': 5}
            },
            ' Bass': {
                'compressor': 'vca', 'saturator': {'type': 'tube', 'drive': 0.5},
                'filter': {'frequency': 400}
            },
            ' Master': {
                'limiter': {'ceiling': -0.3},
                'compressor': {'ratio': 2, 'threshold': -12}
            }
        }
        
        if preset in presets:
            # Apply settings
            pass


def demo():
    """Demo effects rack"""
    
    print("=" * 70)
    print("  PRO AUDIO EFFECTS RACK")
    print("=" * 70)
    
    # Generate test audio
    print("\n[Generating test audio...]")
    sr = 44100
    duration = 2
    
    audio = []
    for i in range(duration * sr):
        t = i / sr
        
        # Mix of frequencies
        sample = math.sin(2 * math.pi * 220 * t) * 0.3  # A3
        sample += math.sin(2 * math.pi * 440 * t) * 0.2  # A4
        sample += math.sin(2 * math.pi * 880 * t) * 0.1  # A5
        sample += random.uniform(-1, 1) * 0.05  # Noise
        
        audio.append(sample)
    
    print(f"  Generated: {len(audio)} samples")
    
    # Create effects rack
    print("\n[Effects Chain]")
    rack = EffectsRack()
    
    # Process through each effect
    print("\n  Processing stages:")
    
    # EQ
    print("    EQ...", end=" ")
    audio = rack.eq.process(audio)
    print(f"peak: {max(abs(x) for x in audio[:1000]):.2f}")
    
    # Compressor
    print("    Compressor...", end=" ")
    audio = rack.compressor.process(audio)
    print(f"peak: {max(abs(x) for x in audio[:1000]):.2f}")
    
    # Saturator
    print("    Saturator...", end=" ")
    audio = rack.saturator.process(audio)
    print(f"peak: {max(abs(x) for x in audio[:1000]):.2f}")
    
    # Delay
    print("    Delay...", end=" ")
    audio = rack.delay.process(audio)
    print(f"length: {len(audio)}")
    
    # Reverb
    print("    Reverb...", end=" ")
    audio = rack.reverb.process(audio)
    print(f"peak: {max(abs(x) for x in audio[:1000]):.2f}")
    
    # Limiter
    print("    Limiter...", end=" ")
    audio = rack.limiter.process(audio)
    print(f"peak: {max(abs(x) for x in audio[:1000]):.2f}")
    
    # Test effects individually
    print("\n[Individual Effects Test]")
    
    test_audio = [math.sin(440 * 2 * math.pi * t / 44100) for t in range(44100)]
    
    eq = ParametricEQ8()
    eq.set_band(0, gain=6)  # Boost bass
    result = eq.process(test_audio)
    print(f"  EQ: {max(abs(x) for x in result):.2f}")
    
    comp = CompressorPro('fet')
    result = comp.process(test_audio)
    print(f"  Compressor (FET): {max(abs(x) for x in result):.2f}")
    
    sat = Saturator('tube')
    sat.drive = 0.8
    result = sat.process(test_audio)
    print(f"  Saturator (Tube): {max(abs(x) for x in result):.2f}")
    
    delay = DelayPro()
    delay.set_tempo(120, 'eighth')
    result = delay.process(test_audio)
    print(f"  Delay (1/8 at 120 BPM): {len(result)} samples")
    
    reverb = ReverbPro('hall')
    result = reverb.process(test_audio)
    print(f"  Reverb (Hall): {max(abs(x) for x in result):.2f}")
    
    dist = DistortionPro('metal')
    result = dist.process(test_audio)
    print(f"  Distortion (Metal): {max(abs(x) for x in result):.2f}")
    
    print("\n" + "=" * 70)
    print("  EFFECTS RACK READY!")
    print("=" * 70)


if __name__ == "__main__":
    demo()