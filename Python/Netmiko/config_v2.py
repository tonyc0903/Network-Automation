"""
Program:
    This program configures multiple cisco devices at a time by using files that consists
    of cisco commands and device IP addresses. 
    Also checks for error handling.
"""
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

username = input('Enter your SSH username: ')
password = getpass('Enter your SSH password: ')
secret = getpass('Enter your secret: ')

with open('command_file1.txt') as f, open('device_file.txt') as b:
    commands_list = f.read().splitlines()
    devices_list = b.read().splitlines()

for devices in devices_list:
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password,
        'secret': secret
    }

    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    try: # validates the secret or throw error
        net_connect.enable()
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device (Maybe port is down?): ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    output = net_connect.send_config_set(commands_list)
    print (output)
