import requests
import json

def get_token():

    api_path = 'https://sandboxdnac.cisco.com/dna'
    auth = ('devnetuser', 'Cisco123!')
    headers = {'Content-Type': 'application/json'}

    auth_resp = requests.post(
        f'{api_path}/system/api/v1/auth/token', auth=auth, headers=headers

    )

    auth_resp.raise_for_status()
    token = auth_resp.json()["Token"]
    return token 

def get_device(token):

    api_path = 'https://sandboxdnac.cisco.com/dna'
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}

    get_resp = requests.get(
        f'{api_path}/intent/api/v1/network-device', headers=headers

    )
    get_resp.raise_for_status()
    print(json.dumps(get_resp.json(), indent=5))
    
    if get_resp.ok:
        for device_num, device in enumerate(get_resp.json()['response']):
            device_ip = device['managementIpAddress']
            device_id = device['id']
            print(f"Device number {device_num+1} has ID of {device_id} and IP of {device_ip}")
    else:
        print(f'Device collection failed with code {get_resp.status_code}')
        print(f'Fail body text {get_resp.text}')


def main():
    
    token = get_token()
    get_device(token)

if __name__ == "__main__":
    main()