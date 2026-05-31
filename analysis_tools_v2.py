"""
MUSIC ANALYSIS TOOLS V2 - Level 2.2-2.5
=========================================
- BPM Detection (tempo)
- Key Detection (musical key)
- Scale Finder
- Reference Match

Building on what we have - making analysis better!
"""

import math
import random
from typing import List, Dict, Tuple, Optional


class BPMDetector:
    """Detect BPM from audio"""
    
    @staticmethod
    def detect_bpm(audio: List[float], sample_rate: int = 44100) -> float:
        """Detect BPM using autocorrelation"""
        
        # Convert to mono if stereo
        if isinstance(audio[0], (list, tuple)):
            audio = [sum(ch)/len(ch) for ch in audio]
        
        # Simple onset detection
        window_size = 1024
        onset_strength = []
        
        for i in range(0, len(audio) - window_size, window_size):
            window = audio[i:i+window_size]
            energy = sum(abs(s) for s in window)
            onset_strength.append(energy)
        
        # Autocorrelation
        min_bpm = 60
        max_bpm = 200
        min_lag = int(60 * sample_rate / max_bpm / window_size)
        max_lag = int(60 * sample_rate / min_bpm / window_size)
        
        best_corr = 0
        best_lag = min_lag
        
        for lag in range(min_lag, max_lag):
            correlation = 0
            for i in range(len(onset_strength) - lag):
                correlation += onset_strength[i] * onset_strength[i + lag]
            
            if correlation > best_corr:
                best_corr = correlation
                best_lag = lag
        
        bpm = 60 * sample_rate / (best_lag * window_size)
        
        # Normalize to standard BPM range
        while bpm < 60:
            bpm *= 2
        while bpm > 200:
            bpm /= 2
        
        return round(bpm, 1)
    
    @staticmethod
    def detect_bpm_from_onsets(audio: List[float], sample_rate: int = 44100) -> float:
        """Alternative BPM detection using onset peaks"""
        
        # Find onset peaks
        onset_times = []
        window = int(sample_rate * 0.02)  # 20ms windows
        
        energies = []
        for i in range(0, len(audio), window):
            energies.append(sum(abs(audio[i:i+window])))
        
        # Find peaks
        threshold = sum(energies) / len(energies) * 1.5
        for i in range(1, len(energies) - 1):
            if energies[i] > threshold and energies[i] > energies[i-1] and energies[i] > energies[i+1]:
                onset_times.append(i * window / sample_rate)
        
        if len(onset_times) < 2:
            return 120.0  # Default
        
        # Calculate average interval
        intervals = []
        for i in range(1, len(onset_times)):
            interval = onset_times[i] - onset_times[i-1]
            if 0.2 < interval < 2.0:  # Reasonable intervals
                intervals.append(interval)
        
        if not intervals:
            return 120.0
        
        avg_interval = sum(intervals) / len(intervals)
        bpm = 60.0 / avg_interval
        
        # Normalize
        while bpm < 60:
            bpm *= 2
        while bpm > 200:
            bpm /= 2
        
        return round(bpm, 1)


class KeyDetector:
    """Detect musical key"""
    
    # Pitch class profile for different keys
    PROFILES = {
        'major': [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
        'minor': [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17],
    }
    
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    @classmethod
    def detect_key(cls, audio: List[float], sample_rate: int = 44100) -> Dict:
        """Detect key from audio"""
        
        # Simple chromagram calculation
        chromagram = [0] * 12
        
        # Analyze audio in chunks
        chunk_size = int(sample_rate * 0.1)  # 100ms chunks
        
        for i in range(0, len(audio) - chunk_size, chunk_size):
            chunk = audio[i:i+chunk_size]
            
            # Estimate pitch class energy
            for pitch_class in range(12):
                freq = 440 * (2 ** ((pitch_class - 9) / 12))
                # Simple dot product with sin/cos
                for j in range(0, len(chunk), 100):
                    t = j / sample_rate
                    phase = 2 * math.pi * freq * t
                    chromagram[pitch_class] += abs(chunk[j]) * abs(math.sin(phase))
        
        # Normalize
        max_val = max(chromagram) if max(chromagram) > 0 else 1
        chromagram = [c / max_val for c in chromagram]
        
        # Compare with profiles
        best_key = 'C'
        best_mode = 'major'
        best_score = -1
        
        for root in range(12):
            for mode in ['major', 'minor']:
                profile = cls.PROFILES[mode]
                
                # Circular shift to match root
                shifted = [profile[(i - root) % 12] for i in range(12)]
                
                # Correlation
                score = sum(shifted[i] * chromagram[i] for i in range(12))
                
                if score > best_score:
                    best_score = score
                    best_key = cls.NOTE_NAMES[root]
                    best_mode = mode
        
        return {
            'key': best_key,
            'mode': best_mode,
            'confidence': round(best_score / 10, 2)  # Normalize
        }
    
    @classmethod
    def get_chord_from_key(cls, key: str, mode: str = 'major') -> List[str]:
        """Get chord progression for key"""
        
        if mode == 'major':
            return ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
        else:
            return ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII']


class ScaleFinder:
    """Find scale from notes"""
    
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'pentatonic_major': [0, 2, 4, 7, 9],
        'pentatonic_minor': [0, 3, 5, 7, 10],
        'blues': [0, 3, 5, 6, 7, 10],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'phrygian': [0, 1, 3, 5, 7, 8, 10],
        'lydian': [0, 2, 4, 6, 7, 9, 11],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    }
    
    @classmethod
    def find_scale(cls, notes: List[int]) -> Dict:
        """Find scale from notes"""
        
        if not notes:
            return {'root': 'C', 'scale': 'major', 'match': 0}
        
        # Get unique pitch classes
        pitch_classes = set(n % 12 for n in notes)
        
        best_root = 0
        best_scale = 'major'
        best_match = 0
        
        for root in range(12):
            for scale_name, intervals in cls.SCALES.items():
                # Create scale from root
                scale_notes = set((root + i) % 12 for i in intervals)
                
                # Calculate match
                matches = len(pitch_classes & scale_notes)
                match_score = matches / len(pitch_classes) if pitch_classes else 0
                
                if match_score > best_match:
                    best_match = match_score
                    best_root = root
                    best_scale = scale_name
        
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        return {
            'root': note_names[best_root],
            'scale': best_scale,
            'match': round(best_match, 2)
        }
    
    @classmethod
    def get_available_notes(cls, root: str, scale: str) -> List[int]:
        """Get all notes in scale"""
        note_names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
                     'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        
        root_idx = note_names.get(root.upper(), 0)
        intervals = cls.SCALES.get(scale, cls.SCALES['major'])
        
        notes = []
        for octave in range(3, 6):  # 3 octaves
            for interval in intervals:
                notes.append(60 + root_idx + interval + (octave - 4) * 12)
        
        return notes


class ReferenceMatch:
    """Compare audio to reference tracks"""
    
    @staticmethod
    def analyze_reference(audio: List[float]) -> Dict:
        """Analyze reference audio"""
        
        # Handle stereo to mono
        if audio and isinstance(audio[0], (list, tuple)):
            audio = [sum(ch)/len(ch) for ch in audio]
        
        # Simple analysis
        audio_list = list(audio)
        rms = math.sqrt(sum(a*a for a in audio_list)) / len(audio_list) if audio_list else 0
        peak = max(abs(a) for a in audio_list) if audio_list else 0
        
        # Estimate frequency content
        quarter = len(audio_list) // 4
        bass_energy = sum(abs(a) for a in audio_list[:quarter])
        mid_energy = sum(abs(a) for a in audio_list[quarter:quarter*2])
        high_energy = sum(abs(a) for a in audio_list[quarter*2:])
        
        total = bass_energy + mid_energy + high_energy
        
        return {
            'loudness_rms': round(rms, 4),
            'peak': round(peak, 4),
            'bass_ratio': round(bass_energy / total, 2) if total > 0 else 0,
            'mid_ratio': round(mid_energy / total, 2) if total > 0 else 0,
            'high_ratio': round(high_energy / total, 2) if total > 0 else 0,
            'dynamic_range': round(peak / rms, 2) if rms > 0 else 0,
        }
    
    @staticmethod
    def suggest_settings(reference: Dict) -> Dict:
        """Suggest mix settings based on reference"""
        
        # Bass-heavy reference = more bass
        bass_gain = 0.5 + (reference.get('bass_ratio', 0.3) - 0.3)
        
        # High energy = less high boost
        high_gain = 0.5 - (reference.get('high_ratio', 0.3) - 0.3)
        
        # Dynamic range affects compression
        dyn_range = reference.get('dynamic_range', 6)
        if dyn_range > 10:
            compression = 'gentle'
        elif dyn_range > 6:
            compression = 'moderate'
        else:
            compression = 'aggressive'
        
        return {
            'eq': {
                'bass': round(bass_gain, 2),
                'mid': 0,
                'high': round(high_gain, 2),
            },
            'compression': compression,
            'target_loudness': -14 if dyn_range > 8 else -10,
        }


def demo():
    print("=" * 60)
    print("  MUSIC ANALYSIS TOOLS V2 - Level 2.2-2.5")
    print("=" * 60)
    
    print("\n=== BPM DETECTION ===")
    # Generate test audio with known tempo (140 BPM)
    import wave
    sample_rate = 44100
    bpm = 140
    duration = 5
    samples = int(sample_rate * duration)
    
    # Create audio with beats at 140 BPM
    audio = []
    beat_interval = 60 / bpm
    for i in range(samples):
        t = i / sample_rate
        # Kick on every beat
        beat_phase = (t % beat_interval) / beat_interval
        if beat_phase < 0.1:
            freq = 60 * (1 - beat_phase * 10)
            audio.append(math.sin(2 * math.pi * freq * t) * (1 - beat_phase * 10))
        else:
            audio.append(0)
    
    detected_bpm = BPMDetector.detect_bpm(audio, sample_rate)
    print(f"  Input BPM: {bpm}, Detected: {detected_bpm}")
    
    print("\n=== KEY DETECTION ===")
    # Simple test - major key
    test_notes = [261.63, 329.63, 392.00]  # C major triad
    test_audio = [math.sin(2 * math.pi * n * (i/sample_rate)) for n in test_notes for i in range(10000)]
    key_result = KeyDetector.detect_key(test_audio, sample_rate)
    print(f"  Detected: {key_result['key']} {key_result['mode']}")
    print(f"  Chord progression: {KeyDetector.get_chord_from_key(key_result['key'], key_result['mode'])}")
    
    print("\n=== SCALE FINDER ===")
    # C major scale notes
    c_major_notes = [60, 62, 64, 65, 67, 69, 71, 72]
    scale_result = ScaleFinder.find_scale(c_major_notes)
    print(f"  Found: {scale_result['root']} {scale_result['scale']} (match: {scale_result['match']})")
    print(f"  Available notes: {ScaleFinder.get_available_notes(scale_result['root'], scale_result['scale'])[:5]}...")
    
    print("\n=== REFERENCE MATCH ===")
    ref_audio = [math.sin(2 * math.pi * 100 * i/sample_rate) * 0.5 for i in range(44100)]
    ref_analysis = ReferenceMatch.analyze_reference(ref_audio)
    print(f"  Reference analysis: {ref_analysis}")
    settings = ReferenceMatch.suggest_settings(ref_analysis)
    print(f"  Suggested settings: {settings}")
    
    print("\n" + "=" * 60)
    print("  ANALYSIS TOOLS V2 - Level 2.2-2.5 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()