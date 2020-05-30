import requests, sys

"""
    This is a sample Python code that uses REST API to communicate with a SD-WAN on SandBox on Cisco DevNet to collect device information
"""

def main():
    api_path = 'https://sandbox-sdwan-1.cisco.com'

    # disable any warnings for self signed cert since the sandbox has one at present present 
    requests.packages.urllib3.disable_warnings()

    login_creds = {'j_username':'devnetuser', 'j_password':'RG!_Yw919_83'}

    sess = requests.Session()
    auth_response = sess.post(f'{api_path}/j_security_check', data=login_creds, verify=False) 

    # check if there are any returned HTML content from auth_response. 
    # This usually means failed authentication and can sometimes contain return code 200 (OK). 
    # exit program if it does
    if '<html>' in auth_response.text:
        print('Authentication Failed!')
        sys.exit(1)
    else:
        print('Success!\n')
    

    device_resp = sess.get(f'{api_path}/dataservice/device', verify=False)

    devices = device_resp.json()['data']
    
    print('Found SD-WAN devices managed by SD-WAN Sandbox\n')
    for device in devices:
        print (f"Device host name is {device['host-name']} and has IP of {device['system-ip']}")


if __name__ == "__main__":
    main()