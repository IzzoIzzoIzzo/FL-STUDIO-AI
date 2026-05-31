"""
AI AGENTS V2 - Level 3.2
=========================
- Mastering Agent
- Mixing Agent  
- Arrangement Agent
- Sound Design Agent

Building on what we have - AI that helps!
"""

import random
import math
from typing import Dict, List, Optional


class MasteringAgent:
    """AI Mastering Agent"""
    
    def __init__(self):
        self.target_loudness = -14  # LUFS
        self.target_crest = 3.0     # Crest factor
    
    def analyze(self, audio: List[float]) -> Dict:
        """Analyze audio for mastering"""
        
        # Calculate metrics
        rms = math.sqrt(sum(a*a for a in audio) / len(audio)) if audio else 0
        peak = max(abs(a) for a in audio) if audio else 0
        
        # Frequency bands
        third = len(audio) // 3
        bass = sum(abs(a) for a in audio[:third])
        mid = sum(abs(a) for a in audio[third:third*2])
        high = sum(abs(a) for a in audio[third*2:])
        total = bass + mid + high
        
        return {
            'loudness_rms': round(20 * math.log10(rms + 0.0001), 1),
            'peak_db': round(20 * math.log10(peak + 0.0001), 1),
            'bass_ratio': round(bass / total * 100, 1) if total > 0 else 0,
            'mid_ratio': round(mid / total * 100, 1) if total > 0 else 0,
            'high_ratio': round(high / total * 100, 1) if total > 0 else 0,
            'dynamic_range': round(peak / rms, 1) if rms > 0 else 0,
        }
    
    def suggest_settings(self, analysis: Dict) -> Dict:
        """Suggest mastering settings"""
        
        settings = {'eq': {}, 'compressor': {}, 'limiter': {}}
        
        # EQ suggestions
        if analysis['bass_ratio'] > 40:
            settings['eq']['low'] = -2
        elif analysis['bass_ratio'] < 25:
            settings['eq']['low'] = 2
        
        if analysis['high_ratio'] > 25:
            settings['eq']['high'] = -1
        elif analysis['high_ratio'] < 15:
            settings['eq']['high'] = 1
        
        # Compression
        if analysis['dynamic_range'] > 10:
            settings['compressor']['threshold'] = -20
            settings['compressor']['ratio'] = 3
        elif analysis['dynamic_range'] < 6:
            settings['compressor']['threshold'] = -15
            settings['compressor']['ratio'] = 1.5
        
        # Limiter
        settings['limiter']['ceiling'] = -0.5
        
        return settings
    
    def apply(self, audio: List[float], settings: Dict) -> List[float]:
        """Apply mastering chain"""
        # Simplified - just normalize for now
        max_val = max(abs(a) for a in audio) if audio else 1
        if max_val > 0:
            return [a * 0.9 / max_val for a in audio]
        return audio


class MixingAgent:
    """AI Mixing Assistant Agent"""
    
    def __init__(self):
        self.tracks = {}
    
    def add_track(self, name: str, audio: List[float]):
        """Add track to mix"""
        rms = math.sqrt(sum(a*a for a in audio) / len(audio)) if audio else 0
        self.tracks[name] = {
            'audio': audio,
            'rms': rms,
            'peak': max(abs(a) for a in audio) if audio else 0,
        }
    
    def analyze_mix(self) -> Dict:
        """Analyze entire mix"""
        
        if not self.tracks:
            return {'balance': [], 'issues': []}
        
        rms_values = [t['rms'] for t in self.tracks.values()]
        max_rms = max(rms_values) if rms_values else 1
        
        balance = []
        issues = []
        
        for name, track in self.tracks.items():
            # Calculate relative level
            relative_level = track['rms'] / max_rms if max_rms > 0 else 0
            
            if relative_level < 0.3:
                issues.append(f"{name} is too quiet")
            elif relative_level > 0.9:
                issues.append(f"{name} might be clipping")
            
            balance.append({
                'track': name,
                'level_db': round(20 * math.log10(relative_level + 0.0001), 1),
            })
        
        return {
            'balance': balance,
            'issues': issues,
            'track_count': len(self.tracks)
        }
    
    def suggest_fixes(self, analysis: Dict) -> List[Dict]:
        """Suggest mixing fixes"""
        
        fixes = []
        
        for issue in analysis['issues']:
            if 'too quiet' in issue:
                track = issue.split(' is')[0]
                fixes.append({
                    'action': 'increase_gain',
                    'track': track,
                    'amount_db': 3
                })
            elif 'clipping' in issue:
                track = issue.split(' might')[0]
                fixes.append({
                    'action': 'reduce_gain',
                    'track': track,
                    'amount_db': -3
                })
        
        # General suggestions
        fixes.append({
            'action': 'solo_check',
            'track': 'all',
            'description': 'Solo each track to check clarity'
        })
        
        return fixes


class ArrangementAgent:
    """AI Arrangement Assistant"""
    
    def __init__(self):
        self.history = []
    
    def analyze_structure(self, sections: List[Dict]) -> Dict:
        """Analyze current structure"""
        
        if not sections:
            return {'issues': [], 'score': 0}
        
        issues = []
        score = 50
        
        # Check variety
        section_names = [s.get('name', '') for s in sections]
        if len(set(section_names)) < 3:
            issues.append('Not enough variety in sections')
            score -= 10
        
        # Check energy flow
        energies = [s.get('energy', 0.5) for s in sections]
        for i in range(len(energies) - 1):
            if abs(energies[i+1] - energies[i]) > 0.5:
                score += 5  # Good dynamic changes
        
        # Check length
        avg_bars = sum(s.get('bars', 8) for s in sections) / len(sections)
        if avg_bars < 4:
            issues.append('Sections may be too short')
            score -= 10
        elif avg_bars > 16:
            issues.append('Sections may be too long')
            score -= 5
        
        return {
            'issues': issues,
            'score': max(0, min(100, score)),
            'energy_flow': energies
        }
    
    def suggest_improvements(self, analysis: Dict) -> List[str]:
        """Suggest arrangement improvements"""
        
        suggestions = []
        
        if analysis['score'] < 60:
            suggestions.append('Add more section variety')
            suggestions.append('Consider a bridge section')
        
        if len(analysis.get('energy_flow', [])) < 3:
            suggestions.append('Build more energy progression')
        
        for issue in analysis.get('issues', []):
            suggestions.append(f'Fix: {issue}')
        
        if not suggestions:
            suggestions.append('Structure looks good!')
        
        return suggestions


class SoundDesignAgent:
    """AI Sound Design Agent"""
    
    # Sound categories
    CATEGORIES = {
        'lead': ['supersaw', 'fm_lead', 'pluck', 'acid'],
        'pad': ['ambient', 'cinematic', 'warm', 'shimmer'],
        'bass': ['sub', '808', 'reese', 'acid'],
        'FX': ['riser', 'impact', 'sweep', 'noise'],
    }
    
    def suggest_sound(self, genre: str, role: str = 'lead') -> Dict:
        """Suggest sound based on genre"""
        
        genre_sounds = {
            'trap': {'lead': 'supersaw', 'bass': '808', 'FX': 'riser'},
            'house': {'lead': 'pluck', 'bass': 'sub', 'FX': 'sweep'},
            'hiphop': {'lead': 'fm_lead', 'bass': 'sub', 'FX': 'impact'},
            'dubstep': {'lead': 'supersaw', 'bass': 'reese', 'FX': 'riser'},
            'ambient': {'lead': 'ambient', 'pad': 'cinematic', 'FX': 'sweep'},
        }
        
        sounds = genre_sounds.get(genre, genre_sounds['house'])
        
        return {
            'suggested_sound': sounds.get(role, 'lead'),
            'category': self.CATEGORIES.get(role, self.CATEGORIES['lead']),
            'genre': genre
        }
    
    def suggest_parameters(self, sound: str, genre: str) -> Dict:
        """Suggest parameters for sound"""
        
        presets = {
            'supersaw': {'detune': 10, 'filter': 'lowpass', 'cutoff': 2500, 'resonance': 0.3},
            '808': {'sub': True, 'distortion': 0.5, 'decay': 0.4},
            'ambient': {'reverb': 0.7, 'filter': 'lowpass', 'attack': 0.5},
            'pluck': {'decay': 0.3, 'filter': 'lowpass', 'resonance': 0.2},
        }
        
        return presets.get(sound, {})


def demo():
    print("=" * 60)
    print("  AI AGENTS V2 - Level 3.2")
    print("=" * 60)
    
    # Mastering Agent
    print("\n=== MASTERING AGENT ===")
    master = MasteringAgent()
    test_audio = [math.sin(440 * 2 * math.pi * i/44100) * 0.5 for i in range(44100)]
    analysis = master.analyze(test_audio)
    print(f"  Analysis: {analysis}")
    settings = master.suggest_settings(analysis)
    print(f"  Suggested: {settings}")
    
    # Mixing Agent
    print("\n=== MIXING AGENT ===")
    mixer = MixingAgent()
    mixer.add_track('kick', [0.8] * 4410)
    mixer.add_track('snare', [0.3] * 4410)
    mixer.add_track('bass', [0.5] * 4410)
    mixer.add_track('pad', [0.2] * 4410)
    mix_analysis = mixer.analyze_mix()
    print(f"  Mix: {mix_analysis['track_count']} tracks")
    print(f"  Issues: {mix_analysis['issues']}")
    fixes = mixer.suggest_fixes(mix_analysis)
    print(f"  Fixes: {len(fixes)} suggested")
    
    # Arrangement Agent
    print("\n=== ARRANGEMENT AGENT ===")
    arranger = ArrangementAgent()
    sections = [
        {'name': 'intro', 'bars': 4, 'energy': 0.3},
        {'name': 'verse', 'bars': 8, 'energy': 0.6},
        {'name': 'chorus', 'bars': 8, 'energy': 1.0},
        {'name': 'verse', 'bars': 8, 'energy': 0.6},
        {'name': 'chorus', 'bars': 8, 'energy': 1.0},
    ]
    arr_analysis = arranger.analyze_structure(sections)
    print(f"  Score: {arr_analysis['score']}/100")
    print(f"  Issues: {arr_analysis['issues']}")
    suggestions = arranger.suggest_improvements(arr_analysis)
    print(f"  Suggestions: {suggestions[:2]}...")
    
    # Sound Design Agent
    print("\n=== SOUND DESIGN AGENT ===")
    sound_agent = SoundDesignAgent()
    sound = sound_agent.suggest_sound('trap', 'lead')
    print(f"  Suggested: {sound}")
    params = sound_agent.suggest_parameters('supersaw', 'trap')
    print(f"  Parameters: {params}")
    
    print("\n" + "=" * 60)
    print("  AI AGENTS V2 - Level 3.2 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()