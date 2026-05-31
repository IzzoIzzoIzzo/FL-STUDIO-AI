"""
AUDIO EXPORTER - MP3/FLAC/WAV Export
====================================
Export audio to multiple formats with quality settings.
"""

import struct
import wave
import os
import subprocess
from typing import List, Optional


class AudioExporter:
    """Export audio to multiple formats"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def _normalize(self, samples: List[float]) -> List[float]:
        max_val = max(abs(s) for s in samples) if samples else 1
        if max_val > 0:
            return [s * 0.95 / max_val for s in samples]
        return samples
    
    def export_wav(self, samples: List[float], filename: str, stereo: bool = True):
        """Export to WAV (uncompressed)"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        samples = self._normalize(samples)
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2 if stereo else 1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            
            for s in samples:
                if stereo:
                    packed = struct.pack('<hh', int(s * 32767), int(s * 32767))
                else:
                    packed = struct.pack('<h', int(s * 32767))
                wav.writeframes(packed)
        
        return filename
    
    def export_wav_mono(self, samples: List[float], filename: str):
        """Export mono WAV"""
        return self.export_wav(samples, filename, stereo=False)
    
    def export_raw_pcm(self, samples: List[float], filename: str):
        """Export raw 16-bit PCM (no header)"""
        samples = self._normalize(samples)
        with open(filename, 'wb') as f:
            for s in samples:
                f.write(struct.pack('<h', int(s * 32767)))
        return filename
    
    def _try_use_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def export_mp3(self, samples: List[float], filename: str, bitrate: int = 320):
        """Export to MP3 using ffmpeg"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        if self._try_use_ffmpeg():
            temp_wav = filename.replace('.mp3', '_temp.wav')
            self.export_wav(samples, temp_wav)
            
            try:
                subprocess.run(['ffmpeg', '-i', temp_wav, '-b:a', f'{bitrate}k', '-y', filename],
                             capture_output=True, timeout=60)
                os.remove(temp_wav)
                return filename
            except:
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
        
        return self.export_wav(samples, filename.replace('.mp3', '.wav'))
    
    def export_flac(self, samples: List[float], filename: str, compression: int = 5):
        """Export to FLAC using ffmpeg"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        if self._try_use_ffmpeg():
            temp_wav = filename.replace('.flac', '_temp.wav')
            self.export_wav(samples, temp_wav)
            
            try:
                subprocess.run(['ffmpeg', '-i', temp_wav, '-compression_level', str(compression), '-y', filename],
                             capture_output=True, timeout=60)
                os.remove(temp_wav)
                return filename
            except:
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
        
        return self.export_wav(samples, filename.replace('.flac', '.wav'))
    
    def export_ogg(self, samples: List[float], filename: str, quality: int = 10):
        """Export to OGG Vorbis"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        if self._try_use_ffmpeg():
            temp_wav = filename.replace('.ogg', '_temp.wav')
            self.export_wav(samples, temp_wav)
            
            try:
                subprocess.run(['ffmpeg', '-i', temp_wav, '-q:a', str(quality), '-y', filename],
                             capture_output=True, timeout=60)
                os.remove(temp_wav)
                return filename
            except:
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
        
        return self.export_wav(samples, filename.replace('.ogg', '.wav'))
    
    def export_aiff(self, samples: List[float], filename: str):
        """Export to AIFF (Apple format)"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        samples = self._normalize(samples)
        
        with open(filename, 'wb') as f:
            f.write(b'FORM')
            data_size = len(samples) * 2
            f.write(struct.pack('>I', 36 + data_size))
            f.write(b'AIFF')
            f.write(b'COMM')
            f.write(struct.pack('>IHHII', 18, 2, self.sample_rate, 16, 0))
            
            f.write(b'SSND')
            f.write(struct.pack('>II', data_size, 0))
            
            for s in samples:
                f.write(struct.pack('>h', int(s * 32767)))
        
        return filename
    
    def export_all_formats(self, samples: List[float], base_name: str):
        """Export to all available formats"""
        results = {}
        
        results['wav'] = self.export_wav(samples, f'{base_name}.wav')
        results['wav_mono'] = self.export_wav_mono(samples, f'{base_name}_mono.wav')
        
        if self._try_use_ffmpeg():
            results['mp3_320'] = self.export_mp3(samples, f'{base_name}_320.mp3', 320)
            results['mp3_128'] = self.export_mp3(samples, f'{base_name}_128.mp3', 128)
            results['flac'] = self.export_flac(samples, f'{base_name}.flac')
            results['ogg'] = self.export_ogg(samples, f'{base_name}.ogg')
        
        results['aiff'] = self.export_aiff(samples, f'{base_name}.aiff')
        
        return results
    
    def create_stem_export(self, stems: dict, base_name: str):
        """Export multi-track stem bundle"""
        os.makedirs(os.path.dirname(base_name) if os.path.dirname(base_name) else '.', exist_ok=True)
        
        results = {}
        for name, audio in stems.items():
            safe_name = name.replace(' ', '_').lower()
            results[safe_name] = self.export_wav(audio, f'{base_name}_{safe_name}.wav')
        
        return results


def demo():
    print("=" * 60)
    print("  AUDIO EXPORTER - MP3/FLAC/WAV")
    print("=" * 60)
    
    import math
    
    exp = AudioExporter(44100)
    
    print("\n[1] Creating test audio...")
    test_tone = [math.sin(2 * math.pi * 440 * (i/44100)) * 0.5 for i in range(44100)]
    print(f"    Generated {len(test_tone)} samples")
    
    print("\n[2] Exporting WAV...")
    exp.export_wav(test_tone, 'audio/test_export.wav')
    print("    Saved: audio/test_export.wav")
    
    print("\n[3] Exporting all formats...")
    results = exp.export_all_formats(test_tone, 'audio/full_export')
    for fmt, path in results.items():
        print(f"    {fmt}: {path}")
    
    print("\n[4] Stem export demo...")
    stems = {
        'drums': test_tone,
        'bass': [s * 0.8 for s in test_tone],
        'melody': [s * 0.6 for s in test_tone],
    }
    stem_files = exp.create_stem_export(stems, 'audio/stems/track')
    for name, path in stem_files.items():
        print(f"    {name}: {path}")
    
    print("\n" + "=" * 60)
    print("  EXPORTER READY!")
    print("=" * 60)


if __name__ == "__main__":
    demo()