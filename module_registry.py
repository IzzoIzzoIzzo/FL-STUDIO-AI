"""
MODULE REGISTRY - Complete Feature Overview
============================================
Shows all available modules and their capabilities!
Motto: "Everything works and is connected"

Connect to main API to access all features!
"""

from typing import Dict, List, Any, Optional


class ModuleRegistry:
    """Registry of all available modules"""
    
    MODULES = {
        # Core Generation
        'super_engine': {
            'name': 'Super Engine',
            'description': 'Main beat generation engine',
            'version': '8.0',
            'features': ['beat_generation', 'full_track', 'all_styles']
        },
        'advanced_synth': {
            'name': 'Advanced Synthesizer',
            'description': 'Professional synthesizer with presets',
            'version': '4.0',
            'features': ['presets', 'arpeggiator', 'filters', 'effects']
        },
        'drum_machine': {
            'name': 'Drum Machine',
            'description': 'Professional drum sequencer',
            'version': '3.0',
            'features': ['kits', 'patterns', 'fills', 'humanize']
        },
        
        # AI & Intelligence
        'ai_melody_engine': {
            'name': 'AI Melody Engine',
            'description': 'AI-powered melody and harmony generation',
            'version': '3.0',
            'features': ['melody_generation', 'chord_progressions', 'innovation']
        },
        'neural_music_generator': {
            'name': 'Neural Music Generator',
            'description': 'Deep learning based music generation',
            'version': '1.0',
            'features': ['melody_generation', 'chord_generation', 'rhythm_generation', 
                        'style_transfer', 'arrangement']
        },
        
        # Processing
        'auto_mixer': {
            'name': 'Auto Mixer',
            'description': 'Automatic mixing and mastering',
            'version': '3.0',
            'features': ['stem_separation', 'vocal_processing', 'mixing', 'mastering']
        },
        'stem_separator': {
            'name': 'Stem Separator',
            'description': 'Professional stem extraction',
            'version': '1.0',
            'features': ['drums', 'bass', 'vocals', 'melody', 'other']
        },
        'vocal_processor': {
            'name': 'Vocal Processor',
            'description': 'Complete vocal chain',
            'version': '1.0',
            'features': ['pitch_correction', 'harmonizer', 'vocoder', 'deesser', 
                        'reverb', 'doubling']
        },
        
        # Synthesis
        'advanced_synthesis_engine': {
            'name': 'Advanced Synthesis Engine',
            'description': 'Wavetable, Granular, FM, Additive, Physical Modeling',
            'version': '1.0',
            'features': ['wavetable', 'granular', 'fm_synthesis', 'additive', 
                        'physical_modeling', 'spectral', 'morphing']
        },
        'esoteric_music_engine': {
            'name': 'Esoteric Music Engine',
            'description': 'Sacred geometry, ancient tuning, sound healing',
            'version': '1.0',
            'features': ['sacred_geometry', 'ancient_tuning', 'microtonal', 'numerology',
                        'sound_healing', 'moon_phase', 'planetary_harmonics']
        },
        
        # Performance & DJ
        'live_performance_dj': {
            'name': 'Live Performance & DJ',
            'description': 'DJ mixer, beatmatching, loops, effects',
            'version': '1.0',
            'features': ['dj_deck', 'mixer', 'beatmatching', 'hot_cues', 
                        'looping', 'performance_effects']
        },
        
        # MIDI & Controllers
        'midi_controller': {
            'name': 'MIDI Controller',
            'description': 'MIDI I/O, mapping, sync',
            'version': '2.0',
            'features': ['midi_input', 'midi_output', 'cc_mapping', 'midi_learn', 
                        'clock_sync', 'sequencer']
        },
        
        # Music Theory
        'music_theory_engine': {
            'name': 'Music Theory Engine',
            'description': 'Scales, chords, progressions',
            'version': '1.0',
            'features': ['50+ scales', '100+ chords', 'progressions', 'voice_leading',
                        'circle_of_fifths']
        },
        
        # Visual & Cymatics
        'music_color_cymatics': {
            'name': 'Music Color & Cymatics',
            'description': 'Frequency-to-color, cymatic patterns, binaural',
            'version': '1.0',
            'features': ['frequency_color', 'cymatic_patterns', 'solfeggio', 
                        'binaural_beats', 'color_theory']
        },
        
        # Auto Creation
        'auto_creator': {
            'name': 'Auto Creator',
            'description': 'Full auto-song generation',
            'version': '1.0',
            'features': ['structure_generation', 'instrument_selection', 
                        'auto_mixing', 'auto_mastering']
        },
        
        # Effects
        'effects_rack': {
            'name': 'Effects Rack',
            'description': '9-effect professional chain',
            'version': '1.0',
            'features': ['eq', 'compressor', 'saturator', 'delay', 'reverb', 
                        'filter', 'distortion', 'limiter', 'gate']
        },
        
        # Instruments & Presets
        'instrument_library': {
            'name': 'Instrument Library',
            'description': '31 virtual instruments',
            'version': '1.0',
            'features': ['piano', 'guitar', 'strings', 'brass', 'synth', 'world']
        },
        'preset_pack_100': {
            'name': 'Preset Pack 100',
            'description': '130+ presets across 11 categories',
            'version': '1.0',
            'features': ['leads', 'basses', 'pads', 'plucks', 'keys', 'strings',
                        'brass', 'fx', 'bells', 'sfx', 'special']
        },
        'enhanced_synth_v4': {
            'name': 'Enhanced Synth V4',
            'description': '47 professional presets',
            'version': '4.0',
            'features': ['preset_categories', 'variations']
        },
        'drum_machine_v3': {
            'name': 'Drum Machine V3',
            'description': '5 drum kits with fills',
            'version': '3.0',
            'features': ['trap', 'house', 'hiphop', 'techno', 'lofi']
        },
        
        # Utilities
        'audio_exporter': {
            'name': 'Audio Exporter',
            'description': 'Export to various formats',
            'version': '1.0',
            'features': ['wav', 'mp3', 'midi', 'stems']
        },
        'beat_visualizer': {
            'name': 'Beat Visualizer',
            'description': 'Visual beat generation',
            'version': '1.0',
            'features': ['visualization', 'animation']
        },
    }
    
    @classmethod
    def get_all_modules(cls) -> Dict:
        """Get all registered modules"""
        return cls.MODULES
    
    @classmethod
    def get_module_info(cls, module_name: str) -> Optional[Dict]:
        """Get info for specific module"""
        return cls.MODULES.get(module_name)
    
    @classmethod
    def list_features(cls) -> List[str]:
        """List all features"""
        features = set()
        for module in cls.MODULES.values():
            features.update(module.get('features', []))
        return sorted(list(features))
    
    @classmethod
    def get_categories(cls) -> Dict:
        """Get modules by category"""
        return {
            'core_generation': ['super_engine', 'advanced_synth', 'drum_machine'],
            'ai_intelligence': ['ai_melody_engine', 'neural_music_generator'],
            'processing': ['auto_mixer', 'stem_separator', 'vocal_processor'],
            'synthesis': ['advanced_synthesis_engine', 'esoteric_music_engine'],
            'performance': ['live_performance_dj'],
            'midi': ['midi_controller'],
            'theory': ['music_theory_engine'],
            'visual': ['music_color_cymatics'],
            'effects': ['effects_rack'],
            'instruments': ['instrument_library', 'preset_pack_100', 'enhanced_synth_v4', 
                          'drum_machine_v3'],
            'creation': ['auto_creator'],
            'utilities': ['audio_exporter', 'beat_visualizer'],
        }
    
    @classmethod
    def get_system_status(cls) -> Dict:
        """Get complete system status"""
        return {
            'total_modules': len(cls.MODULES),
            'categories': len(cls.get_categories()),
            'total_features': len(cls.list_features()),
            'version': '8.0',
            'motto': 'Everything works and is connected!'
        }


def print_system_info():
    """Print complete system information"""
    print("=" * 70)
    print("  SHADDAI/FL STUDIO AI - MODULE REGISTRY")
    print("  Motto: Everything works and is connected!")
    print("=" * 70)
    
    status = ModuleRegistry.get_system_status()
    print(f"\nSystem Status:")
    print(f"  Total Modules: {status['total_modules']}")
    print(f"  Categories: {status['categories']}")
    print(f"  Total Features: {status['total_features']}")
    print(f"  Version: {status['version']}")
    print(f"  Motto: {status['motto']}")
    
    categories = ModuleRegistry.get_categories()
    
    print("\n" + "-" * 70)
    print("CATEGORIES & MODULES:")
    print("-" * 70)
    
    for category, modules in categories.items():
        print(f"\n[{category.upper().replace('_', ' ')}]")
        for mod in modules:
            info = ModuleRegistry.get_module_info(mod)
            if info:
                print(f"  ✓ {mod}")
                print(f"      {info['description']}")
    
    print("\n" + "-" * 70)
    print("ALL FEATURES:")
    print("-" * 70)
    
    features = ModuleRegistry.list_features()
    for i in range(0, len(features), 4):
        row = features[i:i+4]
        print("  " + ", ".join(row))
    
    print("\n" + "=" * 70)
    print("  SYSTEM READY!")
    print("=" * 70)


def get_module_features(module_name: str) -> List[str]:
    """Get features for a specific module"""
    info = ModuleRegistry.get_module_info(module_name)
    return info.get('features', []) if info else []


if __name__ == "__main__":
    print_system_info()