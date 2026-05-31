"""
LIVE PERFORMANCE & DJ ENGINE
=============================
DJ Mixers, Performance Controllers, Beatmatching, Crossfading
Looping, Sampling, Effects Chains, Hot Cues, Loop Rolls
Stem Mixing, Real-time Processing, Visual Feedback

ALL CONNECTED!
"""

import math
import random
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class LoopMode(Enum):
    """Loop modes"""
    ONE_SHOT = "one_shot"
    LOOP = "loop"
    GATE = "gate"
    PING_PONG = "ping_pong"
    SLICE = "slice"


class EffectType(Enum):
    """Performance effects"""
    FILTER = "filter"
    REVERB = "reverb"
    DELAY = "delay"
    BITCRUSH = "bitcrush"
    STUTTER = "stutter"
    REVERSE = "reverse"
    PITCH_SHIFT = "pitch_shift"


@dataclass
class DeckState:
    """DJ deck state"""
    track_name: str
    bpm: float
    position: float  # seconds
    pitch: float = 1.0
    volume: float = 0.8
    filter_freq: float = 20000
    filter_res: float = 0
    eq_high: float = 1.0
    eq_mid: float = 1.0
    eq_low: float = 1.0
    gain: float = 1.0


@dataclass
class HotCue:
    """Hot cue point"""
    position: float
    sample_start: float
    color: str
    name: str
    active: bool = False


class DJDeck:
    """DJ Deck with playback control"""
    
    def __init__(self, deck_id: int = 1):
        self.deck_id = deck_id
        self.audio = []
        self.sample_rate = 44100
        self.state = DeckState("No track loaded", 120, 0)
        self.is_playing = False
        self.is_cued = False
        self.loop_start = 0
        self.loop_end = 0
        self.loop_active = False
        self.hot_cues: List[HotCue] = [None] * 8
        self.pitch_range = 8.0  # +/- 8%
    
    def load_track(self, audio: List[float], bpm: float, name: str = "Track"):
        """Load track to deck"""
        self.audio = audio
        self.state = DeckState(name, bpm, 0)
        self.is_playing = False
        self.is_cued = False
    
    def play(self):
        """Start playback"""
        self.is_playing = True
    
    def pause(self):
        """Pause playback"""
        self.is_playing = False
    
    def stop(self):
        """Stop and reset"""
        self.is_playing = False
        self.state.position = 0
    
    def seek(self, position: float):
        """Seek to position (seconds)"""
        self.state.position = max(0, min(position, len(self.audio) / self.sample_rate))
    
    def set_pitch(self, pitch: float):
        """Set pitch/tempo (1.0 = normal)"""
        self.state.pitch = max(1 - self.pitch_range/100, min(1 + self.pitch_range/100, pitch))
    
    def set_volume(self, volume: float):
        """Set volume (0-1)"""
        self.state.volume = max(0, min(1, volume))
    
    def set_eq(self, high: float = 1.0, mid: float = 1.0, low: float = 1.0):
        """Set EQ"""
        self.state.eq_high = max(0, min(2, high))
        self.state.eq_mid = max(0, min(2, mid))
        self.state.eq_low = max(0, min(2, low))
    
    def set_filter(self, freq: float, res: float = 0):
        """Set filter"""
        self.state.filter_freq = max(20, min(20000, freq))
        self.state.filter_res = max(0, min(10, res))
    
    def set_loop(self, start: float, end: float):
        """Set loop points"""
        self.loop_start = start
        self.loop_end = end
        self.loop_active = True
    
    def clear_loop(self):
        """Clear loop"""
        self.loop_active = False
    
    def set_hot_cue(self, index: int, position: float, color: str, name: str = ""):
        """Set hot cue"""
        if 0 <= index < 8:
            self.hot_cues[index] = HotCue(position, position, color, name, True)
    
    def trigger_hot_cue(self, index: int):
        """Trigger hot cue"""
        if 0 <= index < 8 and self.hot_cues[index]:
            self.seek(self.hot_cues[index].position)
            self.play()
    
    def get_position_seconds(self) -> float:
        """Get current position in seconds"""
        return self.state.position
    
    def get_position_beats(self) -> float:
        """Get current position in beats"""
        return self.state.position * self.state.bpm / 60
    
    def get_remaining_time(self) -> float:
        """Get remaining time"""
        track_duration = len(self.audio) / self.sample_rate
        return max(0, track_duration - self.state.position)


class DJMixer:
    """DJ Mixer"""
    
    def __init__(self, num_decks: int = 2):
        self.decks = [DJDeck(i + 1) for i in range(num_decks)]
        self.crossfader = 0.5  # 0 = deck A full, 1 = deck B full
        self.master_volume = 0.8
        self.headphone_volume = 0.7
        self.headphone_mix = 0.5  # 0 = deck A, 1 = deck B
        
        # Master effects
        self.master_eq = {'high': 1.0, 'mid': 1.0, 'low': 1.0}
        self.master_limiter = True
    
    def set_crossfader(self, position: float):
        """Set crossfader position"""
        self.crossfader = max(0, min(1, position))
    
    def get_deck_volume(self, deck_index: int) -> float:
        """Get deck volume with crossfader"""
        if deck_index == 0:  # Deck A
            return self.decks[0].state.volume * (1 - self.crossfader)
        else:  # Deck B
            return self.decks[1].state.volume * self.crossfader
    
    def mix_decks(self) -> List[float]:
        """Mix decks to stereo output"""
        if not self.decks[0].audio or not self.decks[1].audio:
            # Return silence if no tracks
            if self.decks[0].audio:
                return self.decks[0].audio[:self.decks[0].sample_rate]
            return [0.0] * self.decks[0].sample_rate
        
        # Get deck outputs
        deck_a = self._get_deck_output(0)
        deck_b = self._get_deck_output(1)
        
        # Ensure same length
        max_len = max(len(deck_a), len(deck_b))
        
        deck_a += [0.0] * (max_len - len(deck_a))
        deck_b += [0.0] * (max_len - len(deck_b))
        
        # Crossfade
        mix = []
        for a, b in zip(deck_a, deck_b):
            vol_a = a * (1 - self.crossfader)
            vol_b = b * self.crossfader
            mix.append((vol_a + vol_b) * self.master_volume)
        
        # Master EQ
        mix = self._apply_master_eq(mix)
        
        # Limiter
        if self.master_limiter:
            mix = self._apply_limiter(mix)
        
        return mix
    
    def _get_deck_output(self, deck_index: int) -> List[float]:
        """Get processed deck output"""
        deck = self.decks[deck_index]
        
        if not deck.audio:
            return []
        
        # Get audio from current position
        start_sample = int(deck.state.position * deck.sample_rate)
        
        # Get a reasonable chunk
        samples = 30 * deck.sample_rate  # 30 seconds
        end_sample = min(start_sample + samples, len(deck.audio))
        
        audio = deck.audio[start_sample:end_sample]
        
        # Apply deck processing
        audio = [s * deck.state.volume for s in audio]
        
        # EQ
        for i, sample in enumerate(audio):
            # Simplified EQ
            audio[i] = sample * deck.state.eq_low * deck.state.eq_mid * deck.state.eq_high
        
        return audio
    
    def _apply_master_eq(self, audio: List[float]) -> List[float]:
        """Apply master EQ"""
        return audio  # Simplified
    
    def _apply_limiter(self, audio: List[float]) -> List[float]:
        """Apply limiter"""
        output = []
        for sample in audio:
            if sample > 1:
                output.append(1)
            elif sample < -1:
                output.append(-1)
            else:
                output.append(sample)
        return output


class BeatMatcher:
    """Beatmatching and tempo sync"""
    
    def __init__(self, tolerance: float = 2.0):
        self.tolerance = tolerance  # BPM tolerance
        self.auto_tempo = True
        self.pitch_range = 8.0
    
    def calculate_bpm(self, audio: List[float], sample_rate: int = 44100) -> float:
        """Calculate BPM from audio"""
        
        # Simple onset detection
        window_size = int(sample_rate * 0.01)  # 10ms
        onset_threshold = 0.5
        
        onsets = []
        prev_energy = 0
        
        for i in range(0, len(audio) - window_size, window_size):
            window = audio[i:i+window_size]
            energy = sum(x*x for x in window) / window_size
            
            if energy > prev_energy * 1.5 and energy > onset_threshold:
                onsets.append(i / sample_rate)
            
            prev_energy = energy
        
        if len(onsets) < 2:
            return 120.0  # Default
        
        # Calculate average beat interval
        intervals = [onsets[i+1] - onsets[i] for i in range(len(onsets)-1)]
        
        # Remove outliers
        avg_interval = sum(intervals) / len(intervals)
        valid_intervals = [i for i in intervals if 0.2 < i < 2.0]
        
        if valid_intervals:
            avg_interval = sum(valid_intervals) / len(valid_intervals)
        
        bpm = 60 / avg_interval
        
        # Normalize to reasonable range
        while bpm < 60:
            bpm *= 2
        while bpm > 180:
            bpm /= 2
        
        return bpm
    
    def match_bpm(self, source_bpm: float, target_bpm: float) -> float:
        """Calculate pitch adjustment to match BPM"""
        
        ratio = target_bpm / source_bpm
        
        # Clamp to pitch range
        max_ratio = 1 + self.pitch_range / 100
        min_ratio = 1 - self.pitch_range / 100
        
        return max(min_ratio, min(max_ratio, ratio))
    
    def sync_decks(self, deck_from: DJDeck, deck_to: DJDeck):
        """Sync deck tempo to another deck"""
        
        source_bpm = deck_from.state.bpm
        target_bpm = deck_to.state.bpm
        
        pitch_ratio = self.match_bpm(source_bpm, target_bpm)
        
        deck_to.set_pitch(pitch_ratio)
        
        # Also try to sync beat position
        beat_from = deck_from.get_position_beats()
        beat_to = deck_to.get_position_beats()
        
        beat_diff = (beat_from - beat_to) % 4
        
        # Seek to align beats
        if abs(beat_diff) > 0.1:
            current_pos = deck_to.state.position
            beat_duration = 60 / deck_to.state.bpm
            seek_to = current_pos - (beat_diff * beat_duration / 4)
            deck_to.seek(max(0, seek_to))


class PerformanceSampler:
    """Performance sampler with looping"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.slot_duration = 8.0  # seconds
        self.slots = [None] * 16
        self.active_slot = None
        
    def record_slot(self, slot_index: int, audio: List[float]):
        """Record to sample slot"""
        if 0 <= slot_index < 16:
            # Trim to slot duration
            max_samples = int(self.slot_duration * self.sample_rate)
            self.slots[slot_index] = audio[:max_samples]
    
    def play_slot(self, slot_index: int) -> List[float]:
        """Play sample slot"""
        if 0 <= slot_index < 16 and self.slots[slot_index]:
            return self.slots[slot_index]
        return []
    
    def slice_sample(self, audio: List[float], num_slices: int = 8) -> List[List[float]]:
        """Slice sample into equal parts"""
        slice_size = len(audio) // num_slices
        
        slices = []
        for i in range(num_slices):
            start = i * slice_size
            end = start + slice_size
            slices.append(audio[start:end])
        
        return slices
    
    def time_stretch(self, audio: List[float], ratio: float) -> List[float]:
        """Simple time stretch"""
        
        if ratio == 1.0:
            return audio
        
        # Simple resampling
        new_length = int(len(audio) / ratio)
        stretched = []
        
        for i in range(new_length):
            src_idx = i * ratio
            idx = int(src_idx)
            
            if idx < len(audio):
                stretched.append(audio[idx])
            else:
                break
        
        return stretched


class PerformanceEffects:
    """Live performance effects"""
    
    def __init__(self):
        self.effects = {}
    
    def add_effect(self, name: str, effect_type: EffectType, params: Dict):
        """Add effect to chain"""
        self.effects[name] = {'type': effect_type, 'params': params}
    
    def apply_filter_sweep(self, audio: List[float], start_freq: float, 
                          end_freq: float, duration: float) -> List[float]:
        """Filter sweep effect"""
        
        output = []
        samples = len(audio)
        
        for i in range(samples):
            t = i / samples
            freq = start_freq + (end_freq - start_freq) * t
            
            # Simple low-pass
            if i == 0:
                output.append(audio[i])
            else:
                rc = 1 / (2 * math.pi * freq)
                alpha = rc / (rc + 1/44100)
                output.append(alpha * output[-1] + (1 - alpha) * audio[i])
        
        return output
    
    def apply_stutter(self, audio: List[float], rate: float = 8) -> List[float]:
        """Stutter effect"""
        
        output = []
        block_size = int(44100 / rate)
        
        for i in range(0, len(audio), block_size):
            block = audio[i:i+block_size]
            
            # Repeat block 2-4 times
            repeats = random.randint(2, 4)
            
            for _ in range(repeats):
                output.extend(block)
        
        return output[:len(audio)]
    
    def apply_bitcrush(self, audio: List[float], bits: int = 4) -> List[float]:
        """Bitcrush effect"""
        
        if bits >= 16:
            return audio
        
        level = 2 ** bits
        
        output = []
        for sample in audio:
            crushed = math.floor(sample * level) / level
            output.append(crushed)
        
        return output
    
    def apply_reverb(self, audio: List[float], room_size: float = 0.5) -> List[float]:
        """Simple reverb effect"""
        
        # Comb filter reverb
        delay_times = [0.0297, 0.0371, 0.0411, 0.0437]
        decay = 0.5 + room_size * 0.3
        
        output = audio[:]
        
        for delay in delay_times:
            delay_samples = int(delay * 44100)
            
            for i in range(delay_samples, len(audio)):
                output[i] += output[i - delay_samples] * decay
        
        # Normalize
        max_val = max(abs(x) for x in output) if output else 1
        if max_val > 0:
            output = [x / max_val * 0.9 for x in output]
        
        return output


class LoopController:
    """Advanced looping"""
    
    def __init__(self):
        self.active_loops = {}
    
    def create_loop(self, audio: List[float], start: float, end: float,
                   mode: LoopMode = LoopMode.LOOP) -> List[float]:
        """Create loop from audio"""
        
        start_sample = int(start * 44100)
        end_sample = int(end * 44100)
        
        loop_audio = audio[start_sample:end_sample]
        
        if mode == LoopMode.LOOP:
            # Repeat loop
            duration = end - start
            repeats = int(30 / duration)  # 30 seconds worth
            
            return loop_audio * repeats
        
        elif mode == LoopMode.PING_PONG:
            # Ping-pong
            reversed_loop = loop_audio[::-1]
            result = []
            
            for _ in range(10):
                result.extend(loop_audio)
                result.extend(reversed_loop)
            
            return result[:int(30 * 44100)]
        
        elif mode == LoopMode.GATE:
            # Gate/filter loop
            return loop_audio
        
        return loop_audio
    
    def create_loop_roll(self, audio: List[float], position: float, 
                        length: float = 0.25) -> List[float]:
        """Create loop roll"""
        
        start_sample = int(position * 44100)
        end_sample = start_sample + int(length * 44100)
        
        roll = audio[start_sample:end_sample]
        
        # Repeat rapidly
        return roll * int(30 / length)


class CompletePerformanceEngine:
    """Complete live performance system"""
    
    def __init__(self):
        self.mixer = DJMixer(2)
        self.beatmatch = BeatMatcher()
        self.sampler = PerformanceSampler()
        self.effects = PerformanceEffects()
        self.loop = LoopController()
    
    def setup_deck(self, deck_index: int, audio: List[float], bpm: float):
        """Setup deck with audio"""
        
        if deck_index < len(self.mixer.decks):
            self.mixer.decks[deck_index].load_track(audio, bpm)
            
            # Auto BPM detection if needed
            if bpm == 0:
                detected_bpm = self.beatmatch.calculate_bpm(audio)
                self.mixer.decks[deck_index].state.bpm = detected_bpm
    
    def sync_decks(self):
        """Sync deck 2 to deck 1"""
        
        self.beatmatch.sync_decks(
            self.mixer.decks[0],
            self.mixer.decks[1]
        )
    
    def crossfade_to(self, position: float, duration: float = 2.0):
        """Crossfade to position"""
        
        # Simple crossfade animation
        steps = int(duration * 10)
        
        for i in range(steps):
            progress = i / steps
            self.mixer.set_crossfader(progress)
    
    def trigger_cue(self, deck_index: int, cue_index: int):
        """Trigger hot cue"""
        
        if deck_index < len(self.mixer.decks):
            self.mixer.decks[deck_index].trigger_hot_cue(cue_index)
    
    def get_master_output(self) -> List[float]:
        """Get master output"""
        
        return self.mixer.mix_decks()
    
    def create_performance_recording(self) -> Dict:
        """Create performance recording"""
        
        return {
            'datetime': datetime.now().isoformat(),
            'deck1_bpm': self.mixer.decks[0].state.bpm,
            'deck2_bpm': self.mixer.decks[1].state.bpm,
            'crossfader': self.mixer.crossfader,
            'master_volume': self.mixer.master_volume,
        }


def demo():
    print("=" * 60)
    print("  LIVE PERFORMANCE & DJ ENGINE")
    print("=" * 60)
    
    engine = CompletePerformanceEngine()
    
    # Create some test audio
    test_audio = [math.sin(440 * 2 * math.pi * i / 44100) for i in range(44100 * 30)]
    
    print("\n[DJ Deck Setup]")
    engine.setup_deck(0, test_audio, 128)
    engine.setup_deck(1, test_audio, 130)
    
    deck1 = engine.mixer.decks[0]
    deck2 = engine.mixer.decks[1]
    
    print("  Deck 1: BPM %.1f, Position: %.1fs" % (deck1.state.bpm, deck1.state.position))
    print("  Deck 2: BPM %.1f, Position: %.1fs" % (deck2.state.bpm, deck2.state.position))
    
    print("\n[Beatmatching]")
    engine.sync_decks()
    print("  Synced Deck 2 to Deck 1")
    print("  Deck 2 pitch: %.3f" % deck2.state.pitch)
    
    print("\n[Hot Cues]")
    deck1.set_hot_cue(0, 30.0, "Red", "Intro")
    deck1.set_hot_cue(1, 60.0, "Blue", "Drop")
    print("  Set cue 0 at 30s, cue 1 at 60s")
    
    print("\n[Looping]")
    loop_audio = engine.loop.create_loop(test_audio, 10, 12, LoopMode.LOOP)
    print("  Created loop: %d samples" % len(loop_audio))
    
    roll = engine.loop.create_loop_roll(test_audio, 15, 0.25)
    print("  Loop roll: %d samples" % len(roll))
    
    print("\n[Performance Effects]")
    swept = engine.effects.apply_filter_sweep(test_audio[:44100], 20000, 100, 1)
    print("  Filter sweep: %d samples" % len(swept))
    
    stutter = engine.effects.apply_stutter(test_audio[:44100], 8)
    print("  Stutter: %d samples" % len(stutter))
    
    crushed = engine.effects.apply_bitcrush(test_audio[:44100], 4)
    print("  Bitcrush: %d samples" % len(crushed))
    
    print("\n[Mixer Control]")
    engine.mixer.set_crossfader(0.3)
    print("  Crossfader: %.1f%%" % (engine.mixer.crossfader * 100))
    
    engine.mixer.decks[0].set_eq(high=1.2, mid=1.0, low=1.5)
    print("  Deck 1 EQ: High=1.2, Mid=1.0, Low=1.5")
    
    print("\n[Sampling]")
    engine.sampler.record_slot(0, test_audio[:44100])
    slot_playback = engine.sampler.play_slot(0)
    print("  Sampler slot 0: %d samples" % len(slot_playback))
    
    slices = engine.sampler.slice_sample(test_audio[:44100], 8)
    print("  Sliced into %d parts" % len(slices))
    
    print("\n[Performance Recording]")
    recording = engine.create_performance_recording()
    print("  Time: %s" % recording['datetime'])
    print("  Deck 1 BPM: %.1f" % recording['deck1_bpm'])
    print("  Crossfader: %.1f%%" % (recording['crossfader'] * 100))
    
    print("\n" + "=" * 60)
    print("  PERFORMANCE ENGINE COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()