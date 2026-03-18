from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

from .crypto import Crypto


class AESGCM(Crypto):

    SALT_SIZE = 16
    NONCE_SIZE = 16
    TAG_SIZE = 16
    KEY_SIZE = 32
    PBKDF2_ITERATIONS = 100_000

    def encrypt(self, data :bytes, password :str) -> bytes:
        """
        Encrypts data using AES-256 in GCM mode

        Output format:
                [ 16 bytes nonce | 16 bytes authentication tag | SALT_SIZE bytes salt | ciphertext ]
        """

        salt = get_random_bytes(self.SALT_SIZE)
        key= self.derive_key(password, salt)

        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return cipher.nonce + tag + salt + ciphertext

    
    def decrypt(self, data :bytes, password :str) -> bytes:
        """
        Decrypts data using AES-256 in GCM mode

        Expected input format:
            [ 16 bytes nonce | 16 bytes authentication tag | SALT_SIZE bytes salt | ciphertext ]

        Raises:
            ValueError if authentication fails
            ValueError if data size < 48
        """

        if len(data) < self.NONCE_SIZE + self.TAG_SIZE + self.SALT_SIZE + self.SALT_SIZE:
            raise ValueError("Invalid encrypted file format")

        nonce = data[: self.NONCE_SIZE]
        tag = data[self.NONCE_SIZE : self.NONCE_SIZE + self.TAG_SIZE]
        salt = data[self.NONCE_SIZE + self.TAG_SIZE : self.NONCE_SIZE + self.TAG_SIZE + self.SALT_SIZE]
        ciphertext = data[self.NONCE_SIZE + self.TAG_SIZE + self.SALT_SIZE:]

        key = self.derive_key(password, salt)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        return cipher.decrypt_and_verify(ciphertext, tag)
