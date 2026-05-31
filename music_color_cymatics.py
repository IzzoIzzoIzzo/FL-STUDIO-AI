"""
MUSIC-COLOR-CYMATICS ENGINE
==========================
Complete integration of:
- Music Theory (scales, chords, progressions)
- Color Theory (synesthesia, visual mapping)
- Cymatics (visualization of sound waves)
- Frequency Mapping (Hz to colors)
- Solfeggio Frequencies
- Binaural Beats
- Harmonic Visualization
- Visual Waveforms

For artists, producers, and visualizers!
"""

import math
import random
from typing import List, Dict, Tuple, Optional


class FrequencyColorMapper:
    """Map frequencies to colors (Hz -> RGB)"""
    
    # Standard color frequencies (Hz)
    FREQ_COLORS = {
        261.63: (255, 0, 0),      # C4 - Red
        293.66: (255, 127, 0),   # D4 - Orange
        329.63: (255, 255, 0),   # E4 - Yellow
        349.23: (127, 255, 0),   # F4 - Green
        392.00: (0, 255, 0),     # G4 - Green
        440.00: (0, 255, 255),    # A4 - Cyan
        493.88: (0, 127, 255),    # B4 - Blue
        523.25: (127, 0, 255),    # C5 - Purple
        587.33: (255, 0, 255),   # D5 - Magenta
        659.25: (255, 0, 127),    # E5 - Pink
    }
    
    # CYMATIC PATTERNS based on frequency
    CYMATIC_PATTERNS = {
        'low': {'circles': 1, 'complexity': 1, 'chaos': 0.2},
        'mid': {'circles': 3, 'complexity': 5, 'chaos': 0.5},
        'high': {'circles': 7, 'complexity': 10, 'chaos': 0.8},
    }
    
    def __init__(self):
        pass
    
    def freq_to_color(self, freq: float) -> Tuple[int, int, int]:
        """Convert frequency to RGB color"""
        
        # Logarithmic mapping
        log_freq = math.log2(max(freq, 20) / 20)
        
        # Map to 0-1 range
        t = min(1, max(0, log_freq / 8))
        
        # Rainbow mapping (ROYGBIV)
        hue = t * 360
        
        return self._hsl_to_rgb(hue, 1.0, 0.5)
    
    def _hsl_to_rgb(self, h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Convert HSL to RGB"""
        
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )
    
    def note_to_color(self, midi_note: int) -> Tuple[int, int, int]:
        """Convert MIDI note to color"""
        
        freq = 440 * 2 ** ((midi_note - 69) / 12)
        return self.freq_to_color(freq)
    
    def chord_to_colors(self, midi_notes: List[int]) -> List[Tuple[int, int, int]]:
        """Get colors for chord"""
        
        return [self.note_to_color(n) for n in midi_notes]


class CymaticVisualizer:
    """Visualize sound as cymatic patterns"""
    
    def __init__(self):
        self.resolution = 100
    
    def generate_pattern(self, freq: float, amplitude: float, 
                       width: int = 100, height: int = 100) -> List[List[float]]:
        """Generate cymatic pattern"""
        
        pattern = []
        
        for y in range(height):
            row = []
            
            for x in range(width):
                # Convert to polar
                cx, cy = width / 2, height / 2
                dx, dy = x - cx, y - cy
                radius = math.sqrt(dx*dx + dy*dy)
                angle = math.atan2(dy, dx)
                
                # Create wave pattern based on frequency
                wave = math.sin(radius * freq / 100 + angle * 2) * amplitude
                
                # Add interference patterns
                wave += math.sin(radius * freq / 150) * amplitude * 0.5
                
                # Clamp
                wave = max(0, min(1, (wave + 1) / 2))
                
                row.append(wave)
            
            pattern.append(row)
        
        return pattern
    
    def generate_standing_wave(self, freq: float, 
                              width: int = 100, height: int = 100) -> List[List[float]]:
        """Generate standing wave pattern"""
        
        pattern = []
        
        for y in range(height):
            row = []
            
            for x in range(width):
                # Standing wave: two waves moving opposite directions
                wave = math.sin(2 * math.pi * freq * x / width) * \
                       math.cos(2 * math.pi * freq * y / height)
                
                # Normalize
                wave = (wave + 1) / 2
                
                row.append(wave)
            
            pattern.append(row)
        
        return pattern
    
    def get_chladni_pattern(self, freq: float, 
                           width: int = 100, height: int = 100) -> List[List[float]]:
        """Generate Chladni pattern (metal plate vibration)"""
        
        pattern = []
        
        for y in range(height):
            row = []
            
            for x in range(width):
                # Chladni: Standing wave nodes
                m, n = 2, 3  # Mode numbers
                
                wave = math.sin(m * math.pi * x / width) * math.sin(n * math.pi * y / height) * \
                       math.sin(2 * math.pi * freq / 100)
                
                # Nodes (where wave = 0) are areas of no vibration
                # Anti-nodes (max) vibrate
                vibration = abs(wave)
                
                row.append(vibration)
            
            pattern.append(row)
        
        return pattern


class SolfeggioFrequencies:
    """Solfeggio frequency mappings"""
    
    FREQUENCIES = {
        'ut': 174,      # Pain relief
        're': 285,      # Healing
        'mi': 396,      # Liberation
        'fa': 417,      # Transformation
        'sol': 528,      # DNA repair
        'la': 639,      # Relationships
        'ti': 741,      # Awakening
        'do_high': 852, # Third eye
        'do_plus': 963, # Crown chakra
    }
    
    # Associated colors
    COLORS = {
        'ut': (255, 100, 100),    # Red
        're': (255, 165, 0),      # Orange
        'mi': (255, 255, 0),      # Yellow
        'fa': (0, 255, 0),        # Green
        'sol': (0, 255, 255),     # Cyan
        'la': (0, 0, 255),        # Blue
        'ti': (128, 0, 255),      # Purple
        'do_high': (255, 0, 255), # Magenta
        'do_plus': (255, 255, 255), # White
    }
    
    # Associated meanings
    MEANINGS = {
        'ut': 'Foundation, Security',
        're': 'Energy, Vitality', 
        'mi': 'Release, Freedom',
        'fa': 'Flow, Change',
        'sol': 'Love, Repair',
        'la': 'Connection, Harmony',
        'ti': 'Clarity, Expression',
        'do_high': 'Intuition, Spirit',
        'do_plus': 'Divine, Unity',
    }
    
    def __init__(self):
        pass
    
    def get_frequency(self, note: str) -> float:
        """Get frequency for solfeggio note"""
        return self.FREQUENCIES.get(note, 440)
    
    def get_color(self, note: str) -> Tuple[int, int, int]:
        """Get color for solfeggio note"""
        return self.COLORS.get(note, (128, 128, 128))
    
    def get_meaning(self, note: str) -> str:
        """Get meaning for solfeggio note"""
        return self.MEANINGS.get(note, 'Unknown')
    
    def get_all(self) -> Dict:
        """Get all solfeggio data"""
        
        result = {}
        
        for note in self.FREQUENCIES:
            result[note] = {
                'frequency': self.FREQUENCIES[note],
                'color': self.COLORS[note],
                'meaning': self.MEANINGS[note]
            }
        
        return result


class BinauralBeats:
    """Generate binaural beats"""
    
    BASE_FREQUENCIES = {
        'delta': {'min': 0.5, 'max': 4, 'color': (0, 0, 139)},
        'theta': {'min': 4, 'max': 8, 'color': (65, 105, 225)},
        'alpha': {'min': 8, 'max': 14, 'color': (0, 100, 0)},
        'beta': {'min': 14, 'max': 30, 'color': (255, 215, 0)},
        'gamma': {'min': 30, 'max': 100, 'color': (139, 0, 0)},
    }
    
    def __init__(self):
        pass
    
    def generate_beats(self, base_freq: float, beat_freq: float,
                       duration: float, sample_rate: int = 44100) -> Tuple[List[float], List[float]]:
        """Generate binaural beat (left/right channels)"""
        
        samples = int(duration * sample_rate)
        
        left = []
        right = []
        
        for i in range(samples):
            t = i / sample_rate
            
            # Left ear: base frequency
            left.append(math.sin(2 * math.pi * base_freq * t))
            
            # Right ear: base + beat frequency (difference = beat freq)
            right.append(math.sin(2 * math.pi * (base_freq + beat_freq) * t))
        
        return left, right
    
    def get_brain_state(self, beat_freq: float) -> Dict:
        """Get brain state for beat frequency"""
        
        for state, data in self.BASE_FREQUENCIES.items():
            if data['min'] <= beat_freq <= data['max']:
                return {
                    'state': state,
                    'description': self._get_state_description(state),
                    'color': data['color']
                }
        
        return {'state': 'unknown', 'description': 'Unknown', 'color': (128, 128, 128)}
    
    def _get_state_description(self, state: str) -> str:
        """Get description of brain state"""
        
        descriptions = {
            'delta': 'Deep sleep, healing',
            'theta': 'Meditation, creativity',
            'alpha': 'Relaxed focus',
            'beta': 'Active thinking',
            'gamma': 'Peak awareness'
        }
        
        return descriptions.get(state, '')


class HarmonicVisualizer:
    """Visualize harmonics and overtones"""
    
    def __init__(self):
        self.harmonic_ratios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    def get_harmonic_series(self, fundamental: float) -> List[float]:
        """Get harmonic series"""
        
        return [fundamental * ratio for ratio in self.harmonic_ratios]
    
    def get_harmonic_colors(self, fundamental: float) -> List[Tuple[int, int, int]]:
        """Get colors for harmonic series"""
        
        mapper = FrequencyColorMapper()
        
        harmonics = self.get_harmonic_series(fundamental)
        
        return [mapper.freq_to_color(h) for h in harmonics]
    
    def visualize_spectrum(self, frequencies: List[float], 
                          amplitudes: List[float],
                          width: int = 100) -> List[Tuple[float, Tuple[int, int, int]]]:
        """Visualize frequency spectrum"""
        
        result = []
        
        mapper = FrequencyColorMapper()
        
        for freq, amp in zip(frequencies, amplitudes):
            color = mapper.freq_to_color(freq)
            result.append((amp, color))
        
        return result
    
    def get_overtone_strengths(self, instrument_type: str) -> Dict[str, float]:
        """Get overtone strengths for instruments"""
        
        profiles = {
            'piano': {1: 1.0, 2: 0.5, 3: 0.25, 4: 0.125},
            'violin': {1: 1.0, 2: 0.8, 3: 0.6, 4: 0.4},
            'flute': {1: 1.0, 2: 0.3, 3: 0.1, 4: 0.05},
            'guitar': {1: 1.0, 2: 0.6, 3: 0.3, 4: 0.15},
            'voice': {1: 1.0, 2: 0.7, 3: 0.5, 4: 0.3},
        }
        
        return profiles.get(instrument_type, {1: 1.0})


class VisualWaveformGenerator:
    """Generate visual waveforms"""
    
    WAVEFORMS = ['sine', 'square', 'saw', 'triangle', 'noise', 'organic']
    
    def __init__(self):
        pass
    
    def generate_waveform(self, waveform: str, width: int = 100,
                         amplitude: float = 1.0) -> List[float]:
        """Generate waveform shape for visualization"""
        
        if waveform == 'sine':
            return [amplitude * math.sin(2 * math.pi * x / width) for x in range(width)]
        
        elif waveform == 'square':
            return [amplitude if x < width/2 else -amplitude for x in range(width)]
        
        elif waveform == 'saw':
            return [amplitude * (2 * (x / width) - 1) for x in range(width)]
        
        elif waveform == 'triangle':
            return [amplitude * (2 * abs(2 * x / width - 1) - 1) for x in range(width)]
        
        elif waveform == 'noise':
            return [amplitude * random.uniform(-1, 1) for _ in range(width)]
        
        elif waveform == 'organic':
            # Combination
            wave = []
            for x in range(width):
                w = math.sin(2 * math.pi * x / width)
                w += 0.3 * math.sin(4 * math.pi * x / width)
                w += 0.1 * random.uniform(-1, 1)
                wave.append(w * amplitude)
            return wave
        
        return [0] * width
    
    def generate_envelope(self, attack: float, decay: float, 
                         sustain: float, release: float,
                         width: int = 100) -> List[float]:
        """Generate ADSR envelope shape"""
        
        # Find positions
        total = attack + decay + sustain * 0.5 + release
        a_end = int(attack / total * width)
        d_end = a_end + int(decay / total * width)
        s_end = d_end + int(sustain * 0.5 / total * width)
        
        envelope = []
        
        for x in range(width):
            if x <= a_end:
                # Attack
                envelope.append(x / a_end if a_end > 0 else 1)
            elif x <= d_end:
                # Decay
                t = (x - a_end) / (d_end - a_end) if d_end > a_end else 0
                envelope.append(1 - (1 - sustain) * t)
            elif x <= s_end:
                # Sustain
                envelope.append(sustain)
            else:
                # Release
                t = (x - s_end) / (width - s_end) if width > s_end else 0
                envelope.append(sustain * (1 - t))
        
        return envelope


class ColorTheoryEngine:
    """Color harmony based on music"""
    
    # Scale to color mapping
    SCALE_COLORS = {
        'major': {'primary': (255, 255, 0), 'mood': 'Bright, Happy'},
        'minor': {'primary': (0, 0, 255), 'mood': 'Dark, Sad'},
        'dorian': {'primary': (0, 255, 255), 'mood': 'Mysterious'},
        'phrygian': {'primary': (255, 0, 255), 'mood': 'Exotic'},
        'lydian': {'primary': (127, 255, 0), 'mood': 'Dreamy'},
        'mixolydian': {'primary': (255, 127, 0), 'mood': 'Funky'},
        'pentatonic': {'primary': (0, 255, 127), 'mood': 'Natural'},
        'blues': {'primary': (0, 0, 139), 'mood': 'Soulful'},
    }
    
    # Chord to color mapping
    CHORD_COLORS = {
        'maj': (255, 255, 0),     # Yellow - bright
        'min': (100, 100, 255),  # Blue - cool
        'dim': (255, 0, 0),      # Red - tense
        'aug': (255, 127, 0),   # Orange - warm
        'sus4': (0, 255, 255),   # Cyan - floating
        '7': (255, 0, 255),     # Magenta - complex
    }
    
    def __init__(self):
        pass
    
    def get_scale_palette(self, scale: str) -> Dict:
        """Get color palette for scale"""
        
        base = self.SCALE_COLORS.get(scale, {'primary': (128, 128, 128), 'mood': 'Neutral'})
        
        # Generate complementary, analogous, triadic
        r, g, b = base['primary']
        
        return {
            'primary': base['primary'],
            'complementary': (255 - r, 255 - g, 255 - b),
            'analogous_1': (max(0, r-30), max(0, g-30), max(0, b-30)),
            'analogous_2': (min(255, r+30), min(255, g+30), min(255, b+30)),
            'mood': base['mood']
        }
    
    def get_chord_palette(self, chord_type: str) -> Tuple[int, int, int]:
        """Get color for chord type"""
        
        return self.CHORD_COLORS.get(chord_type, (128, 128, 128))
    
    def generate_gradient(self, start_color: Tuple[int, int, int],
                          end_color: Tuple[int, int, int],
                          steps: int = 10) -> List[Tuple[int, int, int]]:
        """Generate color gradient"""
        
        gradient = []
        
        for i in range(steps):
            t = i / (steps - 1)
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            
            gradient.append((r, g, b))
        
        return gradient


class MusicColorCymaticsEngine:
    """Complete engine integrating all"""
    
    def __init__(self):
        self.color_mapper = FrequencyColorMapper()
        self.cymatic = CymaticVisualizer()
        self.solfeggio = SolfeggioFrequencies()
        self.binaural = BinauralBeats()
        self.harmonic = HarmonicVisualizer()
        self.waveform = VisualWaveformGenerator()
        self.color_theory = ColorTheoryEngine()
    
    def analyze_chord(self, midi_notes: List[int]) -> Dict:
        """Complete analysis of chord"""
        
        colors = self.color_mapper.chord_to_colors(midi_notes)
        
        # Get frequencies
        freqs = [440 * 2 ** ((n - 69) / 12) for n in midi_notes]
        
        # Get cymatic pattern
        if freqs:
            pattern = self.cymatic.generate_pattern(freqs[0], 0.8)
        
        # Get harmonic series
        if freqs:
            harmonics = self.harmonic.get_harmonic_series(freqs[0])
            harmonic_colors = self.harmonic.get_harmonic_colors(freqs[0])
        
        return {
            'midi_notes': midi_notes,
            'frequencies': freqs,
            'colors': colors,
            'cymatic_pattern': pattern if freqs else None,
            'harmonics': harmonics if freqs else [],
            'harmonic_colors': harmonic_colors if freqs else []
        }
    
    def create_solfeggio_track(self, solfeggio_note: str, duration: float) -> Dict:
        """Create track using solfeggio frequency"""
        
        freq = self.solfeggio.get_frequency(solfeggio_note)
        color = self.solfeggio.get_color(solfeggio_note)
        meaning = self.solfeggio.get_meaning(solfeggio_note)
        
        # Generate audio
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        audio = [math.sin(2 * math.pi * freq * t / sample_rate) for t in range(samples)]
        
        return {
            'note': solfeggio_note,
            'frequency': freq,
            'color': color,
            'meaning': meaning,
            'audio': audio
        }
    
    def create_binaural_track(self, base_freq: float, target_state: str,
                             duration: float) -> Dict:
        """Create binaural beat track"""
        
        # Determine beat frequency for target state
        state_info = self.binaural.get_brain_state(target_state)
        
        beat_freq = (state_info.get('min', 10) + state_info.get('max', 10)) / 2
        
        left, right = self.binaural.generate_beats(base_freq, beat_freq, duration)
        
        return {
            'base_freq': base_freq,
            'beat_freq': beat_freq,
            'brain_state': state_info,
            'left_channel': left,
            'right_channel': right
        }
    
    def generate_visualization(self, audio: List[float], width: int = 100,
                              height: int = 100) -> Dict:
        """Generate complete visualization"""
        
        # Get waveform
        waveform = self.waveform.generate_waveform('organic', width)
        
        # Get frequency data (simplified)
        import struct
        avg = sum(abs(x) for x in audio) / len(audio) if audio else 0
        
        # Map to color
        color = self.color_mapper.freq_to_color(440)
        
        return {
            'waveform': waveform,
            'avg_amplitude': avg,
            'dominant_color': color,
            'height': height,
            'width': width
        }


def demo():
    """Demo the complete engine"""
    
    print("=" * 60)
    print("  MUSIC-COLOR-CYMATICS ENGINE")
    print("=" * 60)
    
    engine = MusicColorCymaticsEngine()
    
    print("\n[Frequency to Color]")
    for freq in [261, 329, 392, 440, 523]:
        color = engine.color_mapper.freq_to_color(freq)
        print("  %d Hz -> RGB%s" % (freq, color))
    
    print("\n[Chord Analysis: C Major]")
    analysis = engine.analyze_chord([60, 64, 67])  # C, E, G
    print("  Notes: %s" % analysis['midi_notes'])
    print("  Colors: %s" % [str(c)[:30] for c in analysis['colors'][:3]])
    
    print("\n[Solfeggio Frequencies]")
    solf = engine.solfeggio.get_all()
    for note, data in list(solf.items())[:3]:
        print("  %s: %.0f Hz -> %s" % (note, data['frequency'], data['meaning']))
    
    print("\n[Binaural Beats: Alpha]")
    binaural = engine.create_binaural_track(200, 'alpha', 1.0)
    print("  Base: %.0f Hz, Beat: %.1f Hz" % (binaural['base_freq'], binaural['beat_freq']))
    print("  State: %s" % binaural['brain_state']['state'])
    
    print("\n[Color Theory: Major Scale]")
    palette = engine.color_theory.get_scale_palette('major')
    print("  Primary: %s" % (palette['primary'],))
    print("  Mood: %s" % palette['mood'])
    
    print("\n" + "=" * 60)
    print("  COMPLETE ENGINE READY!")
    print("=" * 60)


if __name__ == "__main__":
    demo()