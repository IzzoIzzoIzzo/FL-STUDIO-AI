"""
INSTRUMENT EMULATOR - Virtual Instrument Collection!
=====================================================
- Pad Synthesizer
- Lead Synthesizer  
- Bass Synthesizer
- Pluck Synthesizer
- Strings Synthesizer

Each instrument with presets and full synthesis!
"""

import math
import random
import struct
import wave
import os
from typing import List, Dict, Optional


class InstrumentSynth:
    """Base instrument synthesizer"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def _generate_adsr(self, duration: float, attack: float = 0.01, 
                       decay: float = 0.1, sustain: float = 0.7, release: float = 0.3) -> List[float]:
        """Generate ADSR envelope"""
        samples = int(self.sample_rate * duration)
        attack_samples = int(self.sample_rate * attack)
        decay_samples = int(self.sample_rate * decay)
        release_samples = int(self.sample_rate * release)
        
        envelope = []
        for i in range(samples):
            if i < attack_samples:
                env = i / attack_samples
            elif i < attack_samples + decay_samples:
                env = 1 - (i - attack_samples) / decay_samples * (1 - sustain)
            elif i < samples - release_samples:
                env = sustain
            else:
                env = sustain * (samples - i) / release_samples
            envelope.append(env)
        return envelope
    
    def _save_wav(self, samples: List[float], filename: str):
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


class PadSynth(InstrumentSynth):
    """Rich, evolving pad synthesizer"""
    
    PRESETS = {
        'ambient': {'attack': 0.5, 'decay': 0.3, 'sustain': 0.8, 'release': 1.0, 'filter_freq': 1500, 'detune': 15, 'voices': 3},
        'cinematic': {'attack': 0.8, 'decay': 0.2, 'sustain': 0.9, 'release': 1.5, 'filter_freq': 2000, 'detune': 20, 'voices': 4},
        'warm': {'attack': 0.3, 'decay': 0.2, 'sustain': 0.7, 'release': 0.8, 'filter_freq': 1000, 'detune': 5, 'voices': 2},
        'shimmer': {'attack': 0.1, 'decay': 0.3, 'sustain': 0.8, 'release': 1.2, 'filter_freq': 3000, 'detune': 30, 'voices': 4},
        'drone': {'attack': 1.0, 'decay': 0.5, 'sustain': 1.0, 'release': 2.0, 'filter_freq': 500, 'detune': 10, 'voices': 3},
    }
    
    def play(self, root_freq: float, duration: float, preset: str = 'ambient') -> List[float]:
        p = self.PRESETS.get(preset, self.PRESETS['ambient'])
        env = self._generate_adsr(duration, p['attack'], p['decay'], p['sustain'], p['release'])
        
        result = []
        for i in range(len(env)):
            t = i / self.sample_rate
            sample = 0
            
            # Multiple detuned voices
            for v in range(p['voices']):
                detune = (v - p['voices']/2) * p['detune'] / 10
                freq = root_freq * (2 ** (detune / 12))
                
                # Layer sine + triangle
                sine = math.sin(2 * math.pi * freq * t)
                triangle = 2 * abs(2 * (t * freq % 1)) - 1
                
                sample += (sine * 0.7 + triangle * 0.3) / p['voices']
            
            result.append(sample * env[i] * 0.5)
        
        return result
    
    def play_chord(self, root: str, chord_type: str, duration: float, preset: str = 'ambient') -> List[float]:
        note_freqs = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.00, 'A': 440.00, 'B': 493.88}
        freq = note_freqs.get(root, 261.63)
        
        intervals = {'major': [0, 4, 7], 'minor': [0, 3, 7], '7th': [0, 4, 7, 10], 
                    'maj7': [0, 4, 7, 11], 'min7': [0, 3, 7, 10], 'sus4': [0, 5, 7]}
        ints = intervals.get(chord_type, [0, 4, 7])
        
        chord_audio = None
        for interval in ints:
            f = freq * (2 ** (interval / 12))
            note_audio = self.play(f, duration, preset)
            
            if chord_audio is None:
                chord_audio = [0] * len(note_audio)
            for i in range(len(note_audio)):
                chord_audio[i] += note_audio[i] / len(ints)
        
        return chord_audio or []


class LeadSynth(InstrumentSynth):
    """Bright, punchy lead synthesizer"""
    
    PRESETS = {
        'super_lead': {'attack': 0.01, 'decay': 0.1, 'sustain': 0.6, 'release': 0.2, 'filter': 3000, 'wave': 'sawtooth'},
        'classic': {'attack': 0.01, 'decay': 0.2, 'sustain': 0.5, 'release': 0.3, 'filter': 2500, 'wave': 'square'},
        'acid': {'attack': 0.01, 'decay': 0.3, 'sustain': 0.4, 'release': 0.1, 'filter': 2000, 'wave': 'sawtooth'},
        'glass': {'attack': 0.005, 'decay': 0.1, 'sustain': 0.8, 'release': 0.1, 'filter': 4000, 'wave': 'sine'},
        'wobble': {'attack': 0.05, 'decay': 0.2, 'sustain': 0.7, 'release': 0.3, 'filter': 1500, 'wave': 'sawtooth'},
    }
    
    def play(self, freq: float, duration: float, preset: str = 'super_lead') -> List[float]:
        p = self.PRESETS.get(preset, self.PRESETS['super_lead'])
        env = self._generate_adsr(duration, p['attack'], p['decay'], p['sustain'], p['release'])
        
        result = []
        for i in range(len(env)):
            t = i / self.sample_rate
            phase = 2 * math.pi * freq * t
            
            if p['wave'] == 'sawtooth':
                sample = 2 * (t * freq % 1) - 1
            elif p['wave'] == 'square':
                sample = 1 if math.sin(phase) > 0 else -1
            elif p['wave'] == 'sine':
                sample = math.sin(phase)
            else:
                sample = math.sin(phase)
            
            result.append(sample * env[i] * 0.6)
        
        return result
    
    def play_arpeggio(self, root: str, scale: str, duration: float, pattern: str = 'up', preset: str = 'super_lead') -> List[float]:
        scales = {'major': [0, 2, 4, 5, 7, 9, 11], 'minor': [0, 2, 3, 5, 7, 8, 10], 
                 'pentatonic': [0, 2, 5, 7, 10], 'dorian': [0, 2, 3, 5, 7, 9, 10]}
        intervals = scales.get(scale, scales['major'])
        
        note_freqs = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.00, 'A': 440.00, 'B': 493.88}
        root_freq = note_freqs.get(root, 261.63)
        
        patterns = {'up': [0, 1, 2, 3, 4, 5, 6], 'down': [6, 5, 4, 3, 2, 1, 0],
                    'updown': [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], 'random': [0, 2, 4, 1, 5, 3]}
        seq = patterns.get(pattern, patterns['up'])
        
        beat_duration = duration / len(seq)
        audio = []
        
        for note_idx in seq:
            f = root_freq * (2 ** (intervals[note_idx % len(intervals)] / 12))
            note_audio = self.play(f, beat_duration * 0.9, preset)
            audio.extend(note_audio)
            
            # Add small gap
            gap = [0] * int(self.sample_rate * beat_duration * 0.1)
            audio.extend(gap)
        
        return audio


class BassSynth(InstrumentSynth):
    """Deep, punchy bass synthesizer"""
    
    PRESETS = {
        'sub': {'attack': 0.01, 'decay': 0.3, 'sustain': 0.4, 'release': 0.1, 'filter': 300, 'wave': 'sine', 'harmonics': [1, 0.5, 0.25]},
        '808': {'attack': 0.01, 'decay': 0.4, 'sustain': 0.3, 'release': 0.2, 'filter': 200, 'wave': 'sawtooth', 'harmonics': [1, 0.3, 0]},
        'acid': {'attack': 0.01, 'decay': 0.2, 'sustain': 0.5, 'release': 0.1, 'filter': 500, 'wave': 'sawtooth', 'harmonics': [1, 0.4, 0.2]},
        'wobble': {'attack': 0.1, 'decay': 0.3, 'sustain': 0.6, 'release': 0.2, 'filter': 400, 'wave': 'sine', 'harmonics': [1, 0.6, 0]},
        'reese': {'attack': 0.02, 'decay': 0.2, 'sustain': 0.5, 'release': 0.1, 'filter': 600, 'wave': 'sawtooth', 'harmonics': [1, 0.5, 0.3]},
    }
    
    def play(self, note: str, octave: int, duration: float, preset: str = 'sub') -> List[float]:
        p = self.PRESETS.get(preset, self.PRESETS['sub'])
        
        note_freqs = {'C': 65.41, 'D': 73.42, 'E': 82.41, 'F': 87.31, 'G': 98.00, 'A': 110.00, 'B': 123.47}
        freq = note_freqs.get(note.upper(), 65.41) * (2 ** octave)
        
        env = self._generate_adsr(duration, p['attack'], p['decay'], p['sustain'], p['release'])
        
        result = []
        for i in range(len(env)):
            t = i / self.sample_rate
            
            sample = 0
            for h, amp in enumerate(p['harmonics']):
                h_freq = freq * (h + 1)
                if p['wave'] == 'sine':
                    h_sample = math.sin(2 * math.pi * h_freq * t)
                else:
                    h_sample = 2 * (t * h_freq % 1) - 1
                sample += h_sample * amp
            
            result.append(sample * env[i] / sum(p['harmonics']) * 0.7)
        
        return result
    
    def play_pattern(self, key: str, style: str, bars: int, bpm: int) -> List[float]:
        patterns = {
            'trap': ['C', 'C', 'F', 'F', 'G', 'G', 'C', 'C'],
            'house': ['C', 'F', 'G', 'F', 'C', 'F', 'G', 'F'],
            'hiphop': ['C', '-', 'G', '-', 'C', '-', 'G', '-'],
            'dubstep': ['C', '-', '-', 'G', '-', '-', 'C', 'G'],
        }
        
        seq = patterns.get(style, patterns['house'])
        beat_dur = 60 / bpm
        
        audio = []
        for bar in range(bars):
            for note in seq:
                if note != '-':
                    note_audio = self.play(note, 0, beat_dur, 'sub')
                    audio.extend(note_audio)
                else:
                    silence = [0] * int(self.sample_rate * beat_dur)
                    audio.extend(silence)
        
        return audio


class PluckSynth(InstrumentSynth):
    """Short, plucky sounds"""
    
    PRESETS = {
        'default': {'attack': 0.001, 'decay': 0.3, 'sustain': 0, 'release': 0.1, 'filter': 3000},
        'harp': {'attack': 0.001, 'decay': 0.5, 'sustain': 0, 'release': 0.2, 'filter': 2000},
        'electric': {'attack': 0.001, 'decay': 0.2, 'sustain': 0, 'release': 0.05, 'filter': 4000},
        'nylon': {'attack': 0.01, 'decay': 0.4, 'sustain': 0, 'release': 0.3, 'filter': 2500},
    }
    
    def play(self, freq: float, duration: float, preset: str = 'default') -> List[float]:
        p = self.PRESETS.get(preset, self.PRESETS['default'])
        env = self._generate_adsr(duration, p['attack'], p['decay'], p['sustain'], p['release'])
        
        result = []
        for i in range(len(env)):
            t = i / self.sample_rate
            # Pluck - mix of harmonics
            sample = math.sin(2 * math.pi * freq * t)
            sample += math.sin(2 * math.pi * freq * 2 * t) * 0.5
            sample += math.sin(2 * math.pi * freq * 3 * t) * 0.25
            sample += (random.random() * 2 - 1) * 0.1  # Slight noise
            
            result.append(sample * env[i] * 0.6)
        
        return result


class StringsSynth(InstrumentSynth):
    """Orchestral strings"""
    
    PRESETS = {
        'section': {'attack': 0.2, 'decay': 0.3, 'sustain': 0.7, 'release': 0.5, 'filter': 2000, 'detune': 5, 'voices': 4},
        'sparse': {'attack': 0.5, 'decay': 0.2, 'sustain': 0.8, 'release': 1.0, 'filter': 1500, 'detune': 2, 'voices': 2},
        'growl': {'attack': 0.1, 'decay': 0.2, 'sustain': 0.6, 'release': 0.3, 'filter': 800, 'detune': 8, 'voices': 3},
    }
    
    def play(self, freq: float, duration: float, preset: str = 'section') -> List[float]:
        p = self.PRESETS.get(preset, self.PRESETS['section'])
        env = self._generate_adsr(duration, p['attack'], p['decay'], p['sustain'], p['release'])
        
        result = []
        for i in range(len(env)):
            t = i / self.sample_rate
            
            sample = 0
            for v in range(p['voices']):
                d = (v - p['voices']/2) * p['detune'] / 100
                f = freq * (1 + d)
                sample += math.sin(2 * math.pi * f * t)
            
            result.append(sample * env[i] / p['voices'] * 0.5)
        
        return result


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  INSTRUMENT EMULATOR TEST")
    print("=" * 60)
    
    # Test Pad
    print("\\n[1] Testing Pad Synth...")
    pad = PadSynth()
    chord_audio = pad.play_chord('C', 'major', 2.0, 'ambient')
    pad._save_wav(chord_audio, 'audio/pad_ambient.wav')
    print("    Saved: audio/pad_ambient.wav")
    
    # Test Lead
    print("\\n[2] Testing Lead Synth...")
    lead = LeadSynth()
    lead_audio = lead.play_arpeggio('C', 'minor', 1.0, 'updown', 'classic')
    lead._save_wav(lead_audio, 'audio/lead_arp.wav')
    print("    Saved: audio/lead_arp.wav")
    
    # Test Bass
    print("\\n3] Testing Bass Synth...")
    bass = BassSynth()
    bass_audio = bass.play_pattern('C', 'trap', 4, 140)
    bass._save_wav(bass_audio, 'audio/bass_trap.wav')
    print("    Saved: audio/bass_trap.wav")
    
    # Test Pluck
    print("\\n[4] Testing Pluck Synth...")
    pluck = PluckSynth()
    pluck_audio = pluck.play(440, 0.5, 'harp')
    pluck._save_wav(pluck_audio, 'audio/pluck.wav')
    print("    Saved: audio/pluck.wav")
    
    # Test Strings
    print("\\n[5] Testing Strings Synth...")
    strings = StringsSynth()
    strings_audio = strings.play(220, 2.0, 'section')
    strings._save_wav(strings_audio, 'audio/strings.wav')
    print("    Saved: audio/strings.wav")
    
    print("\\n" + "=" * 60)
    print("  INSTRUMENT EMULATOR READY!")
    print("=" * 60)