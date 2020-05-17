"""
Program 3:
    This program configures multiple cisco devices at a time by opening a file that consists
    the cisco commands and pushing the configs to the devices
"""
from netmiko import ConnectHandler
from getpass import getpass

device1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.82',
    'username': 'tony',
    'password': getpass("Enter password for device 1: ")
}

device2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.83',
    'username': 'tony',
    'password': getpass("Enter password for device 2: ")
}

device3 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.84',
    'username': 'tony',
    'password': getpass("Enter password for device 3: ")
}

device4 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.85',
    'username': 'tony',
    'password': getpass("Enter password for device 4: ")
}

device5 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.86',
    'username': 'tony',
    'password': getpass("Enter password for device 5: ")
}

# seperate cisco ios command text files so you can configure certain devices with different
# configurations (useful when devices needs to have different configurations) 

with open('commandFile1.txt') as f, open('commandFile2.txt') as b:
    lines1 = f.read().splitlines()
    lines2 = b.read().splitlines()

print('Group1 lists: \n')
print (lines1)
print('\n\n')
print('Group2 lists: \n')
print (lines2)


group1_devices = [device3, device4, device5]

for devices in group1_devices:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_config_set(lines1)
    print (output)

group2_devices = [device5, device4, device3, device2, device1]

for devices in group2_devices:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_config_set(lines2)
    print (output)
