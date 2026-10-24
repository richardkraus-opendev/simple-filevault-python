import os
import pytest
from filevault.crypto.aes import AESGCM

def test_successful_encryption_and_decryption_aes():

    original_data = create_bytes(50) 
    password = "Password1234"
    
    aes = AESGCM()
    
    encrypted_data = aes.encrypt(original_data, password)
    
    decrypted_data = aes.decrypt(encrypted_data, password)
    
    assert decrypted_data == original_data
    
    assert encrypted_data != original_data

def test_output_starts_with_magic_bytes_aes():

    original_data = create_bytes(50) 
    password = "Password1234"
    
    aes = AESGCM()
    
    encrypted_data = aes.encrypt(original_data, password)

    assert encrypted_data.startswith(AESGCM.MAGIC)

def test_encryption_is_randomized_aes():
    
    original_data = create_bytes(50) 
    password = "Password1234"
    
    aes = AESGCM()
    
    encrypted_data_1 = aes.encrypt(original_data, password)
    encrypted_data_2 = aes.encrypt(original_data, password)

    assert encrypted_data_1 != encrypted_data_2

def test_tampered_data_raises_error_aes():
    
    original_data = create_bytes(50) 
    password = "Password1234"
    
    aes = AESGCM()
    
    encrypted_data = aes.encrypt(original_data, password)

    tampered_data = bytearray(encrypted_data)
    tampered_data[-1] = (tampered_data[-1] + 1) % 256

    tampered_data = bytes(tampered_data)

    with pytest.raises(ValueError):
        aes.decrypt(tampered_data, password)

def test_bad_password_raises_error_aes():
    
    original_data = create_bytes(50) 
    password = "Password1234"
    
    aes = AESGCM()
    
    encrypted_data = aes.encrypt(original_data, password)

    with pytest.raises(ValueError):
        aes.decrypt(encrypted_data, "bad_password")

def create_bytes(size) -> bytes:
    return os.urandom(size)