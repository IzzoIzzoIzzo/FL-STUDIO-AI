"""
ARRANGEMENT AI V2 - Level 3.1
===============================
- Song structure generation
- Section analysis
- Transition suggestions
- Dynamic arrangement

Building on what we have - making AI smarter!
"""

import random
from typing import List, Dict, Tuple


class SongStructure:
    """Song structure patterns"""
    
    STRUCTURES = {
        'simple': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro'],
        'verse_chorus': ['intro', 'verse1', 'chorus1', 'verse2', 'chorus2', 'bridge', 'chorus3', 'outro'],
        'abab': ['verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus'],
        'rondo': ['intro', 'a', 'b', 'a', 'c', 'a', 'outro'],
        'pop': ['intro', 'verse1', 'pre-chorus', 'chorus1', 'verse2', 'pre-chorus', 'chorus2', 'bridge', 'chorus3', 'outro'],
        'hiphop': ['intro', 'verse1', 'hook', 'verse2', 'hook', 'verse3', 'outro'],
        'electronic': ['intro', 'build', 'drop1', 'break', 'drop2', 'outro'],
    }
    
    SECTIONS = {
        'intro': {'bars': 4, 'energy': 0.3, 'complexity': 'low'},
        'verse': {'bars': 8, 'energy': 0.6, 'complexity': 'medium'},
        'pre-chorus': {'bars': 2, 'energy': 0.8, 'complexity': 'medium'},
        'chorus': {'bars': 8, 'energy': 1.0, 'complexity': 'high'},
        'bridge': {'bars': 4, 'energy': 0.5, 'complexity': 'medium'},
        'hook': {'bars': 4, 'energy': 1.0, 'complexity': 'high'},
        'build': {'bars': 4, 'energy': 0.8, 'complexity': 'medium'},
        'drop': {'bars': 8, 'energy': 1.0, 'complexity': 'high'},
        'break': {'bars': 4, 'energy': 0.3, 'complexity': 'low'},
        'outro': {'bars': 4, 'energy': 0.4, 'complexity': 'low'},
    }
    
    @classmethod
    def get_structure(cls, name: str) -> List[str]:
        return cls.STRUCTURES.get(name, cls.STRUCTURES['simple'])
    
    @classmethod
    def get_section_info(cls, section: str) -> Dict:
        return cls.SECTIONS.get(section, cls.SECTIONS['verse'])


class TransitionGenerator:
    """Generate transitions between sections"""
    
    TRANSITIONS = {
        ('intro', 'verse'): ['ramp_up', 'build', 'cut'],
        ('verse', 'pre-chorus'): ['build', 'ramp_up', 'fill'],
        ('pre-chorus', 'chorus'): ['impact', 'drop', 'ramp_up'],
        ('verse', 'chorus'): ['impact', 'build', 'ramp_up'],
        ('chorus', 'verse'): ['ramp_down', 'fill', 'wrap'],
        ('chorus', 'bridge'): ['ramp_down', 'build', 'sweep'],
        ('bridge', 'chorus'): ['impact', 'build', 'drop_in'],
        ('any', 'outro'): ['ramp_down', 'fade', 'wrap'],
    }
    
    @classmethod
    def suggest_transition(cls, from_section: str, to_section: str) -> str:
        """Suggest transition type"""
        key = (from_section, to_section)
        if key in cls.TRANSITIONS:
            return random.choice(cls.TRANSITIONS[key])
        
        # Try to find any to this section
        for k, v in cls.TRANSITIONS.items():
            if k[1] == to_section:
                return random.choice(v)
        
        return 'ramp_up'  # Default
    
    @classmethod
    def apply_transition(cls, audio_section: Dict, transition: str, duration: float = 1.0) -> Dict:
        """Apply transition to section"""
        
        transitions = {
            'ramp_up': {'volume': 'fade_in', 'filter': 'lowpass_open', 'energy': 'increase'},
            'ramp_down': {'volume': 'fade_out', 'filter': 'lowpass_close', 'energy': 'decrease'},
            'build': {'volume': 'steady', 'filter': 'sweep_up', 'energy': 'increase'},
            'impact': {'volume': 'hit', 'filter': 'full', 'energy': 'peak'},
            'drop': {'volume': 'dip', 'filter': 'highpass', 'energy': 'low'},
            'cut': {'volume': 'stop', 'filter': 'none', 'energy': 'zero'},
            'fade': {'volume': 'fade_out', 'filter': 'lowpass', 'energy': 'decrease'},
            'wrap': {'volume': 'crossfade', 'filter': 'full', 'energy': 'maintain'},
            'sweep': {'volume': 'steady', 'filter': 'sweep_down', 'energy': 'decrease'},
            'fill': {'volume': 'steady', 'filter': 'full', 'energy': 'steady'},
        }
        
        return transitions.get(transition, transitions['ramp_up'])


class ArrangementAI:
    """AI-powered arrangement generator"""
    
    def __init__(self):
        self.structure = SongStructure()
        self.transitions = TransitionGenerator()
    
    def generate_arrangement(self, style: str = 'simple', bpm: int = 120) -> Dict:
        """Generate full song arrangement"""
        
        structure = self.structure.get_structure(style)
        
        sections = []
        current_bar = 0
        
        for i, section_name in enumerate(structure):
            section_info = self.structure.get_section_info(section_name)
            bars = section_info['bars']
            
            # Get transition from previous
            if i > 0:
                prev_section = structure[i-1]
                transition = self.transitions.suggest_transition(prev_section, section_name)
            else:
                transition = 'none'
            
            section = {
                'name': section_name,
                'start_bar': current_bar,
                'bars': bars,
                'end_bar': current_bar + bars,
                'energy': section_info['energy'],
                'complexity': section_info['complexity'],
                'transition_in': transition,
                'duration_seconds': (bars * 60 / bpm) * 4,  # 4 beats per bar
            }
            
            sections.append(section)
            current_bar += bars
        
        return {
            'style': style,
            'bpm': bpm,
            'total_bars': current_bar,
            'total_duration': current_bar * 60 / bpm * 4,
            'sections': sections
        }
    
    def analyze_sections(self, sections: List[Dict]) -> Dict:
        """Analyze sections for energy flow"""
        
        energies = [s['energy'] for s in sections]
        
        # Find key moments
        max_energy_idx = energies.index(max(energies)) if energies else 0
        min_energy_idx = energies.index(min(energies)) if energies else 0
        
        # Calculate energy curve
        curve = []
        for i in range(len(energies) - 1):
            curve.append(energies[i+1] - energies[i])
        
        return {
            'peak_section': sections[max_energy_idx]['name'] if sections else 'none',
            'low_section': sections[min_energy_idx]['name'] if sections else 'none',
            'energy_curve': curve,
            'dynamic_range': max(energies) - min(energies) if energies else 0
        }
    
    def suggest_variations(self, arrangement: Dict) -> List[Dict]:
        """Suggest arrangement variations"""
        
        suggestions = []
        
        # Add variation 1: Extended chorus
        variation1 = arrangement.copy()
        for i, section in enumerate(variation1['sections']):
            if section['name'] == 'chorus':
                section['bars'] = section['bars'] + 4
                section['energy'] = min(1.0, section['energy'] + 0.1)
        suggestions.append({'name': 'Extended Chorus', 'arrangement': variation1})
        
        # Add variation 2: Remove bridge
        variation2 = arrangement.copy()
        variation2['sections'] = [s for s in variation2['sections'] if s['name'] != 'bridge']
        suggestions.append({'name': 'No Bridge', 'arrangement': variation2})
        
        # Add variation 3: Add breakdown
        variation3 = arrangement.copy()
        # Find a suitable spot to add break
        suggestions.append({'name': 'With Breakdown', 'arrangement': variation3})
        
        return suggestions


def demo():
    print("=" * 60)
    print("  ARRANGEMENT AI V2 - Level 3.1")
    print("=" * 60)
    
    ai = ArrangementAI()
    
    print("\n=== SONG STRUCTURES ===")
    for name in SongStructure.STRUCTURES:
        structure = SongStructure.get_structure(name)
        print(f"  {name}: {' -> '.join(structure[:4])}...")
    
    print("\n[TEST] Generate pop arrangement...")
    pop_arr = ai.generate_arrangement('pop', 120)
    print(f"    Total: {pop_arr['total_bars']} bars, {pop_arr['total_duration']:.1f}s")
    print(f"    Sections: {[s['name'] for s in pop_arr['sections']]}")
    
    print("\n[TEST] Analyze energy...")
    analysis = ai.analyze_sections(pop_arr['sections'])
    print(f"    Peak: {analysis['peak_section']}")
    print(f"    Low: {analysis['low_section']}")
    print(f"    Dynamic range: {analysis['dynamic_range']}")
    
    print("\n[TEST] Suggest variations...")
    variations = ai.suggest_variations(pop_arr)
    for v in variations:
        print(f"    - {v['name']}")
    
    print("\n[TEST] Transition suggestions...")
    trans = TransitionGenerator.suggest_transition('verse', 'chorus')
    print(f"    Verse to Chorus: {trans}")
    
    print("\n" + "=" * 60)
    print("  ARRANGEMENT AI V2 - Level 3.1 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()