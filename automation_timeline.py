"""
AUTOMATION TIMELINE SYSTEM - Professional Production!
======================================================
- Create automation clips
- Parametric automation curves
- Timeline arrangement
- Mix automation
- Effect automation

Innovation: Full DAW-style automation in Python!
"""

import math
import json
import os
import struct
import wave
from typing import List, Dict, Optional, Callable, Tuple
from datetime import datetime
from enum import Enum


class AutomationType(Enum):
    """Types of automation"""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    SINE = "sine"
    SQUARE = "square"
    SAMPLE_HOLD = "sample_hold"
    RAMP = "ramp"


class AutomationPoint:
    """Single automation point"""
    
    def __init__(self, time: float, value: float, curve: str = "linear"):
        self.time = time  # Time in beats
        self.value = value  # Value 0-1
        self.curve = curve  # Interpolation type


class AutomationClip:
    """Automation clip for a single parameter"""
    
    def __init__(self, name: str, min_val: float = 0, max_val: float = 1):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.points = []
        self.enabled = True
    
    def add_point(self, time: float, value: float, curve: str = "linear"):
        """Add automation point"""
        value = max(0, min(1, value))  # Normalize to 0-1
        self.points.append(AutomationPoint(time, value, curve))
        self.points.sort(key=lambda p: p.time)
    
    def get_value(self, time: float) -> float:
        """Get value at specific time"""
        
        if not self.points:
            return (self.max_val - self.min_val) / 2 + self.min_val
        
        # Find surrounding points
        if time <= self.points[0].time:
            return self._scale(self.points[0].value)
        
        if time >= self.points[-1].time:
            return self._scale(self.points[-1].value)
        
        # Interpolate between points
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            
            if p1.time <= time <= p2.time:
                # Normalize time between points
                t = (time - p1.time) / (p2.time - p1.time)
                
                # Apply curve
                if p1.curve == "linear":
                    value = p1.value + (p2.value - p1.value) * t
                elif p1.curve == "exponential":
                    value = p1.value * (p2.value / p1.value) ** t if p1.value > 0 else p2.value
                elif p1.curve == "sine":
                    value = p1.value + (p2.value - p1.value) * (1 - math.cos(t * math.pi)) / 2
                else:
                    value = p1.value + (p2.value - p1.value) * t
                
                return self._scale(value)
        
        return self._scale(0.5)
    
    def _scale(self, normalized: float) -> float:
        """Scale normalized value to min-max range"""
        return self.min_val + normalized * (self.max_val - self.min_val)
    
    def clear(self):
        """Clear all points"""
        self.points = []


class TimelineTrack:
    """A track in the timeline (audio, MIDI, or automation)"""
    
    def __init__(self, name: str, track_type: str = "audio"):
        self.name = name
        self.track_type = track_type  # audio, midi, automation
        self.clips = []  # List of audio/MIDI clips
        self.automation = {}  # Dict of parameter name -> AutomationClip
        self.volume = 1.0
        self.pan = 0.5  # 0 = left, 0.5 = center, 1 = right
        self.mute = False
        self.solo = False
    
    def add_automation(self, param_name: str, min_val: float = 0, max_val: float = 1):
        """Add automation track for a parameter"""
        self.automation[param_name] = AutomationClip(param_name, min_val, max_val)
    
    def get_automation_value(self, param_name: str, time: float) -> float:
        """Get automation value at time"""
        if param_name in self.automation:
            return self.automation[param_name].get_value(time)
        return 0.5


class Timeline:
    """Complete timeline with tracks and arrangement"""
    
    def __init__(self, bpm: int = 120, time_signature: Tuple[int, int] = (4, 4)):
        self.bpm = bpm
        self.time_signature = time_signature
        self.tracks = []
        self.total_bars = 16
        self.playhead = 0
        self.is_playing = False
        
        # Transport state
        self.loop_start = 0
        self.loop_end = 16
        self.loop_enabled = False
    
    def add_track(self, name: str, track_type: str = "audio") -> TimelineTrack:
        """Add a track to the timeline"""
        track = TimelineTrack(name, track_type)
        self.tracks.append(track)
        return track
    
    def get_track(self, name: str) -> Optional[TimelineTrack]:
        """Get track by name"""
        for track in self.tracks:
            if track.name == name:
                return track
        return None
    
    def get_beat_duration(self) -> float:
        """Get duration of one beat in seconds"""
        return 60.0 / self.bpm
    
    def get_bar_duration(self) -> float:
        """Get duration of one bar in seconds"""
        return self.get_beat_duration() * self.time_signature[0]
    
    def time_to_beats(self, time_seconds: float) -> float:
        """Convert time in seconds to beats"""
        return time_seconds * self.bpm / 60
    
    def beats_to_time(self, beats: float) -> float:
        """Convert beats to time in seconds"""
        return beats * 60 / self.bpm
    
    def set_loop(self, start: int, end: int):
        """Set loop region"""
        self.loop_start = max(0, start)
        self.loop_end = min(self.total_bars, end)
        self.loop_enabled = True
    
    def clear_loop(self):
        """Clear loop"""
        self.loop_enabled = False


class AutomationTimeline(AutomationClip):
    """Automation timeline with presets"""
    
    PRESETS = {
        'fade_in': [(0, 0), (4, 1)],
        'fade_out': [(0, 1), (4, 0)],
        'swell': [(0, 0), (2, 1), (4, 0)],
        'pulse': [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        'ramp_up': [(0, 0), (4, 1), "linear"],
        'ramp_down': [(0, 1), (4, 0), "linear"],
        'sine_wave': [(0, 0.5), (1, 1), (2, 0.5), (3, 0), (4, 0.5), "sine"],
        'step': [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), "sample_hold"],
    }
    
    @classmethod
    def from_preset(cls, name: str, duration_bars: int = 4) -> 'AutomationTimeline':
        """Create automation from preset"""
        
        if name not in cls.PRESETS:
            name = 'swell'
        
        auto = cls("preset")
        
        preset = cls.PRESETS[name]
        points_data = preset[:-1] if len(preset) > 2 else preset
        
        for i, point_data in enumerate(points_data):
            time_ratio = i / (len(points_data) - 1) if len(points_data) > 1 else 0
            time = time_ratio * duration_bars * 4  # Convert to beats
            curve = preset[-1] if isinstance(preset[-1], str) else "linear"
            
            auto.add_point(time, point_data[1], curve)
        
        return auto


class MixAutomation:
    """Mix automation - volume, pan, mute, solo"""
    
    def __init__(self, timeline: Timeline):
        self.timeline = timeline
    
    def create_volume_automation(self, track_name: str, points: List[Tuple[float, float]]):
        """Create volume automation for a track"""
        
        track = self.timeline.get_track(track_name)
        if not track:
            return
        
        track.add_automation("volume", 0, 1)
        volume_auto = track.automation["volume"]
        
        for time, value in points:
            volume_auto.add_point(time, value, "linear")
    
    def create_pan_automation(self, track_name: str, points: List[Tuple[float, float]]):
        """Create pan automation (-1 to 1)"""
        
        track = self.timeline.get_track(track_name)
        if not track:
            return
        
        track.add_automation("pan", -1, 1)
        pan_auto = track.automation["pan"]
        
        for time, value in points:
            pan_auto.add_point(time, value, "linear")
    
    def create_mix_snapshot(self, name: str, volumes: Dict[str, float], pans: Dict[str, float]):
        """Create a mix snapshot (static mix)"""
        
        for track_name, vol in volumes.items():
            track = self.timeline.get_track(track_name)
            if track:
                track.volume = vol
        
        for track_name, pan in pans.items():
            track = self.timeline.get_track(track_name)
            if track:
                track.pan = pan
        
        print(f"Mix snapshot '{name}' created")
    
    def interpolate_volumes(self, track_name: str, duration_bars: int, 
                           start_vol: float, end_vol: float):
        """Create volume fade over duration"""
        
        self.create_volume_automation(
            track_name,
            [
                (0, start_vol),
                (duration_bars * 4, end_vol)
            ]
        )
    
    def create_crossfade(self, track_a: str, track_b: str, duration_beats: float = 8):
        """Create crossfade between two tracks"""
        
        # Track A fades out
        self.create_volume_automation(
            track_a,
            [
                (0, 1),
                (duration_beats, 0)
            ]
        )
        
        # Track B fades in
        self.create_volume_automation(
            track_b,
            [
                (0, 0),
                (duration_beats, 1)
            ]
        )


class EffectAutomation:
    """Automation for effects parameters"""
    
    def __init__(self, timeline: Timeline):
        self.timeline = timeline
    
    def automate_filter_cutoff(self, track_name: str, start_freq: float, 
                               end_freq: float, duration_bars: int):
        """Automate filter cutoff (simple version)"""
        
        track = self.timeline.get_track(track_name)
        if not track:
            return
        
        track.add_automation("filter_freq", 100, 10000)
        filter_auto = track.automation["filter_freq"]
        
        # Convert to normalized 0-1
        start_norm = (math.log10(start_freq) - 2) / 3  # 100Hz = ~0, 10kHz = ~1
        end_norm = (math.log10(end_freq) - 2) / 3
        
        filter_auto.add_point(0, start_norm, "linear")
        filter_auto.add_point(duration_bars * 4, end_norm, "linear")
    
    def automate_reverb_wet(self, track_name: str, points: List[Tuple[float, float]]):
        """Automate reverb wet/dry mix"""
        
        track = self.timeline.get_track(track_name)
        if not track:
            return
        
        track.add_automation("reverb_wet", 0, 1)
        reverb_auto = track.automation["reverb_wet"]
        
        for time, value in points:
            reverb_auto.add_point(time, value, "linear")
    
    def automate_distortion_drive(self, track_name: str, points: List[Tuple[float, float]]):
        """Automate distortion drive amount"""
        
        track = self.timeline.get_track(track_name)
        if not track:
            return
        
        track.add_automation("distortion_drive", 0, 1)
        drive_auto = track.automation["distortion_drive"]
        
        for time, value in points:
            drive_auto.add_point(time, value, "linear")


class TimelineExporter:
    """Export timeline to audio file"""
    
    def __init__(self, timeline: Timeline, sample_rate: int = 44100):
        self.timeline = timeline
        self.sample_rate = sample_rate
    
    def export_wav(self, filename: str):
        """Export timeline to WAV"""
        
        duration_sec = self.timeline.total_bars * self.timeline.get_bar_duration()
        total_samples = int(duration_sec * self.sample_rate)
        
        # Mix all tracks
        mixed = [0.0] * total_samples
        
        for track in self.timeline.tracks:
            if track.mute:
                continue
            
            # For now, add placeholder silence for each track
            # In real implementation, would add actual audio clips
            track_gain = track.volume
            
            # Apply track volume automation at each sample
            for i in range(total_samples):
                time_beats = self.timeline.time_to_beats(i / self.sample_rate)
                
                # Get volume at this time
                if "volume" in track.automation:
                    vol = track.automation["volume"].get_value(time_beats)
                else:
                    vol = track.volume
                
                # Apply
                if not track.mute:
                    # Placeholder - in real implementation would add actual audio
                    pass
        
        # Normalize
        max_val = max(abs(s) for s in mixed) if mixed else 1
        if max_val > 0:
            mixed = [s * 0.8 / max_val for s in mixed]
        
        # Save
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            for s in mixed:
                packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
                wav.writeframes(packed)
        
        return filename
    
    def export_mixdown_json(self, filename: str):
        """Export timeline as JSON for external rendering"""
        
        data = {
            'bpm': self.timeline.bpm,
            'time_signature': list(self.timeline.time_signature),
            'total_bars': self.timeline.total_bars,
            'tracks': []
        }
        
        for track in self.timeline.tracks:
            track_data = {
                'name': track.name,
                'type': track.track_type,
                'volume': track.volume,
                'pan': track.pan,
                'mute': track.mute,
                'solo': track.solo,
                'automation': {}
            }
            
            for param, auto in track.automation.items():
                points = [(p.time, p.value, p.curve) for p in auto.points]
                track_data['automation'][param] = points
            
            data['tracks'].append(track_data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  AUTOMATION TIMELINE SYSTEM TEST")
    print("=" * 60)
    
    # Create timeline
    timeline = Timeline(bpm=120)
    
    # Add tracks
    drums = timeline.add_track("Drums", "audio")
    bass = timeline.add_track("Bass", "audio")
    synths = timeline.add_track("Synths", "audio")
    
    # Create mix automation
    mix = MixAutomation(timeline)
    
    # Volume automation - fade in drums
    mix.interpolate_volumes("Drums", 4, 0, 1)
    
    # Volume automation - fade out bass at end
    mix.create_volume_automation("Bass", [
        (0, 0.8),
        (12, 0.8),
        (16, 0.2)
    ])
    
    # Pan automation - synths move left to right
    mix.create_pan_automation("Synths", [
        (0, -0.5),
        (8, 0),
        (16, 0.5)
    ])
    
    print("\nCreated automation:")
    print(f"  Drums: Volume fade in over 4 bars")
    print(f"  Bass: Volume fade out at end")
    print(f"  Synths: Pan left to right")
    
    # Create effect automation
    effects = EffectAutomation(timeline)
    effects.automate_filter_cutoff("Synths", 500, 5000, 8)
    
    print(f"  Synths: Filter sweep 500Hz -> 5kHz")
    
    # Test automation point value
    synth_track = timeline.get_track("Synths")
    if synth_track and "volume" in synth_track.automation:
        vol_auto = synth_track.automation["volume"]
        print(f"\nVolume at beat 0: {vol_auto.get_value(0):.2f}")
        print(f"Volume at beat 8: {vol_auto.get_value(8):.2f}")
        print(f"Volume at beat 16: {vol_auto.get_value(16):.2f}")
    
    # Test preset
    print("\nTesting presets...")
    fade_in = AutomationTimeline.from_preset('fade_in', 4)
    pulse = AutomationTimeline.from_preset('pulse', 4)
    
    print(f"  Fade in value at beat 2: {fade_in.get_value(8):.2f}")
    print(f"  Pulse value at beat 1: {pulse.get_value(4):.2f}")
    
    # Export
    exporter = TimelineExporter(timeline)
    exporter.export_mixdown_json("audio/timeline_export.json")
    
    print("\n[OK] Timeline exported to audio/timeline_export.json")
    print("\nAutomation system ready!")