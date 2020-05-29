from dnacentersdk import api


"""
    This is a sample Python code that uses DNA Center's SDK to communicate with a DNA Center's
    always on SandBox on Cisco DevNet to collect device information
"""

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