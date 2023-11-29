"""
    https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch04.asciidoc#bitcoin-addresses
"""

import ecdsa
import base58
import hashlib
from ripemd.ripemd160 import ripemd160

def generate_key_pair():
    # Step 1 : Generate a private key
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Step 2 : Derive the corresponding public key
    public_key = private_key.get_verifying_key().to_string()

    return private_key, public_key

def hash_public_key(public_key):
    # Step 3: Hash the public key using SHA-256 and RIPEMD-160
    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = ripemd160(sha256_hash)

    return ripemd160_hash

def generate_bitcoin_address(public_key_hash):
    # Step 4: Encode the hash in Base58Check encoding
    version_prefix = b'\x00'  # Mainnet version prefix for Bitcoin addresses
    checksum = hashlib.sha256(hashlib.sha256(version_prefix + public_key_hash).digest()).digest()[:4]
    # See 'Mastering Bitcoin'
    # https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch04.asciidoc#base58-and-base58check-encoding
    address_bytes = version_prefix + public_key_hash + checksum
    bitcoin_address = base58.b58encode(address_bytes).decode('utf-8')

    return bitcoin_address

# Example 
private_key, public_key = generate_key_pair()
public_key_hash = hash_public_key(public_key)
bitcoin_address = generate_bitcoin_address(public_key_hash)

print("Private Key:", private_key.to_string().hex())
print("Public Key:", public_key.hex())
print("Bitcoin Address:", bitcoin_address)

