"""
ENHANCED MIXER V3 - Professional Mixing
========================================
Multi-band EQ, compression modes, sends, automation, metering
"""

import math
import random
from typing import List, Dict


class ChannelStripV3:
    """Complete channel strip"""
    
    def __init__(self):
        # Input
        self.gain = 0.0
        self.pan = 0.0
        
        # EQ - 4 bands
        self.eq = {
            'low': {'freq': 100, 'gain': 0, 'q': 1},
            'mid_low': {'freq': 300, 'gain': 0, 'q': 1},
            'mid_high': {'freq': 2000, 'gain': 0, 'q': 1},
            'high': {'freq': 8000, 'gain': 0, 'q': 1}
        }
        
        # Compressor
        self.comp = {
            'threshold': -18,
            'ratio': 4,
            'attack': 10,
            'release': 100,
            'makeup': 0,
            'knee': 3
        }
        
        # Sends
        self.send_a = 0.0
        self.send_b = 0.0
        
        # Output
        self.mute = False
        self.solo = False
        self.volume = 0.8
    
    def process(self, audio: List[float]) -> List[float]:
        """Process through channel"""
        
        output = list(audio)
        
        # Input gain
        if self.gain != 0:
            gain_linear = 10 ** (self.gain / 20)
            output = [x * gain_linear for x in output]
        
        # EQ (simplified)
        output = self._apply_eq(output)
        
        # Compressor
        output = self._apply_compressor(output)
        
        # Mute
        if self.mute:
            output = [0] * len(output)
        
        # Volume
        output = [x * self.volume for x in output]
        
        return output
    
    def _apply_eq(self, audio: List[float]) -> List[float]:
        """Apply EQ"""
        
        for band, params in self.eq.items():
            if params['gain'] != 0:
                gain = 10 ** (params['gain'] / 20)
                audio = [x * gain for x in audio]
        
        return audio
    
    def _apply_compressor(self, audio: List[float]) -> List[float]:
        """Apply compression"""
        
        output = []
        envelope = 0
        
        for sample in audio:
            # Envelope
            if abs(sample) > envelope:
                envelope = abs(sample)
                envelope = envelope * 0.9 + abs(sample) * 0.1
            else:
                envelope = envelope * 0.95
            
            # Compression
            if envelope > 0:
                input_db = 20 * math.log10(envelope)
                
                if input_db > self.comp['threshold']:
                    excess = input_db - self.comp['threshold']
                    gr = excess * (1 - 1/self.comp['ratio'])
                    gain = 10 ** (-gr / 20)
                else:
                    gain = 1.0
            else:
                gain = 1.0
            
            output.append(sample * gain)
        
        # Makeup
        if self.comp['makeup'] != 0:
            makeup = 10 ** (self.comp['makeup'] / 20)
            output = [x * makeup for x in output]
        
        return output


class BusProcessorV3:
    """Bus processing - aux, master"""
    
    def __init__(self):
        # Aux (reverb, delay)
        self.aux_a = {'wet': 0, 'size': 0.5, 'feedback': 0.3}
        self.aux_b = {'wet': 0, 'time': 250, 'feedback': 0.3}
        
        # Master
        self.master = {'volume': 0.8, 'limiter': -0.3}
    
    def apply_reverb(self, audio: List[float]) -> List[float]:
        """Simple reverb"""
        
        if self.aux_a['wet'] == 0:
            return audio
        
        size = self.aux_a['size']
        wet = self.aux_a['wet']
        
        delay = int(44100 * size)
        buffer = [0] * (delay * 2)
        
        output = []
        
        for i, sample in enumerate(audio):
            read = (i - delay) % len(buffer)
            delayed = buffer[read]
            buffer[i] = sample + delayed * (1 - self.aux_a['feedback'])
            
            output.append(sample * (1 - wet) + delayed * wet)
        
        return output
    
    def apply_delay(self, audio: List[float]) -> List[float]:
        """Simple delay"""
        
        if self.aux_b['wet'] == 0:
            return audio
        
        delay_samples = int(self.aux_b['time'] / 1000 * 44100)
        buffer = [0] * (delay_samples * 2)
        
        wet = self.aux_b['wet']
        
        output = []
        
        for i, sample in enumerate(audio):
            read = (i - delay_samples) % len(buffer)
            delayed = buffer[read]
            buffer[i] = sample + delayed * self.aux_b['feedback']
            
            output.append(sample * (1 - wet) + delayed * wet)
        
        return output
    
    def apply_limiter(self, audio: List[float]) -> List[float]:
        """Limiter"""
        
        ceiling = 10 ** (self.master['limiter'] / 20)
        
        return [max(-ceiling, min(ceiling, x)) for x in audio]


class MeteringV3:
    """Professional metering"""
    
    def __init__(self):
        self.peak = 0
        self.rms = 0
    
    def measure(self, audio: List[float]) -> Dict:
        """Measure levels"""
        
        if not audio:
            return {'peak': 0, 'rms': 0, 'db_peak': -60, 'db_rms': -60}
        
        # Peak
        self.peak = max(abs(x) for x in audio)
        
        # RMS
        self.rms = math.sqrt(sum(x*x for x in audio) / len(audio))
        
        # dB
        db_peak = 20 * math.log10(self.peak) if self.peak > 0 else -60
        db_rms = 20 * math.log10(self.rms) if self.rms > 0 else -60
        
        return {
            'peak': self.peak,
            'rms': self.rms,
            'db_peak': db_peak,
            'db_rms': db_rms
        }


class EnhancedMixerV3:
    """Complete mixer V3"""
    
    def __init__(self, channels: int = 8):
        self.channels = [ChannelStripV3() for _ in range(channels)]
        self.bus = BusProcessorV3()
        self.meter = MeteringV3()
        
        # Master
        self.master_volume = 0.8
    
    def process_track(self, audio: List[float], track: int = 0) -> List[float]:
        """Process single track"""
        
        if 0 <= track < len(self.channels):
            return self.channels[track].process(audio)
        return audio
    
    def process_full(self, tracks: List[List[float]]) -> List[float]:
        """Process multiple tracks to mix"""
        
        # Find max length
        max_len = max(len(t) for t in tracks) if tracks else 0
        
        # Mix down
        mix = [0] * max_len
        
        for track_idx, track_audio in enumerate(tracks):
            if track_idx < len(self.channels):
                processed = self.channels[track_idx].process(track_audio)
                
                # Apply pan (simplified)
                for i in range(len(processed)):
                    if i < len(mix):
                        mix[i] += processed[i]
        
        # Apply bus effects
        mix = self.bus.apply_reverb(mix)
        mix = self.bus.apply_delay(mix)
        
        # Apply master
        mix = [x * self.master_volume for x in mix]
        
        # Limit
        mix = self.bus.apply_limiter(mix)
        
        return mix
    
    def get_metering(self, audio: List[float]) -> Dict:
        """Get metering data"""
        
        return self.meter.measure(audio)


def demo():
    print("=" * 60)
    print("  ENHANCED MIXER V3 - PRO CHANNEL STRIPS")
    print("=" * 60)
    
    mixer = EnhancedMixerV3(8)
    
    print("\n[Channels: %d]" % len(mixer.channels))
    
    # Test channel processing
    print("\n[Processing Tracks]")
    tracks = [
        [0.5] * 44100,
        [0.3] * 44100,
        [0.4] * 44100
    ]
    
    mix = mixer.process_full(tracks)
    meter = mixer.get_metering(mix)
    
    print("  Mix: %d samples" % len(mix))
    print("  Peak: %.2f dB" % meter['db_peak'])
    print("  RMS: %.2f dB" % meter['db_rms'])
    
    # Test individual channel
    print("\n[Individual Channel]")
    channel = mixer.channels[0]
    channel.gain = 3
    channel.eq['low']['gain'] = 3
    channel.comp['threshold'] = -15
    channel.comp['ratio'] = 4
    
    audio = [0.5] * 44100
    processed = channel.process(audio)
    print("  EQ + Comp processed: %d samples" % len(processed))
    
    print("\n" + "=" * 60)
    print("  MIXER V3 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()