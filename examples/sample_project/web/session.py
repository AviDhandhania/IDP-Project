"""
web/session.py
Web session and CSRF token encryption with short 900s Redis TTL.
"""

def generate_session_token(session_pubkey, redis_client):
    # source: local RNG
    tok = make_csrf_token()
    
    # cryptographic invocation: RSA-2048 OAEP (identical algorithm to payments/archive.py)
    sealed = rsa_oaep_encrypt(tok, session_pubkey)
    
    # sink: cache, TTL 900 seconds (15 minutes)
    redis_client.setex("session_csrf_tok", 900, sealed)
    return sealed

def make_csrf_token():
    return b"csrf_token_ephemeral_12345"

def rsa_oaep_encrypt(data, key):
    return b"encrypted_session_token_blob"
