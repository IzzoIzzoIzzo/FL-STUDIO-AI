"""
WEB3 BASICS V2 - Level 4.1
===========================
- Beat hashing (unique IDs)
- Timestamp verification
- Simple license generation
- Metadata management

Building on what we have - Web3 foundation!
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional


class BeatHasher:
    """Create unique hash for beats"""
    
    @staticmethod
    def hash_audio(audio: List[float], sample_rate: int = 44100) -> str:
        """Create SHA-256 hash of audio"""
        
        # Convert to bytes
        audio_bytes = b''
        for sample in audio[:100000]:  # Limit for performance
            int_sample = int(max(-1, min(1, sample)) * 32767)
            audio_bytes += int_sample.to_bytes(2, 'little', signed=True)
        
        # Create hash
        hash_obj = hashlib.sha256(audio_bytes)
        return hash_obj.hexdigest()
    
    @staticmethod
    def hash_content(content: str) -> str:
        """Hash any content"""
        return hashlib.sha256(content.encode()).hexdigest()


class TimestampVerification:
    """Verify when beat was created"""
    
    @staticmethod
    def create_timestamp(audio_hash: str, metadata: Dict = None) -> Dict:
        """Create timestamp record"""
        
        timestamp = {
            'audio_hash': audio_hash,
            'timestamp': datetime.now().isoformat(),
            'unix_time': int(time.time()),
            'version': '1.0',
            'metadata': metadata or {}
        }
        
        # Create verification hash
        content = json.dumps(timestamp, sort_keys=True)
        timestamp['verification_hash'] = hashlib.sha256(content.encode()).hexdigest()
        
        return timestamp
    
    @staticmethod
    def verify_timestamp(timestamp: Dict) -> bool:
        """Verify timestamp is valid"""
        
        # Reconstruct and verify
        stored_hash = timestamp.get('verification_hash', '')
        
        # Remove verification hash for recalculation
        check_data = {
            'audio_hash': timestamp.get('audio_hash'),
            'timestamp': timestamp.get('timestamp'),
            'unix_time': timestamp.get('unix_time'),
            'version': timestamp.get('version'),
            'metadata': timestamp.get('metadata', {})
        }
        
        content = json.dumps(check_data, sort_keys=True)
        calc_hash = hashlib.sha256(content.encode()).hexdigest()
        
        return stored_hash == calc_hash


class BeatLicense:
    """Generate licenses for beats"""
    
    LICENSE_TYPES = {
        'non_exclusive': {
            'price': 29.99,
            'rights': ['personal_use', 'performance'],
            'limitations': ['no_resale', 'no_dj_pool']
        },
        'exclusive': {
            'price': 499.99,
            'rights': ['personal_use', 'commercial', 'performance', 'publishing'],
            'limitations': []
        },
        'royalty_free': {
            'price': 149.99,
            'rights': ['unlimited_use', 'commercial'],
            'limitations': ['attribution_required']
        },
        ' stems': {
            'price': 999.99,
            'rights': ['all_above', 'stem_files'],
            'limitations': []
        }
    }
    
    @staticmethod
    def generate_license(beat_id: str, buyer_address: str, 
                         license_type: str, creator: str = 'AI FL Studio') -> Dict:
        """Generate license"""
        
        if license_type not in BeatLicense.LICENSE_TYPES:
            license_type = 'non_exclusive'
        
        template = BeatLicense.LICENSE_TYPES[license_type]
        
        license = {
            'license_id': f"LIC-{beat_id[:8]}-{int(time.time())}",
            'beat_id': beat_id,
            'buyer': buyer_address,
            'creator': creator,
            'type': license_type,
            'price': template['price'],
            'rights': template['rights'],
            'limitations': template['limitations'],
            'created': datetime.now().isoformat(),
            'expires': None,
            'transferable': True
        }
        
        # Sign (simple for now)
        license['signature'] = hashlib.sha256(
            json.dumps(license, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        return license
    
    @staticmethod
    def verify_license(license: Dict) -> bool:
        """Verify license is valid"""
        
        # Simple verification
        required = ['license_id', 'beat_id', 'buyer', 'type', 'signature']
        
        for field in required:
            if field not in license:
                return False
        
        return True


class MetadataManager:
    """Manage beat metadata"""
    
    @staticmethod
    def create_metadata(beat_info: Dict, audio_hash: str) -> Dict:
        """Create complete metadata"""
        
        metadata = {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            
            # Core info
            'title': beat_info.get('title', 'Untitled Beat'),
            'artist': beat_info.get('artist', 'AI Generated'),
            'genre': beat_info.get('genre', 'Electronic'),
            'style': beat_info.get('style', 'trap'),
            'bpm': beat_info.get('bpm', 140),
            'key': beat_info.get('key', 'C minor'),
            
            # Technical
            'audio_hash': audio_hash,
            'duration_seconds': beat_info.get('duration', 0),
            'sample_rate': beat_info.get('sample_rate', 44100),
            
            # Rights
            'creator': beat_info.get('artist', 'AI FL Studio'),
            'rights_holder': beat_info.get('artist', 'AI FL Studio'),
            'iswc': None,  # Would be assigned by registrar
            
            # Tags
            'tags': beat_info.get('tags', []),
            'instruments': beat_info.get('instruments', []),
            
            # Description
            'description': beat_info.get('description', 'AI generated beat'),
        }
        
        return metadata
    
    @staticmethod
    def export_json(metadata: Dict, filename: str) -> str:
        """Export metadata to JSON"""
        
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return filename


class Web3BeatManager:
    """Complete Web3 beat management"""
    
    def __init__(self):
        self.hasher = BeatHasher()
        self.timestamp = TimestampVerification()
        self.license = BeatLicense()
        self.metadata = MetadataManager()
    
    def register_beat(self, audio: List[float], info: Dict) -> Dict:
        """Register beat with all Web3 features"""
        
        # Create hash
        audio_hash = self.hasher.hash_audio(audio)
        
        # Create timestamp
        timestamp = self.timestamp.create_timestamp(audio_hash, info)
        
        # Create metadata
        metadata = self.metadata.create_metadata(info, audio_hash)
        
        # Generate license template
        license = self.license.generate_license(
            audio_hash, 
            info.get('buyer', 'creator'),
            info.get('license', 'non_exclusive'),
            info.get('creator', 'AI FL Studio')
        )
        
        return {
            'beat_id': audio_hash[:16],
            'audio_hash': audio_hash,
            'timestamp': timestamp,
            'metadata': metadata,
            'license': license,
            'registered': True
        }


def demo():
    print("=" * 60)
    print("  WEB3 BASICS V2 - Level 4.1")
    print("=" * 60)
    
    web3 = Web3BeatManager()
    
    # Create test audio
    import math
    test_audio = [math.sin(440 * 2 * math.pi * i/44100) for i in range(44100)]
    
    print("\n[TEST] Register beat...")
    beat_info = {
        'title': 'Test Beat',
        'genre': 'Electronic',
        'style': 'trap',
        'bpm': 140,
        'key': 'C minor',
        'duration': 30,
        'creator': 'AI Studio'
    }
    
    registration = web3.register_beat(test_audio, beat_info)
    print(f"  Beat ID: {registration['beat_id']}")
    print(f"  Audio Hash: {registration['audio_hash'][:32]}...")
    
    print("\n[TEST] Timestamp verification...")
    ts = registration['timestamp']
    print(f"  Timestamp: {ts['timestamp']}")
    verified = web3.timestamp.verify_timestamp(ts)
    print(f"  Verified: {verified}")
    
    print("\n[TEST] License...")
    lic = registration['license']
    print(f"  Type: {lic['type']}")
    print(f"  Price: ${lic['price']}")
    print(f"  Rights: {lic['rights'][:2]}...")
    
    print("\n[TEST] Metadata...")
    meta = registration['metadata']
    print(f"  Title: {meta['title']}")
    print(f"  Genre: {meta['genre']}")
    print(f"  BPM: {meta['bpm']}")
    
    print("\n" + "=" * 60)
    print("  WEB3 BASICS V2 - Level 4.1 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()