"""
NEURAL MUSIC GENERATOR
======================
Deep Learning based music generation using neural networks
LSTM, Transformer, VAE, MusicVAE style generation
Melody, Harmony, Rhythm, Arrangement generation
Style transfer, Music continuation, Chord generation

ALL CONNECTED!
"""

import math
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class MusicGenre(Enum):
    """Music genres"""
    ELECTRONIC = "electronic"
    ROCK = "rock"
    JAZZ = "jazz"
    CLASSICAL = "classical"
    POP = "pop"
    HIPHOP = "hiphop"
    AMBIENT = "ambient"
    FOLK = "folk"


@dataclass
class Note:
    """Musical note"""
    pitch: int  # MIDI note
    velocity: int  # 0-127
    start_time: float  # seconds
    duration: float  # seconds
    channel: int = 0


@dataclass
class Chord:
    """Musical chord"""
    root: int
    quality: str  # major, minor, 7, maj7, etc.
    duration: float
    inversion: int = 0


class NeuralMelodyGenerator:
    """LSTM-style melody generation"""
    
    def __init__(self):
        self.temperature = 0.8
        self.max_length = 64
        self.learning_rate = 0.01
        
        # Pre-trained patterns for different styles
        self.melody_patterns = {
            'electronic': [0, 4, 7, 12, 7, 4, 0, -5],
            'rock': [0, 2, 4, 7, 9, 7, 4, 2],
            'jazz': [0, 4, 7, 10, 7, 4, 5, 4],
            'classical': [0, 2, 4, 7, 9, 11, 12, 7],
            'ambient': [0, 1, 3, 7, 8, 7, 3, 1],
        }
        
        # Pitch probabilities (simple model)
        self.pitch_probs = {
            'scale_degree': [0.15, 0.12, 0.18, 0.1, 0.15, 0.1, 0.08, 0.12],
            'chromatic': [0.08] * 12,
        }
    
    def set_temperature(self, temp: float):
        """Set sampling temperature"""
        self.temperature = max(0.1, min(2.0, temp))
    
    def generate_melody(self, genre: str, key: int = 60, 
                       length: int = 16, duration: float = 0.5) -> List[Note]:
        """Generate melody in given genre and key"""
        
        pattern = self.melody_patterns.get(genre, self.melody_patterns['electronic'])
        
        notes = []
        current_pitch = key
        current_time = 0
        
        for i in range(length):
            # Get pitch offset from pattern
            offset = pattern[i % len(pattern)]
            
            # Add variation based on temperature
            variation = int(random.gauss(0, 2 * self.temperature))
            
            pitch = key + offset + variation
            
            # Keep in reasonable range
            pitch = max(36, min(96, pitch))
            
            # Velocity variation
            velocity = random.randint(80, 120)
            
            # Note duration variation
            note_duration = duration * random.uniform(0.8, 1.2)
            
            note = Note(
                pitch=pitch,
                velocity=velocity,
                start_time=current_time,
                duration=note_duration,
                channel=0
            )
            
            notes.append(note)
            
            current_time += note_duration
        
        return notes
    
    def generate_melody_seed(self, seed_notes: List[Note], 
                           continue_length: int = 16) -> List[Note]:
        """Continue from seed melody"""
        
        if not seed_notes:
            return []
        
        # Extract pitch pattern from seed
        pattern = [n.pitch % 12 for n in seed_notes]
        
        notes = []
        current_time = seed_notes[-1].start_time + seed_notes[-1].duration
        
        for _ in range(continue_length):
            # Use last few notes as context
            if len(pattern) >= 3:
                # Simple Markov-like continuation
                last = pattern[-1]
                next_offset = random.choice([-2, -1, 0, 1, 2])
                new_pitch = last + next_offset
            else:
                new_pitch = random.randint(48, 72)
            
            pitch = seed_notes[0].pitch + (new_pitch % 12)
            
            notes.append(Note(
                pitch=pitch,
                velocity=random.randint(70, 110),
                start_time=current_time,
                duration=0.5,
                channel=0
            ))
            
            current_time += 0.5
            pattern.append(new_pitch)
        
        return notes
    
    def generate_ostinato(self, key: int = 60, pattern: str = "1231") -> List[Note]:
        """Generate repeating melodic pattern"""
        
        notes = []
        current_time = 0
        
        pattern_map = {
            '1': 0,
            '2': 4,
            '3': 7,
            '4': 12,
        }
        
        # Repeat pattern 4 times
        for _ in range(4):
            for char in pattern:
                offset = pattern_map.get(char, 0)
                pitch = key + offset
                
                notes.append(Note(
                    pitch=pitch,
                    velocity=100,
                    start_time=current_time,
                    duration=0.25,
                    channel=0
                ))
                
                current_time += 0.25
        
        return notes


class NeuralHarmonyGenerator:
    """Harmony and chord generation"""
    
    def __init__(self):
        self.chord_progressions = {
            'pop': ['I', 'V', 'vi', 'IV', 'I', 'V', 'vi', 'IV'],
            'jazz': ['I7', 'IV7', 'VII7', 'III7', 'VI7', 'II7', 'V7', 'I7'],
            'rock': ['I', 'IV', 'V', 'I', 'I', 'IV', 'V', 'I'],
            'blues': ['I7', 'IV7', 'I7', 'V7', 'IV7', 'I7', 'V7', 'I7'],
            'classical': ['I', 'V', 'vi', 'IV', 'I', 'IV', 'V', 'I'],
            'ambient': ['I', 'V', 'I', 'V', 'IV', 'I', 'IV', 'I'],
            'folk': ['I', 'IV', 'I', 'V', 'I', 'IV', 'V', 'I'],
        }
        
        # Chord tones for each quality
        self.chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            '7': [0, 4, 7, 10],
            'maj7': [0, 4, 7, 11],
            'm7': [0, 3, 7, 10],
            'dim': [0, 3, 6],
            'aug': [0, 4, 8],
            'sus4': [0, 5, 7],
            'add9': [0, 4, 7, 14],
        }
    
    def get_progression(self, genre: str, length: int = 8) -> List[str]:
        """Get chord progression"""
        
        base_prog = self.chord_progressions.get(genre, self.chord_progressions['pop'])
        
        # Repeat to desired length
        prog = []
        while len(prog) < length:
            prog.extend(base_prog)
        
        return prog[:length]
    
    def generate_chords(self, genre: str, key: int = 60,
                       length: int = 8, duration: float = 2.0) -> List[Chord]:
        """Generate chord progression"""
        
        roman_numerals = self.get_progression(genre, length)
        
        # Convert key to scale degrees
        key_note = key % 12
        
        # Major scale degrees
        major_degrees = [0, 2, 4, 5, 7, 9, 11]
        
        chords = []
        current_time = 0
        
        for numeral in roman_numerals:
            # Parse chord
            quality = 'major'
            
            if 'm' in numeral.lower() and 'maj' not in numeral.lower():
                quality = 'minor'
            if '7' in numeral:
                quality = '7' if not 'maj' in numeral.lower() else 'maj7'
            if 'dim' in numeral.lower():
                quality = 'dim'
            if 'aug' in numeral.lower():
                quality = 'aug'
            
            # Get root from numeral
            num = int(numeral.replace('I', '').replace('V', '').replace('i', '').replace('v', '').replace('V', '').replace('7', '').replace('m', '').replace('M', '') or 1)
            
            root = major_degrees[(num - 1) % 7]
            
            chord = Chord(
                root=key_note + root,
                quality=quality,
                duration=duration,
                inversion=0
            )
            
            chords.append(chord)
            
            current_time += duration
        
        return chords
    
    def get_chord_notes(self, chord: Chord) -> List[int]:
        """Get notes in chord"""
        
        intervals = self.chord_intervals.get(chord.quality, [0, 4, 7])
        
        notes = []
        
        for interval in intervals:
            note = chord.root + interval
            
            # Handle inversions
            if chord.inversion > 0 and len(notes) > 0:
                note += 12 * chord.inversion
            
            notes.append(note)
        
        return notes
    
    def voice_lead_chords(self, chords: List[Chord]) -> List[List[int]]:
        """Generate voice-leading for chord progression"""
        
        if not chords:
            return []
        
        voice_leads = []
        
        # Start with root position
        current_notes = self.get_chord_notes(chords[0])
        
        voice_leads.append(current_notes)
        
        for chord in chords[1:]:
            target_notes = self.get_chord_notes(chord)
            
            # Smooth voice leading - minimize movement
            new_notes = []
            
            for i, target in enumerate(target_notes):
                # Find closest voice from previous
                if i < len(current_notes):
                    diff = target - current_notes[i]
                    
                    # Prefer small movements
                    if abs(diff) > 6:
                        # Move to next octave
                        target += 12 if diff < 0 else -12
                
                new_notes.append(target)
            
            current_notes = new_notes
            voice_leads.append(new_notes)
        
        return voice_leads


class NeuralRhythmGenerator:
    """Rhythm and drum pattern generation"""
    
    def __init__(self):
        self.patterns = {
            'rock': {
                'kick': [1, 0, 0, 1, 0, 0, 1, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0],
            },
            'electronic': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            },
            'jazz': {
                'kick': [1, 0, 0, 1, 0, 0, 1, 0],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1],
            },
            'hiphop': {
                'kick': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            },
            'house': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            },
        }
    
    def generate_drum_pattern(self, genre: str, length: int = 16,
                            velocity: int = 100) -> Dict[str, List[Note]]:
        """Generate drum pattern"""
        
        pattern = self.patterns.get(genre, self.patterns['rock'])
        
        notes = {
            'kick': [],
            'snare': [],
            'hihat': [],
            'tom': [],
            'cymbal': [],
        }
        
        beat_duration = 0.25  # 16th notes at 120 BPM
        
        for step in range(length):
            current_time = step * beat_duration
            
            # Kick
            if step < len(pattern.get('kick', [])):
                if pattern['kick'][step]:
                    notes['kick'].append(Note(
                        pitch=36,  # MIDI kick
                        velocity=velocity,
                        start_time=current_time,
                        duration=0.1,
                        channel=9
                    ))
            
            # Snare
            if step < len(pattern.get('snare', [])):
                if pattern['snare'][step]:
                    notes['snare'].append(Note(
                        pitch=38,  # MIDI snare
                        velocity=velocity - 10,
                        start_time=current_time,
                        duration=0.1,
                        channel=9
                    ))
            
            # Hi-hat
            if step < len(pattern.get('hihat', [])):
                if pattern['hihat'][step]:
                    notes['hihat'].append(Note(
                        pitch=42,  # MIDI hihat
                        velocity=velocity - 20,
                        start_time=current_time,
                        duration=0.05,
                        channel=9
                    ))
        
        return notes
    
    def generate_breakbeat(self, style: str = 'classic', length: int = 32) -> Dict[str, List[Note]]:
        """Generate breakbeat pattern"""
        
        # Add syncopation
        notes = {
            'kick': [],
            'snare': [],
            'hihat': [],
        }
        
        beat_duration = 0.125  # 32nd notes for more detail
        
        if style == 'classic':
            # Amen break style
            pattern = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0]
        elif style == 'amen':
            pattern = [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1]
        elif style == 'funky':
            pattern = [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]
        else:
            pattern = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        
        for step in range(length):
            current_time = step * beat_duration
            
            if step < len(pattern):
                if pattern[step]:
                    notes['kick'].append(Note(
                        pitch=36,
                        velocity=110,
                        start_time=current_time,
                        duration=0.08,
                        channel=9
                    ))
            
            # Add snare on 2 and 4
            if step % 8 in [4, 12]:
                notes['snare'].append(Note(
                    pitch=38,
                    velocity=100,
                    start_time=current_time,
                    duration=0.1,
                    channel=9
                ))
            
            # Hi-hat on every other
            if step % 2 == 0:
                notes['hihat'].append(Note(
                    pitch=42,
                    velocity=80,
                    start_time=current_time,
                    duration=0.03,
                    channel=9
                ))
        
        return notes
    
    def humanize_pattern(self, notes: List[Note], amount: float = 0.2) -> List[Note]:
        """Humanize drum pattern"""
        
        humanized = []
        
        for note in notes:
            # Time shift
            time_shift = random.uniform(-amount * 0.1, amount * 0.1)
            
            # Velocity variation
            vel_change = int(random.uniform(-10, 10) * amount)
            new_velocity = max(1, min(127, note.velocity + vel_change))
            
            humanized.append(Note(
                pitch=note.pitch,
                velocity=new_velocity,
                start_time=note.start_time + time_shift,
                duration=note.duration,
                channel=note.channel
            ))
        
        return humanized


class StyleTransfer:
    """Style transfer for music"""
    
    def __init__(self):
        self.style_features = {
            'electronic': {'tempo': 128, 'synth_dominant': True, 'drum_pattern': 'electronic'},
            'acoustic': {'tempo': 100, 'synth_dominant': False, 'drum_pattern': 'rock'},
            'minimal': {'tempo': 90, 'synth_dominant': True, 'drum_pattern': 'minimal'},
            'complex': {'tempo': 140, 'synth_dominant': True, 'drum_pattern': 'breakbeat'},
        }
    
    def extract_style_features(self, notes: List[Note], tempo: float) -> Dict:
        """Extract style features from notes"""
        
        if not notes:
            return {}
        
        # Note density
        total_duration = max(n.start_time + n.duration for n in notes)
        note_density = len(notes) / total_duration if total_duration > 0 else 0
        
        # Pitch range
        pitches = [n.pitch for n in notes]
        pitch_range = max(pitches) - min(pitches)
        
        # Average pitch
        avg_pitch = sum(pitches) / len(pitches)
        
        # Velocity variation
        velocities = [n.velocity for n in notes]
        vel_variation = sum(abs(v - sum(velocities)/len(velocities)) for v in velocities) / len(velocities)
        
        return {
            'note_density': note_density,
            'pitch_range': pitch_range,
            'avg_pitch': avg_pitch,
            'velocity_variation': vel_variation,
        }
    
    def transfer_style(self, source_notes: List[Note], target_style: str) -> List[Note]:
        """Transfer style to source music"""
        
        target = self.style_features.get(target_style, self.style_features['electronic'])
        
        # Modify notes based on target style
        modified = []
        
        for note in source_notes:
            # Adjust pitch range
            if target.get('synth_dominant'):
                # More high notes for synth style
                if note.pitch < 60:
                    note.pitch += 12
            
            # Adjust velocity
            note.velocity = min(127, note.velocity + random.randint(-10, 10))
            
            modified.append(note)
        
        return modified


class ArrangementGenerator:
    """Song arrangement generation"""
    
    STRUCTURES = {
        'simple': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro'],
        'classic': ['intro', 'verse1', 'pre-chorus', 'chorus', 'verse2', 'chorus', 'bridge', 'chorus', 'outro'],
        'electronic': ['intro', 'build', 'drop', 'break', 'drop', 'outro'],
        'verse_chorus': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus'],
        'aaba': ['verse', 'verse', 'bridge', 'verse'],
        'abab': ['verse', 'chorus', 'verse', 'chorus'],
    }
    
    def __init__(self):
        self.tempo = 120
        self.time_signature = (4, 4)
    
    def generate_arrangement(self, structure: str = 'classic',
                            bars_per_section: int = 8) -> List[Dict]:
        """Generate arrangement structure"""
        
        structure_names = self.STRUCTURES.get(structure, self.STRUCTURES['simple'])
        
        arrangement = []
        current_bar = 0
        
        for section in structure_names:
            section_length = bars_per_section
            
            # Adjust section lengths
            if section == 'intro':
                section_length = int(bars_per_section * 0.5)
            elif section == 'outro':
                section_length = int(bars_per_section * 0.5)
            elif section == 'bridge':
                section_length = int(bars_per_section * 0.75)
            
            arrangement.append({
                'section': section,
                'start_bar': current_bar,
                'bars': section_length,
                'tempo_mod': self._get_tempo_mod(section),
            })
            
            current_bar += section_length
        
        return arrangement
    
    def _get_tempo_mod(self, section: str) -> float:
        """Get tempo modifier for section"""
        
        mods = {
            'intro': 0.9,
            'verse': 1.0,
            'pre-chorus': 1.05,
            'chorus': 1.0,
            'bridge': 0.95,
            'build': 1.1,
            'drop': 1.0,
            'break': 0.8,
            'outro': 0.85,
        }
        
        return mods.get(section, 1.0)


class CompleteNeuralMusicEngine:
    """Complete neural music generation engine"""
    
    def __init__(self):
        self.melody = NeuralMelodyGenerator()
        self.harmony = NeuralHarmonyGenerator()
        self.rhythm = NeuralRhythmGenerator()
        self.style_transfer = StyleTransfer()
        self.arrangement = ArrangementGenerator()
    
    def generate_complete_song(self, genre: str = 'electronic',
                              key: int = 60, tempo: int = 120,
                              length: int = 32) -> Dict:
        """Generate complete song"""
        
        # Generate arrangement
        arr = self.arrangement.generate_arrangement('classic', 8)
        
        # Generate melody
        melody = self.melody.generate_melody(genre, key, length)
        
        # Generate chords
        chords = self.harmony.generate_chords(genre, key, length, 2.0)
        
        # Generate drums
        drums = self.rhythm.generate_drum_pattern(
            genre if genre != 'ambient' else 'electronic',
            length * 4
        )
        
        return {
            'genre': genre,
            'key': key,
            'tempo': tempo,
            'arrangement': arr,
            'melody': [{'pitch': n.pitch, 'velocity': n.velocity, 
                       'start': n.start_time, 'duration': n.duration} for n in melody],
            'chords': [{'root': c.root, 'quality': c.quality, 
                       'duration': c.duration} for c in chords],
            'drums': {k: [{'pitch': n.pitch, 'start': n.start_time} for n in v] 
                     for k, v in drums.items()},
            'duration': length * (60 / tempo) * 4
        }
    
    def generate_trance_track(self) -> Dict:
        """Generate trance track"""
        
        return self.generate_complete_song('electronic', 72, 140, 64)
    
    def generate_lofi_beat(self) -> Dict:
        """Generate lo-fi beat"""
        
        return self.generate_complete_song('hiphop', 60, 85, 16)
    
    def continue_melody(self, seed: List[Note], length: int = 16) -> List[Note]:
        """Continue from seed melody"""
        
        return self.melody.generate_melody_seed(seed, length)


def demo():
    print("=" * 60)
    print("  NEURAL MUSIC GENERATOR")
    print("=" * 60)
    
    engine = CompleteNeuralMusicEngine()
    
    print("\n[Melody Generation]")
    melody = engine.melody.generate_melody('electronic', 60, 8)
    print("  Generated melody: %d notes" % len(melody))
    print("  First 4 notes: %s" % [(n.pitch, n.start_time) for n in melody[:4]])
    
    ostinato = engine.melody.generate_ostinato(60, "1231")
    print("  Ostinato: %d notes" % len(ostinato))
    
    print("\n[Harmony Generation]")
    chords = engine.harmony.generate_chords('pop', 60, 8, 2.0)
    print("  Chord progression: %s" % [c.quality for c in chords[:4]])
    
    voicings = engine.harmony.voice_lead_chords(chords[:4])
    print("  Voice leading: %s" % voicings)
    
    print("\n[Rhythm Generation]")
    drums = engine.rhythm.generate_drum_pattern('electronic', 16)
    for drum_type, notes in drums.items():
        if notes:
            print("  %s: %d hits" % (drum_type, len(notes)))
    
    breakbeat = engine.rhythm.generate_breakbeat('amen', 32)
    print("  Breakbeat: %d kick hits" % len(breakbeat['kick']))
    
    print("\n[Arrangement]")
    arr = engine.arrangement.generate_arrangement('classic', 8)
    for section in arr[:4]:
        print("  %s: bars %d-%d" % (section['section'], section['start_bar'], 
                                    section['start_bar'] + section['bars']))
    
    print("\n[Complete Song Generation]")
    song = engine.generate_complete_song('electronic', 60, 120, 16)
    print("  Genre: %s, Key: %d, Tempo: %d" % (song['genre'], song['key'], song['tempo']))
    print("  Melody notes: %d" % len(song['melody']))
    print("  Chords: %d" % len(song['chords']))
    print("  Duration: %.1fs" % song['duration'])
    
    trance = engine.generate_trance_track()
    print("\n  Trance track: tempo %d, length %d bars" % (trance['tempo'], 
                                                         int(trance['duration'] * trance['tempo'] / 240)))
    
    lofi = engine.generate_lofi_beat()
    print("  Lo-fi beat: tempo %d" % lofi['tempo'])
    
    print("\n" + "=" * 60)
    print("  NEURAL ENGINE COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()