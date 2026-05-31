"""
LEVEL 3.3 - MORE AI ENHANCEMENTS
================================
- Creative AI
- Style Learning
- Prediction AI

Making Level 3 even smarter!
"""

import random
from typing import List, Dict


class CreativeAI:
    """AI-powered creative suggestions"""
    
    @staticmethod
    def suggest_variation(current: Dict, style: str = 'add') -> Dict:
        """Suggest a variation"""
        
        variations = {
            'add': {
                'description': 'Add new element',
                'actions': ['add_pad', 'add_strings', 'add_effect']
            },
            'remove': {
                'description': 'Remove element',
                'actions': ['remove_hi_hats', 'simplify_bass', 'reduce_drums']
            },
            'transform': {
                'description': 'Transform existing',
                'actions': ['pitch_shift', 'reverse', 'filter_sweep']
            },
            'enhance': {
                'description': 'Enhance current',
                'actions': ['add_reverb', 'add_delay', 'increase_energy']
            }
        }
        
        if style not in variations:
            style = random.choice(list(variations.keys()))
        
        action = random.choice(variations[style]['actions'])
        
        return {
            'type': style,
            'description': variations[style]['description'],
            'action': action,
            'confidence': random.uniform(0.7, 0.95)
        }
    
    @staticmethod
    def generate_alternatives(beat: Dict, count: int = 3) -> List[Dict]:
        """Generate alternative versions"""
        
        alternatives = []
        
        for i in range(count):
            alt = {
                'version': f"alt_{i+1}",
                'bpm': beat.get('bpm', 120) + random.choice([-10, -5, 0, 5, 10]),
                'key': beat.get('key', 'C'),
                'style_mod': random.choice(['lighter', 'darker', 'faster', 'slower']),
                'changes': []
            }
            
            if random.random() > 0.5:
                alt['changes'].append('add_intro')
            if random.random() > 0.5:
                alt['changes'].append('extend_chorus')
            
            alternatives.append(alt)
        
        return alternatives


class StyleLearning:
    """Learn from user patterns"""
    
    def __init__(self):
        self.patterns = []
        self.preferences = {}
    
    def learn_from(self, user_data: Dict) -> Dict:
        """Learn from user data"""
        
        # Analyze patterns
        if 'bpm' in user_data:
            avg_bpm = user_data['bpm']
            self.preferences['avg_bpm'] = avg_bpm
        
        if 'style' in user_data:
            style = user_data['style']
            count = self.preferences.get(style, 0)
            self.preferences[style] = count + 1
        
        if 'genre' in user_data:
            genre = user_data['genre']
            self.preferences['genre'] = genre
        
        # Calculate pattern
        self.patterns.append(user_data)
        
        return {
            'learned': True,
            'patterns_count': len(self.patterns),
            'preferences': self.preferences
        }
    
    def suggest_based_on_learned(self) -> Dict:
        """Suggest based on learned patterns"""
        
        if not self.preferences:
            return {'suggestion': 'No patterns learned yet'}
        
        # Most common style
        most_common = max(self.preferences.items(), key=lambda x: x[1] if isinstance(x[1], int) else 0)
        
        avg_bpm = self.preferences.get('avg_bpm', 120)
        
        return {
            'suggested_style': most_common[0],
            'suggested_bpm': int(avg_bpm),
            'confidence': 0.8
        }


class PredictionAI:
    """AI that predicts next elements"""
    
    @staticmethod
    def predict_next_section(current_section: str) -> str:
        """Predict next section"""
        
        transitions = {
            'intro': ['verse', 'build'],
            'verse': ['pre_chorus', 'chorus', 'verse'],
            'pre_chorus': ['chorus'],
            'chorus': ['verse', 'bridge', 'outro'],
            'bridge': ['chorus', 'outro'],
            'build': ['drop', 'chorus'],
            'drop': ['break', 'outro'],
            'break': ['drop', 'outro'],
            'outro': []
        }
        
        options = transitions.get(current_section, ['verse'])
        return random.choice(options) if options else 'end'
    
    @staticmethod
    def predict_melody_direction(current_notes: List[int]) -> str:
        """Predict melody direction"""
        
        if len(current_notes) < 2:
            return 'neutral'
        
        # Analyze direction
        direction = current_notes[-1] - current_notes[-2]
        
        if direction > 2:
            return 'ascending'
        elif direction < -2:
            return 'descending'
        else:
            return 'neutral'
    
    @staticmethod
    def suggest_next_note(current_note: int, scale: List[int], context: str = 'verse') -> int:
        """Suggest next note"""
        
        # Context influences note selection
        context_weights = {
            'intro': [0.3, 0.2, 0.1, 0.4],  # Prefer middle
            'verse': [0.2, 0.3, 0.3, 0.2],  # Balanced
            'chorus': [0.1, 0.2, 0.3, 0.4],  # Prefer high
            'bridge': [0.4, 0.3, 0.2, 0.1],  # Prefer low
            'outro': [0.4, 0.3, 0.2, 0.1]   # Descending
        }
        
        weights = context_weights.get(context, [0.25, 0.25, 0.25, 0.25])
        
        # Choose based on weights
        rand = random.random()
        if rand < weights[0]:
            step = -2  # Step down
        elif rand < weights[0] + weights[1]:
            step = -1  # Slight down
        elif rand < weights[0] + weights[1] + weights[2]:
            step = 1  # Slight up
        else:
            step = 2  # Step up
        
        return current_note + step


class AutoArranger:
    """Auto-arrange complete tracks"""
    
    @staticmethod
    def create_full_arrangement(style: str, duration_minutes: float = 3.0) -> Dict:
        """Create full arrangement"""
        
        bpm = 120
        seconds_per_bar = 4 * 60 / bpm
        total_bars = int((duration_minutes * 60) / seconds_per_bar)
        
        structures = {
            'standard': ['intro', 'verse', 'verse', 'chorus', 'chorus', 'outro'],
            'pop': ['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus', 'bridge', 'chorus', 'outro'],
            'edm': ['intro', 'build', 'drop', 'break', 'drop', 'outro'],
            'hiphop': ['intro', 'verse', 'hook', 'verse', 'hook', 'verse', 'outro'],
        }
        
        structure = structures.get(style, structures['standard'])
        
        arrangement = []
        bar_counter = 0
        
        for section in structure:
            section_length = 8 if section in ['verse', 'chorus'] else 4
            if section == 'intro':
                section_length = 4
            elif section == 'outro':
                section_length = 4
            
            arrangement.append({
                'section': section,
                'start_bar': bar_counter,
                'bars': section_length,
                'end_bar': bar_counter + section_length
            })
            
            bar_counter += section_length
        
        return {
            'style': style,
            'bpm': bpm,
            'total_bars': bar_counter,
            'duration_minutes': bar_counter * seconds_per_bar / 60,
            'arrangement': arrangement
        }


def demo():
    print("=" * 60)
    print("  LEVEL 3.3 - MORE AI ENHANCEMENTS")
    print("=" * 60)
    
    # Creative AI
    print("\n[Creative AI]")
    variation = CreativeAI.suggest_variation({'bpm': 140}, 'add')
    print(f"  Variation: {variation}")
    
    alts = CreativeAI.generate_alternatives({'bpm': 140, 'key': 'C'}, 2)
    print(f"  Alternatives: {len(alts)} generated")
    
    # Style Learning
    print("\n[Style Learning]")
    learner = StyleLearning()
    learner.learn_from({'bpm': 140, 'style': 'trap', 'genre': 'electronic'})
    learner.learn_from({'bpm': 130, 'style': 'house'})
    suggestion = learner.suggest_based_on_learned()
    print(f"  Suggestion: {suggestion}")
    
    # Prediction AI
    print("\n[Prediction AI]")
    next_section = PredictionAI.predict_next_section('verse')
    print(f"  Next after verse: {next_section}")
    
    # Auto Arranger
    print("\n[Auto Arranger]")
    full = AutoArranger.create_full_arrangement('pop', 2.5)
    print(f"  Pop arrangement: {full['total_bars']} bars, {len(full['arrangement'])} sections")
    
    print("\n" + "=" * 60)
    print("  LEVEL 3.3 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()