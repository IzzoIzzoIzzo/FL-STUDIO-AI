"""
MIDI PATTERN GENERATOR WITH VARIATIONS
=======================================
Generate patterns with structure: AABB, ABAB, ABCABC, etc.
Create motif variations, fills, and arrangements.
"""

import random
import struct
import os
from typing import List, Dict, Tuple


class MIDIPatternGenerator:
    """Generate MIDI patterns with variations"""
    
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.ticks_per_beat = 480
        self.ticks_per_bar = self.ticks_per_beat * 4
        
    def _note_to_midi(self, note: str) -> int:
        notes = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        note = note.upper()
        if note[0] in notes:
            octave = int(note[-1]) if note[-1].isdigit() else 4
            pitch = notes[note[0]] + (octave + 1) * 12
            if '#' in note:
                pitch += 1
            elif 'b' in note:
                pitch -= 1
            return pitch
        return 60
    
    def _create_note_on(self, channel: int, note: int, velocity: int, tick: int) -> bytes:
        return bytes([0x90 | channel, note, velocity, 0x90 | channel, note, 0])
    
    def _create_note_off(self, channel: int, note: int, tick: int) -> bytes:
        return bytes([0x80 | channel, note, 0])
    
    def _create_delta(self, ticks: int) -> bytes:
        result = []
        if ticks == 0:
            return bytes([0x00])
        while ticks > 0:
            chunk = ticks & 0x7F
            result.insert(0, chunk | (0x80 if ticks > 0x7F else 0))
            ticks >>= 7
        return bytes(result)
    
    def _varition_transform(self, pattern: List[Tuple[int, int, int]], variation_type: str) -> List[Tuple[int, int, int]]:
        """Apply variation to pattern"""
        if variation_type == 'none':
            return pattern
        elif variation_type == 'reverse':
            return list(reversed(pattern))
        elif variation_type == 'octave_up':
            return [(note + 12, vel, dur) for note, vel, dur in pattern]
        elif variation_type == 'octave_down':
            return [(max(0, note - 12), vel, dur) for note, vel, dur in pattern]
        elif variation_type == 'velocity_up':
            return [(note, min(127, vel + 20), dur) for note, vel, dur in pattern]
        elif variation_type == 'velocity_down':
            return [(note, max(20, vel - 20), dur) for note, vel, dur in pattern]
        elif variation_type == 'syncopate':
            result = []
            for note, vel, dur in pattern:
                result.append((note, vel, dur // 2))
                result.append((note, vel, dur // 2))
            return result
        elif variation_type == 'fill':
            return [(max(0, note + random.choice([-2, -1, 1, 2])), vel, dur // 2) for note, vel, dur in pattern]
        elif variation_type == 'staccato':
            return [(note, vel, dur // 4) for note, vel, dur in pattern]
        elif variation_type == 'legato':
            return [(note, vel, dur * 2) for note, vel, dur in pattern]
        return pattern
    
    def generate_motif(self, scale: List[int], root: int = 60, length: int = 4) -> List[Tuple[int, int, int]]:
        """Generate a melodic motif"""
        motif = []
        current_pos = 0
        for _ in range(length):
            note = root + random.choice(scale)
            duration = random.choice([120, 240, 480])
            velocity = random.randint(80, 120)
            motif.append((note, velocity, duration))
            current_pos += duration
        return motif
    
    def generate_drum_pattern(self, kit: str = '808') -> List[Tuple[int, int, int]]:
        """Generate drum pattern"""
        drums_808 = {
            'kick': 36, 'snare': 38, 'hh_closed': 46, 'hh_open': 46,
            'clap': 39, 'cowbell': 56, 'tom_low': 41, 'tom_high': 48
        }
        drums_909 = {
            'kick': 36, 'snare': 38, 'hh_closed': 46, 'hh_open': 44,
            'ride': 51, 'crash': 49, 'tom_low': 41, 'tom_high': 48
        }
        drums_acoustic = {
            'kick': 36, 'snare': 38, 'hh_closed': 42, 'hh_open': 46,
            'ride': 51, 'crash': 49, 'tom': 45, 'hihat': 22
        }
        
        kit_map = {'808': drums_808, '909': drums_909, 'acoustic': drums_acoustic}
        drums = kit_map.get(kit, drums_808)
        
        pattern = []
        beat = 480
        
        if kit == '808':
            pattern.extend([(drums['kick'], 100, beat), (0, 0, beat)])
            pattern.extend([(0, 0, beat), (drums['hh_closed'], 60, beat)])
            pattern.extend([(drums['kick'], 100, beat), (0, 0, beat)])
            pattern.extend([(drums['snare'], 90, beat), (drums['hh_closed'], 60, beat)])
        elif kit == '909':
            pattern.extend([(drums['kick'], 100, beat), (drums['hh_closed'], 60, beat)])
            pattern.extend([(drums['hh_open'], 40, beat), (0, 0, beat)])
            pattern.extend([(drums['kick'], 100, beat), (drums['hh_closed'], 60, beat)])
            pattern.extend([(drums['snare'], 90, beat), (drums['ride'], 50, beat)])
        else:
            pattern.extend([(drums['kick'], 100, beat), (drums['hihat'], 60, beat)])
            pattern.extend([(drums['hihat'], 40, beat), (0, 0, beat)])
            pattern.extend([(drums['kick'], 100, beat), (drums['hihat'], 60, beat)])
            pattern.extend([(drums['snare'], 90, beat), (drums['hihat'], 40, beat)])
        
        return pattern
    
    def generate_structure(self, structure: str, bar_length: int = 4) -> Dict[str, List[Tuple[int, int, int]]]:
        """Generate pattern with structure variations"""
        structures = {
            'simple': {'A': 1, 'B': 0},
            'verse': {'A': 4, 'B': 2},
            'chorus': {'A': 2, 'B': 2, 'C': 2},
            'bridge': {'A': 2, 'B': 2, 'C': 4},
            'complex': {'A': 2, 'B': 2, 'C': 2, 'D': 2},
            'rondo': {'A': 2, 'B': 2, 'A': 2, 'C': 2},
        }
        
        structure_map = structures.get(structure, structures['simple'])
        result = {}
        
        scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 5, 7, 10],
            'dorian': [0, 2, 3, 5, 7, 9, 10]
        }
        
        for pattern_name, count in structure_map.items():
            pattern = self.generate_motif(scales['major'], 60, bar_length)
            result[pattern_name] = pattern
        
        return result
    
    def generate_with_variations(self, base_pattern: List[Tuple[int, int, int]], 
                                 structure: str = 'AABB') -> Dict[str, List[Tuple[int, int, int]]]:
        """Generate pattern with specified variation structure"""
        variations = {
            'AABB': {'A': 'none', 'B': 'octave_up'},
            'ABAB': {'A': 'none', 'B': 'velocity_up'},
            'ABCABC': {'A': 'none', 'B': 'syncopate', 'C': 'fill'},
            'AAAB': {'A': 'none', 'B': 'fill'},
            'ABBA': {'A': 'none', 'B': 'reverse', 'A2': 'velocity_down'},
            'AABA': {'A': 'none', 'B': 'syncopate', 'A2': 'legato'},
        }
        
        var_map = variations.get(structure, variations['AABB'])
        result = {}
        
        for pattern_name, var_type in var_map.items():
            if pattern_name == 'A2':
                result['A2'] = self._varition_transform(base_pattern, 'velocity_down')
            else:
                result[pattern_name] = self._varition_transform(base_pattern, var_type)
        
        return result
    
    def export_midi(self, tracks: Dict[str, List[Tuple[int, int, int]]], filename: str):
        """Export to MIDI file"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        header = b'MThd' + struct.pack('>HHH', 0, 1, len(tracks))
        
        midi_data = header
        for track_name, pattern in tracks.items():
            track_data = bytearray()
            
            if 'drum' in track_name.lower():
                channel = 9
            else:
                channel = 0
            
            track_data.extend(b'\x00\xFF\x03\x00' + track_name.encode())
            
            current_tick = 0
            for note, velocity, duration in pattern:
                if note > 0:
                    if current_tick > 0:
                        track_data.extend(self._create_delta(current_tick))
                    track_data.extend(bytes([0x90 | channel, note, velocity]))
                    track_data.extend(self._create_delta(duration))
                    track_data.extend(bytes([0x80 | channel, note, 0]))
                    current_tick = 0
                else:
                    current_tick += duration
            
            track_data.extend(b'\x00\xFF\x2F\x00')
            
            track_header = b'MTrk' + struct.pack('>I', len(track_data))
            midi_data += track_header + bytes(track_data)
        
        with open(filename, 'wb') as f:
            f.write(midi_data)


def demo():
    print("=" * 60)
    print("  MIDI PATTERN GENERATOR WITH VARIATIONS")
    print("=" * 60)
    
    gen = MIDIPatternGenerator(bpm=128)
    
    print("\n[1] Generating drum pattern...")
    drums = gen.generate_drum_pattern('808')
    print(f"    Generated {len(drums)} drum hits")
    
    print("\n[2] Generating melodic motif...")
    motif = gen.generate_motif([0, 2, 4, 5, 7, 9, 11], 60, 4)
    print(f"    Generated motif with {len(motif)} notes")
    
    print("\n[3] Generating structure (AABB)...")
    structured = gen.generate_structure('verse', 4)
    print(f"    Created sections: {list(structured.keys())}")
    
    print("\n[4] Generating with variations (AABB)...")
    varied = gen.generate_with_variations(motif, 'ABCABC')
    print(f"    Created variations: {list(varied.keys())}")
    
    print("\n[5] Exporting to MIDI...")
    gen.export_midi({'melody': motif, 'drums': drums, 'variation_A': varied['A'], 'variation_B': varied.get('B', [])}, 
                    'exports/pattern_variations.mid')
    print("    Saved: exports/pattern_variations.mid")
    
    print("\n" + "=" * 60)
    print("  MIDI PATTERN GENERATOR READY!")
    print("=" * 60)


if __name__ == "__main__":
    demo()