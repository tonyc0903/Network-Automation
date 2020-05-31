import requests

"""
    This is a sample Python code that uses REST API to communicate with a ACI always on SandBox on Cisco DevNet to collect EPG information
"""

def main():
    api_path = 'https://sandboxapicdc.cisco.com/api'

    # disable any warnings for self signed cert since the sandbox has one at present present 
    requests.packages.urllib3.disable_warnings()

    # body in dict format that contains the name and password
    body = {"aaaUser": {"attributes": {"name": "admin", "pwd": "ciscopsdt"}}}


    auth_response = requests.post(f'{api_path}/aaaLogin.json', json=body, verify=False) 

    # if HTTP POST fails, throw error, otherwise return json body
    auth_response.raise_for_status()
    auth = auth_response.json()
    
    # Upon successful login, grab the token from the json 
    token = auth['imdata'][0]['aaaLogin']['attributes']['token']

    # token must be applied to the header for future authentication 
    headers = {'Cookie': f"APIC-Cookie={token}"}
    
    epg_resp = requests.get(f'{api_path}/class/fvAEPg.json', headers=headers, verify=False)
    
    # if HTTP POST fails, throw error, otherwise return json body
    epg_resp.raise_for_status()
    epgs = epg_resp.json()
    
    # prints the totalCount key value from the json
    print(f"Total epgs found: {epgs['totalCount']}")

    # for loop to grap the epg names from the json
    for epg in epgs['imdata']:
        print(f"EPG names: {epg['fvAEPg']['attributes']['dn']}")


if __name__ == "__main__":
    main()