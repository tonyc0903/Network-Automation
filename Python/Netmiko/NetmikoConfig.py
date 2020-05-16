from netmiko import ConnectHandler
from getpass import getpass

# This will turn the string into a list of strings. Each string equals the router IP 
devices = '''
172.16.1.1
172.16.2.1
172.16.3.1
172.16.4.1

'''.strip().splitlines()

# specifying the device
device_type = 'cisco_ios',
username = 'cisco',
password = getpass('password')
verbose = True

#looping through each router 
for device in devices:
    print(" Connecting to Device: " + device)
    # connecting to the router
    net_connect = ConnectHandler(
        ip=device, 
        device_type=device_type, 
        username=username, 
        password=password)

    prompt = net_connect.find_prompt()
    print(prompt)

    # commands 
    show_run_config = net_connect.send_command('show run | sec eigrp')
    eigrp_commands = ['router eigrp 1', 'network 0.0.0.0 255.255.255.255']
    
    #check if eigrp is configured and decide if you want to configure it 
    if not 'router eigrp' in show_run_config:
        print('EIGRP is not enabled on device:' + device)
        answer = input(f'Would you like to enable EIGRP on {device}' + 'Y/N?')

        if answer == 'Y':
            eigrp_config = net_connect.send_command(eigrp_commands)
            print(eigrp_config)
            print('EIGRP is now configured')
        else:
            print('Did not configure EIGRP')
    # eigrp already configured
    else:
        print('EIGRP is already configured')

    # disconnect from thr router
    net_connect.disconnect()
