import requests
import json

"""
    This is a sample Python code that uses REST API to communicate with a Meraki Always on SandBox on Cisco DevNet to collect device information
"""

def meraki_get(resource):

    api_path = 'https://dashboard.meraki.com/api/v0'
    headers = {'Content-Type': 'application/json', 'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'}

    
    get_response = requests.get(    
        f'{api_path}/{resource}', headers=headers

    )
    get_response.raise_for_status() # raise error if one occured
    return get_response.json()

def get_meraki_org():
    
    organization = meraki_get('organizations') # get list of organizations 
    print('List of organizations:\n')

    org_id = [] # list to save each organization ID

    # loop through the json containing the organization name and ID, and append ID to the list
    for org in organization:
        print(f"The DevNet organization {org['name']} has ID {org['id']}")
        org_id.append(org['id'])


    print('\n')

    return org_id

def get_org_networks(org_ID):

    dev_network = [] # list to save networks from each organization 
    
    # loop through each networks found in each Organization, print errors if there is any
    for eachNetwork in org_ID:
        try:
            networks = meraki_get(f'organizations/{eachNetwork}/networks')
        except Exception as e:
            print(f'Following Error occured for network {eachNetwork}: {e}\n')

        print(f'Networks found for Organization ID {eachNetwork}:')

        # loop through networks and print its name and ID
        for network_info in networks:
            print(f"Name of network: {network_info['name']}, ID of Network: {network_info['id']}")
            dev_network.append(network_info['id'])
        print('\n')

    print('\n')

    return dev_network

def get_networks_devices(networks):
    print('\n')
    
    # loop throuch each networks to find devices
    for eachNetwork in networks:
        
        devices = meraki_get(f'networks/{eachNetwork}/devices')
        
        # check if networks have devices
        if devices:
            print(f'Devices found for Network {eachNetwork}:')
        else:
            print(f'No devices in Network {eachNetwork}')

        # loop through each device with error checking 
        try:
            for device in devices:
                print(f"Model: {device['model']}, MAC Address: {device['mac']}, Serial# {device['serial']}, IP Address: {device['lanIp']}")
        
        except Exception as e:
            print(f'Device does not have the following information: {e}')
        
        print('\n')

def main():
    get_org = get_meraki_org()
    device_networks = get_org_networks(get_org)
    get_networks_devices(device_networks)


if __name__ == "__main__":
    main()