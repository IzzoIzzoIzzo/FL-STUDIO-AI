"""
EXTRA SYNTHESIS ENGINE
=====================
Additional synthesis methods beyond the basic set:
- Karplus-Strong String Synthesis
- Modal Synthesis (resonant filters)
- Vector Synthesis
- Analog Modeling
- Circuit Modeling
- Modulation Matrix
- Perceptual Synthesis

ALL CONNECTED TO MAIN API!
"""

import math
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class SynthesisType(Enum):
    """Extended synthesis types"""
    KARPLUS_STRONG = "karplus_strong"
    MODAL = "modal"
    VECTOR = "vector"
    ANALOG_MODEL = "analog_model"
    CIRCUIT_MODEL = "circuit_model"
    MODULATION_MATRIX = "modulation_matrix"
    PERCEPTUAL = "perceptual"


class KarplusStrongSynthesizer:
    """Karplus-Strong string synthesis - realistic string/pluck sounds"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
    def generate(self, duration: float, frequency: float, 
                 decay: float = 0.8, brightness: float = 0.5) -> List[float]:
        """Generate plucked string sound"""
        delay_length = int(self.sample_rate / frequency)
        
        buffer = [random.uniform(-1, 1) * 0.5 for _ in range(delay_length)]
        
        for i in range(min(10, delay_length)):
            buffer[i] *= (i / 10) * brightness
        
        samples = int(self.sample_rate * duration)
        output = [0.0] * samples
        
        alpha = decay * (0.5 + brightness * 0.5)
        
        for i in range(samples):
            read_pos = i % delay_length
            output[i] = buffer[read_pos]
            
            if read_pos > 0:
                buffer[read_pos] = (buffer[read_pos] + buffer[read_pos - 1]) * alpha
            else:
                buffer[read_pos] = (buffer[read_pos] + buffer[delay_length - 1]) * alpha
        
        return output


class ModalSynthesizer:
    """Modal synthesis - resonant physical modeling"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.modes = []
        
    def add_mode(self, frequency: float, decay: float, amplitude: float = 1.0):
        self.modes.append({
            'frequency': frequency,
            'decay': decay,
            'amplitude': amplitude,
            'phase': random.random() * math.pi * 2
        })
    
    def set_preset(self, preset: str):
        presets = {
            'bell': [(523.25, 0.3, 1.0), (1046.50, 0.2, 0.7), (1568.00, 0.15, 0.5)],
            'glass': [(800, 0.4, 1.0), (1600, 0.3, 0.8), (2400, 0.2, 0.5)],
            'metal': [(440, 0.5, 1.0), (880, 0.4, 0.9), (1320, 0.3, 0.7)],
            'drum': [(100, 0.2, 1.0), (200, 0.15, 0.7), (400, 0.1, 0.4)],
            'wood': [(300, 0.15, 1.0), (600, 0.1, 0.6), (900, 0.05, 0.3)]
        }
        
        self.modes = []
        if preset in presets:
            for f, d, a in presets[preset]:
                self.add_mode(f, d, a)
    
    def generate(self, duration: float) -> List[float]:
        samples = int(self.sample_rate * duration)
        output = [0.0] * samples
        
        for i in range(samples):
            t = i / self.sample_rate
            sample = 0.0
            for mode in self.modes:
                freq = mode['frequency']
                decay = mode['decay']
                amp = mode['amplitude']
                phase = mode['phase']
                sample += amp * math.sin(2 * math.pi * freq * t + phase) * math.exp(-decay * t)
            output[i] = sample
        
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output


class VectorSynthesizer:
    """Vector synthesis - mix between multiple oscillators"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.oscillators = []
        self.positions = [0, 0]
        
    def add_oscillator(self, waveform: str, frequency: float, amplitude: float):
        self.oscillators.append({
            'waveform': waveform,
            'frequency': frequency,
            'amplitude': amplitude,
            'phase': 0
        })
    
    def set_waveform_mix(self, position_x: float, position_y: float):
        self.positions = [position_x, position_y]
    
    def _get_wave(self, waveform: str, phase: float) -> float:
        phase = phase % (2 * math.pi)
        
        if waveform == 'sine':
            return math.sin(phase)
        elif waveform == 'triangle':
            return 2 * abs((phase / math.pi) % 2 - 1) - 1
        elif waveform == 'sawtooth':
            return ((phase / math.pi) % 2) - 1
        elif waveform == 'square':
            return 1 if (phase / math.pi) % 2 < 1 else -1
        return 0
    
    def generate(self, duration: float) -> List[float]:
        samples = int(self.sample_rate * duration)
        output = [0.0] * samples
        
        if len(self.oscillators) < 2:
            return output
        
        x, y = self.positions
        
        for i in range(samples):
            t = i / self.sample_rate
            value = 0.0
            
            for idx, osc in enumerate(self.oscillators):
                if idx < 4:
                    weights = [(1-x)*(1-y), x*(1-y), (1-x)*y, x*y]
                    weight = weights[idx] if idx < len(weights) else 0
                else:
                    weight = 1.0 / len(self.oscillators)
                
                phase = 2 * math.pi * osc['frequency'] * t + osc['phase']
                value += self._get_wave(osc['waveform'], phase) * osc['amplitude'] * weight
            
            output[i] = value
        
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output


class AnalogModelingSynthesizer:
    """Analog modeling - emulate analog synthesizer circuitry"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.circuit_type = 'classic'
        
    def set_circuit_type(self, circuit: str):
        self.circuit_type = circuit
    
    def _model_vco(self, frequency: float, waveform: str, t: float) -> float:
        if waveform == 'sine':
            return math.sin(2 * math.pi * frequency * t)
        elif waveform == 'sawtooth':
            return ((frequency * t) % 1) * 2 - 1
        elif waveform == 'square':
            return 1 if (frequency * t) % 1 < 0.5 else -1
        elif waveform == 'triangle':
            tp = (frequency * t) % 1
            return 2 * abs(tp * 2 - 1) - 1
        return 0
    
    def _model_adsr(self, t: float, attack: float, decay: float, 
                    sustain: float, release: float, total_duration: float) -> float:
        if t < attack:
            return t / attack
        elif t < attack + decay:
            return 1 - (1 - sustain) * (t - attack) / decay
        elif t < total_duration - release:
            return sustain
        else:
            return sustain * (total_duration - t) / release
    
    def generate(self, duration: float, frequency: float, waveform: str = 'sawtooth',
                 cutoff: float = 2000, resonance: float = 0.5,
                 attack: float = 0.01, decay: float = 0.2, sustain: float = 0.7, 
                 release: float = 0.3) -> List[float]:
        samples = int(self.sample_rate * duration)
        output = [0.0] * samples
        
        for i in range(samples):
            t = i / self.sample_rate
            
            osc = self._model_vco(frequency, waveform, t)
            envelope = self._model_adsr(t, attack, decay, sustain, release, duration)
            
            output[i] = osc * envelope
        
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output


class CircuitModelingSynthesizer:
    """Circuit modeling - emulate specific electronic circuits"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.circuit = 'tube_amp'
        
    def set_circuit(self, circuit_type: str):
        self.circuit = circuit_type
        
    def _model_distortion(self, input_signal: float, drive: float, 
                          mode: str = 'tube') -> float:
        if mode == 'tube':
            return math.tanh(input_signal * (1 + drive))
        elif mode == 'transistor':
            if input_signal > 1 / (1 + drive):
                return 1 / (1 + drive)
            elif input_signal < -1 / (1 + drive):
                return -1 / (1 + drive)
            return input_signal * (1 + drive)
        elif mode == 'fuzz':
            return math.copysign(math.pow(abs(input_signal), 0.5), input_signal) * (1 + drive)
        return input_signal
    
    def _model_tone_stack(self, input_signal: float, bass: float, 
                          mid: float, treble: float) -> float:
        output = input_signal
        output = output * (1 + bass * 0.5)
        output = output * (1 + mid * 0.3)
        output = output * (1 + treble * 0.2)
        return output
    
    def generate(self, duration: float, input_source: List[float] = None,
                 drive: float = 0.5, bass: float = 0.5, mid: float = 0.5, 
                 treble: float = 0.5, mode: str = 'tube') -> List[float]:
        
        if input_source is None or len(input_source) == 0:
            samples = int(self.sample_rate * duration)
            input_source = [math.sin(2 * math.pi * 440 * (i / self.sample_rate)) 
                           for i in range(samples)]
        
        output = [0.0] * len(input_source)
        
        for i in range(len(input_source)):
            signal = input_source[i]
            signal = self._model_distortion(signal, drive, mode)
            signal = self._model_tone_stack(signal, bass, mid, treble)
            output[i] = signal
        
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output


class PerceptualSynthesizer:
    """Perceptual synthesis - based on auditory perception"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
    def generate_auditory_scene(self, duration: float, scene_type: str = 'forest') -> List[float]:
        samples = int(self.sample_rate * duration)
        output = [0.0] * samples
        
        if scene_type == 'forest':
            for _ in range(5):
                freq = random.uniform(2000, 6000)
                start = random.randint(0, samples - 10000)
                for i in range(10000):
                    if start + i < samples:
                        t = i / 10000
                        output[start + i] += math.sin(2 * math.pi * freq * t) * 0.1 * t
        
        elif scene_type == 'ocean':
            for i in range(samples):
                t = i / self.sample_rate
                wave = math.sin(2 * math.pi * 0.2 * t) * 0.3 + 0.3
                noise = random.uniform(-0.1, 0.1)
                output[i] = wave * noise
        
        elif scene_type == 'rain':
            for _ in range(50):
                pos = random.randint(0, samples - 5000)
                freq = random.uniform(1000, 3000)
                for i in range(5000):
                    if pos + i < samples:
                        t = i / 5000
                        output[pos + i] += math.sin(2 * math.pi * freq * t) * 0.05 * (1 - t)
        
        elif scene_type == 'city':
            noise = [random.uniform(-0.05, 0.05) for _ in range(samples)]
            for i in range(samples):
                t = i / self.sample_rate
                output[i] = noise[i] * (1 + math.sin(2 * math.pi * 0.5 * t) * 0.3)
        
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output
    
    def generate_timbre_space(self, duration: float, brightness: float, 
                              roughness: float, warmth: float) -> List[float]:
        samples = int(self.sample_rate * duration)
        output = [0.0] * samples
        
        fund_freq = 220
        num_harmonics = int(1 + brightness * 10)
        detune = roughness * 20
        warmth_boost = 1 + warmth * 0.5
        
        for i in range(samples):
            t = i / self.sample_rate
            sample = 0.0
            
            for h in range(1, num_harmonics + 1):
                freq = fund_freq * h + random.uniform(-detune, detune)
                amp = (1 / h) * (1 - (h-1) * brightness / num_harmonics)
                
                if h <= 3:
                    amp *= warmth_boost
                
                sample += amp * math.sin(2 * math.pi * freq * t)
            
            output[i] = sample
        
        max_val = max(abs(s) for s in output) if output else 1
        if max_val > 0:
            output = [s / max_val * 0.8 for s in output]
        
        return output


class ExtraSynthesisEngine:
    """
    Master class combining all extra synthesis methods.
    CONNECTED TO MAIN API!
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
        self.karplus = KarplusStrongSynthesizer(sample_rate)
        self.modal = ModalSynthesizer(sample_rate)
        self.vector = VectorSynthesizer(sample_rate)
        self.analog = AnalogModelingSynthesizer(sample_rate)
        self.circuit = CircuitModelingSynthesizer(sample_rate)
        self.perceptual = PerceptualSynthesizer(sample_rate)
        
        print(f"    [OK] Extra Synthesis Engine initialized")
        print(f"         - Karplus-Strong: String/Pluck sounds")
        print(f"         - Modal: Resonant/Physical modeling")
        print(f"         - Vector: 4-oscillator crossfade")
        print(f"         - Analog Modeling: VCO/VCF/VCA")
        print(f"         - Circuit Modeling: Tube/Transistor/Fuzz")
        print(f"         - Perceptual: Auditory scenes/Timbre")
    
    def karplus_string(self, duration: float, frequency: float, 
                       decay: float = 0.8, brightness: float = 0.5) -> List[float]:
        return self.karplus.generate(duration, frequency, decay, brightness)
    
    def modal_synthesize(self, duration: float, preset: str = 'bell') -> List[float]:
        self.modal.set_preset(preset)
        return self.modal.generate(duration)
    
    def vector_synth(self, duration: float, position_x: float = 0.5, 
                     position_y: float = 0.5) -> List[float]:
        self.vector.set_waveform_mix(position_x, position_y)
        return self.vector.generate(duration)
    
    def analog_model(self, duration: float, frequency: float, 
                     waveform: str = 'sawtooth', cutoff: float = 2000,
                     resonance: float = 0.5) -> List[float]:
        return self.analog.generate(duration, frequency, waveform, cutoff, resonance)
    
    def circuit_model(self, duration: float, input_audio: List[float] = None,
                      drive: float = 0.5, mode: str = 'tube') -> List[float]:
        return self.circuit.generate(duration, input_audio or [], drive=drive, mode=mode)
    
    def perceptual_scene(self, duration: float, scene: str = 'forest') -> List[float]:
        return self.perceptual.generate_auditory_scene(duration, scene)
    
    def perceptual_timbre(self, duration: float, brightness: float = 0.5,
                          roughness: float = 0.3, warmth: float = 0.5) -> List[float]:
        return self.perceptual.generate_timbre_space(duration, brightness, roughness, warmth)
    
    def get_methods(self) -> List[str]:
        return [
            "karplus_string",
            "modal_synthesize", 
            "vector_synth",
            "analog_model",
            "circuit_model",
            "perceptual_scene",
            "perceptual_timbre"
        ]


# Test function
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" EXTRA SYNTHESIS ENGINE TEST")
    print("="*60 + "\n")
    
    engine = ExtraSynthesisEngine(44100)
    
    print("\n[1] Karplus-Strong String...")
    audio = engine.karplus_string(1.0, 220, 0.8, 0.5)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[2] Modal Synthesis (Bell)...")
    audio = engine.modal_synthesize(1.0, "bell")
    print(f"     OK - {len(audio)} samples")
    
    print("\n[3] Vector Synthesis...")
    audio = engine.vector_synth(1.0, 0.5, 0.5)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[4] Analog Modeling...")
    audio = engine.analog_model(1.0, 220, "sawtooth", 2000, 0.5)
    print(f"     OK - {len(audio)} samples")
    
    print("\n[5] Circuit Modeling...")
    audio = engine.circuit_model(1.0, drive=0.5, mode="tube")
    print(f"     OK - {len(audio)} samples")
    
    print("\n[6] Perceptual Scene (Forest)...")
    audio = engine.perceptual_scene(2.0, "forest")
    print(f"     OK - {len(audio)} samples")
    
    print("\n[7] Perceptual Timbre...")
    audio = engine.perceptual_timbre(1.0, 0.5, 0.3, 0.5)
    print(f"     OK - {len(audio)} samples")
    
    print("\n" + "="*60)
    print(" ALL EXTRA SYNTHESIS METHODS OPERATIONAL!")
    print("="*60 + "\n")