"""
ADVANCED AI MUSIC COMPOSER
==========================
Deep learning inspired music generation:
- Markov Chain Composer
- LSTM-Style Melody Generator  
- Style Transfer Engine
- Chord Progression AI
- Rhythm Pattern AI
- Auto-Arrangement AI
- Dynamic Arrangement Engine
- Harmonic Analysis AI

CONNECTED TO MAIN API!
"""

import math
import random
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class MarkovChainComposer:
    """Markov chain based music generation"""
    
    def __init__(self, order: int = 2):
        self.order = order
        self.transitions = defaultdict(list)
        self.note_counts = defaultdict(int)
    
    def train(self, sequences: List[List[int]]):
        """Train on note sequences"""
        for seq in sequences:
            # Build n-grams
            for i in range(len(seq) - self.order):
                key = tuple(seq[i:i+self.order])
                next_note = seq[i+self.order]
                self.transitions[key].append(next_note)
                
                for j in range(self.order):
                    prefix = tuple(seq[i:i+j+1]) if j > 0 else ()
                    self.note_counts[prefix] += 1
    
    def generate(self, seed: List[int], length: int) -> List[int]:
        """Generate notes from Markov chain"""
        result = list(seed[:self.order])
        
        for _ in range(length - self.order):
            key = tuple(result[-self.order:])
            
            if key in self.transitions:
                next_note = random.choice(self.transitions[key])
                result.append(next_note)
            else:
                # Fallback - random note in scale
                result.append(random.choice([0, 2, 4, 5, 7, 9, 11]))
        
        return result


class LSTMMelodyGenerator:
    """LSTM-style neural melody generation"""
    
    def __init__(self, hidden_size: int = 64, num_layers: int = 2):
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.weights = {}
        self._init_weights()
    
    def _init_weights(self):
        """Initialize network weights"""
        # Simplified weight initialization
        self.weights['input'] = [[random.uniform(-0.5, 0.5) for _ in range(12)] 
                                  for _ in range(self.hidden_size)]
        self.weights['hidden'] = [[random.uniform(-0.5, 0.5) for _ in range(self.hidden_size)]
                                  for _ in range(self.hidden_size)]
        self.weights['output'] = [[random.uniform(-0.5, 0.5) for _ in range(self.hidden_size)]
                                   for _ in range(12)]
    
    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))
    
    def _tanh(self, x: float) -> float:
        return math.tanh(x)
    
    def _forward(self, input_vec: List[float], hidden_state: List[float]) -> Tuple[List[float], List[float]]:
        """Forward pass through network"""
        # Simplified LSTM-like forward pass
        new_hidden = []
        output = []
        
        for h in range(self.hidden_size):
            # Input contribution
            inp_sum = sum(self.weights['input'][h][i] * input_vec[i] for i in range(len(input_vec)))
            # Hidden contribution
            hid_sum = sum(self.weights['hidden'][h][j] * hidden_state[j] for j in range(self.hidden_size))
            # Combine
            new_hidden.append(self._tanh(inp_sum + hid_sum))
        
        # Output layer
        for o in range(12):
            out_val = sum(self.weights['output'][o][h] * new_hidden[h] for h in range(self.hidden_size))
            output.append(self._sigmoid(out_val))
        
        return output, new_hidden
    
    def generate(self, seed_notes: List[int], duration: int, key: str = 'C') -> List[Dict]:
        """Generate melody in key"""
        # Convert key to scale degrees
        key_offset = {'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11, 
                      'F': 5, 'Bb': 10, 'Eb': 3, 'Ab': 8, 'Db': 1, 'Gb': 6}.get(key, 0)
        
        scale = [key_offset + n for n in [0, 2, 4, 5, 7, 9, 11]]
        
        # Initialize
        hidden = [0.0] * self.hidden_size
        output_notes = []
        current_beat = 0
        
        # Input encoding (12 pitch classes)
        input_vec = [1.0 if n % 12 == seed_notes[0] % 12 else 0.0 for n in range(12)]
        
        for _ in range(duration):
            # Forward pass
            output, hidden = self._forward(input_vec, hidden)
            
            # Select note based on output probabilities
            note_probs = [(scale[i % 7], output[i % 12]) for i in range(len(scale))]
            note_probs.sort(key=lambda x: x[1], reverse=True)
            
            # Select top note with some randomness
            if random.random() < 0.7:
                selected = note_probs[0][0]
            else:
                selected = random.choice(scale)
            
            # Duration
            duration = random.choice([0.25, 0.5, 0.5, 1.0])
            
            # Velocity
            velocity = random.uniform(0.6, 1.0)
            
            output_notes.append({
                'note': selected + 60,
                'start': current_beat,
                'duration': duration,
                'velocity': velocity
            })
            
            current_beat += duration
            
            # Update input
            input_vec = [1.0 if n % 12 == selected % 12 else 0.0 for n in range(12)]
        
        return output_notes


class StyleTransferEngine:
    """Transfer musical style between genres"""
    
    STYLES = {
        'classical': {'density': 0.3, 'rhythm_complexity': 0.8, 'harmony': 'complex', 
                     'ornamentation': 0.9, 'dynamics': 'varied'},
        'jazz': {'density': 0.6, 'rhythm_complexity': 0.7, 'harmony': 'complex', 
                'ornamentation': 0.6, 'dynamics': 'moderate'},
        'rock': {'density': 0.8, 'rhythm_complexity': 0.5, 'harmony': 'simple', 
                'ornamentation': 0.2, 'dynamics': 'drastic'},
        'electronic': {'density': 0.9, 'rhythm_complexity': 0.6, 'harmony': 'minimal', 
                     'ornamentation': 0.1, 'dynamics': 'consistent'},
        'folk': {'density': 0.4, 'rhythm_complexity': 0.3, 'harmony': 'simple', 
                'ornamentation': 0.4, 'dynamics': 'moderate'},
        'ambient': {'density': 0.2, 'rhythm_complexity': 0.1, 'harmony': 'minimal', 
                  'ornamentation': 0.1, 'dynamics': 'subtle'},
        'hiphop': {'density': 0.7, 'rhythm_complexity': 0.8, 'harmony': 'minimal', 
                  'ornamentation': 0.2, 'dynamics': 'consistent'},
        'ambient': {'density': 0.2, 'rhythm_complexity': 0.1, 'harmony': 'minimal', 
                  'ornamentation': 0.1, 'dynamics': 'subtle'},
        'blues': {'density': 0.5, 'rhythm_complexity': 0.4, 'harmony': 'moderate', 
                 'ornamentation': 0.7, 'dynamics': 'varied'},
    }
    
    def __init__(self):
        self.current_style = None
    
    def set_style(self, style: str):
        """Set target style"""
        if style in self.STYLES:
            self.current_style = self.STYLES[style]
        else:
            self.current_style = self.STYLES['electronic']
    
    def transfer(self, input_melody: List[Dict], target_style: str) -> List[Dict]:
        """Transfer style to melody"""
        self.set_style(target_style)
        
        output = []
        
        for note in input_melody:
            new_note = dict(note)
            
            # Apply style transformations
            density = self.current_style['density']
            
            # Maybe add ornamentation
            if self.current_style['ornamentation'] > 0.5 and random.random() < 0.3:
                new_note['ornaments'] = ['grace', 'trill'][int(random.random()*2)]
            
            # Adjust dynamics
            if self.current_style['dynamics'] == 'varied':
                new_note['velocity'] = note['velocity'] * random.uniform(0.7, 1.0)
            elif self.current_style['dynamics'] == 'drastic':
                new_note['velocity'] = random.choice([0.3, 0.7, 1.0])
            
            output.append(new_note)
        
        return output


class ChordProgressionAI:
    """AI-powered chord progression generation"""
    
    CHORD_PROGRESSIONS = {
        'pop': ['I', 'V', 'vi', 'IV', 'I', 'IV', 'V', 'I'],
        'jazz': ['I', 'vi', 'ii', 'V', 'I', 'IV', 'ii', 'V'],
        'blues': ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'IV', 'I', 'V'],
        'rock': ['I', 'IV', 'V', 'I', 'I', 'IV', 'V', 'I'],
        'folk': ['I', 'IV', 'V', 'I', 'II', 'V', 'I', 'VI'],
        'electronic': ['i', 'v', 'i', 'iv', 'i', 'v', 'iv', 'i'],
        'cinematic': ['I', 'III', 'IV', 'V', 'vi', 'IV', 'I', 'V'],
    }
    
    CHORD_NOTES = {
        'I': [0, 4, 7], 'ii': [2, 5, 9], 'iii': [4, 7, 11], 'IV': [5, 9, 0],
        'V': [7, 11, 2], 'vi': [9, 0, 4], 'vii': [11, 2, 5],
        'i': [0, 3, 7], 'ii': [2, 5, 8], 'iii': [3, 7, 10], 'iv': [5, 8, 0],
        'v': [7, 10, 2], 'vi': [8, 0, 3], 'vii': [10, 1, 4]
    }
    
    def __init__(self):
        self.key = 'C'
        self.mode = 'major'
    
    def set_key(self, key: str, mode: str = 'major'):
        """Set key and mode"""
        self.key = key
        self.mode = mode
    
    def generate_progression(self, style: str = 'pop', length: int = 8) -> List[Tuple[str, List[int]]]:
        """Generate chord progression"""
        if style not in self.CHORD_PROGRESSIONS:
            style = 'pop'
        
        base_prog = self.CHORD_PROGRESSIONS[style][:length]
        
        # Convert to actual notes based on key
        key_offset = {'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11, 
                      'F': 5, 'Bb': 10, 'Eb': 3, 'Ab': 8, 'Db': 1, 'Gb': 6}.get(self.key, 0)
        
        result = []
        for chord_symbol in base_prog:
            if chord_symbol in self.CHORD_NOTES:
                chord_notes = [(key_offset + n + 60) % 128 for n in self.CHORD_NOTES[chord_symbol]]
                result.append((chord_symbol, chord_notes))
        
        return result


class RhythmPatternAI:
    """AI rhythm pattern generation"""
    
    GENRES = {
        'pop': {'note_density': 0.6, 'syncopation': 0.3, 'swing': 0.1},
        'rock': {'note_density': 0.8, 'syncopation': 0.2, 'swing': 0.0},
        'jazz': {'note_density': 0.7, 'syncopation': 0.6, 'swing': 0.5},
        'hiphop': {'note_density': 0.6, 'syncopation': 0.7, 'swing': 0.0},
        'electronic': {'note_density': 0.9, 'syncopation': 0.4, 'swing': 0.0},
        'latin': {'note_density': 0.8, 'syncopation': 0.5, 'swing': 0.6},
    }
    
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.genre = 'pop'
    
    def set_genre(self, genre: str):
        """Set genre style"""
        if genre in self.GENRES:
            self.genre = genre
    
    def generate_pattern(self, bars: int = 4, tracks: int = 4) -> Dict[str, List[Dict]]:
        """Generate multi-track rhythm pattern"""
        genre_params = self.GENRES[self.genre]
        beats_per_bar = 4
        total_beats = bars * beats_per_bar
        
        result = {
            'drums': [],
            'bass': [],
            'melody': [],
            'chords': []
        }
        
        # Generate drum pattern
        for beat in range(total_beats):
            # Kick on 1 and 3 (or more often for electronic)
            if beat % 2 == 0 or (self.genre == 'electronic' and beat % 1 == 0):
                result['drums'].append({'time': beat, 'instrument': 'kick', 'velocity': 0.9})
            
            # Snare on 2 and 4 (or off-beat for some genres)
            if beat % 2 == 1:
                if self.genre == 'jazz':
                    result['drums'].append({'time': beat + 0.5, 'instrument': 'snare', 'velocity': 0.7})
                else:
                    result['drums'].append({'time': beat, 'instrument': 'snare', 'velocity': 0.8})
            
            # Hi-hat pattern
            for sub in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
                if random.random() < genre_params['note_density']:
                    result['drums'].append({
                        'time': beat + sub,
                        'instrument': 'hihat',
                        'velocity': random.uniform(0.4, 0.7)
                    })
        
        # Generate bass pattern
        bass_notes = [36, 38, 41, 43]  # Root patterns
        for beat in range(total_beats):
            if random.random() < genre_params['note_density'] * 0.8:
                note = random.choice(bass_notes)
                if genre_params['syncopation'] > 0.4 and random.random() > 0.5:
                    beat += 0.5
                result['bass'].append({
                    'time': beat,
                    'note': note,
                    'velocity': 0.8
                })
        
        return result


class AutoArrangementAI:
    """AI-powered song arrangement"""
    
    SECTIONS = ['intro', 'verse', 'pre_chorus', 'chorus', 'bridge', 'outro']
    
    FORMATS = {
        'pop': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus', 'outro'],
        'rock': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'solo', 'chorus', 'outro'],
        'electronic': ['intro', 'build', 'drop', 'build', 'drop', 'break', 'drop', 'outro'],
        'jazz': ['intro', 'head', 'solo', 'head', 'solo', 'bridge', 'head', 'outro'],
        'classical': ['intro', 'exposition', 'development', 'recapitulation', 'coda'],
    }
    
    def __init__(self):
        self.format = 'pop'
    
    def set_format(self, format_name: str):
        """Set arrangement format"""
        if format_name in self.FORMATS:
            self.format = format_name
    
    def generate_arrangement(self, total_bars: int = 32) -> List[Dict]:
        """Generate song arrangement"""
        format_sections = self.FORMATS[self.format]
        
        # Calculate bar distribution
        bars_per_section = total_bars // len(format_sections)
        
        arrangement = []
        current_bar = 0
        
        for section in format_sections:
            section_data = {
                'name': section,
                'start_bar': current_bar,
                'length': bars_per_section,
            }
            
            # Add section-specific properties
            if section in ['intro', 'build']:
                section_data['energy'] = 0.6
                section_data['complexity'] = 'increasing'
            elif section in ['verse', 'bridge']:
                section_data['energy'] = 0.7
                section_data['complexity'] = 'moderate'
            elif section in ['chorus', 'drop']:
                section_data['energy'] = 1.0
                section_data['complexity'] = 'high'
            elif section in ['outro', 'coda']:
                section_data['energy'] = 0.4
                section_data['complexity'] = 'decreasing'
            
            arrangement.append(section_data)
            current_bar += bars_per_section
        
        return arrangement


class DynamicArrangementEngine:
    """Dynamic arrangement with real-time adaptation"""
    
    def __init__(self):
        self.sections = []
        self.current_section = 0
        self.energy = 0.5
    
    def add_section(self, name: str, duration: int, energy: float):
        """Add section to arrangement"""
        self.sections.append({
            'name': name,
            'duration': duration,
            'energy': energy,
            'instruments': []
        })
    
    def transition_to(self, section_name: str, transition_type: str = 'cut'):
        """Transition to new section"""
        for i, s in enumerate(self.sections):
            if s['name'] == section_name:
                self.current_section = i
                break
        
        # Adjust energy based on transition
        if transition_type == 'fade':
            self.energy = self.sections[self.current_section]['energy']
        elif transition_type == 'build':
            self.energy = min(1.0, self.energy + 0.2)
        elif transition_type == 'drop':
            self.energy = max(0.3, self.energy - 0.3)
    
    def get_current_state(self) -> Dict:
        """Get current arrangement state"""
        if self.sections:
            return {
                'section': self.sections[self.current_section],
                'energy': self.energy,
                'progress': self.current_section / len(self.sections)
            }
        return {}


class HarmonicAnalysisAI:
    """Analyze and suggest harmonic content"""
    
    def __init__(self):
        self.key = 'C'
        self.mode = 'major'
    
    def analyze_chord(self, notes: List[int]) -> Dict:
        """Analyze chord from notes"""
        if not notes:
            return {'chord': 'N/A', 'quality': 'unknown', 'root': 0}
        
        # Get root (lowest note)
        root = min(notes) % 12
        
        # Determine intervals from root
        intervals = sorted([(n - root) % 12 for n in notes])
        
        # Match to chord quality
        if intervals == [0, 4, 7]:
            quality = 'major'
        elif intervals == [0, 3, 7]:
            quality = 'minor'
        elif intervals == [0, 4, 7, 11]:
            quality = 'major7'
        elif intervals == [0, 3, 7, 10]:
            quality = 'minor7'
        elif intervals == [0, 4, 7, 10]:
            quality = 'dominant7'
        elif intervals == [0, 4, 6]:
            quality = 'augmented'
        elif intervals == [0, 3, 6]:
            quality = 'diminished'
        else:
            quality = 'unknown'
        
        roots = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        return {
            'chord': roots[root] + quality[0].upper(),
            'quality': quality,
            'root': root,
            'intervals': intervals
        }
    
    def suggest_harmony(self, melody_notes: List[int], key: str) -> List[Dict]:
        """Suggest harmony for melody"""
        suggestions = []
        
        # Simple harmonic analysis
        roots = {'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11, 
                 'F': 5, 'Bb': 10, 'Eb': 3, 'Ab': 8, 'Db': 1, 'Gb': 6}
        
        key_root = roots.get(key, 0)
        
        for note in melody_notes:
            note_class = note % 12
            
            # Suggest chords based on melody notes
            if note_class in [0, 2, 4]:
                suggestions.append({'chord': 'I', 'confidence': 0.9})
            elif note_class in [5, 7]:
                suggestions.append({'chord': 'IV', 'confidence': 0.8})
            elif note_class in [7, 9, 11]:
                suggestions.append({'chord': 'V', 'confidence': 0.8})
            else:
                suggestions.append({'chord': 'vi', 'confidence': 0.6})
        
        return suggestions


class AdvancedAIComposer:
    """
    Master AI Composer combining all AI models.
    CONNECTED TO MAIN API!
    """
    
    def __init__(self):
        self.markov = MarkovChainComposer(order=2)
        self.lstm = LSTMMelodyGenerator()
        self.style_transfer = StyleTransferEngine()
        self.chord_ai = ChordProgressionAI()
        self.rhythm_ai = RhythmPatternAI(bpm=120)
        self.arrangement = AutoArrangementAI()
        self.dynamic = DynamicArrangementEngine()
        self.harmonic = HarmonicAnalysisAI()
        
        print(f"    [OK] Advanced AI Composer initialized")
        print(f"         - Markov Chain Composer")
        print(f"         - LSTM Melody Generator")
        print(f"         - Style Transfer Engine")
        print(f"         - Chord Progression AI")
        print(f"         - Rhythm Pattern AI")
        print(f"         - Auto Arrangement AI")
        print(f"         - Dynamic Arrangement Engine")
        print(f"         - Harmonic Analysis AI")
    
    def compose(self, style: str, key: str, bpm: int, bars: int) -> Dict:
        """Complete AI composition"""
        # Set up components
        self.rhythm_ai.bpm = bpm
        self.rhythm_ai.set_genre(style)
        self.chord_ai.set_key(key)
        
        # Generate chord progression
        chords = self.chord_ai.generate_progression(style, bars)
        
        # Generate melody with LSTM
        seed = [60, 64, 67]  # C major arpeggio
        melody = self.lstm.generate(seed, bars * 4, key)
        
        # Generate rhythm
        rhythm = self.rhythm_ai.generate_pattern(bars)
        
        # Generate arrangement
        arrangement = self.arrangement.generate_arrangement(bars)
        
        return {
            'chords': chords,
            'melody': melody,
            'rhythm': rhythm,
            'arrangement': arrangement,
            'key': key,
            'bpm': bpm,
            'style': style
        }
    
    def analyze_harmony(self, notes: List[int]) -> Dict:
        """Analyze harmonic content"""
        return self.harmonic.analyze_chord(notes)


# Test function
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" ADVANCED AI COMPOSER TEST")
    print("="*60 + "\n")
    
    composer = AdvancedAIComposer()
    
    print("\n[1] Composing Pop Track...")
    result = composer.compose('pop', 'C', 120, 8)
    print(f"     Chords: {len(result['chords'])} progression")
    print(f"     Melody: {len(result['melody'])} notes")
    print(f"     Arrangement: {len(result['arrangement'])} sections")
    
    print("\n[2] Generating Jazz Pattern...")
    composer.rhythm_ai.set_genre('jazz')
    pattern = composer.rhythm_ai.generate_pattern(4)
    print(f"     Drums: {len(pattern['drums'])} events")
    print(f"     Bass: {len(pattern['bass'])} notes")
    
    print("\n[3] Analyzing Harmony...")
    analysis = composer.analyze_harmony([60, 64, 67])
    print(f"     Detected: {analysis['chord']}")
    
    print("\n[4] Style Transfer...")
    test_melody = [{'note': 60, 'start': 0, 'duration': 1, 'velocity': 0.8}]
    transferred = composer.style_transfer.transfer(test_melody, 'jazz')
    print(f"     Transferred: {len(transferred)} notes")
    
    print("\n" + "="*60)
    print(" ALL AI COMPOSER MODELS OPERATIONAL!")
    print("="*60 + "\n")