"""
PRESET MANAGER - Save/Load System
==================================
Save and load synthesizer presets, drum kits, effects chains, and full project states.
"""

import json
import os
import struct
import wave
from typing import Dict, List, Optional, Any


class PresetManager:
    """Save and load all types of presets"""
    
    def __init__(self, preset_dir: str = 'presets'):
        self.preset_dir = preset_dir
        os.makedirs(preset_dir, exist_ok=True)
    
    def save_json(self, data: Dict, filename: str) -> str:
        """Save data as JSON"""
        path = os.path.join(self.preset_dir, filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return path
    
    def load_json(self, filename: str) -> Dict:
        """Load data from JSON"""
        path = os.path.join(self.preset_dir, filename)
        with open(path, 'r') as f:
            return json.load(f)
    
    def save_synth_preset(self, name: str, params: Dict) -> str:
        """Save synth preset"""
        preset = {
            'type': 'synth',
            'name': name,
            'oscillators': params.get('oscillators', []),
            'filter': params.get('filter', {}),
            'envelope': params.get('envelope', {}),
            'effects': params.get('effects', []),
            'lfo': params.get('lfo', {}),
        }
        return self.save_json(preset, f'synth_{name}.json')
    
    def load_synth_preset(self, name: str) -> Dict:
        """Load synth preset"""
        return self.load_json(f'synth_{name}.json')
    
    def save_drum_kit(self, name: str, kit: Dict) -> str:
        """Save drum kit"""
        preset = {
            'type': 'drum_kit',
            'name': name,
            'kit': kit,
        }
        return self.save_json(preset, f'kit_{name}.json')
    
    def load_drum_kit(self, name: str) -> Dict:
        """Load drum kit"""
        return self.load_json(f'kit_{name}.json')
    
    def save_effect_chain(self, name: str, chain: List[Dict]) -> str:
        """Save effects chain"""
        preset = {
            'type': 'effect_chain',
            'name': name,
            'chain': chain,
        }
        return self.save_json(preset, f'fx_{name}.json')
    
    def load_effect_chain(self, name: str) -> List[Dict]:
        """Load effects chain"""
        data = self.load_json(f'fx_{name}.json')
        return data.get('chain', [])
    
    def save_project(self, name: str, project: Dict) -> str:
        """Save full project state"""
        preset = {
            'type': 'project',
            'name': name,
            'version': '1.0',
            'bpm': project.get('bpm', 120),
            'key': project.get('key', 'C'),
            'tracks': project.get('tracks', []),
            'patterns': project.get('patterns', {}),
            'mixer': project.get('mixer', {}),
            'master': project.get('master', {}),
        }
        return self.save_json(preset, f'project_{name}.json')
    
    def load_project(self, name: str) -> Dict:
        """Load full project"""
        return self.load_json(f'project_{name}.json')
    
    def list_presets(self, filter_type: str = None) -> List[str]:
        """List all saved presets"""
        files = []
        for f in os.listdir(self.preset_dir):
            if f.endswith('.json'):
                try:
                    data = json.load(open(os.path.join(self.preset_dir, f)))
                    if filter_type is None or data.get('type') == filter_type:
                        files.append(f.replace('.json', ''))
                except:
                    pass
        return files
    
    def delete_preset(self, filename: str):
        """Delete a preset"""
        path = os.path.join(self.preset_dir, filename)
        if os.path.exists(path):
            os.remove(path)
    
    def export_binary_preset(self, name: str, data: bytes) -> str:
        """Export preset as binary file"""
        path = os.path.join(self.preset_dir, f'{name}.bin')
        with open(path, 'wb') as f:
            f.write(data)
        return path
    
    def import_binary_preset(self, name: str) -> bytes:
        """Import preset from binary file"""
        path = os.path.join(self.preset_dir, f'{name}.bin')
        with open(path, 'rb') as f:
            return f.read()
    
    def save_sample(self, name: str, audio: List[float], sample_rate: int = 44100) -> str:
        """Save audio sample as WAV"""
        os.makedirs(self.preset_dir, exist_ok=True)
        
        path = os.path.join(self.preset_dir, f'{name}.wav')
        max_val = max(abs(s) for s in audio) if audio else 1
        if max_val > 0:
            audio = [s * 0.95 / max_val for s in audio]
        
        with wave.open(path, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            for s in audio:
                wav.writeframes(struct.pack('<h', int(s * 32767)))
        
        return path
    
    def load_sample(self, name: str) -> tuple:
        """Load audio sample from WAV"""
        path = os.path.join(self.preset_dir, f'{name}.wav')
        with wave.open(path, 'r') as wav:
            frames = wav.readframes(wav.getnframes())
            samples = list(struct.unpack(f'{len(frames)//2}h', frames))
            return samples, wav.getframerate()
    
    def create_preset_bundle(self, name: str, presets: Dict[str, Any]) -> str:
        """Create a bundle of multiple presets"""
        bundle = {
            'type': 'bundle',
            'name': name,
            'version': '1.0',
            'presets': presets,
        }
        return self.save_json(bundle, f'bundle_{name}.json')
    
    def load_preset_bundle(self, name: str) -> Dict:
        """Load a preset bundle"""
        return self.load_json(f'bundle_{name}.json')


def demo():
    print("=" * 60)
    print("  PRESET MANAGER - Save/Load System")
    print("=" * 60)
    
    pm = PresetManager('presets')
    
    print("\n[1] Saving synth preset...")
    synth_params = {
        'oscillators': [
            {'type': 'sawtooth', 'detune': 5, 'volume': 0.8},
            {'type': 'square', 'detune': -5, 'volume': 0.5},
        ],
        'filter': {'type': 'lowpass', 'cutoff': 2000, 'resonance': 2},
        'envelope': {'attack': 0.01, 'decay': 0.2, 'sustain': 0.7, 'release': 0.3},
        'effects': [{'type': 'reverb', 'mix': 0.3}],
    }
    pm.save_synth_preset('warm_lead', synth_params)
    print("    Saved: presets/synth_warm_lead.json")
    
    print("\n[2] Saving drum kit...")
    kit = {
        'kick': {'file': 'kick.wav', 'pitch': 0, 'volume': 1.0},
        'snare': {'file': 'snare.wav', 'pitch': 0, 'volume': 0.9},
        'hihat': {'file': 'hihat.wav', 'pitch': 0, 'volume': 0.7},
    }
    pm.save_drum_kit('my_kit', kit)
    print("    Saved: presets/kit_my_kit.json")
    
    print("\n[3] Saving effect chain...")
    chain = [
        {'type': 'compressor', 'threshold': -20, 'ratio': 4},
        {'type': 'eq', 'bands': [{'freq': 100, 'gain': 2}, {'freq': 1000, 'gain': -1}]},
        {'type': 'reverb', 'room_size': 0.5, 'mix': 0.3},
    ]
    pm.save_effect_chain('vocal_chain', chain)
    print("    Saved: presets/fx_vocal_chain.json")
    
    print("\n[4] Saving full project...")
    project = {
        'bpm': 128,
        'key': 'Am',
        'tracks': [
            {'name': 'Drums', 'volume': 0.8, 'pan': 0},
            {'name': 'Bass', 'volume': 0.9, 'pan': 0},
        ],
        'patterns': {'drums': [1, 0, 1, 0, 1, 0, 1, 0]},
    }
    pm.save_project('my_beat', project)
    print("    Saved: presets/project_my_beat.json")
    
    print("\n[5] Listing all presets...")
    all_presets = pm.list_presets()
    print(f"    Found: {all_presets}")
    
    print("\n[6] Creating preset bundle...")
    bundle = {
        'synth_preset': synth_params,
        'drum_kit': kit,
        'effect_chain': chain,
    }
    pm.create_preset_bundle('my_bundle', bundle)
    print("    Saved: presets/bundle_my_bundle.json")
    
    print("\n" + "=" * 60)
    print("  PRESET MANAGER READY!")
    print("=" * 60)


if __name__ == "__main__":
    demo()