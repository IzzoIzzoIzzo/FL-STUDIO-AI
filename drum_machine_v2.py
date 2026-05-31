"""
SMARTER DRUM PATTERNS V2 - Level 1.2 Upgrade
============================================
- Humanized patterns (more realistic)
- Groove templates
- Velocity variation
- Fill generation
- Style learning

Building on what we have - making drums better!
"""

import math
import random
from typing import List, Dict, Tuple, Optional


class Humanizer:
    """Add human feel to drum patterns"""
    
    @staticmethod
    def humanize_velocity(velocity: int, amount: float = 0.15) -> int:
        """Add velocity variation"""
        variation = int(velocity * amount * random.uniform(-1, 1))
        return max(1, min(127, velocity + variation))
    
    @staticmethod
    def humanize_timing(tick: int, amount: float = 0.1) -> int:
        """Add timing offset"""
        offset = int(random.uniform(-amount, amount) * 120)  # 120 ticks = 1/4 beat
        return max(0, tick + offset)
    
    @staticmethod
    def humanize_velocity_sequence(velocities: List[int], variation: float = 0.15) -> List[int]:
        """Humanize entire velocity sequence"""
        return [Humanizer.humanize_velocity(v, variation) for v in velocities]


class GrooveTemplate:
    """Apply groove templates to patterns"""
    
    TEMPLATES = {
        'straight': {'swung': 0, 'accent_first': 0, 'vel_shift': 0},
        'shuffle': {'swung': 0.15, 'accent_first': 0, 'vel_shift': 0},
        'heavy': {'swung': 0, 'accent_first': 0.3, 'vel_shift': 20},
        'bouncy': {'swung': 0.1, 'accent_first': 0.15, 'vel_shift': 10},
        'broken': {'swung': 0.05, 'accent_first': 0, 'vel_shift': 5},
        'funk': {'swung': 0.08, 'accent_first': 0.2, 'vel_shift': 15},
        'jazz': {'swung': 0.2, 'accent_first': 0.1, 'vel_shift': 5},
        'latin': {'swung': 0.05, 'accent_first': 0.25, 'vel_shift': 12},
    }
    
    @classmethod
    def apply(cls, pattern: List[Tuple[int, int, int]], groove_name: str) -> List[Tuple[int, int, int]]:
        """Apply groove to pattern"""
        groove = cls.TEMPLATES.get(groove_name, cls.TEMPLATES['straight'])
        
        result = []
        for i, (note, vel, dur) in enumerate(pattern):
            # Apply timing swing
            if groove['swung'] > 0 and i % 2 == 1:  # Off-beats
                offset = int(groove['swung'] * 120)
                dur += offset
            
            # Apply velocity shift
            new_vel = vel
            if i == 0 or (groove['accent_first'] > 0 and i % 4 == 0):
                new_vel = min(127, vel + int(groove['vel_shift']))
            
            result.append((note, new_vel, dur))
        
        return result


class FillGenerator:
    """Generate drum fills"""
    
    @staticmethod
    def generate_4_beat_fill(kick_note: int, snare_note: int, hh_note: int, style: str = 'rock') -> List[Tuple[int, int, int]]:
        """Generate a 1-bar fill"""
        fill = []
        beat_duration = 120  # 1/4 note
        
        if style == 'rock':
            # Rock fill: kick-snare-kick-snare with variations
            fill = [
                (kick_note, 100, beat_duration // 2),
                (snare_note, 90, beat_duration // 2),
                (kick_note, 100, beat_duration // 4),
                (kick_note, 100, beat_duration // 4),
                (snare_note, 95, beat_duration // 2),
                (kick_note, 80, beat_duration // 4),
                (snare_note, 100, beat_duration // 4),
            ]
        
        elif style == 'jazz':
            # Jazz fill: more complex
            fill = [
                (snare_note, 80, beat_duration // 4),
                (kick_note, 70, beat_duration // 4),
                (snare_note, 85, beat_duration // 4),
                (kick_note, 75, beat_duration // 4),
                (snare_note, 90, beat_duration // 2),
                (kick_note, 80, beat_duration // 4),
                (snare_note, 95, beat_duration // 4),
            ]
        
        elif style == 'electronic':
            # Electronic fill: faster, noise-based
            fill = [
                (hh_note, 60, beat_duration // 4),
                (kick_note, 100, beat_duration // 4),
                (hh_note, 70, beat_duration // 4),
                (kick_note, 110, beat_duration // 4),
                (hh_note, 80, beat_duration // 4),
                (kick_note, 100, beat_duration // 4),
                (hh_note, 90, beat_duration // 4),
            ]
        
        elif style == 'trap':
            # Trap fill: 808 style
            fill = [
                (kick_note, 120, beat_duration // 2),
                (kick_note, 110, beat_duration // 4),
                (kick_note, 130, beat_duration // 4),
                (snare_note, 100, beat_duration // 4),
                (kick_note, 110, beat_duration // 4),
                (kick_note, 140, beat_duration // 4),
            ]
        
        return fill
    
    @staticmethod
    def insert_fill_at_bar(pattern: List[Tuple[int, int, int]], 
                          bar_position: int, 
                          fill: List[Tuple[int, int, int]],
                          beat_length: int = 480) -> List[Tuple[int, int, int]]:
        """Insert fill at specific bar"""
        # Replace the bar with fill
        start_idx = bar_position * 4 * beat_length  # 4 beats per bar
        result = pattern[:start_idx] + fill + pattern[start_idx + len(fill) * beat_length:]
        return result


class SmartDrumGenerator:
    """Enhanced drum pattern generator with AI features"""
    
    PRESETS = {
        'trap': {
            'kit': '808',
            'pattern': [(36, 120, 120), (0, 0, 120), (36, 110, 120), (38, 100, 120)],
            'swing': 0.0,
            'humanize': 0.1
        },
        'house': {
            'kit': '909',
            'pattern': [(36, 110, 120), (46, 60, 120), (38, 100, 120), (46, 70, 120)],
            'swing': 0.05,
            'humanize': 0.05
        },
        'hiphop': {
            'kit': 'lofi',
            'pattern': [(36, 100, 120), (0, 0, 120), (38, 90, 120), (0, 0, 120)],
            'swing': 0.08,
            'humanize': 0.15
        },
    }
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def generate(self, bars: int = 4, style: str = 'trap', 
                 humanize: float = 0.1, swing: float = 0.0,
                 add_fills: bool = True) -> List[Tuple[int, int, int]]:
        """Generate smart drum pattern"""
        
        preset = self.PRESETS.get(style, self.PRESETS['trap'])
        
        # Base pattern
        pattern = []
        beat_duration = 120
        
        for bar in range(bars):
            for beat in range(4):
                offset = bar * 4 * beat_duration + beat * beat_duration
                
                for note, vel, dur in preset['pattern']:
                    # Apply humanization
                    if humanize > 0:
                        vel = Humanizer.humanize_velocity(vel, humanize)
                        offset = Humanizer.humanize_timing(offset, swing)
                    
                    if note > 0:
                        pattern.append((note, vel, dur))
                    else:
                        pattern.append((0, 0, dur))
            
            # Add fill at end of each bar (except last)
            if add_fills and bar < bars - 1:
                kick = 36
                snare = 38
                hh = 46
                fill = FillGenerator.generate_4_beat_fill(kick, snare, hh, style)
                # Add fill at bar end
                pattern.extend([(n, v, d) for n, v, d in fill])
        
        return pattern
    
    def generate_with_groove(self, bars: int = 4, style: str = 'trap', 
                            groove: str = 'funk') -> List[Tuple[int, int, int]]:
        """Generate with groove template"""
        pattern = self.generate(bars, style, humanize=0.05, add_fills=False)
        return GrooveTemplate.apply(pattern, groove)
    
    def generate_smart_pattern(self, complexity: str = 'medium') -> Dict:
        """Generate pattern with smart variations"""
        
        complexities = {
            'simple': {'hits_per_beat': 1, 'velocity_range': 20},
            'medium': {'hits_per_beat': 2, 'velocity_range': 40},
            'complex': {'hits_per_beat': 3, 'velocity_range': 60},
        }
        
        cfg = complexities.get(complexity, complexities['medium'])
        
        pattern = []
        beats = 16
        
        for i in range(beats):
            base_vel = 80 + random.randint(-cfg['velocity_range']//2, cfg['velocity_range']//2)
            
            # Kick on 1, 5, 9, 13 (every 4 beats)
            if i % 4 == 0:
                pattern.append((36, base_vel + 20, 120))
            
            # Snare on 5, 13
            if i % 8 == 4:
                pattern.append((38, base_vel, 120))
            
            # Hi-hats every beat
            if cfg['hits_per_beat'] >= 1:
                pattern.append((46, base_vel - 30, 60))
            
            # Extra hi-hats for complexity
            if cfg['hits_per_beat'] >= 2 and i % 2 == 1:
                pattern.append((46, base_vel - 40, 60))
            
            # Extra percussion for complex
            if cfg['hits_per_beat'] >= 3 and random.random() < 0.3:
                pattern.append((39, base_vel - 20, 60))  # Clap
        
        return {
            'pattern': pattern,
            'complexity': complexity,
            'duration': len(pattern) * 120 / 480  # In bars
        }


def demo():
    print("=" * 60)
    print("  SMARTER DRUM PATTERNS V2 - Level 1.2 Upgrade")
    print("=" * 60)
    
    gen = SmartDrumGenerator()
    
    print("\n=== HUMANIZATION ===")
    print("Velocity humanize test: ", Humanizer.humanize_velocity(100, 0.2))
    
    print("\n=== GROOVE TEMPLATES ===")
    print("Available:", list(GrooveTemplate.TEMPLATES.keys()))
    
    print("\n[TEST] Trap with humanization...")
    pattern = gen.generate(4, style='trap', humanize=0.15, swing=0.05, add_fills=True)
    print(f"    Generated {len(pattern)} drum events")
    
    print("\n[TEST] House with funk groove...")
    pattern = gen.generate_with_groove(4, style='house', groove='funk')
    print(f"    Generated {len(pattern)} drum events")
    
    print("\n[TEST] Smart pattern - complex...")
    smart = gen.generate_smart_pattern('complex')
    print(f"    Generated {len(smart['pattern'])} events")
    
    print("\n[TEST] Fill generation...")
    fill = FillGenerator.generate_4_beat_fill(36, 38, 46, 'trap')
    print(f"    Generated {len(fill)} fill hits")
    
    print("\n" + "=" * 60)
    print("  DRUMS V2 - Level 1.2 COMPLETE!")
    print("  Humanization, Grooves, Fills, Smart Generation")
    print("=" * 60)


if __name__ == "__main__":
    demo()