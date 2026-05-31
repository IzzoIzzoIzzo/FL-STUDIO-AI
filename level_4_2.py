"""
LEVEL 4.2 - MORE WEB3 FEATURES
==============================
- NFT Metadata Standard
- Royalty Splitter
- Collection Manager
- Marketplace Integration

Making Level 4 even more complete!
"""

import json
import time
import hashlib
from typing import List, Dict


class NFTMetadataStandard:
    """Standardized NFT metadata"""
    
    @staticmethod
    def create_full_metadata(beat: Dict, audio_hash: str, image_url: str = None) -> Dict:
        """Create full ERC-721 compatible metadata"""
        
        metadata = {
            # Standard ERC-721/4907 fields
            "name": beat.get('title', 'Untitled Beat'),
            "description": beat.get('description', 'AI-generated beat'),
            "image": image_url or "ipfs://placeholder",
            
            # Animation/audio
            "animation_url": f"ipfs://{audio_hash}",
            "youtube_url": None,
            
            # External URLs
            "external_url": beat.get('external_url', ''),
            
            # Attributes (for rarity)
            "attributes": [
                {"trait_type": "Genre", "value": beat.get('genre', 'Electronic')},
                {"trait_type": "Style", "value": beat.get('style', 'trap')},
                {"trait_type": "BPM", "value": beat.get('bpm', 140)},
                {"trait_type": "Key", "value": beat.get('key', 'C minor')},
                {"trait_type": "Duration", "value": f"{beat.get('duration', 30)}s"},
                {"trait_type": "Creator", "value": beat.get('creator', 'AI FL Studio')},
            ],
            
            # Audio-specific
            "audio_hash": audio_hash,
            "duration_seconds": beat.get('duration', 30),
            "bpm": beat.get('bpm', 140),
            "key": beat.get('key', 'C minor'),
            
            # License
            "license_type": beat.get('license', 'non_exclusive'),
            "rights": beat.get('rights', []),
        }
        
        return metadata
    
    @staticmethod
    def export_json(metadata: Dict, filename: str) -> str:
        """Export to JSON"""
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        return filename


class RoyaltySplitter:
    """Split royalties between collaborators"""
    
    def __init__(self):
        self.splits = {}
    
    def create_split(self, beat_id: str, collaborators: List[Dict]) -> Dict:
        """Create royalty split"""
        
        total = sum(c.get('percentage', 0) for c in collaborators)
        
        if abs(total - 100) > 0.01:
            # Normalize
            for c in collaborators:
                c['percentage'] = (c['percentage'] / total) * 100
        
        split = {
            'beat_id': beat_id,
            'created': time.time(),
            'collaborators': collaborators,
            'total_percentage': sum(c['percentage'] for c in collaborators)
        }
        
        self.splits[beat_id] = split
        
        return split
    
    def calculate_earnings(self, beat_id: str, total_revenue: float) -> Dict:
        """Calculate each collaborator's earnings"""
        
        if beat_id not in self.splits:
            return {'error': 'No split found'}
        
        split = self.splits[beat_id]
        earnings = {}
        
        for collaborator in split['collaborators']:
            name = collaborator.get('name', 'Unknown')
            percentage = collaborator.get('percentage', 0)
            earnings[name] = {
                'percentage': percentage,
                'amount': total_revenue * (percentage / 100),
                'wallet': collaborator.get('wallet', None)
            }
        
        return {
            'beat_id': beat_id,
            'total_revenue': total_revenue,
            'earnings': earnings
        }


class CollectionManager:
    """Manage NFT collections"""
    
    def __init__(self):
        self.collections = {}
    
    def create_collection(self, name: str, description: str, creator: str) -> Dict:
        """Create collection"""
        
        collection = {
            'name': name,
            'description': description,
            'creator': creator,
            'created': time.time(),
            'beats': [],
            'total_supply': 0,
            'is_verified': False
        }
        
        self.collections[name] = collection
        return collection
    
    def add_beat(self, collection_name: str, beat_id: str):
        """Add beat to collection"""
        
        if collection_name in self.collections:
            self.collections[collection_name]['beats'].append(beat_id)
            self.collections[collection_name]['total_supply'] += 1
    
    def get_collection(self, name: str) -> Dict:
        """Get collection"""
        return self.collections.get(name, {})


class MarketplaceIntegration:
    """Marketplace listing integration"""
    
    @staticmethod
    def create_listing(beat_id: str, price_eth: float, seller: str, 
                     listing_type: str = 'sale') -> Dict:
        """Create marketplace listing"""
        
        listing = {
            'listing_id': f"LIST-{beat_id}-{int(time.time())}",
            'beat_id': beat_id,
            'price_eth': price_eth,
            'seller': seller,
            'type': listing_type,
            'created': time.time(),
            'status': 'active'
        }
        
        return listing
    
    @staticmethod
    def create_offer(offer_id: str, beat_id: str, buyer: str, 
                    price_eth: float) -> Dict:
        """Create offer"""
        
        return {
            'offer_id': offer_id,
            'beat_id': beat_id,
            'buyer': buyer,
            'price_eth': price_eth,
            'created': time.time(),
            'status': 'pending'
        }


class Web3Manager:
    """Complete Web3 management"""
    
    def __init__(self):
        self.metadata = NFTMetadataStandard()
        self.royalties = RoyaltySplitter()
        self.collections = CollectionManager()
        self.marketplace = MarketplaceIntegration()
    
    def register_beat_with_all(self, beat: Dict) -> Dict:
        """Register beat with all Web3 features"""
        
        # Create hash
        audio_hash = hashlib.sha256(str(beat).encode()).hexdigest()
        
        # Create metadata
        full_meta = self.metadata.create_full_metadata(beat, audio_hash)
        
        # Create collection entry
        collection = beat.get('collection', 'Default')
        self.collections.add_beat(collection, audio_hash[:16])
        
        return {
            'beat_id': audio_hash[:16],
            'audio_hash': audio_hash,
            'metadata': full_meta,
            'collection': collection,
            'registered': True
        }


def demo():
    print("=" * 60)
    print("  LEVEL 4.2 - MORE WEB3 FEATURES")
    print("=" * 60)
    
    # Metadata
    print("\n[NFT Metadata]")
    beat = {'title': 'My Beat', 'genre': 'Trap', 'bpm': 140, 'duration': 30}
    meta = NFTMetadataStandard.create_full_metadata(beat, 'abc123')
    print(f"  Metadata: {meta['name']}, {len(meta['attributes'])} attributes")
    
    # Royalty Splitter
    print("\n[Royalty Splitter]")
    splitter = RoyaltySplitter()
    collaborators = [
        {'name': 'Producer', 'percentage': 50, 'wallet': '0x123...'},
        {'name': 'Writer', 'percentage': 30, 'wallet': '0x456...'},
        {'name': 'Featured', 'percentage': 20, 'wallet': '0x789...'},
    ]
    split = splitter.create_split('beat_001', collaborators)
    earnings = splitter.calculate_earnings('beat_001', 1000)
    print(f"  Split created: {len(split['collaborators'])} collaborators")
    print(f"  Earnings: Producer ${earnings['earnings']['Producer']['amount']:.2f}")
    
    # Collection Manager
    print("\n[Collection Manager]")
    cm = CollectionManager()
    cm.create_collection('Trap Masters', 'Best trap beats', 'AI Studio')
    cm.add_beat('Trap Masters', 'beat_001')
    col = cm.get_collection('Trap Masters')
    print(f"  Collection: {col.get('name', 'N/A')}, {col.get('total_supply', 0)} beats")
    
    # Marketplace
    print("\n[Marketplace]")
    listing = MarketplaceIntegration.create_listing('beat_001', 0.5, '0xSeller')
    print(f"  Listing: {listing['listing_id']}, Price: {listing['price_eth']} ETH")
    
    # Complete Web3 Manager
    print("\n[Web3 Manager]")
    web3 = Web3Manager()
    registered = web3.register_beat_with_all(beat)
    print(f"  Registered: {registered['beat_id']}")
    
    print("\n" + "=" * 60)
    print("  LEVEL 4.2 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    demo()