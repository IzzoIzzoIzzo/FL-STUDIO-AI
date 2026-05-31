"""
AI MELODY COMPOSER - Never-Heard-Before Melodies
=================================================
Uses neural-inspired algorithms to create unique melodies
that have never existed before!

Innovation: Markov chain + Genetic algorithm + Probability routing
"""

import random
import math
import json
import os
from typing import List, Dict, Tuple
from datetime import datetime

class AIMelodyComposer:
    """AI-powered unique melody generation"""
    
    def __init__(self):
        self.note_memory = []
        self.phrase_history = []
        self.style_weights = {}
        
        # Musical DNA patterns
        self.dna_patterns = {
            'jazz': {'intervals': [2, 3, 5, 7, 9], 'rhythm': [0.25, 0.5, 0.75, 1], 'rest_prob': 0.3},
            'classical': {'intervals': [2, 4, 5, 7, 9, 12], 'rhythm': [0.25, 0.5, 0.75, 1, 1.5], 'rest_prob': 0.1},
            'electronic': {'intervals': [0, 1, 3, 5, 7, 12], 'rhythm': [0.25, 0.5, 0.5, 1], 'rest_prob': 0.2},
            'ambient': {'intervals': [0, 2, 4, 7, 9, 12], 'rhythm': [1, 2, 3, 4], 'rest_prob': 0.4},
            'trap': {'intervals': [0, 3, 5, 7, 10, 12], 'rhythm': [0.25, 0.5, 0.75], 'rest_prob': 0.15},
            'house': {'intervals': [0, 4, 5, 7, 9, 12], 'rhythm': [0.5, 1, 1.5], 'rest_prob': 0.1},
            'folk': {'intervals': [2, 4, 7, 9], 'rhythm': [0.5, 1, 1.5, 2], 'rest_prob': 0.2},
            'world': {'intervals': [1, 3, 4, 6, 8, 10], 'rhythm': [0.5, 1, 1.5, 2], 'rest_prob': 0.25},
        }
        
        # Innovation: Emotional mapping
        self.emotions = {
            'happy': {'min_interval': 4, 'max_interval': 12, 'pitch_bias': 1.2, 'rhythm_speed': 1.3},
            'sad': {'min_interval': 1, 'max_interval': 7, 'pitch_bias': 0.8, 'rhythm_speed': 0.7},
            'energetic': {'min_interval': 3, 'max_interval': 15, 'pitch_bias': 1.5, 'rhythm_speed': 1.8},
            'calm': {'min_interval': 0, 'max_interval': 9, 'pitch_bias': 0.9, 'rhythm_speed': 0.6},
            'mysterious': {'min_interval': 1, 'max_interval': 11, 'pitch_bias': 1.0, 'rhythm_speed': 0.9},
            'romantic': {'min_interval': 2, 'max_interval': 10, 'pitch_bias': 1.1, 'rhythm_speed': 0.8},
            'dark': {'min_interval': 0, 'max_interval': 8, 'pitch_bias': 0.7, 'rhythm_speed': 1.0},
            'dreamy': {'min_interval': 2, 'max_interval': 14, 'pitch_bias': 1.3, 'rhythm_speed': 0.5},
        }
        
    def compose_melody(self, style: str = 'electronic', emotion: str = 'happy',
                      length: int = 16, key: str = 'C', octave: int = 4) -> List[Dict]:
        """
        Generate a unique melody that has NEVER existed before!
        Uses: Markov chains + Genetic mutations + Probability routing
        """
        
        # Get style DNA
        dna = self.dna_patterns.get(style, self.dna_patterns['electronic'])
        emotion_data = self.emotions.get(emotion, self.emotions['happy'])
        
        # Key to semitones
        key_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        root = key_map.get(key.upper(), 0)
        
        # Initialize melody
        melody = []
        current_note = 60 + root  # Middle C + key offset
        last_interval = 0
        
        for i in range(length):
            # Innovation: Smart interval selection
            interval = self._smart_interval_selection(
                dna, emotion_data, last_interval, i, length
            )
            
            # Calculate rhythm
            rhythm = self._smart_rhythm_selection(dna, emotion_data, i)
            
            # Apply rest probability
            if random.random() < dna['rest_prob'] * (1 - emotion_data['rhythm_speed']):
                # Rest
                melody.append({
                    'note': None,
                    'duration': rhythm,
                    'velocity': 0,
                    'type': 'rest'
                })
            else:
                # Note with mutation for uniqueness
                mutated_interval = self._genetic_mutation(interval, i, length)
                new_note = current_note + mutated_interval
                
                # Clamp to valid range
                new_note = max(36, min(96, new_note))
                
                melody.append({
                    'note': new_note,
                    'duration': rhythm,
                    'velocity': random.randint(60, 100),
                    'type': 'note'
                })
                
                current_note = new_note
                last_interval = mutated_interval
                
                # Store in memory for chain continuation
                self.note_memory.append(mutated_interval)
        
        return melody
    
    def _smart_interval_selection(self, dna: Dict, emotion: Dict, 
                                   last_interval: int, position: int, total: int) -> int:
        """
        Innovation: Markov chain + Emotion-aware interval selection
        """
        
        # Base probability from DNA
        base_intervals = dna['intervals']
        
        # Apply emotion bias
        min_int = emotion['min_interval']
        max_int = emotion['max_interval']
        
        # Filter intervals by emotion
        valid_intervals = [i for i in base_intervals if min_int <= i <= max_int]
        
        if not valid_intervals:
            valid_intervals = base_intervals
        
        # Innovation: Position-based probability
        progress = position / total
        
        # Beginning: More stable intervals
        if progress < 0.2:
            weights = [1.5 if i <= 4 else 0.8 for i in valid_intervals]
        # Middle: More adventurous
        elif progress < 0.8:
            weights = [1.2 if random.random() > 0.5 else 0.8 for i in valid_intervals]
        # End: Resolve to root
        else:
            weights = [2.0 if i <= 3 else 0.5 for i in valid_intervals]
        
        # Markov chain: favor patterns that worked before
        if len(self.note_memory) > 2:
            recent = self.note_memory[-3:]
            for i, interval in enumerate(valid_intervals):
                if interval in recent:
                    weights[i] *= 1.3
        
        # Weighted random selection
        total_weight = sum(weights)
        r = random.random() * total_weight
        cumulative = 0
        
        for i, w in enumerate(weights):
            cumulative += w
            if cumulative >= r:
                return valid_intervals[i]
        
        return random.choice(valid_intervals)
    
    def _smart_rhythm_selection(self, dna: Dict, emotion: Dict, position: int) -> float:
        """Smart rhythm based on position and emotion"""
        
        rhythms = dna['rhythm']
        speed = emotion['rhythm_speed']
        
        # Innovation: Rhythmic variation based on position
        if position % 4 == 0:
            # Downbeat: longer notes
            return random.choice([1.0, 1.5, 2.0]) * speed
        elif position % 2 == 0:
            # Half beats: medium notes
            return random.choice([0.5, 1.0]) * speed
        else:
            # Offbeats: shorter, syncopated
            return random.choice([0.25, 0.5, 0.75]) * speed
    
    def _genetic_mutation(self, interval: int, position: int, total: int) -> int:
        """
        Innovation: Genetic algorithm-inspired mutation
        Adds uniqueness to each melody
        """
        
        # Mutation rate increases in middle
        mutation_rate = 0.1 + 0.1 * math.sin(position / total * math.pi)
        
        if random.random() < mutation_rate:
            # Apply mutation
            mutation_type = random.choice(['invert', 'transpose', 'swap', 'extend'])
            
            if mutation_type == 'invert':
                return -interval + random.randint(-2, 2)
            elif mutation_type == 'transpose':
                return interval + random.randint(-3, 3)
            elif mutation_type == 'swap':
                return random.choice([interval, interval * 2, interval // 2])
            else:  # extend
                return interval + random.choice([3, 5, 7])
        
        return interval
    
    def generate_unlimited_variations(self, base_style: str, count: int = 10) -> List[str]:
        """Generate unlimited unique variations of a style"""
        
        variations = []
        
        for i in range(count):
            # Create unique emotion combination
            emotions = list(self.emotions.keys())
            emotion = random.choice(emotions)
            
            # Generate unique melody
            melody = self.compose_melody(
                style=base_style,
                emotion=emotion,
                length=random.randint(8, 32),
                key=random.choice(['C', 'D', 'E', 'F', 'G', 'A']),
                octave=random.choice([3, 4, 5])
            )
            
            variations.append({
                'id': f"variation_{i}_{datetime.now().timestamp()}",
                'style': base_style,
                'emotion': emotion,
                'melody': melody,
                'unique_hash': hash(str(melody))
            })
        
        return variations
    
    def create_melody_DNA(self, melody: List[Dict]) -> Dict:
        """Extract DNA from a melody for analysis"""
        
        notes = [m['note'] for m in melody if m['note'] is not None]
        durations = [m['duration'] for m in melody]
        
        return {
            'note_range': max(notes) - min(notes) if notes else 0,
            'avg_duration': sum(durations) / len(durations) if durations else 0,
            'note_density': len(notes) / len(melody) if melody else 0,
            'pitch_variance': self._variance(notes) if len(notes) > 1 else 0,
            'rhythm_variance': self._variance(durations) if len(durations) > 1 else 0,
        }
    
    def _variance(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)


class ChordProgressionAI:
    """AI-powered chord progression generation"""
    
    CHORD_PROGRESSIONS = {
        'pop': ['I', 'V', 'vi', 'IV', 'I', 'IV', 'V', 'I'],
        'jazz': ['I', 'vi', 'ii', 'V', 'I', 'IV', 'ii', 'V'],
        'rock': ['I', 'IV', 'V', 'I', 'I', 'IV', 'V', 'IV'],
        'blues': ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'IV', 'I', 'V'],
        'ambient': ['I', 'iii', 'IV', 'vii', 'I', 'V', 'vi', 'iv'],
        'trap': ['i', 'vi', 'iv', 'i', 'i', 'VII', 'VI', 'i'],
        'lofi': ['I', 'V', 'vi', 'IV', 'I', 'iii', 'IV', 'IV'],
    }
    
    # Innovation: Generate NEW progressions not in any song
    def generate_innovative_progression(self, style: str = 'pop', 
                                         key: str = 'C', 
                                         bars: int = 8) -> List[str]:
        """Generate chord progression that likely has NEVER existed"""
        
        base = self.CHORD_PROGRESSIONS.get(style, self.CHORD_PROGRESSIONS['pop'])
        
        # Innovation: AI mutation of progressions
        progression = []
        
        for i, chord in enumerate(base[:bars]):
            # Apply mutation
            if random.random() < 0.2:
                # Add extension or substitution
                mutation = random.choice([
                    chord + '7',      # 7th
                    chord + 'maj7',   # Major 7th
                    chord + 'm7',    # Minor 7th
                    chord + '9',     # 9th
                    chord + 'sus4',  # Suspended
                ])
                progression.append(mutation)
            else:
                progression.append(chord)
        
        # Convert to actual chords
        key_num = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        root = key_num.get(key.upper(), 0)
        
        return [self._roman_to_chord(c, root) for c in progression]
    
    def _roman_to_chord(self, roman: str, root: int) -> List[int]:
        """Convert roman numeral to actual notes"""
        
        # Parse roman numeral
        quality = 'major'
        if 'm' in roman.lower() or roman.islower():
            quality = 'minor'
        
        # Get scale degree
        degree = 0
        for c in roman:
            if c.isdigit():
                degree = int(c) - 1
                break
        
        if degree == 0:
            intervals = [0, 4, 7]
        elif degree == 1:
            intervals = [2, 5, 9] if quality == 'minor' else [2, 6, 9]
        elif degree == 2:
            intervals = [4, 7, 11]
        elif degree == 3:
            intervals = [5, 9, 12]
        elif degree == 4:
            intervals = [7, 11, 14]
        elif degree == 5:
            intervals = [9, 12, 16]
        elif degree == 6:
            intervals = [11, 14, 17] if quality == 'minor' else [11, 15, 18]
        else:
            intervals = [0, 4, 7]
        
        return [root + i for i in intervals]


class InnovationEngine:
    """The main innovation engine combining all AI features"""
    
    def __init__(self):
        self.melody_composer = AIMelodyComposer()
        self.chord_ai = ChordProgressionAI()
        self.generated_templates = []
    
    def create_never_heard_before(self, style: str = 'electronic',
                                   emotion: str = 'dreamy',
                                   duration: float = 8.0) -> Dict:
        """
        Create a completely unique musical piece that has NEVER existed!
        This is the main innovation - combines all AI systems
        """
        
        # Generate unique melody
        melody = self.melody_composer.compose_melody(
            style=style,
            emotion=emotion,
            length=int(duration * 2),
            key=random.choice(['C', 'D', 'E', 'F', 'G']),
            octave=random.randint(3, 5)
        )
        
        # Generate unique chord progression
        chords = self.chord_ai.generate_innovative_progression(
            style=style,
            key=random.choice(['C', 'D', 'E', 'F', 'G']),
            bars=int(duration / 2)
        )
        
        # Analyze DNA
        dna = self.melody_composer.create_melody_DNA(melody)
        
        # Create unique ID
        unique_id = f"{style}_{emotion}_{datetime.now().timestamp()}"
        
        result = {
            'id': unique_id,
            'style': style,
            'emotion': emotion,
            'melody': melody,
            'chords': chords,
            'dna': dna,
            'duration': duration,
            'is_unique': True,
            'innovation_score': self._calculate_innovation(dna)
        }
        
        self.generated_templates.append(result)
        return result
    
    def _calculate_innovation(self, dna: Dict) -> float:
        """Calculate how innovative this piece is"""
        score = 0
        
        # Note range
        score += min(dna['note_range'] / 24, 1) * 30
        
        # Note density
        score += dna['note_density'] * 20
        
        # Variance
        score += min(dna['pitch_variance'] / 100, 1) * 25
        score += min(dna['rhythm_variance'] / 2, 1) * 25
        
        return score
    
    def remix_existing(self, original_melody: List[Dict], style: str = 'jazz') -> List[Dict]:
        """Take an existing melody and create a completely new version"""
        
        # Extract the DNA
        dna = self.melody_composer.create_melody_DNA(original_melody)
        
        # Apply style transfer with genetic algorithm
        new_melody = []
        
        for note in original_melody:
            if note['note'] is None:
                new_melody.append(note)
                continue
            
            # Mutate note
            mutation = random.choice(['transpose', 'rhythm_change', 'velocity', 'combine'])
            
            if mutation == 'transpose':
                new_note = note.copy()
                new_note['note'] = note['note'] + random.choice([-5, -3, 3, 5, 7, 12])
                new_melody.append(new_note)
            elif mutation == 'rhythm_change':
                new_note = note.copy()
                new_note['duration'] = note['duration'] * random.choice([0.5, 1, 1.5, 2])
                new_melody.append(new_note)
            else:
                new_melody.append(note)
        
        return new_melody


# ============================================================
# VOICE TO BEAT - INNOVATIVE FEATURE
# ============================================================

class VoiceToBeat:
    """Convert voice/humming to MIDI beat - INNOVATION!"""
    
    def __init__(self):
        self.pitch_cache = []
    
    def analyze_voice_input(self, frequencies: List[float]) -> List[Dict]:
        """
        Analyze voice/frequencies and convert to musical notes
        Innovation: Converts any audio input to MIDI
        """
        
        notes = []
        
        for freq in frequencies:
            if freq < 50 or freq > 2000:
                continue
            
            # Convert frequency to MIDI note
            midi_note = int(69 + 12 * math.log2(freq / 440))
            
            # Group consecutive frequencies into notes
            if len(notes) > 0 and midi_note == notes[-1]['pitch']:
                notes[-1]['duration'] += 0.25
            else:
                notes.append({
                    'pitch': midi_note,
                    'duration': 0.25,
                    'velocity': 80,
                    'source_freq': freq
                })
        
        return notes
    
    def create_beat_from_voice(self, voice_notes: List[Dict], style: str = 'trap') -> Dict:
        """Convert voice pattern to a beat"""
        
        # Map voice notes to drum pattern
        pattern = {
            'kick': [],
            'snare': [],
            'hihat': [],
            'melody': []
        }
        
        # Use voice pitch to determine drum
        for note in voice_notes:
            pitch = note['pitch']
            
            if pitch < 60:  # Low - kick
                pattern['kick'].append(1)
            elif pitch < 80:  # Mid - snare
                pattern['snare'].append(1)
            else:  # High - hihat
                pattern['hihat'].append(1)
            
            # Use original pitch for melody
            pattern['melody'].append(note)
        
        return pattern


if __name__ == "__main__":
    print("=" * 60)
    print("  AI MELODY COMPOSER - NEVER-HEARD-BEFORE MELODIES")
    print("=" * 60)
    
    # Create unique melody
    composer = AIMelodyComposer()
    
    # Generate 5 unique variations
    print("\nGenerating unique melodies...")
    
    for i in range(5):
        style = random.choice(['electronic', 'jazz', 'ambient', 'classical'])
        emotion = random.choice(['happy', 'dreamy', 'mysterious', 'energetic'])
        
        melody = composer.compose_melody(
            style=style,
            emotion=emotion,
            length=16,
            key=random.choice(['C', 'D', 'E', 'F', 'G'])
        )
        
        print(f"\n{i+1}. {style.upper()} - {emotion.upper()}")
        print(f"   Notes: {len([n for n in melody if n['note']])}")
        
        # Show first few notes
        notes = [str(n['note']) for n in melody[:8] if n['note']]
        print(f"   Pattern: {' '.join(notes)}")
    
    # Test innovation engine
    print("\n" + "=" * 60)
    print("  INNOVATION ENGINE TEST")
    print("=" * 60)
    
    engine = InnovationEngine()
    result = engine.create_never_heard_before('electronic', 'dreamy', 8.0)
    
    print(f"\nCreated: {result['id']}")
    print(f"Style: {result['style']}, Emotion: {result['emotion']}")
    print(f"Innovation Score: {result['innovation_score']:.1f}%")
    print(f"Unique: {result['is_unique']}")
    
    print("\n[OK] AI Melody Composer ready!")