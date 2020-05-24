from cryptography.fernet import Fernet


###############################################################################
#                                   FUNCTIONS                                 #
###############################################################################
def encryption(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)


def decryption(output_file, key):
    with open(output_file, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    return encrypted


def main():

    # Uncomment the following block of code if you are running this for the first time! 
    # After that comment it out!
    """
    secret_key = Fernet.generate_key()
    with open('key','wb') as f:
        f.write(secret_key)
    """

    # reading the key from the file 
    # Warning: bad idea in a production environment! Best to manually set secret_key with the generated key (you will store it in a safe place)
    with open('key') as f:
        secret_key = f.read()

    file_to_encrypt = 'device-creds' # afer running for the first time you can delete this file
    encrypted_file = input('Enter file where encrypted information is written to (encrypted-device-creds by default): ') or 'encrypted-device-creds'


    
    encryption(file_to_encrypt, encrypted_file, secret_key) # encrypts the device-creds file
                                                            # After running this code for the first time, You can:
                                                            # delete the device-file and comment out the function for safety purposes

    decryption(encrypted_file, secret_key) #decrypts the encrypted file with the key


###############################################################################
#                                   MAIN                                      #
###############################################################################
if __name__ == "__main__":
    main()
