from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from abc import ABC, abstractmethod

class Crypto(ABC):
    """
    Abstract base class for cryptographic algorithms
    """

    SALT_SIZE: int
    NONCE_SIZE: int
    TAG_SIZE: int
    KEY_SIZE: int
    PBKDF2_ITERATIONS: int


    def derive_key(self, password: str, salt: bytes)-> bytes:
        """
        Derives KEY_SIZE bytes long key from string (password)
        """

        key = PBKDF2(
            password,
            salt,
            dkLen=self.KEY_SIZE,
            count=self.PBKDF2_ITERATIONS,
            hmac_hash_module=SHA256
        )

        return key

    @abstractmethod
    def encrypt():
        pass

    @abstractmethod
    def decrypt():
        pass