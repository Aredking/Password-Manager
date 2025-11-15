import bcrypt
import keyring
import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class PasswordsCipher:
    __SERVICE_NAME = "Passwords Manager"
    __USERNAME = "aes_key"

    def __init__(self):
        self.aes_key = None
        self.__load_key()

    def __load_key(self) -> None:
        aes_key_str = keyring.get_password(PasswordsCipher.__SERVICE_NAME, PasswordsCipher.__USERNAME)
        if aes_key_str is None:
            self.aes_key = get_random_bytes(32)
            aes_key_str = base64.b64encode(self.aes_key).decode('utf-8')
            keyring.set_password(PasswordsCipher.__SERVICE_NAME, PasswordsCipher.__USERNAME, aes_key_str)
        else:
            self.aes_key = base64.b64decode(aes_key_str)


    def encode(self, data: str) -> bytes:
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return cipher.iv + ct_bytes

    def decode(self, ciphered_data: bytes) -> str:
        iv = ciphered_data[:AES.block_size]
        ct = ciphered_data[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        plaintext_padded = cipher.decrypt(ct)
        plaintext = unpad(plaintext_padded, AES.block_size)
        return plaintext.decode('utf-8')

def check_passwords_hash(password: bytes, hash: bytes) -> bool: # Сравнение паролей
    return bcrypt.checkpw(password, hash)

def get_hash_password(password: bytes) -> bytes: # Получение хэша пароля
    return bcrypt.hashpw(password, bcrypt.gensalt())


