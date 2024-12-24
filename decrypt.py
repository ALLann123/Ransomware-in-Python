from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import gc

print("*****[+]Starting to decrypt files****")
print("--------------------------------------")

# Load the private key from a file
with open("/home/kali/allan_python/cryptography/private_key.key", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,  # Replace with the actual password if the private key is password-protected
        backend=default_backend()
    )

# Load the encrypted symmetric key from a file
with open("encryptedSymmetricKey.key", "rb") as key_file:
    encryptedSymmetricKey = key_file.read()

# Decrypt the symmetric key using the private key
decryptedSymmetricKey = private_key.decrypt(
    encryptedSymmetricKey,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Create a Fernet instance with the decrypted symmetric key
FernetInstance = Fernet(decryptedSymmetricKey)

# Read the encrypted file
filePath = "/home/kali/allan_python/cryptography/ransom/plan.txt"
with open(filePath, "rb") as file:
    encrypted_data = file.read()

# Decrypt the file data using the symmetric key
decrypted_data = FernetInstance.decrypt(encrypted_data)

# Write the decrypted data to a new file
with open("/home/kali/allan_python/cryptography/ransom/decrypted_plan.txt", "wb") as file:
    file.write(decrypted_data)

# Explicitly delete the symmetric key and Fernet instance from memory
del decryptedSymmetricKey
del FernetInstance
gc.collect()  # Invoke the garbage collector to ensure the key is removed from memory

# Quit the program
quit()
