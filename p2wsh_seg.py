import ecdsa
import bech32
import hashlib
from ripemd.ripemd160 import ripemd160

def generate_key_pair():
    # Generate a private key
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Derive the corresponding public key
    public_key = private_key.get_verifying_key().to_string()

    return private_key, public_key

def create_script():
    # Create a sample witness script (e.g., a simple P2PKH witness script)
    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = ripemd160(sha256_hash)
    witness_script = bytes.fromhex("76a914") + ripemd160_hash + bytes.fromhex("88ac")

    return witness_script

def hash_script(script):
    # Hash the script using SHA-256
    sha256_hash = hashlib.sha256(script).digest()

    return sha256_hash

def generate_p2wsh_address(script):
    # Create the witness version byte and encode it in Bech32 format
    witness_version = 0x00  # Version 0 for P2WSH (Pay-to-Witness-Script-Hash)
    witness_program = hashlib.sha256(script).digest()
    bech32_address = bech32.encode("bc", witness_version, witness_program)

    return bech32_address

# Example usage
private_key, public_key = generate_key_pair()
witness_script = create_script()
witness_script_hash = hash_script(witness_script)
p2wsh_address = generate_p2wsh_address(witness_script_hash)

print("Private Key:", private_key.to_string().hex())
print("Public Key:", public_key.hex())
print("P2WSH Address:", p2wsh_address)


"""
Explanation :  witness_script = bytes.fromhex("76a914") + ripemd160_hash + bytes.fromhex("88ac")

This line is constructing a witness script, which is a part of the Bitcoin scripting language. 
In this specific case, it's building a Pay-to-Witness-Public-Key-Hash (P2WPKH) script. Let's go through each component:

1. `bytes.fromhex("76a914")`: This represents the OP_DUP (0x76), OP_HASH160 (0xa9), 
and the length of the following data (0x14) operations in the Bitcoin script. 
These are standard operations used in Bitcoin scripts.

2. `ripemd160_hash`: This is the RIPEMD-160 hash of the public key. 
In Bitcoin, the address is derived from the hash of the public key, and in the case of P2WPKH, 
it is further processed with RIPEMD-160.

3. `bytes.fromhex("88ac")`: This represents the OP_EQUALVERIFY (0x88) and OP_CHECKSIG (0xac) operations 
in the Bitcoin script. These are also standard operations used to validate the signature against the public key hash.

So, when combined, this line creates a complete P2WPKH witness script, 
which can be used in the locking script of a transaction output. 
The locking script, when satisfied by a corresponding unlocking script in a spending transaction, 
allows the spending of the Bitcoin associated with that output.

In summary, this line assembles the script operations necessary for P2WPKH, 
including the OP_DUP, OP_HASH160, the public key hash, and the OP_EQUALVERIFY and OP_CHECKSIG operations.
"""

# https://slowli.github.io/bech32-buffer/
