from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def get_keys_32() -> bytes:
    """
    returns random 32 bytes
    """
    return get_random_bytes(32)


def encrypt_AES(data: bytes, key: bytes) -> bytes:
    """
    Encrypts data using AES-256 in GCM mode.

    Output format:
            [ 16 bytes nonce | 16 bytes authentication tag | ciphertext ]
    """

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return cipher.nonce + tag + ciphertext


def decrypt_AES(data: bytes, key: bytes) -> bytes:
    """
    Decrypts data produced by the encrypt() function.

    Expected input format od data:
        [ 16 bytes nonce | 16 bytes authentication tag | ciphertext ]

    Raises:
        ValueError if authentication fails.
    """

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    return cipher.decrypt_and_verify(ciphertext, tag)

