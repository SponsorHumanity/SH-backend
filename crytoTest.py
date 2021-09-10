import cryptography
import logging


from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    print(decrypted_message.decode())
    return( decrypted_message.decode())

if __name__ == "__main__":
    message_string = "encrypt this message"


    logging.basicConfig(format='%(levelname)s %(asctime)s :%(message)s', level=logging.DEBUG)
    logging.debug('This message should appear on the console')
    logging.info('So should this')
    logging.warning('And this, too')


    generate_key()
    encrypted_string = encrypt_message( message_string ) 
    print("Encrypted message = ", encrypted_string )

    f = open('passwords.bin','wb')
    f.write( encrypted_string ) # writing to file
    f.close() 

    encrypted_string = open('passwords.bin','rb').read()
    print( " Before: ", encrypted_string )
    msg = decrypt_message( encrypted_string )
    print( "end: ", msg )

