"""
ARPEGGIATOR PRO V2 - Level 2.1
===============================
- Advanced arpeggio patterns
- Chord-to-arp conversion
- Swing control
- Octave ranges

Building on what we have - adding more musical tools!
"""

import random
from typing import List, Dict, Tuple, Optional


class ArpPattern:
    """Arpeggio patterns"""
    
    PATTERNS = {
        'up': [0, 1, 2, 3, 2, 1],
        'down': [3, 2, 1, 0, 1, 2],
        'updown': [0, 1, 2, 3, 2, 1, 0],
        'up_octave': [0, 1, 2, 3, 4, 5, 6, 7],
        'down_octave': [7, 6, 5, 4, 3, 2, 1, 0],
        'random': [0, 2, 1, 3, 0, 2, 1, 3],
        'alley': [0, 0, 1, 1, 2, 2, 3, 3],
        'alley_rev': [3, 3, 2, 2, 1, 1, 0, 0],
        'cascade': [0, 1, 2, 3, 2, 1, 0, 1],
        'quantum': [0, 2, 4, 5, 4, 2, 0, 3],
    }
    
    @classmethod
    def get(cls, name: str) -> List[int]:
        return cls.PATTERNS.get(name, cls.PATTERNS['up'])


class ArpPro:
    """Professional arpeggiator"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.rate = 120  # BPM
        self.pattern = 'up'
        self.octave_range = 1
        self.swing = 0.0
        self.gate = 1.0  # 100%
        self.hold = False
    
    def set_rate(self, bpm: int):
        self.rate = max(30, min(300, bpm))
    
    def set_pattern(self, pattern: str):
        if pattern in ArpPattern.PATTERNS:
            self.pattern = pattern
    
    def generate_from_notes(self, notes: List[int], duration: float = 4.0) -> List[Dict]:
        """Generate arpeggio from notes"""
        
        pattern = ArpPattern.get(self.pattern)
        beat_duration = 60.0 / self.rate
        notes_per_beat = 4  # 16th notes
        
        arp_notes = []
        current_beat = 0
        current_bar = 0
        
        # Expand pattern across octaves if needed
        expanded_pattern = []
        for step in pattern:
            for oct in range(self.octave_range):
                expanded_pattern.append(step + oct * 12)
        
        # Add repeat pattern
        pattern_repeated = expanded_pattern * 4
        
        total_steps = int(duration / beat_duration * notes_per_beat)
        
        for i in range(total_steps):
            pattern_idx = i % len(pattern_repeated)
            note_offset = pattern_repeated[pattern_idx]
            
            # Get base note from chord
            if notes:
                base_note = notes[pattern_idx % len(notes)]
                note = base_note + note_offset
                
                # Calculate timing with swing
                beat_pos = i % notes_per_beat
                if beat_pos % 2 == 1 and self.swing > 0:
                    timing = beat_duration / notes_per_beat * (1 + self.swing)
                else:
                    timing = beat_duration / notes_per_beat
                
                # Apply gate
                duration = timing * self.gate
                
                # Velocity with variation
                velocity = random.randint(80, 100)
                
                arp_notes.append({
                    'note': note,
                    'timing': i * (beat_duration / notes_per_beat),
                    'duration': duration,
                    'velocity': velocity
                })
        
        return arp_notes
    
    def generate_from_chord(self, root: int, chord_type: str, duration: float = 4.0) -> List[Dict]:
        """Generate arpeggio from chord"""
        
        # Chord intervals
        chords = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            '7th': [0, 4, 7, 10],
            'maj7': [0, 4, 7, 11],
            'min7': [0, 3, 7, 10],
            'dim': [0, 3, 6],
            'aug': [0, 4, 8],
            'sus2': [0, 2, 7],
            'sus4': [0, 5, 7],
        }
        
        intervals = chords.get(chord_type, [0, 4, 7])
        notes = [root + i for i in intervals]
        
        return self.generate_from_notes(notes, duration)


class ChordToArp:
    """Convert chord progressions to arpeggios"""
    
    @staticmethod
    def progression_to_arp(root: int, progression: List[str], 
                          scale: str = 'major', 
                          duration_per_chord: float = 4.0) -> List[Dict]:
        """Convert chord progression to arp"""
        
        # Chord to interval mapping
        chord_map = {
            'I': [0, 4, 7], 'ii': [0, 3, 7], 'iii': [0, 4, 7],
            'IV': [0, 5, 7], 'V': [0, 4, 7], 'vi': [0, 3, 7], 'vii': [0, 3, 6],
            'I7': [0, 4, 7, 10], 'V7': [0, 4, 7, 10],
        }
        
        arp = ArpPro()
        all_notes = []
        
        # Map scale to notes
        scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
        }
        
        intervals = scales.get(scale, scales['major'])
        
        for chord_symbol in progression:
            # Get intervals
            if chord_symbol in chord_map:
                chord_intervals = chord_map[chord_symbol]
            else:
                chord_intervals = [0, 4, 7]
            
            # Convert to actual notes
            notes = [root + intervals[i % len(intervals)] + (i // len(intervals)) * 12 
                    for i in chord_intervals]
            
            # Generate arp for this chord
            chord_arp = arp.generate_from_notes(notes, duration_per_chord)
            all_notes.extend(chord_arp)
        
        return all_notes


def demo():
    print("=" * 60)
    print("  ARPEGGIATOR PRO V2 - Level 2.1")
    print("=" * 60)
    
    arp = ArpPro()
    
    print("\n=== PATTERNS ===")
    print(list(ArpPattern.PATTERNS.keys()))
    
    print("\n[TEST] Simple arp from notes...")
    notes = [60, 64, 67]  # C major triad
    arp.set_pattern('up')
    result = arp.generate_from_notes(notes, 2.0)
    print(f"    Generated {len(result)} arp notes")
    print(f"    First note: MIDI {result[0]['note']}")
    
    print("\n[TEST] Down octave pattern...")
    arp.set_pattern('down_octave')
    arp.octave_range = 2
    result = arp.generate_from_notes(notes, 2.0)
    print(f"    Generated {len(result)} arp notes")
    
    print("\n[TEST] Chord to arp...")
    arp.set_pattern('updown')
    chord_arp = arp.generate_from_chord(60, 'major', 4.0)
    print(f"    Generated {len(chord_arp)} notes")
    
    print("\n[TEST] Chord progression to arp...")
    progression = ['I', 'V', 'vi', 'IV']
    prog_arp = ChordToArp.progression_to_arp(60, progression, 'major', 2.0)
    print(f"    Generated {len(prog_arp)} notes from {len(progression)} chords")
    
    print("\n" + "=" * 60)
    print("  ARPEGGIATOR PRO V2 - Level 2.1 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()