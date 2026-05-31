"""
ENHANCED DRUMS V3 - Professional Drum Machine
=============================================
Multiple drum kits, patterns by genre, humanization, fills, swing
"""

import random
import math
from typing import List, Dict


class DrumKitV3:
    """Multiple drum kits"""
    
    KITS = {
        'trap': {
            'kick': {'note': 36, 'pitch': 45, 'decay': 0.3},
            'snare': {'note': 38, 'pitch': 200, 'decay': 0.2},
            'hihat': {'note': 42, 'pitch': 8000, 'decay': 0.05},
            'openhihat': {'note': 46, 'pitch': 6000, 'decay': 0.3},
            'clap': {'note': 39, 'pitch': 1500, 'decay': 0.15},
            'rim': {'note': 37, 'pitch': 500, 'decay': 0.05},
            '808sub': {'note': 36, 'pitch': 30, 'decay': 0.5},
            'fx': {'note': 50, 'pitch': 1000, 'decay': 0.2}
        },
        'house': {
            'kick': {'note': 36, 'pitch': 55, 'decay': 0.25},
            'snare': {'note': 38, 'pitch': 180, 'decay': 0.2},
            'hihat': {'note': 42, 'pitch': 9000, 'decay': 0.05},
            'clap': {'note': 39, 'pitch': 1200, 'decay': 0.1},
            'ride': {'note': 51, 'pitch': 5000, 'decay': 0.4},
            'cowbell': {'note': 56, 'pitch': 800, 'decay': 0.2}
        },
        'hiphop': {
            'kick': {'note': 36, 'pitch': 50, 'decay': 0.35},
            'snare': {'note': 38, 'pitch': 220, 'decay': 0.25},
            'hihat': {'note': 42, 'pitch': 8500, 'decay': 0.05},
            'shaker': {'note': 70, 'pitch': 3000, 'decay': 0.1},
            'rim': {'note': 37, 'pitch': 600, 'decay': 0.03},
            'perc': {'note': 75, 'pitch': 1500, 'decay': 0.1}
        },
        'techno': {
            'kick': {'note': 36, 'pitch': 45, 'decay': 0.4},
            'snare': {'note': 38, 'pitch': 250, 'decay': 0.3},
            'hihat': {'note': 42, 'pitch': 10000, 'decay': 0.02},
            'clap': {'note': 39, 'pitch': 1800, 'decay': 0.1},
            'tom_low': {'note': 41, 'pitch': 80, 'decay': 0.3},
            'tom_high': {'note': 48, 'pitch': 150, 'decay': 0.25}
        },
        'lofi': {
            'kick': {'note': 36, 'pitch': 40, 'decay': 0.5},
            'snare': {'note': 38, 'pitch': 150, 'decay': 0.4},
            'hihat': {'note': 42, 'pitch': 6000, 'decay': 0.1},
            'vinyl': {'note': 60, 'pitch': 100, 'decay': 0.8},
            'crackle': {'note': 61, 'pitch': 2000, 'decay': 0.05}
        }
    }
    
    def __init__(self, kit_name: str = 'trap'):
        self.kit = self.KITS.get(kit_name, self.KITS['trap'])
        self.kit_name = kit_name
    
    def get_instruments(self) -> List[str]:
        return list(self.kit.keys())


class DrumPatternV3:
    """Pattern generator by genre"""
    
    PATTERNS = {
        'trap': {
            'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'clap': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        },
        'house': {
            'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'clap': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        },
        'hiphop': {
            'kick': [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            'hihat': [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
            'shaker': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        },
        'techno': {
            'kick': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'clap': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        },
        'lofi': {
            'kick': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            'snare': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            'hihat': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        }
    }
    
    def __init__(self):
        self.current_pattern = 'trap'
    
    def get_pattern(self, genre: str) -> Dict:
        return self.PATTERNS.get(genre, self.PATTERNS['trap'])


class HumanizerV3:
    """Advanced humanization"""
    
    def __init__(self):
        self.timing_variation = 0.1  # ms
        self.velocity_variation = 0.1  # 0-1
        self.pitch_variation = 5  # cents
    
    def humanize_timing(self, position: int) -> float:
        """Add timing variation"""
        return position + random.uniform(-self.timing_variation, self.timing_variation)
    
    def humanize_velocity(self, velocity: float) -> float:
        """Add velocity variation"""
        return max(0, min(1, velocity + random.uniform(-self.velocity_variation, self.velocity_variation)))
    
    def humanize_pitch(self, pitch: float) -> float:
        """Add pitch variation"""
        return pitch + random.uniform(-self.pitch_variation, self.pitch_variation)


class FillGeneratorV3:
    """Generate drum fills"""
    
    FILLS = {
        'simple': [0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0],
        'double': [0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,0],
        'roll': [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
        'ghost': [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
        'crash': [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
    }
    
    def generate_fill(self, fill_type: str = 'simple') -> List[int]:
        return self.FILLS.get(fill_type, self.FILLS['simple'])


class SmartDrumV3:
    """Complete drum machine V3"""
    
    def __init__(self):
        self.kit = DrumKitV3('trap')
        self.pattern = DrumPatternV3()
        self.humanizer = HumanizerV3()
        self.fill_gen = FillGeneratorV3()
        self.swing = 0  # 0-1
        self.bpm = 140
    
    def set_kit(self, kit_name: str):
        """Set drum kit"""
        self.kit = DrumKitV3(kit_name)
    
    def set_genre(self, genre: str):
        """Set genre"""
        self.kit = DrumKitV3(genre)
        self.pattern.current_pattern = genre
    
    def generate(self, bars: int, genre: str = 'trap') -> List[Dict]:
        """Generate drum pattern"""
        
        pattern = self.pattern.get_pattern(genre)
        events = []
        
        steps_per_bar = 16
        
        for bar in range(bars):
            # Regular pattern or fill every 4th bar
            if bar > 0 and bar % 4 == 3:
                fill = self.fill_gen.generate_fill(random.choice(['simple', 'double', 'roll']))
                bar_pattern = fill
            else:
                bar_pattern = None
            
            for step in range(steps_per_bar):
                beat_time = (bar * 4 + step / 4) * 60 / self.bpm
                
                for instrument, pattern_data in pattern.items():
                    if bar_pattern and instrument in ['kick', 'snare']:
                        step_pattern = bar_pattern
                    else:
                        step_pattern = pattern_data
                    
                    if step < len(step_pattern) and step_pattern[step]:
                        velocity = self.humanizer.humanize_velocity(0.8)
                        timing = self.humanizer.humanize_timing(beat_time)
                        
                        events.append({
                            'instrument': instrument,
                            'time': timing,
                            'velocity': velocity,
                            'note': self.kit.kit.get(instrument, {}).get('note', 36)
                        })
        
        return events


def demo():
    print("=" * 60)
    print("  SMART DRUMS V3 - 5 KITS, MULTIPLE GENRES")
    print("=" * 60)
    
    drums = SmartDrumV3()
    
    print("\n[Kits Available]")
    for kit in ['trap', 'house', 'hiphop', 'techno', 'lofi']:
        drums.set_kit(kit)
        insts = drums.kit.get_instruments()
        print("  %s: %s" % (kit, ', '.join(insts)))
    
    print("\n[Generating Patterns]")
    
    for genre in ['trap', 'house', 'hiphop', 'techno']:
        drums.set_genre(genre)
        events = drums.generate(4, genre)
        print("  %s: %d events" % (genre, len(events)))
    
    print("\n[Humanization]")
    h = HumanizerV3()
    print("  Timing: %.2f" % h.humanize_timing(1.0))
    print("  Velocity: %.2f" % h.humanize_velocity(0.8))
    print("  Pitch: %.2f" % h.humanize_pitch(440))
    
    print("\n" + "=" * 60)
    print("  DRUMS V3 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()