"""
FL STUDIO AI - MASTER BUILD v6.0
===============================
The ultimate beat making toolkit for everyone
- Beginners: Simple wizard, one-click beats
- Pros: Advanced automation, full control
- 10 years old to 60 years old: Anyone can use!

Version: MASTER BUILD
"""

import json
import math
import os
import random
import struct
import sys
import time
import wave
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, List, Dict

# Color output for Windows
try:
    import colorama
    colorama.init()
    COLORS = True
except ImportError:
    COLORS = False


def cprint(text, color='white'):
    """Print colored text"""
    if not COLORS:
        print(text)
        return
    colors = {
        'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
        'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m',
        'white': '\033[97m', 'bold': '\033[1m', 'reset': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")


# ============================================================
# CORE MUSIC ENGINE - IMPROVED
# ============================================================

class MusicTheory:
    """Complete music theory engine"""
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "pentatonic": [0, 2, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
        "whole_tone": [0, 2, 4, 6, 8, 10],
    }
    
    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    CHORD_TYPES = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "7th": [0, 4, 7, 10],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "sus4": [0, 5, 7],
        "dim": [0, 3, 6],
        "aug": [0, 4, 8],
    }
    
    @classmethod
    def get_note_frequency(cls, note: str, octave: int = 4) -> float:
        """Get frequency of a note"""
        try:
            note_idx = cls.NOTES.index(note.upper().replace('♯', '#').replace('♭', 'b'))
        except ValueError:
            note_idx = 0
        semitones = (octave - 4) * 12 + note_idx
        return 261.63 * (2 ** (semitones / 12))
    
    @classmethod
    def get_scale_notes(cls, root: str, scale: str) -> List[str]:
        """Get all notes in a scale"""
        try:
            root_idx = cls.NOTES.index(root.upper().replace('♯', '#'))
        except ValueError:
            root_idx = 0
        intervals = cls.SCALES.get(scale, cls.SCALES['major'])
        return [cls.NOTES[(root_idx + i) % 12] for i in intervals]
    
    @classmethod
    def get_chord_notes(cls, root: str, chord_type: str) -> List[str]:
        """Get notes in a chord"""
        try:
            root_idx = cls.NOTES.index(root.upper().replace('♯', '#'))
        except ValueError:
            root_idx = 0
        intervals = cls.CHORD_TYPES.get(chord_type, cls.CHORD_TYPES['major'])
        return [cls.NOTES[(root_idx + i) % 12] for i in intervals]


# ============================================================
# AUDIO SYNTHESIS ENGINE
# ============================================================

class AudioSynthesizer:
    """Professional audio synthesis"""
    
    SAMPLE_RATE = 44100
    
    def __init__(self):
        self.sample_rate = self.SAMPLE_RATE
    
    def generate_wave(self, freq: float, duration: float, waveform: str = 'sine', 
                     attack: float = 0.01, decay: float = 0.1, sustain: float = 0.7, 
                     release: float = 0.3) -> List[float]:
        """Generate waveform with ADSR envelope"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        attack_samples = int(self.sample_rate * attack)
        decay_samples = int(self.sample_rate * decay)
        release_samples = int(self.sample_rate * release)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            phase = 2 * math.pi * freq * t
            
            # Waveform
            if waveform == 'sine':
                sample = math.sin(phase)
            elif waveform == 'square':
                sample = 1 if math.sin(phase) > 0 else -1
            elif waveform == 'sawtooth':
                sample = 2 * (t * freq - math.floor(t * freq + 0.5))
            elif waveform == 'triangle':
                sample = 2 * abs(2 * (t * freq - math.floor(t * freq + 0.5))) - 1
            elif waveform == 'noise':
                sample = random.random() * 2 - 1
            else:
                sample = math.sin(phase)
            
            # ADSR envelope
            if i < attack_samples:
                env = i / attack_samples
            elif i < attack_samples + decay_samples:
                env = 1 - (i - attack_samples) / decay_samples * (1 - sustain)
            elif i < num_samples - release_samples:
                env = sustain
            else:
                env = sustain * (num_samples - i) / release_samples
            
            samples.append(sample * env * 0.5)
        
        return samples
    
    def apply_filter(self, samples: List[float], filter_type: str, freq: float) -> List[float]:
        """Apply filter to audio"""
        if filter_type == 'lowpass':
            result = []
            val = 0
            f = 2 * math.sin(math.pi * freq / self.sample_rate)
            for s in samples:
                val += f * (s - val)
                result.append(val)
            return result
        return samples
    
    def apply_reverb(self, samples: List[float], room_size: float = 0.5, wet: float = 0.3) -> List[float]:
        """Apply reverb effect"""
        import random
        length = int(len(samples) * room_size)
        impulse = [(random.random() * 2 - 1) * math.exp(-3 * i / length) * wet 
                   for i in range(length)]
        
        result = samples.copy()
        for i in range(len(samples)):
            reverb_sum = sum(samples[i - j] * impulse[j] for j in range(min(i, len(impulse))))
            result[i] = samples[i] + reverb_sum * 0.3
        
        return self.normalize(result)
    
    def normalize(self, samples: List[float]) -> List[float]:
        """Normalize audio"""
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            return [s * 0.8 / max_val for s in samples]
        return samples
    
    def save_wav(self, samples: List[float], filename: str):
        """Save audio to WAV file"""
        os.makedirs(os.path.dirname(filename) if '/' in filename and os.path.dirname(filename) else '.', exist_ok=True)
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            for sample in samples:
                packed = struct.pack('<hh', int(sample * 32767), int(sample * 32767))
                wav.writeframes(packed)
    
    def generate_kick(self) -> List[float]:
        """Generate kick drum"""
        samples = []
        for i in range(int(self.sample_rate * 0.3)):
            t = i / self.sample_rate
            freq = 150 * (1 - t / 0.3 * 0.7) + 40
            env = (1 - t / 0.3) ** 2
            samples.append(math.sin(2 * math.pi * freq * t) * env)
        return self.normalize(samples)
    
    def generate_snare(self) -> List[float]:
        """Generate snare drum"""
        samples = []
        for i in range(int(self.sample_rate * 0.2)):
            t = i / self.sample_rate
            env = (1 - t / 0.2) ** 1.5
            tone = math.sin(2 * math.pi * 200 * t) * 0.3
            noise = (random.random() * 2 - 1) * 0.7
            samples.append((tone + noise) * env)
        return self.normalize(samples)
    
    def generate_hihat(self) -> List[float]:
        """Generate hi-hat"""
        samples = []
        for i in range(int(self.sample_rate * 0.05)):
            t = i / self.sample_rate
            env = (1 - t / 0.05) ** 2
            samples.append((random.random() * 2 - 1) * env * 0.5)
        return self.normalize(samples)


# ============================================================
# DRUM PATTERN GENERATOR
# ============================================================

class DrumGenerator:
    """Generate drum patterns for any style"""
    
    STYLES = {
        'trap': {'kick': [1,0,0,1], 'snare': [0,0,1,0], 'hihat': [1,1,1,1,1,1,1,1], 'bpm': 140},
        'house': {'kick': [1,0,1,0], 'snare': [0,0,1,0], 'hihat': [1,0,1,0,1,0,1,0], 'bpm': 128},
        'hiphop': {'kick': [1,0,0,1], 'snare': [0,0,1,0], 'hihat': [1,1,0,1,1,1,0,1], 'bpm': 90},
        'dubstep': {'kick': [1,0,0,0,1,0,0,0], 'snare': [0,0,1,0,0,0,1,0], 'hihat': [1,1,1,1,1,1,1,1], 'bpm': 140},
        'dnb': {'kick': [1,0,0,1], 'snare': [0,0,1,1], 'hihat': [1,1,1,1,1,1,1,1], 'bpm': 170},
        'lofi': {'kick': [1,0,0,0], 'snare': [0,0,1,0], 'hihat': [1,0,1,0,1,0,1,0], 'bpm': 80},
        'edm': {'kick': [1,0,1,0], 'snare': [0,0,1,0], 'hihat': [1,1,1,1,1,1,1,1], 'bpm': 128},
        'jazz': {'kick': [1,0,0,1], 'snare': [0,0,1,0], 'hihat': [1,0,1,0,1,0,1,0], 'bpm': 120},
    }
    
    def __init__(self):
        self.synth = AudioSynthesizer()
    
    def generate_track_audio(self, style: str, bars: int = 4) -> List[float]:
        """Generate full drum track as audio"""
        pattern = self.STYLES.get(style, self.STYLES['trap'])
        bpm = pattern['bpm']
        beat_duration = 60 / bpm
        samples_per_beat = int(self.synth.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        track = [0.0] * total_samples
        
        for bar in range(bars):
            for beat in range(4):
                beat_start = (bar * 4 + beat) * samples_per_beat
                
                # Kick
                if pattern['kick'][beat]:
                    kick = self.synth.generate_kick()
                    for i, s in enumerate(kick):
                        if beat_start + i < len(track):
                            track[beat_start + i] += s * 0.8
                
                # Snare
                if pattern['snare'][beat]:
                    snare = self.synth.generate_snare()
                    for i, s in enumerate(snare):
                        if beat_start + i < len(track):
                            track[beat_start + i] += s * 0.6
                
                # Hi-hats
                for sub in range(4):
                    sub_idx = (beat * 4 + sub) % 8
                    if pattern['hihat'][sub_idx]:
                        hihat = self.synth.generate_hihat()
                        hihat_start = beat_start + sub * samples_per_beat // 4
                        for i, s in enumerate(hihat):
                            if hihat_start + i < len(track):
                                track[hihat_start + i] += s * 0.3
        
        return track


# ============================================================
# MELODY & BASS GENERATOR
# ============================================================

class MelodyGenerator:
    """Generate melodies and bass lines"""
    
    def __init__(self):
        self.synth = AudioSynthesizer()
    
    def generate_melody(self, key: str, scale: str, bars: int, bpm: int) -> List[float]:
        """Generate melody"""
        scale_notes = MusicTheory.get_scale_notes(key, scale)
        beat_duration = 60 / bpm
        samples_per_beat = int(self.synth.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        track = [0.0] * total_samples
        
        for bar in range(bars):
            for beat in range(4):
                if random.random() > 0.3:
                    beat_start = (bar * 4 + beat) * samples_per_beat
                    
                    note = random.choice(scale_notes)
                    freq = MusicTheory.get_note_frequency(note, random.choice([4, 5]))
                    
                    note_audio = self.synth.generate_wave(
                        freq, beat_duration * 0.8, 
                        random.choice(['sine', 'triangle', 'square']),
                        attack=0.02, decay=0.1, sustain=0.5, release=0.2
                    )
                    note_audio = self.synth.apply_filter(note_audio, 'lowpass', 3000)
                    note_audio = self.synth.apply_reverb(note_audio, 0.4, 0.3)
                    
                    for i, s in enumerate(note_audio):
                        if beat_start + i < len(track):
                            track[beat_start + i] += s * 0.5
        
        return self.synth.normalize(track)
    
    def generate_bass(self, key: str, style: str, bars: int, bpm: int) -> List[float]:
        """Generate bass line"""
        beat_duration = 60 / bpm
        samples_per_beat = int(self.synth.sample_rate * beat_duration)
        total_samples = bars * 4 * samples_per_beat
        
        track = [0.0] * total_samples
        
        patterns = {
            'trap': [1,0,0,1],
            'house': [1,0,1,0],
            'hiphop': [1,0,0,1],
            'dubstep': [1,0,0,0,1,0,0,0],
        }
        pattern = patterns.get(style, [1,0,0,1])
        
        freq = MusicTheory.get_note_frequency(key, 2)
        
        for bar in range(bars):
            for beat in range(4):
                if pattern[beat % len(pattern)]:
                    beat_start = (bar * 4 + beat) * samples_per_beat
                    
                    bass_note = self.synth.generate_wave(
                        freq * (1 if beat % 2 == 0 else 1.5),
                        beat_duration * 0.9, 'sawtooth',
                        attack=0.01, decay=0.1, sustain=0.6, release=0.2
                    )
                    bass_note = self.synth.apply_filter(bass_note, 'lowpass', 800)
                    
                    for i, s in enumerate(bass_note):
                        if beat_start + i < len(track):
                            track[beat_start + i] += s * 0.7
        
        return self.synth.normalize(track)


# ============================================================
# PRESET LIBRARY
# ============================================================

class PresetLibrary:
    """Easy preset selection for any user level"""
    
    PRESETS = {
        # Beginner presets - simple one-click
        "baby_first_beat": {
            "style": "lofi", "bpm": 70, "bars": 2, "complexity": "minimal",
            "description": "Simple beat for beginners", "key": "C"
        },
        "easy_hiphop": {
            "style": "hiphop", "bpm": 85, "bars": 2, "complexity": "minimal",
            "description": "Easy hip hop beat", "key": "D"
        },
        "simple_house": {
            "style": "house", "bpm": 120, "bars": 2, "complexity": "minimal",
            "description": "Basic house rhythm", "key": "E"
        },
        
        # Intermediate presets
        "trap_banger": {
            "style": "trap", "bpm": 140, "bars": 4, "complexity": "medium",
            "description": "Classic trap beat", "key": "C"
        },
        "edm_drop": {
            "style": "edm", "bpm": 128, "bars": 4, "complexity": "medium",
            "description": "EDM with build up", "key": "A"
        },
        "lofi_chill": {
            "style": "lofi", "bpm": 75, "bars": 2, "complexity": "medium",
            "description": "Relaxing lofi beat", "key": "F"
        },
        
        # Advanced presets
        "pro_dnb": {
            "style": "dnb", "bpm": 170, "bars": 4, "complexity": "advanced",
            "description": "Full DNB track", "key": "D"
        },
        "dubstep_wobble": {
            "style": "dubstep", "bpm": 140, "bars": 4, "complexity": "advanced",
            "description": "Dubstep with bass wobbles", "key": "A"
        },
        
        # Mood-based presets
        "chill_vibes": {"style": "lofi", "bpm": 70, "bars": 2, "complexity": "minimal", "key": "G"},
        "workout_energy": {"style": "edm", "bpm": 140, "bars": 4, "complexity": "medium", "key": "E"},
        "study_focus": {"style": "lofi", "bpm": 80, "bars": 2, "complexity": "minimal", "key": "C"},
        "party_mode": {"style": "trap", "bpm": 150, "bars": 4, "complexity": "medium", "key": "C"},
    }
    
    @classmethod
    def get_presets_by_level(cls, level: str) -> Dict:
        """Get presets by user level"""
        if level == "beginner":
            return {k: v for k, v in cls.PRESETS.items() if v.get("complexity") == "minimal"}
        elif level == "intermediate":
            return {k: v for k, v in cls.PRESETS.items() if v.get("complexity") == "medium"}
        elif level == "advanced":
            return {k: v for k, v in cls.PRESETS.items() if v.get("complexity") == "advanced"}
        return cls.PRESETS
    
    @classmethod
    def get_mood_presets(cls, mood: str) -> Dict:
        """Get presets by mood"""
        return {k: v for k, v in cls.PRESETS.items() if mood.lower() in k.lower() or 
                (mood == "relax" and "lofi" in v["style"]) or
                (mood == "energy" and v["bpm"] > 120)}


# ============================================================
# AUTOMATION ENGINE
# ============================================================

class AutomationEngine:
    """Schedule and automate beat generation"""
    
    def __init__(self):
        self.scheduled_tasks = []
        self.is_running = False
    
    def schedule_beat(self, preset: str, interval_minutes: int = 60):
        """Schedule automatic beat generation"""
        task = {
            "preset": preset,
            "interval": interval_minutes,
            "last_run": None,
            "total_generated": 0
        }
        self.scheduled_tasks.append(task)
        return task
    
    def cancel_schedule(self, preset: str):
        """Cancel scheduled task"""
        self.scheduled_tasks = [t for t in self.scheduled_tasks if t["preset"] != preset]
    
    def get_status(self) -> Dict:
        """Get automation status"""
        return {
            "active": len(self.scheduled_tasks) > 0,
            "tasks": self.scheduled_tasks,
            "total_beats_generated": sum(t["total_generated"] for t in self.scheduled_tasks)
        }


# ============================================================
# SMART RECOMMENDATIONS
# ============================================================

class SmartRecommendations:
    """AI-powered recommendations"""
    
    @staticmethod
    def suggest_preset(time_of_day: str, user_level: str) -> str:
        """Suggest preset based on time and user level"""
        suggestions = {
            ("morning", "beginner"): "study_focus",
            ("morning", "intermediate"): "simple_house",
            ("morning", "advanced"): "lofi_chill",
            ("afternoon", "beginner"): "easy_hiphop",
            ("afternoon", "intermediate"): "trap_banger",
            ("afternoon", "advanced"): "pro_dnb",
            ("evening", "beginner"): "chill_vibes",
            ("evening", "intermediate"): "party_mode",
            ("evening", "advanced"): "dubstep_wobble",
            ("night", "beginner"): "baby_first_beat",
            ("night", "intermediate"): "lofi_chill",
            ("night", "advanced"): "pro_dnb",
        }
        return suggestions.get((time_of_day, user_level), "baby_first_beat")
    
    @staticmethod
    def suggest_next_style(current_style: str) -> str:
        """Suggest next style to try"""
        progression = {
            "lofi": "hiphop",
            "hiphop": "house",
            "house": "trap",
            "trap": "edm",
            "edm": "dubstep",
            "dubstep": "dnb",
            "dnb": "lofi",
        }
        return progression.get(current_style, "trap")


# ============================================================
# MIDI EXPORT
# ============================================================

class MIDIExporter:
    """Export beats to MIDI for FL Studio"""
    
    def __init__(self):
        self.header = b'MThd' + struct.pack('>HHH', 0, 1, 480)
    
    def create_track(self, notes: List[tuple], channel: int = 0) -> bytes:
        """Create MIDI track from notes (pitch, time, duration)"""
        events = []
        current_time = 0
        
        for pitch, start, duration in notes:
            delta = start - current_time
            events.append(self._write_var_length(delta))
            events.append(bytes([0x90 | channel, pitch, 100]))
            events.append(self._write_var_length(duration))
            events.append(bytes([0x80 | channel, pitch, 0]))
            current_time = start + duration
        
        events.append(self._write_var_length(0))
        events.append(bytes([0xFF, 0x2F, 0x00]))
        
        track = b'MTrk' + struct.pack('>I', len(b''.join(events))) + b''.join(events)
        return track
    
    def _write_var_length(self, value: int) -> bytes:
        """Write variable length quantity"""
        result = []
        result.append(value & 0x7F)
        value >>= 7
        while value > 0:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        return bytes(reversed(result))
    
    def export_drums(self, style: str, bars: int, filename: str):
        """Export drum pattern to MIDI"""
        drum_gen = DrumGenerator()
        pattern = DrumGenerator.STYLES.get(style, DrumGenerator.STYLES['trap'])
        
        notes = []
        time = 0
        beat = 480
        
        for bar in range(bars):
            for b in range(4):
                # Kick (pitch 36)
                if pattern['kick'][b]:
                    notes.append((36, time, beat))
                # Snare (pitch 38)
                if pattern['snare'][b]:
                    notes.append((38, time, beat))
                # Hi-hat (pitch 42)
                for h in range(4):
                    if pattern['hihat'][(b * 4 + h) % 8]:
                        notes.append((42, time + h * beat // 4, beat // 4))
                time += beat
        
        track_data = self.create_track(notes)
        midi_data = self.header + track_data
        
        with open(filename, 'wb') as f:
            f.write(midi_data)


# ============================================================
# WIZARD INTERFACE - FOR BEGINNERS
# ============================================================

class BeginnerWizard:
    """Step-by-step wizard for beginners"""
    
    @staticmethod
    def run():
        """Run beginner wizard"""
        cprint("\n" + "="*50, 'cyan')
        cprint("    WELCOME TO FL STUDIO AI!", 'bold')
        cprint("    Let's make your first beat!", 'cyan')
        cprint("="*50 + "\n", 'cyan')
        
        cprint("First, how old are you? (This helps us help you)", 'yellow')
        cprint("  1. I'm a kid (under 12)", 'white')
        cprint("  2. I'm a teenager (12-17)", 'white')
        cprint("  3. I'm an adult (18-59)", 'white')
        cprint("  4. I'm a senior (60+)", 'white')
        
        age_choice = input("\nYour choice: ").strip()
        
        cprint("\nWhat mood are you in?", 'yellow')
        cprint("  1. Relaxed/Chill", 'white')
        cprint("  2. Energetic/Hype", 'white')
        cprint("  3. Focus/Study", 'white')
        cprint("  4. Party/Fun", 'white')
        
        mood_choice = input("Your choice: ").strip()
        
        mood_map = {'1': 'relax', '2': 'energy', '3': 'focus', '4': 'party'}
        mood = mood_map.get(mood_choice, 'relax')
        
        preset = SmartRecommendations.suggest_preset("afternoon", "beginner")
        
        cprint(f"\n[OK] Let's make a {preset.replace('_', ' ')} beat for you!", 'green')
        
        return preset


# ============================================================
# MASTER INTERFACE
# ============================================================

class MasterInterface:
    """Main interface - works for everyone"""
    
    def __init__(self):
        self.synth = AudioSynthesizer()
        self.drums = DrumGenerator()
        self.melody = MelodyGenerator()
        self.presets = PresetLibrary()
        self.automation = AutomationEngine()
        self.midi = MIDIExporter()
    
    def one_click_beat(self, preset_name: str = None):
        """One-click beat generation"""
        if not preset_name:
            preset_name = "baby_first_beat"
        
        preset = self.presets.PRESETS.get(preset_name, self.presets.PRESETS["baby_first_beat"])
        
        cprint(f"\n[OK] Creating {preset_name.replace('_', ' ')}...", 'cyan')
        cprint(f"    Style: {preset['style']}, BPM: {preset['bpm']}, Bars: {preset['bars']}", 'white')
        
        # Generate drums only (faster)
        track = self.drums.generate_track_audio(preset['style'], preset['bars'])
        
        # Save immediately
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(script_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        filename = os.path.join(audio_dir, f"{preset_name}.wav")
        self.synth.save_wav(track, filename)
        
        # Export MIDI
        midi_dir = os.path.join(script_dir, "exports")
        os.makedirs(midi_dir, exist_ok=True)
        midi_file = os.path.join(midi_dir, f"{preset_name}.mid")
        self.midi.export_drums(preset['style'], preset['bars'], midi_file)
        
        duration = len(track) / self.synth.sample_rate
        cprint(f"\n[OK] Beat created!", 'green')
        cprint(f"    Audio: {filename}", 'white')
        cprint(f"    MIDI:  {midi_file}", 'white')
        cprint(f"    Duration: {duration:.1f} seconds", 'white')
        
        return filename
        
        # Save
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(script_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        filename = os.path.join(audio_dir, f"{preset_name}.wav")
        self.synth.save_wav(mixed, filename)
        
        # Export MIDI
        midi_dir = os.path.join(script_dir, "exports")
        os.makedirs(midi_dir, exist_ok=True)
        midi_file = os.path.join(midi_dir, f"{preset_name}.mid")
        self.midi.export_drums(preset['style'], preset['bars'], midi_file)
        
        duration = len(mixed) / self.synth.sample_rate
        cprint(f"\n[OK] Beat created!", 'green')
        cprint(f"    Audio: {filename}", 'white')
        cprint(f"    MIDI:  {midi_file}", 'white')
        cprint(f"    Duration: {duration:.1f} seconds", 'white')
        
        return filename
    
    def show_menu(self):
        """Show main menu"""
        cprint("\n" + "="*60, 'cyan')
        cprint("     FL STUDIO AI - MASTER BUILD", 'bold')
        cprint("     For Everyone: Kids to Seniors, Newbie to Pro", 'cyan')
        cprint("="*60, 'cyan')
        
        cprint("\n  QUICK START - One Click!", 'yellow')
        cprint("    1. Make My First Beat (for beginners)", 'white')
        cprint("    2. Magic Beat (surprise me!)", 'white')
        
        cprint("\n  CHOOSE YOUR MOOD:", 'yellow')
        cprint("    3. Relaxing/Chill", 'white')
        cprint("    4. Energetic/Hype", 'white')
        cprint("    5. Focus/Study", 'white')
        cprint("    6. Party Time", 'white')
        
        cprint("\n  STYLE SELECTION:", 'yellow')
        cprint("    7. Trap", 'white')
        cprint("    8. House", 'white')
        cprint("    9. Hip Hop", 'white')
        cprint("   10. Lo-Fi", 'white')
        cprint("   11. Dubstep", 'white')
        cprint("   12. Drum & Bass", 'white')
        cprint("   13. EDM", 'white')
        
        cprint("\n  ADVANCED:", 'yellow')
        cprint("   14. Custom Beat Builder", 'white')
        cprint("   15. Schedule Auto-Beats", 'white')
        cprint("   16. View All Presets", 'white')
        
        cprint("\n   0. Exit", 'white')
        print()
    
    def run(self):
        """Run the master interface"""
        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.one_click_beat("baby_first_beat")
            elif choice == "2":
                preset = random.choice(list(self.presets.PRESETS.keys()))
                self.one_click_beat(preset)
            elif choice == "3":
                self.one_click_beat("chill_vibes")
            elif choice == "4":
                self.one_click_beat("workout_energy")
            elif choice == "5":
                self.one_click_beat("study_focus")
            elif choice == "6":
                self.one_click_beat("party_mode")
            elif choice == "7":
                self.one_click_beat("trap_banger")
            elif choice == "8":
                self.one_click_beat("simple_house")
            elif choice == "9":
                self.one_click_beat("easy_hiphop")
            elif choice == "10":
                self.one_click_beat("lofi_chill")
            elif choice == "11":
                self.one_click_beat("dubstep_wobble")
            elif choice == "12":
                self.one_click_beat("pro_dnb")
            elif choice == "13":
                self.one_click_beat("edm_drop")
            elif choice == "14":
                self.custom_beat()
            elif choice == "15":
                self.schedule_automation()
            elif choice == "16":
                self.show_presets()
            elif choice == "0":
                cprint("\nThanks for using FL Studio AI! Bye!", 'cyan')
                break
            else:
                cprint("\nInvalid choice. Try again!", 'red')
            
            input("\nPress Enter to continue...")
    
    def custom_beat(self):
        """Custom beat builder"""
        cprint("\n--- Custom Beat Builder ---", 'cyan')
        
        style = input("Style (trap/house/hiphop/lofi/dubstep/dnb/edm): ").strip().lower()
        bpm = input("BPM (60-200): ").strip()
        bpm = int(bpm) if bpm.isdigit() else 120
        bars = input("Bars (2-16): ").strip()
        bars = int(bars) if bars.isdigit() else 4
        
        track = self.drums.generate_track_audio(style, bars)
        filename = f"audio/custom_{style}_{bpm}bpm.wav"
        self.synth.save_wav(track, filename)
        
        cprint(f"[OK] Custom beat saved to {filename}", 'green')
    
    def schedule_automation(self):
        """Schedule automation"""
        cprint("\n--- Auto-Beat Scheduler ---", 'cyan')
        cprint("This feature generates beats automatically!", 'yellow')
        cprint("1. Hourly beats", 'white')
        cprint("2. Daily at specific time", 'white')
        
        choice = input("Choice: ").strip()
        
        if choice == "1":
            self.automation.schedule_beat("baby_first_beat", 60)
            cprint("[OK] Hourly beats scheduled!", 'green')
    
    def show_presets(self):
        """Show all presets"""
        cprint("\n--- All Presets ---", 'cyan')
        for name, preset in self.presets.PRESETS.items():
            print(f"  {name}: {preset['style']} @ {preset['bpm']} BPM ({preset.get('description', '')})")


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Main entry point"""
    master = MasterInterface()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1].lower()
        
        preset_map = {
            "1": "baby_first_beat",
            "2": "pro_dnb",  # magic
            "3": "chill_vibes",
            "4": "workout_energy",
            "5": "study_focus",
            "6": "party_mode",
            "7": "trap_banger",
            "8": "simple_house",
            "9": "easy_hiphop",
            "10": "lofi_chill",
            "11": "dubstep_wobble",
            "12": "pro_dnb",
            "13": "edm_drop",
            "wizard": "wizard",
            "oneclick": "baby_first_beat",
            "magic": "pro_dnb",
            "relax": "chill_vibes",
            "energy": "workout_energy",
            "focus": "study_focus",
            "party": "party_mode",
            "trap": "trap_banger",
            "house": "simple_house",
            "hiphop": "easy_hiphop",
            "lofi": "lofi_chill",
            "dubstep": "dubstep_wobble",
            "dnb": "pro_dnb",
            "edm": "edm_drop",
            "presets": "show",
        }
        
        if command == "wizard":
            BeginnerWizard.run()
        elif command == "presets":
            master.show_presets()
        elif command == "custom":
            master.custom_beat()
        elif command in preset_map:
            preset = preset_map[command]
            if preset != "wizard":
                master.one_click_beat(preset)
        else:
            master.one_click_beat(command)
    else:
        # Interactive mode
        master.run()


if __name__ == "__main__":
    main()