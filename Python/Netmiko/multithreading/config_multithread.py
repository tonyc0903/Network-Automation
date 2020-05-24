from cryptography.fernet import Fernet
from pprint import pprint
from netmiko import ConnectHandler
from time import time
from multiprocessing.dummy import Pool as ThreadPool
"""
Can use concurrent.futures, just have to modify the main func a bit, will provide the changes in a block of code there
"""
# from concurrent.futures import ThreadPoolExecutor

###############################################################################
#                                   FUNCTIONS                                 #
###############################################################################

# encryption and decryption func using crypto library 
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

# function to read devices from the file
def read_devices(devices_filename):

    devices = {}  # create our dictionary for storing devices and their info

    with open(devices_filename) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',')  #e xtract device info from line

            device = {'ipaddr': device_info[0],
                      'type':   device_info[1],
                      'name':   device_info[2]}  # create dictionary of device objects ...

            devices[device['ipaddr']] = device  # store our device in the devices dictionary
                                                # note the key for devices dictionary entries is ipaddr

    print('\n###########------devices------###########')
    pprint(devices)

    return devices

# function to convert decrypted data into dictionaries of lists
def data_to_dictLists(decrypted_data):

    decoded_data = decrypted_data.decode('utf-8') # decodes the decrypted data which is in bytes to strings
    decoded_data = decoded_data.split() # split it so it becomes a list, which is needed for modifying it after

    device_creds_list = []
    ip_address = []

    for x in decoded_data:
        device_in_file = x.strip().split(',')  # strip spaces and split list into its own list of item
        device_creds_list.append(device_in_file) # append to the new list
        ip_address.append(x.split(',')[0]) # gets the ip address only and append to the new list


    device_creds = {addr:dev for addr, dev in zip(ip_address, device_creds_list)} # combine the two new lists into a dict of lists
    print('\n###########------device creds------###########')
    pprint(device_creds)

    return device_creds

# function to connect to all the devices to get config information
# can also modify to write configs to devices!
def get_write_config(device_and_creds):

    # For threadpool library we had to pass only one argument, so extract the two
    # pieces (device and creds) out of the one tuple passed.
    device = device_and_creds[0]
    creds = device_and_creds[1]

    """
    [({'ipaddr': '192.168.122.71', 'name': ' R1', 'type': ' cisco_ios'},    # this is device_and_creds[0]
    ['192.168.122.71', 'tony', 'cisco']),                                   # this is device_and_creds[1]
    ({'ipaddr': '192.168.122.72', 'name': ' SW1', 'type': ' cisco_ios'},
    ['192.168.122.72', 'tony', 'cisco']),
    ({'ipaddr': '192.168.122.82', 'name': ' SW2', 'type': ' cisco_ios'},
    ['192.168.122.82', 'tony', 'cisco']),
    ({'ipaddr': '192.168.122.83', 'name': ' SW3', 'type': ' cisco_ios'},
    ['192.168.122.83', 'tony', 'cisco']),
    ({'ipaddr': '192.168.122.84', 'name': ' SW4', 'type': ' cisco_ios'},
    ['192.168.122.84', 'tony', 'cisco']),
    ({'ipaddr': '192.168.122.85', 'name': ' SW5', 'type': ' cisco_ios'},
    ['192.168.122.85', 'tony', 'cisco']),
    ({'ipaddr': '192.168.122.86', 'name': ' SW6', 'type': ' cisco_ios'},
    ['192.168.122.86', 'tony', 'cisco'])]
    """



    # Connecting to the devices based on type
    # can add more device appliances if needed
    if   device['type'] == 'junos-srx': 
        device_type = 'juniper'
    elif device['type'] == 'cisco-ios': 
        device_type = 'cisco_ios'
    elif device['type'] == 'cisco-xr':  
        device_type = 'cisco_xr'
    else:                               
        device_type = 'cisco_ios'    # attempt Cisco IOS as default

    print('#### Connecting to device {0}, username={1}, password={2}'.format(device['ipaddr'],
                                                                                creds[1], creds[2]) + ' ####')

    # Connect to the device
    session = ConnectHandler(device_type=device_type, ip=device['ipaddr'],
                                                       username=creds[1], password=creds[2])
    
    # sending commands to get device information based on its type
    if device_type == 'juniper':
        print ('---- Getting configuration from device ' + device['ipaddr'])
        session.send_command('configure terminal')
        config_data = session.send_command('show configuration')

    if device_type == 'cisco_ios':
        print ('---- Getting configuration from device ' + device['ipaddr'])
        config_data = session.send_command('show run')

    if device_type == 'cisco_xr':
        print ('---- Getting configuration from device ' + device['ipaddr'])
        config_data = session.send_command('show configuration running-config')

    # Write out configuration information to file for each devices
    config_filename = 'config-' + device['ipaddr']

    print ('###### Writing configuration ######: ', config_filename)
    with open(config_filename, 'w') as config_out:  
        config_out.write(config_data)

    session.disconnect()

# main function to run multi threading
def main():
    # generates a secrey key used for encrypting/decrypting
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
    
    decrypted_data = decryption(encrypted_file, secret_key) #decrypts the encrypted file with the key


    devices_file = read_devices('device-file') 
    creds = data_to_dictLists(decrypted_data) # convert the decrpyted data into dict of lists for easy reference 

    num_threads_str = input('\nNumber of threads (default is 5): ') or '5'
    num_threads = int(num_threads_str)

    #creating list containing dictionaries of device info, and the list of credentials for that device 
    config_params_list = []
    for ipaddr, device in devices_file.items():
        config_params_list.append((device, creds[ipaddr]))

    starting_time = time()

    print('\n######## Creating threadpool, launching get config threads ########\n')
    threads = ThreadPool(num_threads)
    threads.map(get_write_config, config_params_list) # calls the get_write_config function with config_params_list as argument

    threads.close()
    threads.join()

    
    """
    Following changes if you want to use concurrent futures: (Remember to uncommennt lines 183-187)
    
    threads = ThreadPoolExecutor(num_threads)
    results = threads.map(get_write_config, config_params_list)

    for result in results:  
        print(result)       # this will print None because i did not return any values in get_write_config function
    """

    print('\n######## End get config threadpool, elapsed time=', time()-starting_time + ' ########')


###############################################################################
#                                   MAIN                                      #
###############################################################################
if __name__ == "__main__":
    main()
    