from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

SALT_SIZE = 16
NONCE_SIZE = 16
TAG_SIZE = 16
KEY_SIZE = 32
PBKDF2_ITERATIONS = 100_000

def derive_key(password: str, salt: bytes)-> bytes:
    """
    Derives KEY_SIZE bytes long key from string (password)
    """

    key = PBKDF2(
        password,
        salt,
        dkLen=KEY_SIZE,
        count=PBKDF2_ITERATIONS,
        hmac_hash_module=SHA256
    )

    return key


def encrypt_AES(data: bytes, password: str) -> bytes:
    """
    Encrypts data using AES-256 in GCM mode

    Output format:
            [ 16 bytes nonce | 16 bytes authentication tag | SALT_SIZE bytes salt | ciphertext ]
    """

    salt = get_random_bytes(SALT_SIZE)
    key= derive_key(password, salt)

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return cipher.nonce + tag + salt + ciphertext


def decrypt_AES(data: bytes, password: str) -> bytes:
    """
    Decrypts data using AES-256 in GCM mode

    Expected input format:
        [ 16 bytes nonce | 16 bytes authentication tag | SALT_SIZE bytes salt | ciphertext ]

    Raises:
        ValueError if authentication fails
        ValueError if data size < 48
    """

    if len(data) < 48:
        raise ValueError("Invalid encrypted file format")

    nonce = data[: NONCE_SIZE]
    tag = data[NONCE_SIZE : NONCE_SIZE + TAG_SIZE]
    salt = data[NONCE_SIZE + TAG_SIZE : NONCE_SIZE + TAG_SIZE + SALT_SIZE]
    ciphertext = data[NONCE_SIZE + TAG_SIZE + SALT_SIZE + SALT_SIZE :]

    key = derive_key(password, salt)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    return cipher.decrypt_and_verify(ciphertext, tag)

