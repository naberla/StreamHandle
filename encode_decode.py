from cryptography.fernet import Fernet

class Protection:
	"""Encryption and decryption of sensitive data"""
	def write_key(self):
	    """
	    Generates a key and save it into a file
	    """
	    key = Fernet.generate_key()
	    with open("key.key", "wb") as key_file:
	        key_file.write(key)

	def load_key(self):
	    """
	    Loads the key from the current directory named `key.key`
	    """
	    return open("key.key", "rb").read()

	def encrypt_message(self, message):
		"""
		Given a message(str) and key (bytes), it encrypts the string and returns the encrypted message
		"""
		f = Fernet(self.key)
		return f.encrypt(message.encode())

	def decrypt_message(self, message):
		"""
		Given an encrypted message(str) and key (bytes), it decrypts the string and returns the decrypted message
		"""
		f = Fernet(self.key)
		return f.decrypt(message)

	def encrypt(self, filename):
	    """
	    Given a filename (str) and key (bytes), it encrypts the file and write it
	    """
	    f = Fernet(self.key)
	    with open(filename, "rb") as file:
	        # read all file data
	        file_data = file.read()
	    # encrypt data
	    encrypted_data = f.encrypt(file_data)
	    # write the encrypted file
	    with open(filename+".enc", "wb") as file:
	        file.write(encrypted_data)

	def decrypt(self, filename):
	    """
	    Given a filename (str) and key (bytes), it decrypts the file and write it
	    """
	    f = Fernet(self.key)
	    with open(filename, "rb") as file:
	        # read the encrypted data
	        encrypted_data = file.read()
	    # decrypt data
	    decrypted_data = f.decrypt(encrypted_data)
	    # write the original filename
	    return decrypted_data

	def __init__(self):
		self.key = self.load_key()

