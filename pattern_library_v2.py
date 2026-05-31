"""
PATTERN LIBRARY V2 - Level 2.6
===============================
- Extended drum patterns
- Bass patterns
- Chord progressions
- Melody sequences

Building on what we have - more patterns!
"""

from typing import List, Dict, Tuple


class PatternLibrary:
    """Complete pattern library"""
    
    # Drum patterns by style
    DRUM_PATTERNS = {
        'trap': [
            {'name': 'Basic Trap', 'pattern': [(36, 120, 120), (0, 0, 120), (36, 110, 120), (38, 100, 120), (0, 0, 120), (36, 115, 120), (0, 0, 120), (38, 95, 120)]},
            {'name': 'Hard Trap', 'pattern': [(36, 127, 60), (36, 120, 60), (46, 80, 120), (36, 125, 60), (46, 85, 60), (36, 127, 60), (38, 110, 120), (39, 100, 120)]},
            {'name': 'Trap Hi-Hats', 'pattern': [(46, 90, 60), (0, 0, 60), (46, 95, 60), (0, 0, 60), (46, 85, 60), (46, 80, 60), (46, 90, 60), (46, 100, 60)]},
        ],
        'house': [
            {'name': 'Four on Floor', 'pattern': [(36, 110, 120), (46, 60, 120), (38, 100, 120), (46, 70, 120)]},
            {'name': 'Tech House', 'pattern': [(36, 100, 120), (46, 50, 60), (0, 0, 60), (38, 90, 120), (46, 60, 60), (0, 0, 60)]},
            {'name': 'Deep House', 'pattern': [(36, 95, 240), (46, 60, 120), (38, 85, 240), (46, 70, 120)]},
        ],
        'hiphop': [
            {'name': 'Boom Bap', 'pattern': [(36, 100, 120), (0, 0, 120), (38, 90, 120), (0, 0, 120), (36, 95, 120), (0, 0, 240), (38, 85, 120)]},
            {'name': 'Trap Hop', 'pattern': [(36, 110, 60), (36, 105, 60), (46, 80, 120), (36, 115, 60), (38, 100, 120), (39, 90, 120)]},
        ],
        'dubstep': [
            {'name': 'Basic Dub', 'pattern': [(36, 120, 120), (0, 0, 120), (36, 110, 120), (0, 0, 120), (38, 100, 120), (0, 0, 120), (36, 115, 120), (38, 95, 120)]},
            {'name': 'Wobble', 'pattern': [(36, 120, 240), (46, 70, 120), (38, 100, 240), (46, 75, 120)]},
        ],
    }
    
    # Bass patterns
    BASS_PATTERNS = {
        'trap': [
            {'name': 'Trap Bass', 'notes': [36, 36, 38, 36, 36, 36, 41, 36], 'durations': [120]*8},
            {'name': '808 Bass', 'notes': [36, 0, 36, 0, 36, 0, 41, 43], 'durations': [120]*8},
        ],
        'house': [
            {'name': 'Walking Bass', 'notes': [36, 38, 41, 43, 44, 43, 41, 38], 'durations': [120]*8},
            {'name': 'House Bass', 'notes': [36, 0, 36, 38, 0, 38, 36, 0], 'durations': [120]*8},
        ],
        'hiphop': [
            {'name': 'Boom Bass', 'notes': [36, 0, 38, 0, 36, 0, 0, 0], 'durations': [240, 120, 240, 120, 240, 120, 240, 240]},
        ],
    }
    
    # Chord progressions
    CHORD_PROGRESSIONS = {
        'pop': [
            {'name': 'I-V-vi-IV', 'chords': ['C', 'G', 'Am', 'F'], 'duration': 4},
            {'name': 'ii-V-I', 'chords': ['Dm', 'G', 'C'], 'duration': 4},
            {'name': 'I-IV-V-I', 'chords': ['C', 'F', 'G', 'C'], 'duration': 4},
        ],
        'minor': [
            {'name': 'i-bVII-IV', 'chords': ['Am', 'G', 'F'], 'duration': 4},
            {'name': 'i-iv-v-i', 'chords': ['Am', 'Dm', 'E', 'Am'], 'duration': 4},
            {'name': 'i-VI-III-VII', 'chords': ['Am', 'F', 'E', 'G'], 'duration': 4},
        ],
        'jazz': [
            {'name': 'ii-V-I', 'chords': ['Dm7', 'G7', 'Cmaj7'], 'duration': 4},
            {'name': 'I-vi-ii-V', 'chords': ['Cmaj7', 'Am7', 'Dm7', 'G7'], 'duration': 4},
        ],
    }
    
    # Melody sequences
    MELODY_TEMPLATES = {
        'happy': [0, 4, 7, 12, 7, 4, 0, 4],
        'sad': [0, -3, -5, -3, 0, 2, 0, -3],
        'build': [0, 4, 7, 12, 14, 12, 7, 12],
        'drop': [12, 14, 12, 7, 4, 7, 0, -2],
    }
    
    @classmethod
    def get_drum_pattern(cls, style: str, name: str = None) -> Dict:
        """Get drum pattern"""
        patterns = cls.DRUM_PATTERNS.get(style, cls.DRUM_PATTERNS['trap'])
        if name:
            for p in patterns:
                if p['name'] == name:
                    return p
        return random.choice(patterns) if patterns else {'name': 'default', 'pattern': []}
    
    @classmethod
    def get_bass_pattern(cls, style: str) -> Dict:
        """Get bass pattern"""
        return cls.BASS_PATTERNS.get(style, cls.BASS_PATTERNS['trap'])[0]
    
    @classmethod
    def get_chord_progression(cls, genre: str, name: str = None) -> Dict:
        """Get chord progression"""
        progressions = cls.CHORD_PROGRESSIONS.get(genre, cls.CHORD_PROGRESSIONS['pop'])
        if name:
            for p in progressions:
                if p['name'] == name:
                    return p
        return random.choice(progressions) if progressions else {'name': 'default', 'chords': ['C'], 'duration': 4}
    
    @classmethod
    def get_melody_template(cls, mood: str) -> List[int]:
        """Get melody template"""
        return cls.MELODY_TEMPLATES.get(mood, cls.MELODY_TEMPLATES['happy'])


# Need random
import random


class StyleMixer:
    """Mix styles together"""
    
    @staticmethod
    def create_hybrid(drum_style: str, bass_style: str, melody_mood: str) -> Dict:
        """Create hybrid track from multiple styles"""
        
        drums = PatternLibrary.get_drum_pattern(drum_style)
        bass = PatternLibrary.get_bass_pattern(bass_style)
        melody = PatternLibrary.get_melody_template(melody_mood)
        
        return {
            'drums': drums,
            'bass': bass,
            'melody': melody,
            'style': f"{drum_style}_{bass_style}_hybrid"
        }
    
    @staticmethod
    def random_hybrid() -> Dict:
        """Create random hybrid"""
        drum_styles = list(PatternLibrary.DRUM_PATTERNS.keys())
        bass_styles = list(PatternLibrary.BASS_PATTERNS.keys())
        moods = list(PatternLibrary.MELODY_TEMPLATES.keys())
        
        return StyleMixer.create_hybrid(
            random.choice(drum_styles),
            random.choice(bass_styles),
            random.choice(moods)
        )


def demo():
    print("=" * 60)
    print("  PATTERN LIBRARY V2 - Level 2.6")
    print("=" * 60)
    
    print("\n=== DRUM PATTERNS ===")
    for style in PatternLibrary.DRUM_PATTERNS:
        print(f"  {style}: {len(PatternLibrary.DRUM_PATTERNS[style])} patterns")
    
    print("\n=== BASS PATTERNS ===")
    for style in PatternLibrary.BASS_PATTERNS:
        print(f"  {style}: {len(PatternLibrary.BASS_PATTERNS[style])} patterns")
    
    print("\n=== CHORD PROGRESSIONS ===")
    for genre in PatternLibrary.CHORD_PROGRESSIONS:
        print(f"  {genre}: {len(PatternLibrary.CHORD_PROGRESSIONS[genre])} progressions")
    
    print("\n[TEST] Get trap drum pattern...")
    trap = PatternLibrary.get_drum_pattern('trap')
    print(f"    {trap['name']}")
    
    print("\n[TEST] Get house bass pattern...")
    house_bass = PatternLibrary.get_bass_pattern('house')
    print(f"    {house_bass['name']}")
    
    print("\n[TEST] Get pop chord progression...")
    pop = PatternLibrary.get_chord_progression('pop')
    print(f"    {pop['name']}: {pop['chords']}")
    
    print("\n[TEST] Create hybrid...")
    hybrid = StyleMixer.create_hybrid('trap', 'house', 'build')
    print(f"    Style: {hybrid['style']}")
    
    print("\n[TEST] Random hybrid...")
    rand = StyleMixer.random_hybrid()
    print(f"    Style: {rand['style']}")
    
    print("\n" + "=" * 60)
    print("  PATTERN LIBRARY V2 - Level 2.6 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()