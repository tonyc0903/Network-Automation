from cryptography.fernet import Fernet

def encryption(input_file, output_file, key):
    with open(input_file, 'r') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    print('Successfully encrypted file!')
    with open(output_file, 'wb') as f:
        f.write(encrypted)


def decryption(input_file, output_file, key):
    with open(output_file, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)
    
    print('Successfully decrypted file!')
    with open(input_file, 'wb') as f:
        f.write(encrypted)

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



    file_to_encrypt = 'device-creds'
    file_to_decrypt = 'encrypted-device-creds'
    encryption(file_to_encrypt, file_to_decrypt, secret_key)
    decryption(file_to_encrypt, file_to_decrypt, secret_key)

if __name__ == "__main__":
    main()
