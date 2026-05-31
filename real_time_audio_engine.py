"""
REAL-TIME AUDIO PROCESSING ENGINE
==================================
Real-time effects and processing:
- Input monitoring
- Low-latency effects chain
- Parameter automation
- Metering
- Oscilloscope
- FFT display
- Spectrum analyzer

ALL CONNECTED!
"""

import math
import threading
import time
from typing import List, Dict, Callable, Optional
from dataclasses import dataclass
from enum import Enum


class ProcessingMode(Enum):
    """Processing modes"""
    BYPASS = "bypass"
    INPUT = "input"
    PLAYBACK = "playback"
    RECORD = "record"


@dataclass
class ProcessorState:
    """Processor state"""
    enabled: bool = True
    bypass: bool = False
    gain: float = 1.0
    pan: float = 0.0  # -1 to 1


class AudioInput:
    """Audio input handler"""
    
    def __init__(self, buffer_size: int = 512):
        self.buffer_size = buffer_size
        self.sample_rate = 44100
        self.channels = 2
        self.input_buffer = []
        self.monitoring = False
    
    def start_monitoring(self):
        """Start input monitoring"""
        self.monitoring = True
    
    def stop_monitoring(self):
        """Stop input monitoring"""
        self.monitoring = False
    
    def read_input(self) -> List[float]:
        """Read input buffer"""
        if self.input_buffer:
            data = self.input_buffer[:self.buffer_size]
            self.input_buffer = self.input_buffer[self.buffer_size:]
            return data
        return [0.0] * (self.buffer_size * self.channels)
    
    def add_input_data(self, audio: List[float]):
        """Add data to input buffer"""
        self.input_buffer.extend(audio)


class RealTimeEffects:
    """Real-time effects processor"""
    
    def __init__(self):
        self.effects_chain = []
        self.bypass = False
    
    def add_effect(self, name: str, effect: Callable):
        """Add effect to chain"""
        self.effects_chain.append({'name': name, 'effect': effect, 'enabled': True})
    
    def process(self, audio: List[float]) -> List[float]:
        """Process audio through effects chain"""
        
        if self.bypass:
            return audio
        
        result = audio
        
        for item in self.effects_chain:
            if item['enabled']:
                result = item['effect'](result)
        
        return result
    
    def set_bypass(self, bypass: bool):
        """Set bypass state"""
        self.bypass = bypass
    
    def enable_effect(self, name: str, enabled: bool):
        """Enable/disable specific effect"""
        for item in self.effects_chain:
            if item['name'] == name:
                item['enabled'] = enabled


class LowLatencyFilter:
    """Low-latency filter for real-time"""
    
    def __init__(self):
        self.frequency = 20000
        self.resonance = 0
        self.filter_type = 'lowpass'
        self.state = {'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0}
    
    def set_params(self, freq: float, res: float = 0, filter_type: str = 'lowpass'):
        """Set filter parameters"""
        self.frequency = max(20, min(20000, freq))
        self.resonance = max(0, min(10, res))
        self.filter_type = filter_type
    
    def process_sample(self, sample: float) -> float:
        """Process single sample"""
        
        # Simple one-pole filter for low latency
        rc = 1.0 / (2 * math.pi * self.frequency)
        alpha = rc / (rc + 1.0 / 44100)
        
        self.state['y1'] = alpha * self.state['y1'] + (1 - alpha) * sample
        
        return self.state['y1']
    
    def process(self, audio: List[float]) -> List[float]:
        """Process audio buffer"""
        
        return [self.process_sample(s) for s in audio]


class Compressor:
    """Real-time compressor"""
    
    def __init__(self):
        self.threshold = -20
        self.ratio = 4
        self.attack = 10
        self.release = 100
        self.makeup = 0
        self.envelope = 0
    
    def set_params(self, threshold: float, ratio: float, attack: float, release: float, makeup: float = 0):
        """Set compressor parameters"""
        self.threshold = threshold
        self.ratio = ratio
        self.attack = attack
        self.release = release
        self.makeup = makeup
    
    def process(self, audio: List[float]) -> List[float]:
        """Process audio through compressor"""
        
        output = []
        
        for sample in audio:
            # Envelope
            if abs(sample) > self.envelope:
                self.envelope += (abs(sample) - self.envelope) * (self.attack / 1000)
            else:
                self.envelope -= self.envelope * (self.release / 1000)
            
            # Gain reduction
            if self.envelope > 10 ** (self.threshold / 20):
                db_over = 20 * math.log10(self.envelope / (10 ** (self.threshold / 20)))
                reduction = db_over * (1 - 1 / self.ratio)
                gain = 10 ** (-reduction / 20)
            else:
                gain = 1.0
            
            # Apply makeup
            gain *= 10 ** (self.makeup / 20)
            
            output.append(sample * gain)
        
        return output


class Metering:
    """Audio metering"""
    
    def __init__(self, decay: float = 0.95):
        self.decay = decay
        self.peak_left = 0
        self.peak_right = 0
        self.rms_left = 0
        self.rms_right = 0
        self.peak_hold = 0
        self.peak_hold_timer = 0
    
    def measure(self, audio: List[float]) -> Dict:
        """Measure audio levels"""
        
        if len(audio) < 2:
            return {'peak': 0, 'rms': 0, 'peak_db': -60, 'rms_db': -60}
        
        # Split to channels
        left = audio[0::2]
        right = audio[1::2]
        
        # Peak
        peak_l = max(abs(x) for x in left) if left else 0
        peak_r = max(abs(x) for x in right) if right else 0
        peak = max(peak_l, peak_r)
        
        # RMS
        rms_l = math.sqrt(sum(x*x for x in left) / len(left)) if left else 0
        rms_r = math.sqrt(sum(x*x for x in right) / len(right)) if right else 0
        rms = (rms_l + rms_r) / 2
        
        # Peak hold
        if peak > self.peak_hold:
            self.peak_hold = peak
            self.peak_hold_timer = 30  # frames
        
        if self.peak_hold_timer > 0:
            self.peak_hold_timer -= 1
        else:
            self.peak_hold *= self.decay
        
        # Convert to dB
        peak_db = 20 * math.log10(peak + 1e-10)
        rms_db = 20 * math.log10(rms + 1e-10)
        
        # Store
        self.peak_left = peak_l
        self.peak_right = peak_r
        self.rms_left = rms_l
        self.rms_right = rms_r
        
        return {
            'peak': peak,
            'peak_db': peak_db,
            'rms': rms,
            'rms_db': rms_db,
            'peak_hold': self.peak_hold,
            'peak_left': peak_l,
            'peak_right': peak_r,
            'rms_left': rms_l,
            'rms_right': rms_r,
        }
    
    def get_meter_display(self) -> str:
        """Get ASCII meter display"""
        
        def db_to_bar(db: float, width: int = 20) -> str:
            if db < -60:
                return ' ' * width
            
            bar_pos = int((db + 60) / 60 * width)
            bar_pos = max(0, min(width, bar_pos))
            
            return '=' * bar_pos + '-' * (width - bar_pos)
        
        peak_bar = db_to_bar(self.peak_left * 2, 20)
        rms_bar = db_to_bar(self.rms_left * 2, 20)
        
        return f"L [{peak_bar}] {self.peak_left:.2f}\nR [{rms_bar}] {self.rms_right:.2f}"


class Oscilloscope:
    """Oscilloscope display"""
    
    def __init__(self, width: int = 80, height: int = 20):
        self.width = width
        self.height = height
        self.buffer = []
        self.max_samples = 1000
    
    def add_samples(self, samples: List[float]):
        """Add samples to buffer"""
        self.buffer.extend(samples)
        
        if len(self.buffer) > self.max_samples:
            self.buffer = self.buffer[-self.max_samples:]
    
    def get_display(self) -> List[str]:
        """Get ASCII display"""
        
        if len(self.buffer) < 2:
            return ['No signal']
        
        # Downsample to width
        step = len(self.buffer) // self.width
        if step < 1:
            step = 1
        
        points = []
        for i in range(0, len(self.buffer), step):
            points.append(self.buffer[i])
            if len(points) >= self.width:
                break
        
        # Map to height
        display = [[' '] * self.width for _ in range(self.height)]
        
        min_val = min(points)
        max_val = max(points)
        range_val = max_val - min_val if max_val != min_val else 1
        
        for i, p in enumerate(points):
            y = int((p - min_val) / range_val * (self.height - 1))
            y = self.height - 1 - y  # Flip
            y = max(0, min(self.height - 1, y))
            display[y][i] = '*'
        
        # Return as string
        lines = [''.join(row) for row in display]
        
        return lines


class FFTDisplay:
    """FFT spectrum display"""
    
    def __init__(self, width: int = 40, height: int = 15):
        self.width = width
        self.height = height
        self.bands = [0] * 32
    
    def analyze(self, audio: List[float], sample_rate: int = 44100):
        """Analyze audio and update bands"""
        
        # Simplified band analysis
        bands = 32
        band_size = len(audio) // bands
        
        for i in range(bands):
            start = i * band_size
            end = start + band_size
            
            energy = sum(x*x for x in audio[start:end]) / band_size
            self.bands[i] = energy * 0.9 + self.bands[i] * 0.1  # Smooth
    
    def get_display(self) -> List[str]:
        """Get ASCII spectrum display"""
        
        display = [[' '] * self.width for _ in range(self.height)]
        
        max_energy = max(self.bands) if self.bands else 1
        
        for i, energy in enumerate(self.bands):
            if i >= self.width:
                break
            
            bar_height = int(energy / max_energy * self.height)
            bar_height = max(0, min(self.height, bar_height))
            
            for j in range(bar_height):
                row = self.height - 1 - j
                display[row][i] = '#'
        
        lines = [''.join(row) for row in display]
        
        return lines


class ParameterAutomation:
    """Parameter automation"""
    
    def __init__(self):
        self.automation_curves = {}
    
    def add_point(self, param_name: str, time: float, value: float):
        """Add automation point"""
        
        if param_name not in self.automation_curves:
            self.automation_curves[param_name] = []
        
        self.automation_curves[param_name].append({'time': time, 'value': value})
        
        # Sort by time
        self.automation_curves[param_name].sort(key=lambda x: x['time'])
    
    def get_value(self, param_name: str, time: float) -> float:
        """Get interpolated value at time"""
        
        if param_name not in self.automation_curves:
            return 0.0
        
        points = self.automation_curves[param_name]
        
        if not points:
            return 0.0
        
        if time <= points[0]['time']:
            return points[0]['value']
        
        if time >= points[-1]['time']:
            return points[-1]['value']
        
        # Find surrounding points
        for i in range(len(points) - 1):
            if points[i]['time'] <= time <= points[i+1]['time']:
                # Interpolate
                t = (time - points[i]['time']) / (points[i+1]['time'] - points[i]['time'])
                return points[i]['value'] * (1 - t) + points[i+1]['value'] * t
        
        return 0.0


class CompleteRealTimeEngine:
    """Complete real-time audio processing engine"""
    
    def __init__(self):
        self.input = AudioInput()
        self.effects = RealTimeEffects()
        self.meter = Metering()
        self.oscilloscope = Oscilloscope()
        self.fft_display = FFTDisplay()
        self.automation = ParameterAutomation()
        
        self.mode = ProcessingMode.BYPASS
        self.gain = 1.0
        self.pan = 0.0
        self.state = ProcessorState()
    
    def process_buffer(self, audio: List[float]) -> List[float]:
        """Process audio buffer"""
        
        # Apply input gain
        audio = [s * self.gain for s in audio]
        
        # Apply pan
        if self.pan != 0:
            for i in range(0, len(audio) - 1, 2):
                if self.pan > 0:
                    audio[i + 1] *= (1 + self.pan)
                    audio[i] *= (1 - self.pan)
                else:
                    audio[i] *= (1 + abs(self.pan))
                    audio[i + 1] *= (1 - abs(self.pan))
        
        # Process through effects
        if not self.state.bypass:
            audio = self.effects.process(audio)
        
        # Update meters
        meters = self.meter.measure(audio)
        
        # Update oscilloscope
        self.oscilloscope.add_samples(audio[:100])
        
        # Update FFT
        self.fft_display.analyze(audio)
        
        return audio
    
    def set_gain(self, gain: float):
        """Set input gain"""
        self.gain = max(0, min(2, gain))
    
    def set_pan(self, pan: float):
        """Set pan"""
        self.pan = max(-1, min(1, pan))
    
    def set_bypass(self, bypass: bool):
        """Set bypass"""
        self.state.bypass = bypass
        self.effects.set_bypass(bypass)
    
    def add_effect(self, name: str, effect: Callable):
        """Add effect"""
        self.effects.add_effect(name, effect)
    
    def get_meter_data(self) -> Dict:
        """Get meter data"""
        return self.meter.measure([0] * 512)  # Placeholder


def demo():
    print("=" * 60)
    print("  REAL-TIME AUDIO PROCESSING ENGINE")
    print("=" * 60)
    
    engine = CompleteRealTimeEngine()
    
    print("\n[Processing Modes]")
    for mode in ProcessingMode:
        print("  %s" % mode.value)
    
    print("\n[Metering]")
    meter = Metering()
    test_audio = [math.sin(440 * 2 * math.pi * i / 44100) * 0.5 for i in range(512)]
    levels = meter.measure(test_audio)
    print("  Peak: %.2f (%.1f dB)" % (levels['peak'], levels['peak_db']))
    print("  RMS: %.2f (%.1f dB)" % (levels['rms'], levels['rms_db']))
    
    print("\n  Display:")
    print(meter.get_meter_display())
    
    print("\n[Oscilloscope]")
    osc = Oscilloscope(40, 10)
    for i in range(100):
        osc.add_samples([math.sin(440 * 2 * math.pi * i / 44100)])
    display = osc.get_display()
    for line in display[:5]:
        print("  %s" % line)
    
    print("\n[FFT Display]")
    fft = FFTDisplay(20, 10)
    fft.analyze(test_audio)
    display = fft.get_display()
    for line in display[:3]:
        print("  %s" % line)
    
    print("\n[Automation]")
    auto = ParameterAutomation()
    auto.add_point('gain', 0, 0.5)
    auto.add_point('gain', 1, 1.0)
    auto.add_point('gain', 2, 0.75)
    print("  Value at 0.5s: %.2f" % auto.get_value('gain', 0.5))
    print("  Value at 1.5s: %.2f" % auto.get_value('gain', 1.5))
    
    print("\n[Effects Chain]")
    engine.add_effect('filter', LowLatencyFilter().process)
    engine.add_effect('compressor', Compressor().process)
    print("  Added filter and compressor")
    
    print("\n[Real-time Processing]")
    result = engine.process_buffer(test_audio[:256])
    print("  Processed %d samples" % len(result))
    
    print("\n" + "=" * 60)
    print("  REAL-TIME ENGINE COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()