#!/usr/bin/python3
#1) Read the key from the file
key=''
with open('myTopSecretKey.key', 'rb') as file:
	key = file.read()
#2)Read the encypted data from file
files=['plan.txt']

for file_path in files:
	encrypted_data=''
	with open(file_path, 'rb') as file:
		encrypted_data = file.read()
	#3)Decrypt the data
	from cryptography.fernet import Fernet
	#create an object from fernet class
	f=Fernet(key)

	decryptedData = f.decrypt(encrypted_data)

	#print('Encrypted data:', encrypted_data.decode())
	#print()
	#print('Decrypted data:', decryptedData.decode())

	with open(file_path, 'wb') as file:
		file.write(decryptedData)
