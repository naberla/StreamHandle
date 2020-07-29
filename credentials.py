import pickle
import sys
from encode_decode import Protection

class credentials:
	"""Loader class for encrypted credentials"""
	def load_credentials(self):
		try:
			vardict = pickle.loads(self.protector.decrypt("credentials.pkl.enc"))
			for _ in vardict.keys():
				setattr(self,_,vardict[_])

		except Exception as e:
			print("Private key file key.key might be missing. Cannot fetch encrypted credentials without it.")
			print(str(e))
			sys.exit(1)

	def __init__(self):
		try:
			self.protector = Protection()
		except Exception as e:
			print("Credentials cannot be checked without the correct key.key file, cannot load credential variables.")
			print(str(e))



