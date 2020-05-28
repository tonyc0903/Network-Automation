from dnacentersdk import api

# Using Cisco DNA Center SDK to access DNA Center and collect a list of devices 
# Similar to using HTTP get request from dna_api.py
def main():
    dna_center_access = api.DNACenterAPI(username="devnetuser",
                        password="Cisco123!",
                        base_url="https://sandboxdnac.cisco.com/dna",)

    get_devices = dna_center_access.devices.get_device_list()

    for device_num, device in enumerate(get_devices['response']):
        device_type = device['type']
        device_ip = device['managementIpAddress']
        device_id = device['id']
        print(f"Device number {device_num+1} is type {device_type} and has ID of {device_id} and IP of {device_ip}")

if __name__ == "__main__":
    main()





