"""
Audio Track Generator - Creates complete audio tracks using advanced synthesis
"""

import sys
import os
import math
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from advanced_audio import AudioEngine, Synthesizer

class TrackGenerator:
    """Generate complete audio tracks"""
    
    def __init__(self):
        self.engine = AudioEngine()
        self.synth = Synthesizer()
        self.sample_rate = 44100
    
    def generate_drum_pattern(self, style: str, bpm: int, bars: int) -> list:
        """Generate drum pattern as audio samples"""
        beat_duration = 60 / bpm
        samples_per_beat = int(self.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        drum_samples = [0.0] * total_samples
        
        patterns = {
            'trap': {'kick': [1,0,0,1], 'snare': [0,0,1,0], 'hihat': [1,1,1,1,1,1,1,1]},
            'house': {'kick': [1,0,1,0], 'snare': [0,0,1,0], 'hihat': [1,0,1,0,1,0,1,0]},
            'hiphop': {'kick': [1,0,0,1], 'snare': [0,0,1,0], 'hihat': [1,1,0,1,1,1,0,1]},
            'dubstep': {'kick': [1,0,0,0,1,0,0,0], 'snare': [0,0,1,0,0,0,1,0], 'hihat': [1,1,1,1,1,1,1,1]},
            'dnb': {'kick': [1,0,0,1], 'snare': [0,0,1,1], 'hihat': [1,1,1,1,1,1,1,1]},
            'lofi': {'kick': [1,0,0,0], 'snare': [0,0,1,0], 'hihat': [1,0,1,0,1,0,1,0]},
        }
        pattern = patterns.get(style, patterns['trap'])
        
        for bar in range(bars):
            for beat in range(4):
                beat_start = (bar * 4 + beat) * samples_per_beat
                
                if pattern['kick'][beat]:
                    kick_samples = self.generate_kick()
                    for i, s in enumerate(kick_samples):
                        if beat_start + i < len(drum_samples):
                            drum_samples[beat_start + i] += s * 0.8
                
                if pattern['snare'][beat]:
                    snare_samples = self.generate_snare()
                    for i, s in enumerate(snare_samples):
                        if beat_start + i < len(drum_samples):
                            drum_samples[beat_start + i] += s * 0.6
                
                for sub in range(4):
                    sub_idx = (beat * 4 + sub) % 8
                    if pattern['hihat'][sub_idx]:
                        hihat_start = beat_start + sub * samples_per_beat // 4
                        hihat_samples = self.generate_hihat()
                        for i, s in enumerate(hihat_samples):
                            if hihat_start + i < len(drum_samples):
                                drum_samples[hihat_start + i] += s * 0.3
        
        return self.normalize(drum_samples)
    
    def generate_kick(self) -> list:
        """Generate kick drum sound"""
        duration = 0.3
        samples = int(self.sample_rate * duration)
        result = []
        
        for i in range(samples):
            t = i / self.sample_rate
            freq = 150 * (1 - t / duration * 0.7) + 40
            env = 1 - t / duration
            env = env ** 2
            sample = math.sin(2 * math.pi * freq * t) * env
            result.append(sample)
        
        return result
    
    def generate_snare(self) -> list:
        """Generate snare drum sound"""
        duration = 0.2
        samples = int(self.sample_rate * duration)
        result = []
        
        import math
        
        for i in range(samples):
            t = i / self.sample_rate
            env = 1 - t / duration
            env = env ** 1.5
            
            tone = math.sin(2 * math.pi * 200 * t) * 0.3
            noise = (random.random() * 2 - 1) * 0.7
            
            result.append((tone + noise) * env)
        
        return result
    
    def generate_hihat(self) -> list:
        """Generate hi-hat sound"""
        duration = 0.05
        samples = int(self.sample_rate * duration)
        result = []
        
        for i in range(samples):
            t = i / self.sample_rate
            env = 1 - t / duration
            env = env ** 2
            noise = random.random() * 2 - 1
            result.append(noise * env * 0.5)
        
        return result
    
    def generate_bass(self, style: str, key: str, bars: int, bpm: int) -> list:
        """Generate bass line"""
        beat_duration = 60 / bpm
        samples_per_beat = int(self.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        bass_samples = [0.0] * total_samples
        
        note_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        root_freq = 55 * (2 ** (note_values.get(key.upper(), 0) / 12))
        
        pattern = {
            'trap': [1,0,0,1],
            'house': [1,0,1,0],
            'hiphop': [1,0,0,1],
            'dubstep': [1,0,0,0,1,0,0,0],
            'dnb': [1,0,0,1],
            'lofi': [1,0,0,0],
        }.get(style, [1,0,0,1])
        
        for bar in range(bars):
            for beat in range(4):
                if pattern[beat % len(pattern)]:
                    beat_start = (bar * 4 + beat) * samples_per_beat
                    note_samples = self.synth.play_note(
                        root_freq * (1 if beat % 2 == 0 else 1.5),
                        beat_duration * 0.9,
                        'sawtooth',
                        attack=0.01, decay=0.1, sustain=0.6, release=0.2,
                        filter_freq=800,
                        effects={'distortion': {'drive': 0.3, 'tone': 0.5}}
                    )
                    
                    for i, s in enumerate(note_samples):
                        if beat_start + i < len(bass_samples):
                            bass_samples[beat_start + i] += s * 0.7
        
        return self.normalize(bass_samples)
    
    def generate_melody(self, key: str, scale: str, bars: int, bpm: int) -> list:
        """Generate melody"""
        beat_duration = 60 / bpm
        samples_per_beat = int(self.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        melody_samples = [0.0] * total_samples
        
        scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 5, 7, 10],
        }
        
        note_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        root_midi = 60 + note_values.get(key.upper(), 0)
        intervals = scales.get(scale, scales['minor'])
        
        for bar in range(bars):
            for beat in range(4):
                if random.random() > 0.3:
                    beat_start = (bar * 4 + beat) * samples_per_beat
                    
                    interval = random.choice(intervals)
                    freq = 261.63 * (2 ** ((root_midi + interval - 60) / 12))
                    
                    note_samples = self.synth.play_note(
                        freq, beat_duration * 0.8,
                        random.choice(['sine', 'triangle', 'square']),
                        attack=0.02, decay=0.1, sustain=0.5, release=0.2,
                        filter_freq=3000,
                        effects={'reverb': {'size': 0.4, 'wet': 0.3}}
                    )
                    
                    for i, s in enumerate(note_samples):
                        if beat_start + i < len(melody_samples):
                            melody_samples[beat_start + i] += s * 0.5
        
        return self.normalize(melody_samples)
    
    def generate_chords(self, key: str, bars: int, bpm: int) -> list:
        """Generate chord progression"""
        beat_duration = 60 / bpm
        samples_per_beat = int(self.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        chord_samples = [0.0] * total_samples
        
        note_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        root_freq = 261.63 * (2 ** (note_values.get(key.upper(), 0) / 12))
        
        progressions = [
            ['major', 'minor', 'major', 'major'],
            ['minor', 'minor', 'major', 'major'],
            ['major', 'major', 'minor', 'major'],
        ]
        
        progression = random.choice(progressions)
        
        for bar in range(bars):
            chord_type = progression[bar % len(progression)]
            chord_start = bar * 4 * samples_per_beat
            
            chord_wav = self.synth.play_chord(root_freq, chord_type, beat_duration * 4,
                                               waveform='sine', attack=0.1, decay=0.2,
                                               sustain=0.6, release=0.4, filter_freq=2000,
                                               effects={'reverb': {'size': 0.6, 'wet': 0.4}})
            
            for i, s in enumerate(chord_wav):
                if chord_start + i < len(chord_samples):
                    chord_samples[chord_start + i] += s * 0.6
        
        return self.normalize(chord_samples)
    
    def normalize(self, samples: list) -> list:
        """Normalize audio"""
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            return [s * 0.8 / max_val for s in samples]
        return samples
    
    def mix_tracks(self, *tracks) -> list:
        """Mix multiple tracks together"""
        max_len = max(len(t) for t in tracks)
        mixed = [0.0] * max_len
        
        for track in tracks:
            for i, s in enumerate(track):
                mixed[i] += s
        
        return self.normalize(mixed)
    
    def generate_full_track(self, style: str = 'trap', key: str = 'C', 
                           scale: str = 'minor', bpm: int = 140, bars: int = 8) -> list:
        """Generate complete audio track"""
        print(f"Generating {style} track in {key} {scale} at {bpm} BPM...")
        
        print("  Creating drums...")
        drums = self.generate_drum_pattern(style, bpm, bars)
        
        print("  Creating bass...")
        bass = self.generate_bass(style, key, bars, bpm)
        
        print("  Creating melody...")
        melody = self.generate_melody(key, scale, bars, bpm)
        
        print("  Creating chords...")
        chords = self.generate_chords(key, bars, bpm)
        
        print("  Mixing tracks...")
        final = self.mix_tracks(drums, bass, melody, chords)
        
        return final


if __name__ == "__main__":
    import math
    
    gen = TrackGenerator()
    
    print("=== Audio Track Generator ===\n")
    print("1. Trap (C minor, 140 BPM)")
    print("2. House (E major, 128 BPM)")
    print("3. Hip Hop (D minor, 90 BPM)")
    print("4. Dubstep (A minor, 140 BPM)")
    print("5. Lo-Fi (F major, 80 BPM)")
    
    choice = input("\nSelect track style (1-5): ").strip()
    
    settings = {
        '1': ('trap', 'C', 'minor', 140, 8),
        '2': ('house', 'E', 'major', 128, 8),
        '3': ('hiphop', 'D', 'minor', 90, 8),
        '4': ('dubstep', 'A', 'minor', 140, 8),
        '5': ('lofi', 'F', 'major', 80, 8),
    }
    
    if choice in settings:
        style, key, scale, bpm, bars = settings[choice]
        track = gen.generate_full_track(style, key, scale, bpm, bars)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "audio", f"{style}_full_track.wav")
        gen.engine.save_wav(track, filename)
        
        duration = len(track) / 44100
        print(f"\n[OK] Track saved: {filename}")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Style: {style}")
        print(f"   Key: {key} {scale}")
        print(f"   BPM: {bpm}")
    else:
        print("Invalid choice")