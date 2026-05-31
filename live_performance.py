"""
LIVE PERFORMANCE MODE - Real-time Beat Making!
==============================================
- Trigger beats live
- Loop/arrange in real-time
- Sync to external MIDI clock
- Hot-swap patterns
- Performance recording

Innovation: Play live like a DJ with generated beats!
"""

import math
import random
import time
import threading
import os
import struct
import wave
from typing import List, Dict, Optional, Callable
from datetime import datetime
from collections import deque


class LiveClock:
    """Synchronized clock for live performance"""
    
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.is_running = False
        self.is_paused = False
        self.start_time = 0
        self.pause_time = 0
        self.paused_duration = 0
        self.beat_count = 0
        self.listeners = []
        
    def start(self):
        self.is_running = True
        self.is_paused = False
        self.start_time = time.time()
        self.beat_count = 0
    
    def stop(self):
        self.is_running = False
        self.is_paused = False
    
    def pause(self):
        if self.is_running:
            self.is_paused = True
            self.pause_time = time.time()
    
    def resume(self):
        if self.is_paused:
            self.paused_duration += time.time() - self.pause_time
            self.is_paused = False
    
    def set_bpm(self, bpm: int):
        self.bpm = max(30, min(300, bpm))
    
    def get_beat_time(self) -> float:
        """Get current beat time"""
        if not self.is_running or self.is_paused:
            return 0
        
        elapsed = time.time() - self.start_time - self.paused_duration
        return elapsed * self.bpm / 60
    
    def get_current_beat(self) -> int:
        """Get current beat number"""
        return int(self.get_beat_time()) % 16
    
    def add_listener(self, callback: Callable):
        self.listeners.append(callback)
    
    def tick(self):
        """Process one tick of the clock"""
        if not self.is_running or self.is_paused:
            return
        
        current_beat = self.get_current_beat()
        
        # Notify listeners on beat change
        if current_beat != self.last_beat:
            for listener in self.listeners:
                listener(current_beat, self.beat_count)
            self.beat_count += 1
            self.last_beat = current_beat
    
    last_beat = 0


class LivePad:
    """Live performance pad - trigger anything instantly!"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.pads = {}
        self.assigned_beats = {}
    
    def assign_beat(self, pad_index: int, style: str, bars: int = 4):
        """Assign a beat to a pad"""
        from super_engine import BeatGenerator
        
        gen = BeatGenerator()
        result = gen.generate(style, bars)
        
        self.assigned_beats[pad_index] = {
            'style': style,
            'bars': bars,
            'audio': result['audio'],
            'bpm': result['bpm'],
            'duration': result['duration']
        }
        
        # Save to file for quick loading
        filename = f"audio/live_pad_{pad_index}.wav"
        self._save_wav(result['audio'], filename)
        
        return filename
    
    def trigger(self, pad_index: int) -> Optional[str]:
        """Trigger a pad"""
        if pad_index in self.assigned_beats:
            # Return audio data for playback
            return self.assigned_beats[pad_index]
        return None
    
    def _save_wav(self, samples: List[float], filename: str):
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # Normalize
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            samples = [s * 0.9 / max_val for s in samples]
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            for s in samples:
                packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
                wav.writeframes(packed)


class LiveArranger:
    """Real-time arrangement builder"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.slots = [None] * 16  # 16 slots for arrangement
        self.current_slot = 0
        self.is_playing = False
        self.loop_enabled = True
    
    def set_slot(self, slot_index: int, audio: List[float], name: str = ""):
        """Set audio for a slot"""
        if 0 <= slot_index < 16:
            self.slots[slot_index] = {
                'audio': audio,
                'name': name or f"Slot {slot_index + 1}"
            }
    
    def next_slot(self) -> Optional[Dict]:
        """Get next slot audio"""
        if not self.is_playing:
            return None
        
        slot = self.slots[self.current_slot]
        
        # Advance to next slot
        self.current_slot = (self.current_slot + 1) % 16
        
        # Loop or stop
        if self.current_slot == 0 and not self.loop_enabled:
            self.is_playing = False
        
        return slot
    
    def start_arrangement(self, loop: bool = True):
        self.loop_enabled = loop
        self.is_playing = True
        self.current_slot = 0
    
    def stop_arrangement(self):
        self.is_playing = False
    
    def clear_slots(self):
        self.slots = [None] * 16
        self.current_slot = 0


class PerformanceRecorder:
    """Record live performances"""
    
    def __init__(self):
        self.is_recording = False
        self.recorded_events = []
        self.start_time = 0
    
    def start_recording(self):
        self.is_recording = True
        self.recorded_events = []
        self.start_time = time.time()
    
    def stop_recording(self) -> List[Dict]:
        self.is_recording = False
        return self.recorded_events
    
    def record_event(self, event_type: str, data: Dict):
        if self.is_recording:
            self.recorded_events.append({
                'time': time.time() - self.start_time,
                'type': event_type,
                'data': data
            })
    
    def save_recording(self, filename: str):
        import json
        with open(filename, 'w') as f:
            json.dump({
                'recorded': datetime.now().isoformat(),
                'events': self.recorded_events
            }, f, indent=2)
    
    def load_recording(self, filename: str) -> List[Dict]:
        import json
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get('events', [])


class LivePerformance:
    """Complete live performance system"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.clock = LiveClock(120)
        self.pad = LivePad(sample_rate)
        self.arranger = LiveArranger(sample_rate)
        self.recorder = PerformanceRecorder()
        
        # Performance state
        self.is_playing = False
        self.current_scene = 0
        self.scenes = {}
        
        # Audio playback
        self.current_audio = None
        self.playback_position = 0
        
        print("=" * 60)
        print("  LIVE PERFORMANCE MODE")
        print("=" * 60)
    
    def setup_scene(self, scene_name: str, beats: Dict[int, str]):
        """Setup a performance scene (16 pads with beats)"""
        
        print(f"Setting up scene: {scene_name}")
        
        for pad_idx, style in beats.items():
            filename = self.pad.assign_beat(pad_idx, style, 4)
            print(f"  Pad {pad_idx + 1}: {style}")
        
        self.scenes[scene_name] = {
            'pads': list(beats.keys()),
            'assigned': self.pad.assigned_beats.copy()
        }
    
    def trigger_pad(self, pad_index: int) -> bool:
        """Trigger a pad - main performance function"""
        
        result = self.pad.trigger(pad_index)
        
        if result:
            self.current_audio = result['audio']
            self.playback_position = 0
            
            # Record event
            self.recorder.record_event('pad_trigger', {
                'pad': pad_index,
                'style': result['style']
            })
            
            return True
        
        return False
    
    def start_performance(self, bpm: int = 120):
        """Start the performance clock"""
        self.clock.set_bpm(bpm)
        self.clock.start()
        self.is_playing = True
        self.recorder.start_recording()
        print(f"Performance started at {bpm} BPM")
    
    def stop_performance(self):
        """Stop the performance"""
        self.clock.stop()
        self.is_playing = False
        events = self.recorder.stop_recording()
        print(f"Performance stopped. Recorded {len(events)} events")
    
    def save_performance(self, filename: str = "performance.json"):
        """Save recorded performance"""
        self.recorder.save_recording(filename)
        print(f"Performance saved: {filename}")
    
    def export_arrangement(self, filename: str = "live_set.wav"):
        """Export the current arrangement as audio"""
        
        # Combine all slots
        combined = []
        
        for slot in self.arranger.slots:
            if slot:
                combined.extend(slot['audio'])
        
        if combined:
            # Normalize and save
            max_val = max(abs(s) for s in combined) if combined else 1
            if max_val > 0:
                combined = [s * 0.9 / max_val for s in combined]
            
            with wave.open(filename, 'w') as wav:
                wav.setnchannels(2)
                wav.setsampwidth(2)
                wav.setframerate(self.sample_rate)
                for s in combined:
                    packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
                    wav.writeframes(packed)
            
            print(f"Arrangement exported: {filename}")
            return filename
        
        return None


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  LIVE PERFORMANCE MODE TEST")
    print("=" * 60)
    
    # Create performance system
    perf = LivePerformance()
    
    # Setup a scene with different beats on pads
    scene_beats = {
        0: 'trap',
        1: 'house',
        2: 'hiphop',
        3: 'dubstep',
        4: 'lofi',
        5: 'edm',
        6: 'dnb',
        7: 'trap',
    }
    
    perf.setup_scene("Main Set", scene_beats)
    
    print("\nTriggering pads...")
    perf.trigger_pad(0)
    print("Pad 0 triggered!")
    perf.trigger_pad(3)
    print("Pad 3 triggered!")
    
    # Test arrangement
    from super_engine import BeatGenerator
    gen = BeatGenerator()
    
    for i in range(4):
        beat = gen.generate(['trap', 'house', 'hiphop'][i % 3], 2)
        perf.arranger.set_slot(i, beat['audio'], f"Part {i+1}")
    
    print("\nArrangement set with 4 parts")
    perf.arranger.start_arrangement(loop=True)
    
    print("\n[OK] Live Performance ready!")
    print("Use perf.trigger_pad(0-7) to trigger beats live!")
    print("Use perf.start_performance(bpm) to start clock!")