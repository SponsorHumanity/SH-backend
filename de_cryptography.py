import cryptography
from cryptography.fernet import Fernet
import logging


def load_key( fileName ):
    """
    Load the previously generated key
    """
    return open( fileName + ".key", "rb").read()

def decrypt_message(file_name, encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key( file_name )
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    #ic(decrypted_message.decode())
    return( decrypted_message.decode())

'''
fin = open('publix.bin','rb')
encrypted_string = fin.read()
pw = decrypt_message( "publix", encrypted_string )
fin.close()
ic (pw)
'''