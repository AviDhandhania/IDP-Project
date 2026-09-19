"""
cache/etags.py
HTTP ETag generator for static asset checksums.
"""
import hashlib

def compute_asset_etag(static_asset_bytes, redis_client):
    # Non-security hash: generating ETag checksum for cache validation
    etag_digest = hashlib.sha256(static_asset_bytes).hexdigest()
    
    # Store checksum in cache with 1-hour TTL
    redis_client.setex(f"etag_{etag_digest}", 3600, etag_digest)
    return etag_digest
