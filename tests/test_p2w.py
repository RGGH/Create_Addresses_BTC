import pytest
from Create_Addresses_BTC.p2wsh_seg import (
    generate_p2wsh_address,
    generate_key_pair,
    create_script,
    hash_script,
)


@pytest.fixture
def key_pair_and_script():
    private_key, public_key = generate_key_pair()
    witness_script = create_script()
    witness_script_hash = hash_script(witness_script)
    return private_key, public_key, witness_script, witness_script_hash


def test_generate_p2wsh_address(key_pair_and_script):
    private_key, public_key, witness_script, witness_script_hash = key_pair_and_script

    # Generate the P2WSH address using the tested function
    p2wsh_address = generate_p2wsh_address(witness_script_hash)

    # Ensure the generated address is not None
    assert p2wsh_address is not None



    # Optional: You can add more assertions or checks based on your requirements


# Run the test using: pytest your_test_file.py
