"""
COMPLETE SAMPLER WORKFLOW - Full Production Pipeline!
=========================================================
Integrates all sampler features with the main system
- Complete sample management
- Slice editing
- Time-stretch/pitch-shift 
- Hot-swap pads
- Pattern sequencing
- Export options

Builds on the base sampler_system.py
"""

import os
import sys
import json
import struct
import wave
import random
import math
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Import base sampler
try:
    from sampler_system import AudioSample, SampleChopper, SamplePad, SampleSequencer, load_wav, save_wav
    SAMPLER_AVAILABLE = True
except ImportError:
    SAMPLER_AVAILABLE = False
    print("[WARNING] Base sampler not available")


class SampleManager:
    """Complete sample management system"""
    
    def __init__(self, library_dir: str = "audio/samples", workspace_dir: str = "audio/workspace"):
        self.library_dir = library_dir
        self.workspace_dir = workspace_dir
        os.makedirs(library_dir, exist_ok=True)
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Sample database
        self.database = {}
        self.current_sample = None
        
        # Processing state
        self.chopped_slices = {}
        self.modified_samples = {}
        
        # Load existing database
        self._load_database()
    
    def _load_database(self):
        """Load sample database from disk"""
        
        db_file = os.path.join(self.library_dir, "database.json")
        if os.path.exists(db_file):
            try:
                with open(db_file, 'r') as f:
                    self.database = json.load(f)
            except:
                self.database = {}
    
    def _save_database(self):
        """Save sample database to disk"""
        
        db_file = os.path.join(self.library_dir, "database.json")
        with open(db_file, 'w') as f:
            json.dump(self.database, f, indent=2)
    
    def import_sample(self, filepath: str, name: str = None, category: str = "imported") -> Optional[AudioSample]:
        """Import a sample into the library"""
        
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return None
        
        # Generate name from filename if not provided
        if not name:
            name = os.path.splitext(os.path.basename(filepath))[0]
        
        # Load sample
        try:
            sample = load_wav(filepath)
            sample.name = name
            
            # Save to library
            dest_path = os.path.join(self.library_dir, f"{name}.wav")
            save_wav(sample.samples, dest_path, sample.sample_rate)
            
            # Add to database
            self.database[name] = {
                'path': dest_path,
                'category': category,
                'duration': sample.duration,
                'sample_rate': sample.sample_rate,
                'imported': datetime.now().isoformat(),
                'transients': len(sample.transients),
                'slices': {}
            }
            
            self._save_database()
            
            print(f"[OK] Imported: {name} ({sample.duration:.2f}s)")
            return sample
            
        except Exception as e:
            print(f"[ERROR] Import failed: {e}")
            return None
    
    def get_sample(self, name: str) -> Optional[AudioSample]:
        """Get a sample by name"""
        
        if name in self.database:
            path = self.database[name]['path']
            if os.path.exists(path):
                return load_wav(path)
        
        return None
    
    def list_samples(self, category: str = None) -> List[str]:
        """List all samples, optionally filtered by category"""
        
        if category:
            return [n for n, info in self.database.items() if info.get('category') == category]
        
        return list(self.database.keys())
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        cats = set()
        for info in self.database.values():
            cats.add(info.get('category', 'uncategorized'))
        return sorted(cats)
    
    def delete_sample(self, name: str):
        """Delete a sample from library"""
        
        if name in self.database:
            path = self.database[name]['path']
            if os.path.exists(path):
                os.remove(path)
            del self.database[name]
            self._save_database()
            print(f"[OK] Deleted: {name}")
    
    def categorize_sample(self, name: str, category: str):
        """Categorize a sample"""
        
        if name in self.database:
            self.database[name]['category'] = category
            self._save_database()


class SliceEditor:
    """Visual slice editor with manipulation"""
    
    def __init__(self, sample: AudioSample):
        self.sample = sample
        self.slices = {}
        self.selected_slice = None
    
    def auto_chop(self, sensitivity: float = 0.5) -> Dict[int, AudioSample]:
        """Auto-chop at transients"""
        
        chopper = SampleChopper(sensitivity)
        self.slices = chopper.chop_by_transients(self.sample)
        
        # Store in database
        for idx, slice_sample in self.slices.items():
            self.sample.slices[idx] = slice_sample
        
        return self.slices
    
    def chop_time(self, slice_duration: float) -> Dict[int, AudioSample]:
        """Chop into equal time slices"""
        
        chopper = SampleChopper()
        self.slices = chopper.chop_by_time(self.sample, slice_duration)
        
        for idx, slice_sample in self.slices.items():
            self.sample.slices[idx] = slice_sample
        
        return self.slices
    
    def chop_beats(self, bpm: int, time_sig: Tuple[int, int] = (4, 4)) -> Dict[int, AudioSample]:
        """Chop at beat boundaries"""
        
        chopper = SampleChopper()
        self.slices = chopper.chop_by_beats(self.sample, bpm, time_sig)
        
        for idx, slice_sample in self.slices.items():
            self.sample.slices[idx] = slice_sample
        
        return self.slices
    
    def manual_chop(self, points: List[float]) -> Dict[int, AudioSample]:
        """Manual chop at specific points"""
        
        chopper = SampleChopper()
        self.slices = chopper.manual_chop(self.sample, points)
        
        for idx, slice_sample in self.slices.items():
            self.sample.slices[idx] = slice_sample
        
        return self.slices
    
    def select_slice(self, index: int):
        """Select a slice for editing"""
        
        if index in self.slices:
            self.selected_slice = index
    
    def delete_slice(self, index: int):
        """Delete a slice"""
        
        if index in self.slices:
            del self.slices[index]
            if self.selected_slice == index:
                self.selected_slice = None
    
    def swap_slices(self, idx1: int, idx2: int):
        """Swap two slices"""
        
        if idx1 in self.slices and idx2 in self.slices:
            self.slices[idx1], self.slices[idx2] = self.slices[idx2], self.slices[idx1]
    
    def reverse_slice(self, index: int):
        """Reverse a specific slice"""
        
        if index in self.slices:
            self.slices[index] = self.slices[index].reverse()
    
    def export_slices(self, directory: str, prefix: str = "slice") -> List[str]:
        """Export all slices as individual files"""
        
        os.makedirs(directory, exist_ok=True)
        
        filenames = []
        for idx, slice_sample in self.slices.items():
            filename = os.path.join(directory, f"{prefix}_{idx}.wav")
            save_wav(slice_sample.samples, filename, slice_sample.sample_rate)
            filenames.append(filename)
        
        return filenames
    
    def reorder_slices(self, order: List[int]):
        """Reorder slices according to new order"""
        
        new_slices = {}
        for new_idx, old_idx in enumerate(order):
            if old_idx in self.slices:
                new_slices[new_idx] = self.slices[old_idx]
        
        self.slices = new_slices


class SampleWorkspace:
    """Complete sample workspace with multiple pads and sequences"""
    
    def __init__(self, num_pads: int = 16, num_sequences: int = 4):
        self.sample_rate = 44100
        # Pads
        self.pads = SamplePad(num_pads, self.sample_rate)
        self.pad_names = {i: f"Pad {i+1}" for i in range(num_pads)}
        
        # Sequences
        self.sequences = [SampleSequencer(self.pads, 16) for _ in range(num_sequences)]
        self.current_sequence = 0
        
        # Pattern storage
        self.patterns = {}
        
        # Mixer
        self.master_volume = 1.0
        self.master_pan = 0.5
        
        # Effects per pad
        self.pad_fx = {i: {'reverse': False, 'gate': False, 'stutter': False} for i in range(num_pads)}
    
    def load_sample_to_pad(self, pad: int, sample: AudioSample, name: str = None):
        """Load sample into pad"""
        
        if 0 <= pad < self.pads.num_pads:
            self.pads.load_sample(pad, sample)
            if name:
                self.pad_names[pad] = name
    
    def load_sample_by_name(self, pad: int, sample_manager: SampleManager, name: str):
        """Load sample by name from manager"""
        
        sample = sample_manager.get_sample(name)
        if sample:
            self.load_sample_to_pad(pad, sample, name)
            return True
        return False
    
    def trigger_pad(self, pad: int) -> Optional[AudioSample]:
        """Trigger pad with effects applied"""
        
        if pad in self.pad_fx and self.pad_fx[pad]['reverse']:
            self.pads.toggle_reverse(pad)
        
        return self.pads.trigger(pad)
    
    def set_pad_fx(self, pad: int, reverse: bool = False, gate: bool = False, stutter: bool = False):
        """Set effects for pad"""
        
        if 0 <= pad < self.pads.num_pads:
            self.pad_fx[pad] = {'reverse': reverse, 'gate': gate, 'stutter': stutter}
    
    def save_pattern(self, name: str, sequence_index: int = None):
        """Save current pattern"""
        
        if sequence_index is None:
            sequence_index = self.current_sequence
        
        seq = self.sequences[sequence_index]
        
        self.patterns[name] = {
            'sequence': seq.sequence.copy(),
            'bpm': seq.bpm,
            'gate_time': seq.gate_time
        }
        
        print(f"[OK] Pattern saved: {name}")
    
    def load_pattern(self, name: str, sequence_index: int = None):
        """Load a saved pattern"""
        
        if name not in self.patterns:
            print(f"[ERROR] Pattern not found: {name}")
            return False
        
        if sequence_index is None:
            sequence_index = self.current_sequence
        
        pattern = self.patterns[name]
        self.sequences[sequence_index].sequence = pattern['sequence'].copy()
        self.sequences[sequence_index].bpm = pattern['bpm']
        self.sequences[sequence_index].gate_time = pattern['gate_time']
        
        print(f"[OK] Pattern loaded: {name}")
        return True
    
    def list_patterns(self) -> List[str]:
        """List all saved patterns"""
        return list(self.patterns.keys())


class SampleExporter:
    """Export samples in various formats"""
    
    @staticmethod
    def export_chopped(sample: AudioSample, output_dir: str, prefix: str = "slice") -> List[str]:
        """Export sample as chopped slices"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        if not sample.slices:
            # Auto-chop first
            chopper = SampleChopper()
            chopper.chop_by_transients(sample)
        
        filenames = []
        for idx, slice_sample in sample.slices.items():
            filename = os.path.join(output_dir, f"{prefix}_{idx:02d}.wav")
            save_wav(slice_sample.samples, filename, slice_sample.sample_rate)
            filenames.append(filename)
        
        return filenames
    
    @staticmethod
    def export_with_variations(sample: AudioSample, output_dir: str, variations: int = 4) -> Dict[str, str]:
        """Export sample with multiple variations"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        # Original
        orig_path = os.path.join(output_dir, "original.wav")
        save_wav(sample.samples, orig_path, sample.sample_rate)
        results['original'] = orig_path
        
        # Reversed
        rev_sample = sample.reverse()
        rev_path = os.path.join(output_dir, "reversed.wav")
        save_wav(rev_sample.samples, rev_path, sample.sample_rate)
        results['reversed'] = rev_path
        
        # Stretched variations
        for i in range(1, variations + 1):
            ratio = 0.5 + (i * 0.25)  # 0.75, 1.0, 1.25, 1.5
            stretched = sample.time_stretch(ratio)
            path = os.path.join(output_dir, f"stretched_{ratio}.wav")
            save_wav(stretched.samples, path, stretched.sample_rate)
            results[f'stretched_{ratio}'] = path
        
        # Pitch shifts
        for semitones in [-5, 5, 12]:
            pitched = sample.pitch_shift(semitones)
            path = os.path.join(output_dir, f"pitch_{semitones:+d}.wav")
            save_wav(pitched.samples, path, pitched.sample_rate)
            results[f'pitch_{semitones:+d}'] = path
        
        # Gated
        gated = sample.gate(threshold=0.2)
        path = os.path.join(output_dir, "gated.wav")
        save_wav(gated.samples, path, gated.sample_rate)
        results['gated'] = path
        
        return results
    
    @staticmethod
    def export_pad_to_audio(workspace: SampleWorkspace, output_file: str):
        """Export pad sampler setup as audio file"""
        
        # Combine all loaded pads
        all_samples = []
        
        for pad_idx in range(workspace.pads.num_pads):
            if workspace.pads.pad_samples[pad_idx]:
                sample = workspace.pads.pad_samples[pad_idx]
                # Add some silence between
                silence = [0] * int(workspace.pads.sample_rate * 0.5)
                all_samples.extend(sample.samples)
                all_samples.extend(silence)
        
        if all_samples:
            save_wav(all_samples, output_file, workspace.pads.sample_rate)
            return output_file
        
        return None


class CompleteSampler:
    """Complete sampler system - ties everything together"""
    
    def __init__(self):
        self.sample_manager = SampleManager()
        self.workspace = SampleWorkspace(16, 4)
        self.current_sample = None
        self.slice_editor = None
        
        print("=" * 60)
        print("  COMPLETE SAMPLER WORKFLOW")
        print("=" * 60)
        print("[OK] Sample Manager initialized")
        print("[OK] Workspace initialized (16 pads, 4 sequences)")
    
    def load_sample(self, name: str) -> bool:
        """Load sample into editor"""
        
        sample = self.sample_manager.get_sample(name)
        if sample:
            self.current_sample = sample
            self.slice_editor = SliceEditor(sample)
            print(f"[OK] Loaded: {name}")
            return True
        
        print(f"[ERROR] Sample not found: {name}")
        return False
    
    def import_and_process(self, filepath: str, name: str = None) -> bool:
        """Import sample and auto-process"""
        
        sample = self.sample_manager.import_sample(filepath, name)
        if sample:
            self.current_sample = sample
            self.slice_editor = SliceEditor(sample)
            
            # Auto-chop
            self.slice_editor.auto_chop(0.5)
            
            print(f"[OK] Imported and chopped: {len(self.slice_editor.slices)} slices")
            return True
        
        return False
    
    def load_to_pad(self, pad: int, sample_name: str) -> bool:
        """Load sample into a pad"""
        
        sample = self.sample_manager.get_sample(sample_name)
        if sample:
            self.workspace.load_sample_to_pad(pad, sample, sample_name)
            print(f"[OK] Loaded to pad {pad + 1}: {sample_name}")
            return True
        
        return False
    
    def export_workspace(self, output_dir: str = "audio/exports") -> Dict:
        """Export entire workspace setup"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        # Export slices
        if self.slice_editor and self.slice_editor.slices:
            slice_files = self.slice_editor.export_slices(output_dir, "slice")
            results['slices'] = slice_files
            print(f"[OK] Exported {len(slice_files)} slices")
        
        # Export patterns
        patterns = self.workspace.list_patterns()
        results['patterns'] = patterns
        print(f"[OK] {len(patterns)} patterns")
        
        # Export pad audio
        pad_audio = os.path.join(output_dir, "workspace.wav")
        SampleExporter.export_pad_to_audio(self.workspace, pad_audio)
        results['workspace'] = pad_audio
        print(f"[OK] Workspace exported")
        
        return results


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  COMPLETE SAMPLER WORKFLOW TEST")
    print("=" * 60)
    
    # Create sampler
    sampler = CompleteSampler()
    
    # Import a test sample
    print("\n[1] Creating test sample for import...")
    
    # Generate test audio
    test_samples = []
    for i in range(44100 * 2):  # 2 seconds
        t = i / 44100
        beat = int(t * 2)
        if beat % 2 == 0:
            sample = math.sin(2 * math.pi * 100 * t) * (1 - t % 1)
        else:
            sample = (random.random() * 2 - 1) * 0.3
        test_samples.append(sample)
    
    test_path = "audio/samples/test_import.wav"
    save_wav(test_samples, test_path, 44100)
    
    # Import it
    print("\n[2] Importing sample...")
    sampler.import_and_process(test_path, "test_beat")
    
    # List library
    print("\n[3] Library contents:")
    samples = sampler.sample_manager.list_samples()
    print(f"   {samples}")
    
    # Load to workspace
    print("\n[4] Loading to pads...")
    sampler.load_to_pad(0, "test_beat")
    sampler.load_to_pad(4, "test_beat")
    sampler.load_to_pad(8, "test_beat")
    
    # Save a pattern
    print("\n[5] Creating pattern...")
    sampler.workspace.sequences[0].set_step(0, 0, 0, 100)
    sampler.workspace.sequences[0].set_step(4, 4, 0, 80)
    sampler.workspace.sequences[0].set_step(8, 8, 0, 120)
    sampler.workspace.sequences[0].set_step(12, 0, 0, 90)
    sampler.workspace.save_pattern("main_pattern")
    
    print(f"   Saved patterns: {sampler.workspace.list_patterns()}")
    
    # Trigger pads
    print("\n[6] Testing pad triggers...")
    result = sampler.workspace.trigger_pad(0)
    print(f"   Pad 0 triggered: {result is not None}")
    
    result = sampler.workspace.trigger_pad(4)
    print(f"   Pad 4 triggered: {result is not None}")
    
    # Export
    print("\n[7] Exporting...")
    exports = sampler.export_workspace()
    print(f"   Exports: {len(exports)} items")
    
    print("\n" + "=" * 60)
    print("  COMPLETE SAMPLER READY!")
    print("=" * 60)