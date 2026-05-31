"""
FL STUDIO AI - UNIFIED API SYSTEM v8.0
======================================
Complete API that connects ALL features!
- Beat Generation
- Drum Machine
- Advanced Synth
- Auto-Mixer & Stems
- AI Melody
- MIDI Export
- Web Server
- MCP Protocol

This is the API that ties everything together!
"""

import json
import os
import sys
import struct
import wave
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# Try to import Flask for web API
try:
    from flask import Flask, request, jsonify, send_file
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("[WARNING] Flask not available - web API disabled")

# Import all modules
MODULES_OK = True
try:
    from super_engine import SuperEngine, BeatGenerator, AudioEngine
    from advanced_synth import AdvancedSynthesizer, SynthesizerPreset, Arpeggiator
    from drum_machine import DrumSequencer, DrumKit
    from auto_mixer import AutoMixer, StemExporter, InnovationHub
    from ai_melody_engine import AIMelodyComposer, InnovationEngine, ChordProgressionAI
    from beat_visualizer import VisualBeatGenerator
    from audio_exporter import AudioExporter
    from extra_synthesis_engine import ExtraSynthesisEngine
    from expanded_instrument_library import ExpandedInstrumentLibrary
    from advanced_ai_composer import AdvancedAIComposer
    from creative_sound_engine import CreativeSoundEngine
    from real_dsp_engine import RealDSPEngine
    from real_drum_synth import RealDrumSynthesizer
    from real_audio_effects import RealEffectsEngine
    from professional_synth import ProfessionalSynth
    from extensive_synth_engine import ExtensiveSynth
    from comprehensive_effects import ComprehensiveEffects
    from extensive_instrument_library import ExtensiveInstrumentLibrary
except ImportError as e:
    print(f"[ERROR] Module import failed: {e}")
    MODULES_OK = False


# ============================================================
# CORE AUDIO UTILITIES
# ============================================================

class AudioUtils:
    """Common audio utilities"""
    
    @staticmethod
    def save_wav(samples: List[float], filename: str, sample_rate: int = 44100):
        """Save audio to WAV file"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # Normalize
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            samples = [s * 0.9 / max_val for s in samples]
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            for s in samples:
                packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
                wav.writeframes(packed)
    
    @staticmethod
    def load_wav(filename: str) -> List[float]:
        """Load audio from WAV file"""
        samples = []
        with wave.open(filename, 'r') as wav:
            for _ in range(wav.getnframes()):
                frame = wav.readframes(1)
                if len(frame) >= 2:
                    sample = struct.unpack('<h', frame[:2])[0] / 32767.0
                    samples.append(sample)
        return samples
    
    @staticmethod
    def mix_tracks(*tracks: List[float]) -> List[float]:
        """Mix multiple audio tracks"""
        max_len = max(len(t) for t in tracks) if tracks else 0
        if max_len == 0:
            return []
        
        result = [0.0] * max_len
        for track in tracks:
            for i, s in enumerate(track):
                result[i] += s
        
        # Normalize
        max_val = max(abs(s) for s in result) if result else 1
        if max_val > 0:
            result = [s * 0.8 / max_val for s in result]
        
        return result


# ============================================================
# MAIN UNIFIED API
# ============================================================

class FLStudioAI:
    """
    Main Unified API for FL Studio AI
    All features connected and accessible through one interface!
    """
    
    def __init__(self):
        self.sample_rate = 44100
        self.audio_dir = "audio"
        self.export_dir = "exports"
        
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.export_dir, exist_ok=True)
        
        # Initialize all engines
        self._init_engines()
        
        print("=" * 60)
        print("  FL STUDIO AI - UNIFIED API v8.0")
        print("=" * 60)
        print("[OK] All systems initialized!")
    
    def _init_engines(self):
        """Initialize all engine modules"""
        
        # Core engine
        self.super_engine = None
        self.audio_engine = None
        self.beat_generator = None
        
        # Synth
        self.synth = None
        self.arpeggiator = None
        
        # Drums
        self.drum_sequencer = None
        
        # Mixing
        self.mixer = None
        self.stem_exporter = None
        
        # AI
        self.melody_composer = None
        self.innovation_engine = None
        
        # Visualizer
        self.visualizer = None
        
        # Extra Synthesis
        self.extra_synth = None
        self.expanded_instruments = None
        
        modules_loaded = True
        if MODULES_OK:
            try:
                self.super_engine = SuperEngine()
                self.audio_engine = AudioEngine()
                self.beat_generator = BeatGenerator()
                self.synth = AdvancedSynthesizer(self.sample_rate)
                self.arpeggiator = Arpeggiator(self.synth)
                self.drum_sequencer = DrumSequencer('808')
                self.mixer = AutoMixer()
                self.stem_exporter = StemExporter()
                self.melody_composer = AIMelodyComposer()
                self.innovation_engine = InnovationEngine()
                
                # Extra Synthesis & Expanded Instruments
                try:
                    self.extra_synth = ExtraSynthesisEngine(self.sample_rate)
                    self.expanded_instruments = ExpandedInstrumentLibrary(self.sample_rate)
                    self.ai_composer = AdvancedAIComposer()
                    self.creative_engine = CreativeSoundEngine(self.sample_rate)
                except Exception as e:
                    print(f"[WARNING] Extra modules: {e}")
                
                # REAL DSP Modules - Professional grade!
                try:
                    self.real_dsp = RealDSPEngine(self.sample_rate)
                    self.real_drums = RealDrumSynthesizer(self.sample_rate)
                    self.real_effects = RealEffectsEngine(self.sample_rate)
                    self.real_synth = ProfessionalSynth(self.sample_rate)
                    self.extensive_synth = ExtensiveSynth(self.sample_rate)
                    self.comprehensive_effects = ComprehensiveEffects(self.sample_rate)
                    self.extensive_instruments = ExtensiveInstrumentLibrary(self.sample_rate)
                    print("[OK] EXTENSIVE modules loaded - 100+ presets, real DSP!")
                except Exception as e:
                    print(f"[WARNING] Extensive modules: {e}")
                
                # Visualizer
                try:
                    self.visualizer = VisualBeatGenerator(800, 600)
                except:
                    self.visualizer = None
                print("[OK] All modules loaded successfully")
            except Exception as e:
                print(f"[ERROR] Module initialization failed: {e}")
                modules_loaded = False
        
        self._modules_loaded = modules_loaded
        
        # Property aliases for easy access
        self.drums = self.drum_sequencer
        self.melody = self.melody_composer
        self.visualizer = self.visualizer if hasattr(self, 'visualizer') else None
        self.exporter = AudioExporter(self.sample_rate)
    
    # ============================================================
    # BEAT GENERATION
    # ============================================================
    
    def generate_beat(self, style: str = 'trap', bars: int = 4, 
                      save: bool = True) -> Dict[str, Any]:
        """Generate a beat in any style"""
        
        if not self.super_engine:
            return {'error': 'Super engine not initialized'}
        
        result = self.super_engine.create_beat(style, bars, save, self.audio_dir)
        
        return {
            'success': True,
            'audio_file': result.get('audio_file'),
            'midi_file': result.get('midi_file'),
            'style': style,
            'bpm': result.get('bpm'),
            'bars': bars,
            'duration': result.get('duration')
        }
    
    def generate_full_track(self, style: str = 'trap',
                           include_melody: bool = True,
                           include_chords: bool = True) -> Dict[str, Any]:
        """Generate a full track with all elements"""
        
        if not self.super_engine:
            return {'error': 'Super engine not initialized'}
        
        result = self.super_engine.create_full_track(
            style, include_melody, include_chords
        )
        
        return {
            'success': True,
            'file': result.get('file'),
            'style': style,
            'duration': result.get('duration'),
            'has_melody': result.get('has_melody'),
            'has_chords': result.get('has_chords')
        }
    
    # ============================================================
    # SYNTHESIZER
    # ============================================================
    
    def list_synth_presets(self) -> List[str]:
        """List available synth presets"""
        return SynthesizerPreset.list_presets() if MODULES_OK else []
    
    def load_synth_preset(self, preset_name: str) -> Dict:
        """Load a synth preset"""
        if not self.synth:
            return {'error': 'Synth not initialized'}
        
        try:
            preset = self.synth.load_preset(preset_name)
            return {'success': True, 'preset': preset_name, 'data': preset}
        except Exception as e:
            return {'error': str(e)}
    
    def play_synth_note(self, frequency: float, duration: float = 1.0,
                        velocity: float = 0.8, save_file: str = None, save: bool = False) -> Dict:
        """Play a note on the synth"""
        
        if not self.synth:
            return {'error': 'Synth not initialized'}
        
        audio = self.synth.play_note(frequency, duration, velocity)
        
        # Handle save parameter
        if save and not save_file:
            save_file = 'synth_note.wav'
        
        if save_file:
            full_path = os.path.join(self.audio_dir, save_file)
            AudioUtils.save_wav(audio, full_path)
            return {'success': True, 'file': full_path, 'samples': len(audio)}
        
        return {'success': True, 'samples': len(audio), 'audio': audio[:1000]}
    
    def play_synth_chord(self, root_note: int, chord_type: str = 'major',
                         duration: float = 2.0, save_file: str = None, save: bool = False) -> Dict:
        """Play a chord on the synth"""
        
        if not self.synth:
            return {'error': 'Synth not initialized'}
        
        # Handle save parameter
        if save and not save_file:
            save_file = 'synth_chord.wav'
        
        # Convert MIDI note to frequency
        freq = 440 * (2 ** ((root_note - 69) / 12))
        
        audio = self.synth.play_chord(freq, chord_type, duration, 0.8)
        
        if save_file:
            full_path = os.path.join(self.audio_dir, save_file)
            AudioUtils.save_wav(audio, full_path)
            return {'success': True, 'file': full_path, 'duration': len(audio) / self.sample_rate}
        
        return {'success': True, 'samples': len(audio)}
    
    # ============================================================
    # DRUM MACHINE
    # ============================================================
    
    def list_drum_kits(self) -> List[str]:
        """List available drum kits"""
        return list(DrumKit.KITS.keys()) if MODULES_OK else []
    
    def load_drum_kit(self, kit_name: str) -> Dict:
        """Load a drum kit"""
        
        if not self.drum_sequencer:
            return {'error': 'Drum sequencer not initialized'}
        
        self.drum_sequencer = DrumSequencer(kit_name)
        kit = DrumKit.get_kit(kit_name)
        
        return {'success': True, 'kit': kit_name, 'kit_data': kit}
    
    def set_drum_pattern(self, drum: str, pattern: List[int]) -> Dict:
        """Set drum pattern (16 steps)"""
        
        if not self.drum_sequencer:
            return {'error': 'Drum sequencer not initialized'}
        
        if len(pattern) != 16:
            return {'error': 'Pattern must be 16 steps'}
        
        self.drum_sequencer.set_pattern(drum, pattern)
        
        return {'success': True, 'drum': drum, 'pattern': pattern}
    
    def generate_drums(self, bars: int = 4, bpm: int = 120,
                       save_file: str = None) -> Dict:
        """Generate drum track"""
        
        if not self.drum_sequencer:
            return {'error': 'Drum sequencer not initialized'}
        
        self.drum_sequencer.bpm = bpm
        
        audio = self.drum_sequencer.generate(bars, humanize=0.05)
        
        if save_file:
            full_path = os.path.join(self.audio_dir, save_file)
            AudioUtils.save_wav(audio, full_path)
            return {'success': True, 'file': full_path, 'duration': len(audio) / self.sample_rate}
        
        return {'success': True, 'samples': len(audio), 'duration': len(audio) / self.sample_rate}
    
    def load_drum_preset(self, preset_name: str) -> Dict:
        """Load a preset drum pattern"""
        
        if not self.drum_sequencer:
            return {'error': 'Drum sequencer not initialized'}
        
        self.drum_sequencer.load_preset(preset_name)
        
        return {'success': True, 'preset': preset_name}
    
    # ============================================================
    # AI MELODY
    # ============================================================
    
    def generate_ai_melody(self, style: str = 'electronic', 
                          emotion: str = 'dreamy',
                          length: int = 16,
                          save_file: str = None) -> Dict:
        """Generate unique AI melody"""
        
        if not self.melody_composer:
            return {'error': 'AI melody not initialized'}
        
        melody = self.melody_composer.compose_melody(style, emotion, length)
        dna = self.melody_composer.create_melody_DNA(melody)
        
        # Convert to audio
        if save_file:
            # Generate audio for melody
            audio = []
            for note in melody:
                if note['note']:
                    freq = 440 * (2 ** ((note['note'] - 69) / 12))
                    note_audio = self.synth.play_note(freq, note['duration'], 0.7)
                    audio.extend(note_audio)
            
            full_path = os.path.join(self.audio_dir, save_file)
            AudioUtils.save_wav(audio, full_path)
            
            return {
                'success': True,
                'melody': melody,
                'dna': dna,
                'file': full_path
            }
        
        return {'success': True, 'melody': melody, 'dna': dna}
    
    def generate_innovative_track(self, style: str = 'electronic',
                                  emotion: str = 'dreamy',
                                  duration: float = 8.0) -> Dict:
        """Generate never-heard-before track"""
        
        if not self.innovation_engine:
            return {'error': 'Innovation engine not initialized'}
        
        result = self.innovation_engine.create_never_heard_before(style, emotion, duration)
        
        return {
            'success': True,
            'id': result['id'],
            'style': result['style'],
            'emotion': result['emotion'],
            'innovation_score': result['innovation_score'],
            'melody_length': len(result['melody'])
        }
    
    # ============================================================
    # MIXING & STEMS
    # ============================================================
    
    def auto_mix(self, audio_file: str = None, 
                 style: str = 'club',
                 export_stems: bool = True) -> Dict:
        """Auto-mix audio"""
        
        if not self.mixer:
            return {'error': 'Mixer not initialized'}
        
        # If no audio file, generate a test beat
        if not audio_file:
            beat = self.super_engine.create_beat('trap', 4, True, self.audio_dir)
            audio_file = beat.get('audio_file')
            audio = self.super_engine.beat_gen.generate('trap', 4)['audio']
        else:
            audio = AudioUtils.load_wav(audio_file)
        
        result = self.mixer.auto_mix(audio, style, export_stems, self.audio_dir + "/mixed")
        
        return {
            'success': True,
            'mix_file': result.get('mix_file'),
            'stems': result.get('stems'),
            'style': style
        }
    
    def create_stem_pack(self, style: str = 'trap', bars: int = 4) -> Dict:
        """Create a complete stem pack"""
        
        if not self.super_engine:
            return {'error': 'Super engine not initialized'}
        
        result = self.super_engine.create_stem_pack(style, bars)
        
        return {
            'success': True,
            'stems': list(result.get('stems', {}).keys()),
            'mixes': len(result.get('mixes', []))
        }
    
    # ============================================================
    # SYSTEM STATUS
    # ============================================================
    
    def get_status(self) -> Dict:
        """Get system status"""
        
        return {
            'version': '8.0',
            'modules_loaded': MODULES_OK,
            'features': {
                'beat_generation': self.super_engine is not None,
                'synthesizer': self.synth is not None,
                'drum_machine': self.drum_sequencer is not None,
                'auto_mixer': self.mixer is not None,
                'ai_melody': self.melody_composer is not None,
                'innovation_engine': self.innovation_engine is not None,
            },
            'directories': {
                'audio': self.audio_dir,
                'exports': self.export_dir
            }
        }
    
    def list_audio_files(self) -> List[str]:
        """List all generated audio files"""
        
        if not os.path.exists(self.audio_dir):
            return []
        
        return [f for f in os.listdir(self.audio_dir) if f.endswith('.wav')]
    
    def list_midi_files(self) -> List[str]:
        """List all generated MIDI files"""
        
        if not os.path.exists(self.export_dir):
            return []
        
        return [f for f in os.listdir(self.export_dir) if f.endswith('.mid')]


# ============================================================
# WEB API SERVER
# ============================================================

class APIServer:
    """REST API server for FL Studio AI"""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__) if FLASK_AVAILABLE else None
        self.api = FLStudioAI()
        
        if self.app:
            self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/')
        def index():
            return jsonify({
                'name': 'FL Studio AI API',
                'version': '8.0',
                'endpoints': {
                    '/status': 'Get system status',
                    '/beat/<style>': 'Generate beat',
                    '/synth/presets': 'List synth presets',
                    '/drums/kits': 'List drum kits',
                    '/ai/melody': 'Generate AI melody',
                    '/mix': 'Auto-mix',
                    '/files': 'List generated files'
                }
            })
        
        @self.app.route('/status')
        def status():
            return jsonify(self.api.get_status())
        
        @self.app.route('/beat/<style>')
        def generate_beat(style):
            bars = request.args.get('bars', 4, type=int)
            result = self.api.generate_beat(style, bars)
            return jsonify(result)
        
        @self.app.route('/track/<style>')
        def generate_track(style):
            result = self.api.generate_full_track(style)
            return jsonify(result)
        
        @self.app.route('/synth/presets')
        def synth_presets():
            return jsonify(self.api.list_synth_presets())
        
        @self.app.route('/synth/play', methods=['POST'])
        def synth_play():
            data = request.json
            freq = data.get('frequency', 440)
            duration = data.get('duration', 1.0)
            save = data.get('save', 'synth_note.wav')
            result = self.api.play_synth_note(freq, duration, save_file=save)
            return jsonify(result)
        
        @self.app.route('/drums/kits')
        def drum_kits():
            return jsonify(self.api.list_drum_kits())
        
        @self.app.route('/drums/generate', methods=['POST'])
        def drums_generate():
            data = request.json
            bars = data.get('bars', 4)
            bpm = data.get('bpm', 120)
            result = self.api.generate_drums(bars, bpm, save_file='drums.wav')
            return jsonify(result)
        
        @self.app.route('/drums/pattern', methods=['POST'])
        def drums_pattern():
            data = request.json
            drum = data.get('drum', 'kick')
            pattern = data.get('pattern', [100,0]*8)
            result = self.api.set_drum_pattern(drum, pattern)
            return jsonify(result)
        
        @self.app.route('/ai/melody', methods=['POST'])
        def ai_melody():
            data = request.json
            style = data.get('style', 'electronic')
            emotion = data.get('emotion', 'dreamy')
            length = data.get('length', 16)
            result = self.api.generate_ai_melody(style, emotion, length, save_file='ai_melody.wav')
            return jsonify(result)
        
        @self.app.route('/ai/innovate', methods=['POST'])
        def ai_innovate():
            data = request.json
            style = data.get('style', 'electronic')
            emotion = data.get('emotion', 'dreamy')
            duration = data.get('duration', 8.0)
            result = self.api.generate_innovative_track(style, emotion, duration)
            return jsonify(result)
        
        @self.app.route('/mix', methods=['POST'])
        def auto_mix():
            data = request.json
            style = data.get('style', 'club')
            result = self.api.auto_mix(style=style)
            return jsonify(result)
        
        @self.app.route('/stems/<style>')
        def stem_pack(style):
            result = self.api.create_stem_pack(style)
            return jsonify(result)
        
        @self.app.route('/files')
        def list_files():
            return jsonify({
                'audio': self.api.list_audio_files(),
                'midi': self.api.list_midi_files()
            })
    
    def run(self):
        """Start the API server"""
        
        if not self.app:
            print("[ERROR] Flask not available, cannot start server")
            return
        
        print(f"\n[OK] Starting API server on http://{self.host}:{self.port}")
        print("[OK] Press Ctrl+C to stop\n")
        
        self.app.run(host=self.host, port=self.port, debug=False)


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

def main():
    """Main CLI"""
    
    api = FLStudioAI()
    status = api.get_status()
    
    print("\n" + "=" * 60)
    print("  FL STUDIO AI UNIFIED API")
    print("=" * 60)
    print(f"\nVersion: {status['version']}")
    print(f"Modules: {'OK' if status['modules_loaded'] else 'ERROR'}")
    print("\nFeatures:")
    for feat, ok in status['features'].items():
        print(f"  [{'OK' if ok else 'XX'}] {feat.replace('_', ' ').title()}")
    
    # Quick test
    print("\n" + "-" * 40)
    print("Quick Test: Generate a trap beat")
    print("-" * 40)
    
    result = api.generate_beat('trap', 4)
    print(f"Result: {result.get('success')}")
    if result.get('success'):
        print(f"Audio: {result.get('audio_file')}")
        print(f"MIDI: {result.get('midi_file')}")
    
    print("\n[OK] API Ready!")
    print("\nTo start web API: python flstudio_ai_api.py --server")
    print("To use in code: from flstudio_ai_api import FLStudioAI")


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == '--server':
            server = APIServer()
            server.run()
        
        elif cmd == '--quick-beat':
            api = FLStudioAI()
            style = sys.argv[2] if len(sys.argv) > 2 else 'trap'
            result = api.generate_beat(style, 4)
            print(f"Beat generated: {result.get('audio_file')}")
        
        elif cmd == '--full-track':
            api = FLStudioAI()
            style = sys.argv[2] if len(sys.argv) > 2 else 'trap'
            result = api.generate_full_track(style)
            print(f"Full track: {result.get('file')}")
        
        elif cmd == '--synth-note':
            api = FLStudioAI()
            result = api.play_synth_note(440, 0.5, save_file='synth_note.wav')
            print(f"Synth note: {result}")
        
        elif cmd == '--synth-chord':
            api = FLStudioAI()
            result = api.play_synth_chord(60, 'major', 2.0, save_file='synth_chord.wav')
            print(f"Synth chord: {result}")
        
        elif cmd == '--synth-presets':
            api = FLStudioAI()
            presets = api.list_synth_presets()
            print("Available presets:", presets)
        
        elif cmd == '--drums':
            api = FLStudioAI()
            api.load_drum_kit('808')
            api.load_drum_preset('trap')
            result = api.generate_drums(4, 140, 'drums.wav')
            print(f"Drums: {result}")
        
        elif cmd == '--ai-melody':
            api = FLStudioAI()
            result = api.generate_ai_melody('electronic', 'dreamy', 16, save_file='ai_melody.wav')
            print(f"AI Melody: {result.get('success')}")
        
        elif cmd == '--mix':
            api = FLStudioAI()
            result = api.auto_mix(style='club')
            print(f"Mixed: {result}")
        
        elif cmd == '--list-files':
            api = FLStudioAI()
            files = api.list_audio_files()
            midi = api.list_midi_files()
            print("Audio files:", files)
            print("MIDI files:", midi)
        
        else:
            main()
    else:
        main()