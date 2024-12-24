# Ransomware-in-Python
Ransomware is malcious code that holds the victim machine hostage by encrypting its files.
Encrypt is the process of scrambling data in as systematic way.
In the above program we are going to use Asymetric cryptography(public key cryptography). This form of cryptography uses two pairs of keys instead of a single shared key that is it generates a public key which everyone can see and a private key which is never shared. Messages that are encrypted with a public key can only be decrypted with a single private key and vice versa. This guarantes that the messahe came from you.

          kali> pip3 install cryptography

NOTE: We are going to generate and use a symmetric key to encrypt the user's files. As the attacker, we will encrypt the symmetric key (used to encrypt the files) using our public key. When the program terminates, the symmetric key will be deleted.

# Tutorial
We first generate a pair of public and private keys using openssl library which is a build in tool on kali linux.

     kali> openssl genrsa -out pub_priv_pair.key 1024
     kali>  openssl rsa -text -in pub_priv_pair.key                #use this to view the keys generated
Extract the public key from the file using the command

    kali> openssl rsa -in pub_priv_pair.key -pubout -out public_key.key
    kali> openssl rsa -text -pubin -in public_key.key             #use to view the public key
Extract the private key from the file using the command

    kali> openssl rsa -in pub_priv_pair.key -out private_key.key

# Advanced Ransomware
We have three scripts, namely ransom_server.py, ransom_client.py, and decrypt.py.

The ransom_server.py script is used to set up a server using Python's socketserver library, enabling it to accept multiple connections. Its purpose is to allow the attacker to receive the encrypted symmetric key from ransom_client.py. The server will then use this key to generate the decrypted symmetric key, which is returned to the user after confirming that payment has been received, possibly in the form of cryptocurrency.

The ransom_client.py is the payload that runs on the host to encrypt the host's files and send the encrypted symmetric key used for encryption to the server. After the program has finished running, Python's memory management is responsible for erasing the symmetric key stored in the computer's memory.

The decrypt file will be used bythe victim to decrypt there files when the user gets the symmetric key after paying the ransom.

We first begin by runing the ransomware server

    kali> python3 ransom_server.py
![server](https://github.com/user-attachments/assets/a35facff-b5a5-4bd7-88f2-31a51b2e2c4c)

We then run the payload i.e ransom_client.py on the victim machine and this sends the encrypted key to the server

    kali> python3 ransom_client.py
![image](https://github.com/user-attachments/assets/303a6045-6c02-45e4-a632-4770bb3b01b5)
The ouput onthe attacker server:
![received](https://github.com/user-attachments/assets/6043dd24-ff00-452e-996d-2c6797e766bb)

Lets check the file onthe victim machine
![encrypted file](https://github.com/user-attachments/assets/93db7564-ac75-4349-bc9d-093ef244d4c0)

Now inthese tutorial for the client to get their files they have to interact with the server and they can utilize netcat to do this

    kali> nc <server_ip> 9100                        #we use the serve ip and the port ip
After connecting to the server you can enter the payment receipt id or something but for the tutorial I just used 1234 in my server code for the payment to get the decryption key. 
![payment verified](https://github.com/user-attachments/assets/3c9bce7d-9e19-40fd-9d48-393a60a9ee5d)
And onthe victim machine when prompted for the receipt the number was 1234 that the server expected and responded back with they key to decrypt the file
![netcat](https://github.com/user-attachments/assets/5fce1ff8-ec08-412d-b863-59a1ff7ec397)

Now with the key use the decrypt.py file to decrypt the encrypted file, by copying it to a file with a name like myTopSecretKey.key and then execute the decrypt.py script which opens the file myTopSecretKey.key and takes the key as input to decrypt the victims file.

    kali> echo "<key_gotten_from_server>" > myTopSecretKey.key
    kali>python3 decrypt.py

The results of the above:
![done](https://github.com/user-attachments/assets/61e8403b-846c-4458-904f-a0e13cfe4278)

# Disclaimer
Use the above for education purposes

The above implementation is very basic
Check the code for various paths to file such as the path to your public key on the ransom_client.py and the path to private key onthe ransom_server.py.
Happy Hacking!!!





