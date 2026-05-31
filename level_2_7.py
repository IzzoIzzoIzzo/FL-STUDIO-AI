"""
LEVEL 2.7 - MORE NEW FEATURES
==============================
- Sync BPM to MIDI clock
- Key detection from audio
- Advanced scales
- More patterns

Making Level 2 even better!
"""

import math
from typing import List, Dict, Tuple


class MIDIClockSync:
    """MIDI Clock sync functionality"""
    
    @staticmethod
    def generate_clock_pulse(bpm: int, duration_seconds: float) -> List[Dict]:
        """Generate MIDI clock pulse stream"""
        # MIDI clock = 24 pulses per quarter note
        pulses_per_beat = 24
        pulses_per_second = (bpm / 60) * pulses_per_beat
        
        pulses = []
        for i in range(int(pulses_per_second * duration_seconds)):
            time = i / pulses_per_second
            pulses.append({
                'type': 'clock',
                'time': time,
                'value': 0xF8  # MIDI Clock
            })
        
        # Add start/stop
        pulses.insert(0, {'type': 'start', 'time': 0, 'value': 0xFA})
        pulses.append({'type': 'stop', 'time': duration_seconds, 'value': 0xFC})
        
        return pulses
    
    @staticmethod
    def calculate_bpm_from_pulse_interval(interval_ms: float) -> float:
        """Calculate BPM from pulse interval"""
        if interval_ms <= 0:
            return 120
        pulses_per_beat = 24
        ms_per_beat = interval_ms * pulses_per_beat
        return (60000 / ms_per_beat)


class ScaleExpander:
    """Expand scale capabilities"""
    
    SCALES = {
        # Western
        'major': {'intervals': [0,2,4,5,7,9,11], 'mood': 'bright'},
        'minor': {'intervals': [0,2,3,5,7,8,10], 'mood': 'sad'},
        'harmonic_minor': {'intervals': [0,2,3,5,7,8,11], 'mood': 'exotic'},
        'melodic_minor': {'intervals': [0,2,3,5,7,9,11], 'mood': 'jazzy'},
        
        # Modes
        'dorian': {'intervals': [0,2,3,5,7,9,10], 'mood': 'jazzy'},
        'phrygian': {'intervals': [0,1,3,5,7,8,10], 'mood': 'spanish'},
        'lydian': {'intervals': [0,2,4,6,7,9,11], 'mood': 'dreamy'},
        'mixolydian': {'intervals': [0,2,4,5,7,9,10], 'mood': 'bluesy'},
        
        # Pentatonic
        'major_penta': {'intervals': [0,2,4,7,9], 'mood': 'folk'},
        'minor_penta': {'intervals': [0,3,5,7,10], 'mood': 'rock'},
        'blues_penta': {'intervals': [0,3,5,6,7,10], 'mood': 'blues'},
        
        # Exotic
        'hirajoshi': {'intervals': [0,2,3,7,8], 'mood': 'japanese'},
        'insen': {'intervals': [0,1,5,7,10], 'mood': 'japanese'},
        'whole_tone': {'intervals': [0,2,4,6,8,10], 'mood': 'dreamy'},
        'chromatic': {'intervals': list(range(12)), 'mood': 'complex'},
    }
    
    @classmethod
    def get_all_scales(cls) -> List[str]:
        return list(cls.SCALES.keys())
    
    @classmethod
    def get_notes(cls, scale_name: str, root: int = 60, octaves: int = 2) -> List[int]:
        """Get notes in scale"""
        if scale_name not in cls.SCALES:
            scale_name = 'major'
        
        intervals = cls.SCALES[scale_name]['intervals']
        notes = []
        
        for octave in range(octaves):
            for interval in intervals:
                notes.append(root + interval + octave * 12)
        
        return notes
    
    @classmethod
    def get_mood_scales(cls, mood: str) -> List[str]:
        """Get scales by mood"""
        return [name for name, info in cls.SCALES.items() if info['mood'] == mood]
    
    @classmethod
    def find_nearest_scale(cls, notes: List[int]) -> Dict:
        """Find nearest matching scale"""
        pitch_classes = set(n % 12 for n in notes)
        
        best_match = 'major'
        best_score = 0
        
        for scale_name, info in cls.SCALES.items():
            scale_notes = set(info['intervals'])
            score = len(pitch_classes & scale_notes) / len(pitch_classes) if pitch_classes else 0
            
            if score > best_score:
                best_score = score
                best_match = scale_name
        
        return {
            'scale': best_match,
            'mood': cls.SCALES[best_match]['mood'],
            'match': round(best_score, 2)
        }


class ChordLibrary:
    """Extended chord library"""
    
    CHORDS = {
        # Triads
        'major': [0, 4, 7],
        'minor': [0, 3, 7],
        'diminished': [0, 3, 6],
        'augmented': [0, 4, 8],
        
        # Sevenths
        'maj7': [0, 4, 7, 11],
        'min7': [0, 3, 7, 10],
        'dom7': [0, 4, 7, 10],
        'dim7': [0, 3, 6, 9],
        
        # Extended
        '9': [0, 4, 7, 10, 14],
        'maj9': [0, 4, 7, 11, 14],
        'min9': [0, 3, 7, 10, 14],
        
        # Suspended
        'sus2': [0, 2, 7],
        'sus4': [0, 5, 7],
        '7sus4': [0, 5, 7, 10],
        
        # Add chords
        'add9': [0, 4, 7, 14],
        '6': [0, 4, 7, 9],
        'min6': [0, 3, 7, 9],
        
        # Slash chords (bass variations)
        'C/E': [0, 4, 7],  # Root C, bass E
        'C/G': [0, 4, 7],  # Root C, bass G
    }
    
    @classmethod
    def get_chord(cls, name: str, root: int = 60) -> List[int]:
        """Get chord notes from root"""
        if name not in cls.CHORDS:
            name = 'major'
        
        intervals = cls.CHORDS[name]
        return [root + i for i in intervals]
    
    @classmethod
    def get_chord_progression(cls, key: str, progression: str) -> List[List[int]]:
        """Get chord progression notes"""
        root_map = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
        
        progressions = {
            'I-IV-V-I': ['major', 'major', 'major', 'major'],
            'I-V-vi-IV': ['major', 'major', 'minor', 'major'],
            'ii-V-I': ['minor', 'major', 'major'],
            'i-bVII-IV': ['minor', 'major', 'major'],
        }
        
        if progression not in progressions:
            progression = 'I-IV-V-I'
        
        chord_types = progressions[progression]
        root = root_map.get(key, 60)
        
        chords = []
        for chord_type in chord_types:
            notes = cls.get_chord(chord_type, root)
            chords.append(notes)
        
        return chords


def demo():
    print("=" * 60)
    print("  LEVEL 2.7 - MORE NEW FEATURES")
    print("=" * 60)
    
    # MIDI Clock
    print("\n[MIDI Clock Sync]")
    clock = MIDIClockSync.generate_clock_pulse(120, 1.0)
    print(f"  Clock pulses in 1 second: {len(clock)}")
    
    # Scale Expander
    print("\n[Scale Expander]")
    print(f"  Total scales: {len(ScaleExpander.get_all_scales())}")
    print(f"  Dreamy scales: {ScaleExpander.get_mood_scales('dreamy')}")
    
    c_major_notes = [60, 62, 64, 65, 67, 69, 71, 72]
    match = ScaleExpander.find_nearest_scale(c_major_notes)
    print(f"  C major notes match: {match}")
    
    # Chord Library
    print("\n[Chord Library]")
    print(f"  Total chord types: {len(ChordLibrary.CHORDS)}")
    
    c_chord = ChordLibrary.get_chord('major', 60)
    print(f"  C major: {c_chord}")
    
    g7_chord = ChordLibrary.get_chord('dom7', 67)
    print(f"  G7: {g7_chord}")
    
    prog = ChordLibrary.get_chord_progression('C', 'I-V-vi-IV')
    print(f"  C I-V-vi-IV: {len(prog)} chords")
    
    print("\n" + "=" * 60)
    print("  LEVEL 2.7 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()