import os
import sys
import getpass
import base64
import re
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HMAC_KEY_LENGTH = 32


def generate_key():
    """
    Generates a new Fernet key and saves it to 'secret.key' file.
    """
    key = Fernet.generate_key()
    key_path = os.path.join(os.path.dirname(__file__), "secret.key")
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved to 'secret.key'.")


def load_key(presentation_method):
    """
    Loads the Fernet key from 'secret.key' file.
    """
    try:
        key_path = os.path.join(os.path.dirname(__file__), "secret.key")
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        print(
            "Key file 'secret.key' not found. Please generate a key first using '-g' option."
        )
        sys.exit(1)


def get_key_from_password(password_provided, salt):
    """
    Derives a cryptographic key from the provided password and salt using PBKDF2 HMAC-SHA256.
    """
    password = password_provided.encode()  # Convert to bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the Fernet key in bytes
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def generate_hmac(key, data):
    """
    Generates an HMAC for the given data using the specified key.
    """
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    return h.finalize()


def verify_hmac(key, data, hmac_to_verify):
    """
    Verifies the HMAC for the given data.
    """
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    try:
        h.verify(hmac_to_verify)
        return True
    except Exception:
        return False


def check_password_strength(password):
    """
    Checks if the password meets the complexity requirements.
    """
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not re.search(r"\d", password):
        print("Password must contain at least one digit.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password must contain at least one special character.")
        return False
    return True


def encrypt_file(file_name, key_method, Presentaion_method):
    """
    Encrypts a file using the specified key method ('key' or 'password') and adds an HMAC.
    """
    try:
        with open(file_name, "rb") as file:
            original = file.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if key_method == "key":
        key = load_key(presentation_method=Presentaion_method)
    elif key_method == "password":
        while True:
            password = getpass.getpass("Enter password for encryption: ")
            if not check_password_strength(password):
                print("Please choose a stronger password.")
                continue
            confirm_password = getpass.getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match.")
                continue
            break
        salt = os.urandom(16)
        key = get_key_from_password(password, salt)

    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)

    hmac_value = generate_hmac(key, encrypted)

    print(f"DEBUG: Generated HMAC (checksum) for encryption: {hmac_value.hex()}")

    encrypted_file_name = file_name + ".encrypted"
    with open(encrypted_file_name, "wb") as encrypted_file:
        if key_method == "password":
            # Prepend the salt to the encrypted data
            encrypted_file.write(salt)
        encrypted_file.write(encrypted + hmac_value)

    print(
        f"File '{file_name}' encrypted successfully as '{encrypted_file_name}' using password-based key derivation."
    )


def decrypt_file(encrypted_file_name, key_method, Presentaion_method):
    """
    Decrypts an encrypted file using the specified key method ('key' or 'password') and verifies the HMAC.
    """
    try:
        with open(encrypted_file_name, "rb") as enc_file:
            encrypted_data = enc_file.read()
    except FileNotFoundError:
        print(f"File '{encrypted_file_name}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if key_method == "key":
        key = load_key(presentation_method=Presentaion_method)
    elif key_method == "password":
        if len(encrypted_data) < 16:
            print("Encrypted file is too short to contain a salt.")
            sys.exit(1)
        salt = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        password = getpass.getpass("Enter password for decryption: ")
        key = get_key_from_password(password, salt)

    hmac_size = hashes.SHA256().digest_size
    encrypted_content = encrypted_data[:-hmac_size]
    hmac_value_stored = encrypted_data[-hmac_size:]

    hmac_value_computed = generate_hmac(key, encrypted_content)

    print(f"DEBUG: Stored HMAC (checksum) in file: {hmac_value_stored.hex()}")
    print(
        f"DEBUG: Computed HMAC (checksum) for verification: {hmac_value_computed.hex()}"
    )

    if not verify_hmac(key, encrypted_content, hmac_value_stored):
        print("Data integrity check failed. The file may have been tampered with.")
        sys.exit(1)

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted_content)
    except InvalidToken:
        print("Decryption failed. Invalid key or corrupted file.")
        sys.exit(1)

    decrypted_file_name = encrypted_file_name.replace(".encrypted", ".decrypted")
    with open(decrypted_file_name, "wb") as dec_file:
        dec_file.write(decrypted)

    print(
        f"File '{encrypted_file_name}' decrypted successfully as '{decrypted_file_name}' using password-based key derivation."
    )


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  To generate a key: python script.py -g")
        print("  To encrypt a file with stored key: python script.py -e -k <filename>")
        print("  To encrypt a file with password: python script.py -e -p <filename>")
        print(
            "  To decrypt a file with stored key: python script.py -d -k <filename>.encrypted"
        )
        print(
            "  To decrypt a file with password: python script.py -d -p <filename>.encrypted"
        )
        sys.exit(1)

    option = sys.argv[1]
    if option == "-g":
        generate_key()
    elif option == "-e" or option == "-d":
        if len(sys.argv) != 4:
            print("Please provide the key method and filename.")
            sys.exit(1)
        key_option = sys.argv[2]
        if key_option == "-k":
            key_method = "key"
        elif key_option == "-p":
            key_method = "password"
        else:
            print(
                "Invalid key method option. Use '-k' for stored key or '-p' for password-based key derivation."
            )
            sys.exit(1)
        file_name = sys.argv[3]
        if option == "-e":
            encrypt_file(file_name, key_method, 1)
        elif option == "-d":
            decrypt_file(file_name, key_method, 1)
    else:
        print("Invalid option.")
        sys.exit(1)


if __name__ == "__main__":
    main()