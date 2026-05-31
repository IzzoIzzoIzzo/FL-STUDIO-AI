"""
ENHANCED MELODIES V2 - Level 1.4 Upgrade
=========================================
- More musical scales
- Smart note selection
- Better rhythms
- Emotion-based generation
- Phrase generation

Building on what we have - making melodies better!
"""

import random
import math
from typing import List, Dict, Tuple, Optional


class MusicalScale:
    """Enhanced musical scales"""
    
    SCALES = {
        # Major scales
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
        'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
        
        # Pentatonic
        'major_penta': [0, 2, 4, 7, 9],
        'minor_penta': [0, 3, 5, 7, 10],
        'blues': [0, 3, 5, 6, 7, 10],
        
        # Exotic
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'phrygian': [0, 1, 3, 5, 7, 8, 10],
        'lydian': [0, 2, 4, 6, 7, 9, 11],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'locrian': [0, 1, 3, 5, 6, 8, 10],
        
        # Modes
        'ionian': [0, 2, 4, 5, 7, 9, 11],
        'aeolian': [0, 2, 3, 5, 7, 8, 10],
        
        # Other
        'whole_tone': [0, 2, 4, 6, 8, 10],
        'chromatic': list(range(12)),
        'japanese': [0, 1, 5, 7, 8],
        'spanish': [0, 1, 4, 5, 7, 8, 10],
        'hungarian': [0, 2, 3, 5, 6, 8, 10],
    }
    
    @classmethod
    def get_notes(cls, scale_name: str, root: int = 60, octaves: int = 2) -> List[int]:
        """Get notes in scale"""
        intervals = cls.SCALES.get(scale_name, cls.SCALES['major'])
        notes = []
        
        for octave in range(octaves):
            for interval in intervals:
                notes.append(root + interval + octave * 12)
        
        return notes
    
    @classmethod
    def get_chord_notes(cls, scale_name: str, root: int, chord_type: str) -> List[int]:
        """Get notes for chord in scale"""
        intervals = cls.SCALES.get(scale_name, cls.SCALES['major'])
        
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            '7': [0, 4, 7, 10],
            'maj7': [0, 4, 7, 11],
            'min7': [0, 3, 7, 10],
            'dim': [0, 3, 6],
            'aug': [0, 4, 8],
            'sus2': [0, 2, 7],
            'sus4': [0, 5, 7],
        }
        
        ints = chord_intervals.get(chord_type, [0, 4, 7])
        
        return [root + intervals[i % len(intervals)] + (i // len(intervals)) * 12 for i in ints]


class EmotionGenerator:
    """Generate melodies based on emotion"""
    
    EMOTION_PROFILES = {
        'happy': {
            'scale': 'major',
            'note_range': [60, 84],
            'rhythm_variation': 0.3,
            'note_density': 0.7,
            'direction': 'up',
            'skip_chance': 0.1,
        },
        'sad': {
            'scale': 'minor',
            'note_range': [48, 72],
            'rhythm_variation': 0.1,
            'note_density': 0.5,
            'direction': 'down',
            'skip_chance': 0.2,
        },
        'energetic': {
            'scale': 'major_penta',
            'note_range': [60, 96],
            'rhythm_variation': 0.6,
            'note_density': 0.9,
            'direction': 'up',
            'skip_chance': 0.05,
        },
        'calm': {
            'scale': 'dorian',
            'note_range': [48, 72],
            'rhythm_variation': 0.1,
            'note_density': 0.4,
            'direction': 'neutral',
            'skip_chance': 0.3,
        },
        'mysterious': {
            'scale': 'phrygian',
            'note_range': [48, 84],
            'rhythm_variation': 0.2,
            'note_density': 0.5,
            'direction': 'neutral',
            'skip_chance': 0.15,
        },
        'dark': {
            'scale': 'harmonic_minor',
            'note_range': [36, 72],
            'rhythm_variation': 0.3,
            'note_density': 0.6,
            'direction': 'down',
            'skip_chance': 0.1,
        },
        'dreamy': {
            'scale': 'lydian',
            'note_range': [48, 84],
            'rhythm_variation': 0.1,
            'note_density': 0.4,
            'direction': 'up',
            'skip_chance': 0.25,
        },
        'romantic': {
            'scale': 'major',
            'note_range': [48, 72],
            'rhythm_variation': 0.2,
            'note_density': 0.5,
            'direction': 'neutral',
            'skip_chance': 0.15,
        },
    }
    
    @classmethod
    def generate(cls, emotion: str, length: int = 16, root: int = 60) -> List[Dict]:
        """Generate melody based on emotion"""
        
        profile = cls.EMOTION_PROFILES.get(emotion, cls.EMOTION_PROFILES['happy'])
        scale_name = profile['scale']
        
        notes = MusicalScale.get_notes(scale_name, root)
        notes = [n for n in notes if profile['note_range'][0] <= n <= profile['note_range'][1]]
        
        melody = []
        current_note = random.choice(notes)
        
        for i in range(length):
            # Skip chance
            if random.random() < profile['skip_chance']:
                melody.append({'note': None, 'duration': 120, 'velocity': 0})
                continue
            
            # Note selection with direction bias
            if profile['direction'] == 'up':
                current_note = min(current_note + random.choice([-2, -1, 1, 2, 3]), profile['note_range'][1])
            elif profile['direction'] == 'down':
                current_note = max(current_note - random.choice([-3, -2, -1, 1, 2]), profile['note_range'][0])
            else:
                current_note = random.choice(notes)
            
            # Ensure note is in scale
            if current_note not in notes:
                current_note = random.choice(notes)
            
            # Duration with variation
            base_duration = 120
            dur = int(base_duration * (1 + random.uniform(-profile['rhythm_variation'], profile['rhythm_variation'])))
            
            velocity = int(80 + random.uniform(-10, 20))
            
            melody.append({
                'note': current_note,
                'duration': dur,
                'velocity': velocity
            })
        
        return melody


class PhraseGenerator:
    """Generate musical phrases"""
    
    @staticmethod
    def generate_phrase(root: int, scale: str, style: str = 'verse') -> List[Dict]:
        """Generate a complete phrase"""
        
        notes = MusicalScale.get_notes(scale, root)
        phrase = []
        
        if style == 'verse':
            # Build up, resolve
            pattern = [0, 2, 4, 5, 4, 2, 0]  # Scale degrees
            durations = [240, 120, 120, 240, 120, 120, 480]
            
            for deg, dur in zip(pattern, durations):
                if deg < len(notes):
                    phrase.append({'note': notes[deg], 'duration': dur, 'velocity': 90})
        
        elif style == 'chorus':
            # More energetic, repetitive
            pattern = [0, 2, 4, 7, 4, 2, 0, 4]
            durations = [120] * 8
            
            for deg, dur in zip(pattern, durations):
                if deg < len(notes):
                    phrase.append({'note': notes[deg], 'duration': dur, 'velocity': 95})
        
        elif style == 'bridge':
            # Dramatic, different
            pattern = [0, 1, 3, 5, 3, 1, 0]
            durations = [180, 120, 180, 360, 180, 120, 480]
            
            for deg, dur in zip(pattern, durations):
                if deg < len(notes):
                    phrase.append({'note': notes[deg], 'duration': dur, 'velocity': 85})
        
        return phrase
    
    @staticmethod
    def generate_call_response(part1: List[Dict], part2_notes: List[int]) -> List[Dict]:
        """Generate call and response"""
        
        response = []
        
        # Response should be different but related
        for note in part2_notes:
            response.append({'note': note, 'duration': 120, 'velocity': 85})
        
        return response


class EnhancedMelodyAI:
    """Complete enhanced melody generation"""
    
    SCALES = MusicalScale.SCALES
    EMOTIONS = list(EmotionGenerator.EMOTION_PROFILES.keys())
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def generate_simple(self, root: int, scale: str, length: int = 16) -> List[Dict]:
        """Simple melody generation"""
        
        notes = MusicalScale.get_notes(scale, root)
        melody = []
        
        current_note = root
        for _ in range(length):
            # Random walk through scale
            step = random.choice([-2, -1, 0, 1, 2])
            current_note = max(notes[0], min(notes[-1], current_note + step))
            
            if current_note not in notes:
                current_note = random.choice(notes)
            
            melody.append({
                'note': current_note,
                'duration': 120,
                'velocity': random.randint(70, 100)
            })
        
        return melody
    
    def generate_emotional(self, emotion: str, root: int = 60, length: int = 16) -> List[Dict]:
        """Generate emotion-based melody"""
        return EmotionGenerator.generate(emotion, length, root)
    
    def generate_phrase(self, root: int, scale: str, style: str = 'verse') -> List[Dict]:
        """Generate complete phrase"""
        return PhraseGenerator.generate_phrase(root, scale, style)
    
    def generate_full_melody(self, root: int, scale: str, 
                            emotion: str = 'happy', structure: str = 'simple') -> Dict:
        """Generate full structured melody"""
        
        if structure == 'simple':
            melody = self.generate_simple(root, scale)
        elif structure == 'emotional':
            melody = self.generate_emotional(emotion, root)
        else:
            # Structured: intro, verse, chorus, outro
            intro = self.generate_phrase(root, scale, 'bridge')
            verse = self.generate_phrase(root, scale, 'verse')
            chorus = self.generate_phrase(root, scale, 'chorus')
            outro = self.generate_phrase(root, scale, 'bridge')
            
            melody = intro + verse + chorus + chorus + outro
        
        return {
            'melody': melody,
            'root': root,
            'scale': scale,
            'emotion': emotion,
            'note_count': len(melody),
            'duration': sum(m.get('duration', 120) for m in melody) / 480  # in bars
        }


def demo():
    print("=" * 60)
    print("  ENHANCED MELODIES V2 - Level 1.4 Upgrade")
    print("=" * 60)
    
    ai = EnhancedMelodyAI()
    
    print("\n=== AVAILABLE SCALES ===")
    print(f"Total: {len(ai.SCALES)} scales")
    print(list(ai.SCALES.keys())[:10], "...")
    
    print("\n=== EMOTION PROFILES ===")
    print(ai.EMOTIONS)
    
    print("\n[TEST] Simple melody...")
    melody = ai.generate_simple(60, 'major', 8)
    print(f"    Generated {len(melody)} notes")
    
    print("\n[TEST] Emotional melody - happy...")
    melody = ai.generate_emotional('happy', 60, 8)
    print(f"    Generated {len(melody)} notes")
    
    print("\n[TEST] Emotional melody - dark...")
    melody = ai.generate_emotional('dark', 48, 8)
    print(f"    Generated {len(melody)} notes")
    
    print("\n[TEST] Phrase generation - verse...")
    phrase = ai.generate_phrase(60, 'minor', 'verse')
    print(f"    Generated {len(phrase)} notes")
    
    print("\n[TEST] Full structured melody...")
    full = ai.generate_full_melody(60, 'dorian', 'dreamy', 'structured')
    print(f"    Generated {full['note_count']} notes, {full['duration']:.1f} bars")
    
    print("\n" + "=" * 60)
    print("  MELODY V2 - Level 1.4 COMPLETE!")
    print("  Scales, Emotions, Phrases, Structure")
    print("=" * 60)


if __name__ == "__main__":
    demo()