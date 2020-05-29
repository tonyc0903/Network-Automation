import requests
import json

"""
    This is a sample Python code that uses REST API to communicate with DNA Center's
    always on SandBox on Cisco DevNet to collect device information
"""

# getting token 
def get_token():

    api_path = 'https://sandboxdnac.cisco.com/dna'
    auth = ('devnetuser', 'Cisco123!')
    headers = {'Content-Type': 'application/json'}

    # performing post request to access the DNA Center for token
    token_response = requests.post(
        f'{api_path}/system/api/v1/auth/token', auth=auth, headers=headers

    )

    token_response.raise_for_status() # raise error if one occured
    token = token_response.json()["Token"]
    return token

# getting device from DNA Center
def get_device(token):

    api_path = 'https://sandboxdnac.cisco.com/dna'
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}

    # performing get request to access the DNA Center
    get_response = requests.get(
        f'{api_path}/intent/api/v1/network-device', headers=headers

    )
    get_response.raise_for_status() # raises any HTTP error if occured
    print(json.dumps(get_response.json(), indent=5)) # prints the data into JSON
    
    if get_response.ok:
        for device_num, device in enumerate(get_response.json()['response']):
            device_ip = device['managementIpAddress']
            device_id = device['id']
            print(f"Device number {device_num+1} has ID of {device_id} and IP of {device_ip}")
    else:
        print(f'Device collection failed with code {get_response.status_code}')
        print(f'Fail body text {get_response.text}')

def main():
      
    token = get_token()
    get_device(token)

if __name__ == "__main__":
    main()