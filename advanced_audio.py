"""
Advanced Audio Engine for FL Studio AI
Real-time audio synthesis with professional-grade oscillators, filters, and effects
"""

import math
import random
import struct
import wave
import os
from typing import List, Optional, Tuple

class AdvancedOscillator:
    """Professional-grade oscillator with multiple waveforms"""
    
    WAVEFORMS = ['sine', 'square', 'sawtooth', 'triangle', 'pulse', 'noise']
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.phase = 0.0
        
    def reset(self):
        self.phase = 0.0
        
    def sine(self, frequency: float, amplitude: float = 1.0) -> float:
        """Pure sine wave"""
        return amplitude * math.sin(2 * math.pi * frequency * self.phase)
    
    def square(self, frequency: float, amplitude: float = 1.0, duty: float = 0.5) -> float:
        """Square wave with adjustable duty cycle"""
        if self.phase % (1.0 / frequency) < duty / frequency:
            return amplitude
        return -amplitude
    
    def sawtooth(self, frequency: float, amplitude: float = 1.0) -> float:
        """Sawtooth wave"""
        return amplitude * (2 * (self.phase * frequency % 1) - 1)
    
    def triangle(self, frequency: float, amplitude: float = 1.0) -> float:
        """Triangle wave"""
        return amplitude * (2 * abs(2 * (self.phase * frequency % 1) - 1) - 1)
    
    def pulse(self, frequency: float, amplitude: float = 1.0, width: float = 0.5) -> float:
        """Pulse wave with PWM"""
        pw = width
        t = self.phase * frequency
        if (t % 1) < pw:
            return amplitude
        return -amplitude * 0.3
    
    def noise(self, amplitude: float = 1.0) -> float:
        """White noise"""
        return amplitude * (random.random() * 2 - 1)
    
    def generate(self, waveform: str, frequency: float, duration: float, 
                 amplitude: float = 1.0, **kwargs) -> List[float]:
        """Generate waveform over duration"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for _ in range(num_samples):
            if waveform == 'sine':
                samples.append(self.sine(frequency, amplitude))
            elif waveform == 'square':
                samples.append(self.square(frequency, amplitude, kwargs.get('duty', 0.5)))
            elif waveform == 'sawtooth':
                samples.append(self.sawtooth(frequency, amplitude))
            elif waveform == 'triangle':
                samples.append(self.triangle(frequency, amplitude))
            elif waveform == 'pulse':
                samples.append(self.pulse(frequency, amplitude, kwargs.get('width', 0.5)))
            elif waveform == 'noise':
                samples.append(self.noise(amplitude))
            else:
                samples.append(self.sine(frequency, amplitude))
            
            self.phase += 1.0 / self.sample_rate
            
        self.reset()
        return samples


class AdvancedFilter:
    """Professional-grade filter with multiple types"""
    
    FILTER_TYPES = ['lowpass', 'highpass', 'bandpass', 'notch', 'peak', 'lowshelf', 'highshelf']
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.low = 0.0
        self.mid = 0.0
        self.high = 0.0
        self.prev_input = 0.0
        self.band = 0.0
    
    def lowpass(self, samples: List[float], frequency: float, resonance: float = 0.5) -> List[float]:
        """Low-pass filter"""
        f = 2 * math.sin(math.pi * frequency / self.sample_rate)
        q = 2 * resonance
        
        result = []
        for sample in samples:
            self.low += f * (sample - self.low + q * (self.low - self.band))
            self.band += f * (self.low - self.band)
            result.append(self.low)
        
        self.low = self.mid = self.high = 0.0
        return result
    
    def highpass(self, samples: List[float], frequency: float, resonance: float = 0.5) -> List[float]:
        """High-pass filter"""
        f = 2 * math.sin(math.pi * frequency / self.sample_rate)
        q = 2 * resonance
        
        result = []
        for sample in samples:
            self.high += f * (sample - self.high)
            result.append(sample - self.high)
        
        return result
    
    def bandpass(self, samples: List[float], frequency: float, bandwidth: float = 1.0) -> List[float]:
        """Band-pass filter"""
        f = 2 * math.sin(math.pi * frequency / self.sample_rate)
        
        result = []
        for sample in samples:
            self.band += f * (sample - self.band)
            self.mid += f * (self.band - self.mid)
            result.append(self.mid)
        
        return result
    
    def apply(self, samples: List[float], filter_type: str, frequency: float, **kwargs) -> List[float]:
        """Apply filter based on type"""
        if filter_type == 'lowpass':
            return self.lowpass(samples, frequency, kwargs.get('resonance', 0.5))
        elif filter_type == 'highpass':
            return self.highpass(samples, frequency, kwargs.get('resonance', 0.5))
        elif filter_type == 'bandpass':
            return self.bandpass(samples, frequency, kwargs.get('bandwidth', 1.0))
        else:
            return samples


class AdvancedEffects:
    """Professional audio effects processor"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.delay_buffer = []
        self.compressor_envelope = 0.0
        
    def reverb(self, samples: List[float], room_size: float = 0.5, damping: float = 0.5, 
               wet: float = 0.3) -> List[float]:
        """Convolution reverb with multiple delays"""
        # Create simple reverb with comb filters
        delays = [0.029, 0.037, 0.041, 0.043]  # Common reverb delays
        max_delay = max(delays)
        
        # Initialize delay buffers
        buffers = [[0.0] * int(self.sample_rate * max_delay) for _ in range(len(delays))]
        buffer_positions = [0] * len(delays)
        
        result = []
        
        for i, sample in enumerate(samples):
            output = sample
            dry = sample
            
            for j, delay_time in enumerate(delays):
                delay_samples = int(self.sample_rate * delay_time)
                idx = (buffer_positions[j] - delay_samples) % len(buffers[j])
                buffered = buffers[j][idx]
                
                # Damping
                buffered *= (1 - damping * 0.01)
                
                # Feedback
                buffers[j][buffer_positions[j]] = sample + buffered * room_size * 0.3
                buffer_positions[j] = (buffer_positions[j] + 1) % len(buffers[j])
                
                output += buffered * wet / len(delays)
            
            result.append(output * 0.7 + dry * 0.3)
        
        return result
    
    def delay(self, samples: List[float], time: float = 0.5, feedback: float = 0.4, 
              wet: float = 0.3) -> List[float]:
        """Tape delay effect"""
        delay_samples = int(self.sample_rate * time)
        
        if len(self.delay_buffer) < delay_samples:
            self.delay_buffer = [0.0] * delay_samples
        
        result = []
        
        for sample in samples:
            delayed = self.delay_buffer[0]
            self.delay_buffer.append(sample + delayed * feedback)
            self.delay_buffer.pop(0)
            result.append(sample + delayed * wet)
        
        return result
    
    def chorus(self, samples: List[float], rate: float = 1.5, depth: float = 0.003,
               wet: float = 0.5) -> List[float]:
        """Chorus effect"""
        result = []
        lfo_phase = 0.0
        lfo_rate = 2 * math.pi * rate / self.sample_rate
        
        for i, sample in enumerate(samples):
            lfo = math.sin(lfo_phase)
            delay_offset = int(depth * self.sample_rate * (1 + lfo))
            
            idx = max(0, i - delay_offset)
            if idx < i:
                delayed = samples[idx]
            else:
                delayed = 0
            
            result.append(sample + delayed * wet)
            lfo_phase += lfo_rate
            if lfo_phase > 2 * math.pi:
                lfo_phase -= 2 * math.pi
        
        return result
    
    def compressor(self, samples: List[float], threshold: float = 0.5, ratio: float = 4.0,
                    attack: float = 0.01, release: float = 0.1) -> List[float]:
        """Dynamic range compressor"""
        result = []
        
        for sample in samples:
            # Envelope
            if abs(sample) > self.compressor_envelope:
                self.compressor_envelope += (abs(sample) - self.compressor_envelope) * attack
            else:
                self.compressor_envelope += (abs(sample) - self.compressor_envelope) * release
            
            # Gain reduction
            if self.compressor_envelope > threshold:
                gain = threshold + (self.compressor_envelope - threshold) / ratio
                if self.compressor_envelope > 0:
                    gain = gain / self.compressor_envelope
            else:
                gain = 1.0
            
            result.append(sample * gain)
        
        return result
    
    def EQ(self, samples: List[float], low: float = 0, mid: float = 0, high: float = 0) -> List[float]:
        """3-band parametric EQ"""
        low_f = 0.95
        mid_f = 0.9
        high_f = 0.85
        
        low_val = mid_val = high_val = 0.0
        result = []
        
        low_boost = 1 + low / 10
        mid_boost = 1 + mid / 10
        high_boost = 1 + high / 10
        
        for sample in samples:
            low_val = low_val * low_f + sample * (1 - low_f)
            mid_val = mid_val * mid_f + sample * (1 - mid_f)
            high_val = sample * high_f + high_val * (1 - high_f)
            
            result.append(low_val * low_boost * 0.3 + mid_val * mid_boost * 0.4 + high_val * high_boost * 0.3)
        
        return result
    
    def distortion(self, samples: List[float], drive: float = 0.5, tone: float = 0.5) -> List[float]:
        """Soft clip distortion"""
        result = []
        gain = 1 + drive * 10
        
        for sample in samples:
            # Soft clipping
            x = sample * gain
            if x > 1:
                result.append(1 - 1 / (x + 1))
            elif x < -1:
                result.append(-1 + 1 / (-x + 1))
            else:
                result.append(x)
            
            # Tone control (simple low-pass)
            result[-1] = result[-1] * (1 - tone * 0.3) + sample * tone * 0.3
        
        return result


class Synthesizer:
    """Full synthesizer with oscillators, filters, and effects"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.osc = AdvancedOscillator(sample_rate)
        self.filter = AdvancedFilter(sample_rate)
        self.effects = AdvancedEffects(sample_rate)
    
    def play_note(self, frequency: float, duration: float, waveform: str = 'sawtooth',
                   attack: float = 0.01, decay: float = 0.1, sustain: float = 0.7, release: float = 0.3,
                   filter_freq: float = 5000, filter_type: str = 'lowpass',
                   effects: dict = None) -> List[float]:
        """Play a note with full synthesis chain"""
        
        # Generate oscillator
        samples = self.osc.generate(waveform, frequency, duration, 0.5)
        
        # Apply ADSR envelope
        num_samples = len(samples)
        attack_samples = int(self.sample_rate * attack)
        decay_samples = int(self.sample_rate * decay)
        release_samples = int(self.sample_rate * release)
        
        for i in range(num_samples):
            if i < attack_samples:
                env = i / attack_samples
            elif i < attack_samples + decay_samples:
                env = 1 - (i - attack_samples) / decay_samples * (1 - sustain)
            elif i < num_samples - release_samples:
                env = sustain
            else:
                env = sustain * (num_samples - i) / release_samples
            
            samples[i] *= env
        
        # Apply filter
        if filter_freq < self.sample_rate / 2:
            samples = self.filter.apply(samples, filter_type, filter_freq)
        
        # Apply effects
        if effects:
            if effects.get('reverb'):
                r = effects['reverb']
                samples = self.effects.reverb(samples, r.get('size', 0.5), r.get('damping', 0.5), r.get('wet', 0.3))
            
            if effects.get('delay'):
                d = effects['delay']
                samples = self.effects.delay(samples, d.get('time', 0.5), d.get('feedback', 0.4), d.get('wet', 0.3))
            
            if effects.get('chorus'):
                c = effects['chorus']
                samples = self.effects.chorus(samples, c.get('rate', 1.5), c.get('depth', 0.003), c.get('wet', 0.5))
            
            if effects.get('distortion'):
                ds = effects['distortion']
                samples = self.effects.distortion(samples, ds.get('drive', 0.5), ds.get('tone', 0.5))
            
            if effects.get('compress'):
                c = effects['compress']
                samples = self.effects.compressor(samples, c.get('threshold', 0.5), c.get('ratio', 4))
            
            if effects.get('eq'):
                eq = effects['eq']
                samples = self.effects.EQ(samples, eq.get('low', 0), eq.get('mid', 0), eq.get('high', 0))
        
        return samples
    
    def play_chord(self, root_freq: float, chord_type: str, duration: float, **kwargs) -> List[float]:
        """Play a chord"""
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            '7th': [0, 4, 7, 10],
            'maj7': [0, 4, 7, 11],
            'min7': [0, 3, 7, 10],
            'sus4': [0, 5, 7],
            'dim': [0, 3, 6],
            'aug': [0, 4, 8],
            'add9': [0, 4, 7, 14],
        }
        
        intervals = chord_intervals.get(chord_type, [0, 4, 7])
        
        # Generate each note and mix
        chord_samples = None
        for interval in intervals:
            freq = root_freq * (2 ** (interval / 12))
            note_samples = self.play_note(freq, duration, **kwargs)
            
            if chord_samples is None:
                chord_samples = note_samples
            else:
                # Mix notes
                for i in range(len(chord_samples)):
                    chord_samples[i] = (chord_samples[i] + note_samples[i]) / 2
        
        return chord_samples or []


class AudioEngine:
    """Main audio engine for FL Studio AI"""
    
    def __init__(self):
        self.synth = Synthesizer()
        self.sample_rate = 44100
    
    def save_wav(self, samples: List[float], filename: str):
        """Save audio to WAV file"""
        os.makedirs(os.path.dirname(filename) if '/' in filename else '.', exist_ok=True)
        
        # Normalize
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            samples = [s * 0.9 / max_val for s in samples]
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            
            for sample in samples:
                packed = struct.pack('<hh', int(sample * 32767), int(sample * 32767))
                wav.writeframes(packed)
    
    def create_pad(self, root: str, scale: str, duration: float, style: str = 'ambient') -> List[float]:
        """Create an ambient pad"""
        scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'dorian': [0, 2, 3, 5, 7, 9, 10],
            'pentatonic': [0, 2, 5, 7, 10],
        }
        
        note_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        root_num = note_values.get(root.upper(), 0)
        intervals = scales.get(scale, [0, 2, 4, 5, 7, 9, 11])
        
        # Create pad with multiple octaves
        pad_samples = None
        for octave in [0, 1, 2]:
            for interval in intervals:
                freq = 261.63 * (2 ** ((root_num + interval + octave * 12 - 60) / 12))
                note_samples = self.synth.play_note(
                    freq, duration, 'sine',
                    attack=0.5, decay=0.3, sustain=0.8, release=1.0,
                    filter_freq=2000,
                    effects={'reverb': {'size': 0.8, 'wet': 0.5}, 'chorus': {'rate': 0.5, 'wet': 0.3}}
                )
                
                if pad_samples is None:
                    pad_samples = note_samples
                else:
                    for i in range(len(pad_samples)):
                        pad_samples[i] += note_samples[i] * 0.5
        
        return pad_samples or []
    
    def create_bass(self, root: str, style: str = 'warm') -> List[float]:
        """Create a bass synth"""
        note_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        freq = 65.41 * (2 ** (note_values.get(root.upper(), 0) / 12))
        
        effect_settings = {
            'warm': {'distortion': {'drive': 0.2, 'tone': 0.6}, 'compressor': {'threshold': 0.5, 'ratio': 3}},
            'acid': {'distortion': {'drive': 0.7, 'tone': 0.3}, 'delay': {'time': 0.25, 'wet': 0.3}},
            '808': {'distortion': {'drive': 0.9, 'tone': 0.8}, 'compressor': {'threshold': 0.7, 'ratio': 8}},
            'reese': {'distortion': {'drive': 0.5, 'tone': 0.4}, 'reverb': {'size': 0.3, 'wet': 0.2}},
        }
        
        effects = effect_settings.get(style, effect_settings['warm'])
        
        return self.synth.play_note(freq, 2.0, 'sawtooth', attack=0.01, decay=0.2, sustain=0.8, release=0.3,
                                   filter_freq=800, filter_type='lowpass', effects=effects) or []
    
    def create_lead(self, note: str, octave: int = 4, duration: float = 1.0) -> List[float]:
        """Create a lead synth"""
        note_freqs = {
            'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.00, 'A': 440.00, 'B': 493.88
        }
        base_freq = note_freqs.get(note.upper(), 440.0)
        freq = base_freq * (2 ** (octave - 4))
        
        return self.synth.play_note(freq, duration, 'square', attack=0.01, decay=0.1, sustain=0.6, release=0.2,
                                    filter_freq=3000, filter_type='lowpass',
                                    effects={'reverb': {'size': 0.4, 'wet': 0.3}, 'chorus': {'rate': 2, 'wet': 0.2}}) or []


if __name__ == "__main__":
    print("=== Advanced Audio Engine Test ===")
    
    engine = AudioEngine()
    
    # Test pad
    print("Creating ambient pad...")
    pad = engine.create_pad('C', 'minor', 3.0)
    engine.save_wav(pad, "audio/advanced_pad.wav")
    print("  Saved: audio/advanced_pad.wav")
    
    # Test bass
    print("Creating warm bass...")
    bass = engine.create_bass('C', 'warm')
    engine.save_wav(bass, "audio/advanced_bass.wav")
    print("  Saved: audio/advanced_bass.wav")
    
    # Test lead
    print("Creating lead synth...")
    lead = engine.create_lead('C', 4, 1.0)
    engine.save_wav(lead, "audio/advanced_lead.wav")
    print("  Saved: audio/advanced_lead.wav")
    
    # Test chord
    print("Creating chord...")
    chord = engine.synth.play_chord(261.63, 'major', 2.0, waveform='sine', attack=0.1, decay=0.2, sustain=0.7, release=0.5,
                                     filter_freq=2500, effects={'reverb': {'size': 0.6, 'wet': 0.4}})
    engine.save_wav(chord, "audio/advanced_chord.wav")
    print("  Saved: audio/advanced_chord.wav")
    
    print("=== All tests complete! ===")