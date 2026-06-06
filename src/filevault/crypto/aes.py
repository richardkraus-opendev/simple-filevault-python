from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

from .crypto import Crypto


class AESGCM(Crypto):

    SALT_SIZE = 16
    NONCE_SIZE = 12
    TAG_SIZE = 16
    KEY_SIZE = 32
    PBKDF2_ITERATIONS = 100_000

    MAGIC = b'FILEVAULT\x00'

    def encrypt(self, data :bytes, password :str) -> bytes:
        """
        Encrypts data using AES-256 in GCM mode

        Output format:
            [ 10 bytes magic | 12 bytes nonce | 16 bytes tag | 16 bytes salt | ciphertext ]
        """

        salt = get_random_bytes(self.SALT_SIZE)
        nonce = get_random_bytes(self.NONCE_SIZE)
        key = self.derive_key(password, salt)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        encrypted = nonce + tag + salt + ciphertext
        return self.MAGIC + encrypted

    
    def decrypt(self, data :bytes, password :str) -> bytes:
        """
        Decrypts data using AES-256 in GCM mode

        Expected input format:
            [ 10 bytes magic | 12 bytes nonce | 16 bytes tag | 16 bytes salt | ciphertext ]

        Raises:
            ValueError if not a valid FileVault file (missing magic)
            ValueError if authentication fails
            ValueError if data size < 54 (10 magic + 44 crypto)
        """

        if not data.startswith(self.MAGIC):
            raise ValueError("Not a valid FileVault encrypted file")
        data = data[len(self.MAGIC):]

        if len(data) < self.NONCE_SIZE + self.TAG_SIZE + self.SALT_SIZE:
            raise ValueError("Invalid encrypted file format")

        nonce = data[: self.NONCE_SIZE]
        tag = data[self.NONCE_SIZE : self.NONCE_SIZE + self.TAG_SIZE]
        salt = data[self.NONCE_SIZE + self.TAG_SIZE : self.NONCE_SIZE + self.TAG_SIZE + self.SALT_SIZE]
        ciphertext = data[self.NONCE_SIZE + self.TAG_SIZE + self.SALT_SIZE:]

        key = self.derive_key(password, salt)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        return cipher.decrypt_and_verify(ciphertext, tag)
