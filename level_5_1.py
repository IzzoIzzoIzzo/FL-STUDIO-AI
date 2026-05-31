"""
LEVEL 5.1 - ADVANCED AUTOMATION & SIDECHAIN
===========================================
- Automation curves
- Sidechain compression
- LFO modulation
- Macro controls

Adding pro DAW features!
"""

import math
import random
from typing import List, Dict


class AutomationCurve:
    """Advanced automation curves"""
    
    TYPES = ['linear', 'exponential', 'logarithmic', 's_curve', 'step', 'bezier']
    
    def __init__(self, name: str, param: str):
        self.name = name
        self.param = param
        self.points = []
        self.curve_type = 'linear'
    
    def add_point(self, beat: float, value: float, curve: str = 'linear'):
        """Add automation point"""
        self.points.append({
            'beat': beat,
            'value': value,
            'curve': curve
        })
        self.points.sort(key=lambda p: p['beat'])
    
    def get_value(self, beat: float) -> float:
        """Get value at beat position"""
        if not self.points:
            return 0.5
        
        if beat <= self.points[0]['beat']:
            return self.points[0]['value']
        if beat >= self.points[-1]['beat']:
            return self.points[-1]['value']
        
        # Find surrounding points
        for i in range(len(self.points) - 1):
            if self.points[i]['beat'] <= beat <= self.points[i+1]['beat']:
                p1 = self.points[i]
                p2 = self.points[i+1]
                
                # Interpolate based on curve type
                t = (beat - p1['beat']) / (p2['beat'] - p1['beat'])
                curve = p1.get('curve', 'linear')
                
                return self._interpolate(p1['value'], p2['value'], t, curve)
        
        return 0.5
    
    def _interpolate(self, v1: float, v2: float, t: float, curve: str) -> float:
        """Interpolate based on curve type"""
        
        if curve == 'linear':
            return v1 + (v2 - v1) * t
        
        elif curve == 'exponential':
            return v1 + (v2 - v1) * (t ** 2)
        
        elif curve == 'logarithmic':
            return v1 + (v2 - v1) * math.sqrt(t)
        
        elif curve == 's_curve':
            return v1 + (v2 - v1) * (t * t * (3 - 2 * t))
        
        elif curve == 'step':
            return v1
        
        else:  # bezier approximation
            return v1 + (v2 - v1) * (t ** 1.5)


class SidechainCompressor:
    """Advanced sidechain compression"""
    
    MODES = ['classic', 'punch', 'smoothing', 'ghost', 'ducking']
    
    def __init__(self, mode: str = 'classic'):
        self.mode = mode
        self.threshold = -12.0  # dB
        self.ratio = 4.0
        self.attack = 10.0  # ms
        self.release = 100.0  # ms
        self.makeup = 0.0
        self.key_input = None
        self._set_mode_params()
    
    def _set_mode_params(self):
        """Set parameters based on mode"""
        
        presets = {
            'classic': {'threshold': -12, 'ratio': 4, 'attack': 10, 'release': 100},
            'punch': {'threshold': -6, 'ratio': 8, 'attack': 1, 'release': 50},
            'smoothing': {'threshold': -18, 'ratio': 2, 'attack': 50, 'release': 200},
            'ghost': {'threshold': -24, 'ratio': 2, 'attack': 100, 'release': 300},
            'ducking': {'threshold': -30, 'ratio': 10, 'attack': 1, 'release': 500},
        }
        
        if self.mode in presets:
            p = presets[self.mode]
            self.threshold = p['threshold']
            self.ratio = p['ratio']
            self.attack = p['attack']
            self.release = p['release']
    
    def process(self, audio: List[float], key_audio: List[float]) -> List[float]:
        """Process audio with sidechain"""
        
        if len(key_audio) == 0:
            return audio
        
        output = []
        
        for i, (sample, key_sample) in enumerate(zip(audio, key_audio)):
            # Get envelope from key
            envelope = abs(key_sample)
            
            # Calculate gain reduction
            if envelope > 0:
                db = 20 * math.log10(envelope)
                if db > self.threshold:
                    excess = db - self.threshold
                    gain_reduction = excess * (1 - 1/self.ratio)
                    gain = 10 ** (-gain_reduction / 20)
                else:
                    gain = 1.0
            else:
                gain = 1.0
            
            # Apply with makeup
            output.append(sample * gain * (10 ** (self.makeup / 20)))
        
        return output
    
    def set_params(self, **kwargs):
        """Set compressor parameters"""
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)


class LFOModulation:
    """LFO for modulation"""
    
    WAVEFORMS = ['sine', 'triangle', 'square', 'saw_up', 'saw_down', 'random']
    
    def __init__(self, waveform: str = 'sine', rate: float = 1.0, depth: float = 1.0):
        self.waveform = waveform
        self.rate = rate  # Hz
        self.depth = depth
        self.phase = 0.0
        self.offset = 0.0
    
    def get_value(self, time_seconds: float) -> float:
        """Get LFO value at time"""
        
        phase = (time_seconds * self.rate * 2 * math.pi) + self.phase
        
        if self.waveform == 'sine':
            value = math.sin(phase)
        elif self.waveform == 'triangle':
            value = 2 * abs((phase / (2 * math.pi)) % 1 - 0.5) - 1
        elif self.waveform == 'square':
            value = 1 if (phase / (2 * math.pi)) % 1 < 0.5 else -1
        elif self.waveform == 'saw_up':
            value = 2 * ((phase / (2 * math.pi)) % 1) - 1
        elif self.waveform == 'saw_down':
            value = 1 - 2 * ((phase / (2 * math.pi)) % 1)
        elif self.waveform == 'random':
            value = random.uniform(-1, 1)
        else:
            value = math.sin(phase)
        
        return value * self.depth + self.offset
    
    def reset_phase(self):
        """Reset phase to start"""
        self.phase = 0.0


class MacroControl:
    """Macro controls for easy manipulation"""
    
    def __init__(self, name: str):
        self.name = name
        self.value = 0.5
        self.min_value = 0.0
        self.max_value = 1.0
        self.mappings = []
        self.automation = None
    
    def set_value(self, value: float):
        """Set macro value"""
        self.value = max(self.min_value, min(self.max_value, value))
        self._update_mappings()
    
    def add_mapping(self, param_name: str, min_val: float, max_val: float, curve: str = 'linear'):
        """Map parameter to macro"""
        self.mappings.append({
            'param': param_name,
            'min': min_val,
            'max': max_val,
            'curve': curve
        })
    
    def _update_mappings(self):
        """Update all mapped parameters"""
        for mapping in self.mappings:
            # Convert 0-1 range to parameter range
            if mapping['curve'] == 'linear':
                mapped_value = mapping['min'] + (mapping['max'] - mapping['min']) * self.value
            elif mapping['curve'] == 'exponential':
                mapped_value = mapping['min'] * (mapping['max'] / mapping['min']) ** self.value
            else:
                mapped_value = mapping['min'] + (mapping['max'] - mapping['min']) * self.value
            
            # Store for later use (in actual DAW this would update the param)
            mapping['current_value'] = mapped_value


class AutomationManager:
    """Manage all automation"""
    
    def __init__(self):
        self.curves = {}
        self.macros = {}
        self.sidechain = SidechainCompressor()
    
    def create_curve(self, name: str, param: str) -> AutomationCurve:
        """Create automation curve"""
        curve = AutomationCurve(name, param)
        self.curves[name] = curve
        return curve
    
    def create_macro(self, name: str) -> MacroControl:
        """Create macro control"""
        macro = MacroControl(name)
        self.macros[name] = macro
        return macro
    
    def add_sidechain_track(self, source: str, target: str, mode: str = 'classic'):
        """Add sidechain routing"""
        return {'source': source, 'target': target, 'mode': mode}


def demo():
    print("=" * 60)
    print("  LEVEL 5.1 - ADVANCED AUTOMATION & SIDECHAIN")
    print("=" * 60)
    
    # Automation Curve
    print("\n[Automation Curve]")
    vol = AutomationCurve("Volume", "volume")
    vol.add_point(0, 0.0, 'linear')
    vol.add_point(4, 0.8, 'exponential')
    vol.add_point(8, 1.0, 'linear')
    vol.add_point(12, 0.3, 's_curve')
    
    print(f"  Value at beat 2: {vol.get_value(2):.2f}")
    print(f"  Value at beat 6: {vol.get_value(6):.2f}")
    print(f"  Value at beat 10: {vol.get_value(10):.2f}")
    
    # Sidechain
    print("\n[Sidechain Compressor]")
    sc = SidechainCompressor('punch')
    print(f"  Mode: {sc.mode}, Threshold: {sc.threshold}dB, Ratio: {sc.ratio}:1")
    
    # LFO
    print("\n[LFO Modulation]")
    lfo = LFOModulation('sine', rate=2.0, depth=0.5)
    print(f"  Waveform: {lfo.waveform}, Rate: {lfo.rate}Hz")
    print(f"  t=0.0s: {lfo.get_value(0.0):.2f}, t=0.25s: {lfo.get_value(0.25):.2f}")
    
    # Macro
    print("\n[Macro Control]")
    macro = MacroControl("Master")
    macro.add_mapping("volume", 0.0, 1.0)
    macro.add_mapping("compressor_threshold", -30, 0)
    macro.set_value(0.75)
    print(f"  Macro 'Master': {macro.value}")
    for m in macro.mappings:
        print(f"    {m['param']}: {m.get('current_value', 'N/A')}")
    
    # Automation Manager
    print("\n[Automation Manager]")
    am = AutomationManager()
    am.create_curve("Filter Cutoff", "filter_freq")
    am.create_macro("Impact")
    print(f"  Curves: {len(am.curves)}, Macros: {len(am.macros)}")
    
    print("\n" + "=" * 60)
    print("  LEVEL 5.1 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()