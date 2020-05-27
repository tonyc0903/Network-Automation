###############################################################################
#                                 DO THIS FIRST:                              #
#   Enter the following commands onto all of your devices:                    #
#    ip scp server enable                                                     #
#    username yourUser privilege 15                                           #
###############################################################################
from napalm import get_network_driver
import json

def main():
    
    #devices ip addresses
    cisco_devices_ip = ['10.1.1.2',
                '10.1.2.2',
                '10.1.3.2',
                '10.1.4.2',
                '10.1.5.2']
    optional_args = {'secret':'cisco'}  # this is not needed since privilege mode 15 is allowed 

    driver = get_network_driver('ios') # set the driver to the platform of the devices

    #for loop to loop through each device and config files for comparison
    for num, device in enumerate(cisco_devices_ip, 1):
        with(driver(device, 'tony', 'cisco', optional_args=optional_args)) as cisco_device: # with block for connectiong to device

            print ("Connecting to " + str(device)) 
            cisco_device.open() # open connection to device 

            device_output = cisco_device.get_facts() # get the device facts
            print(json.dumps(device_output, indent=4)) # print the output and convert into json for easier read
            

            cisco_device.load_merge_candidate(filename=f'eigrp{num}.cfg') # load the config file assoicate to each device for comparing

            diffs = cisco_device.compare_config() # FROM the DOCS:
                                                  # difference between the running configuration and the candidate configuration
                                                  # the running_config is loaded automatically just before doing the comparison so there is no need 
                                                  # for you to do it
           
            # check if there is anything different from the running and file config and apply changes if necessary
            if len(diffs) > 0:
                print('Applying EIGRP')
                print(diffs)
                cisco_device.commit_config()
            else:
                print('No EIGRP changes required.')
                cisco_device.discard_config()

    print('All done, have a good day!')


if __name__ == "__main__":
    main()