from src.security.password_cipher import PasswordsCipher

if __name__ == "__main__":
    cipher = PasswordsCipher()

    text = "hello"

    ciphered_text = cipher.encode(text)
    print(ciphered_text)

    plain_text = cipher.decode(ciphered_text)
    print(plain_text)