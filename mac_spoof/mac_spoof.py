#!/usr/bin/env python


# this module allows you to take user input
import subprocess
# this module parses user input
import optparse
#this module allows for filering using regex
import re
#

# "input()" is python 3 syntax
# "raw_input()" is python 2 syntax


def get_arguments():
    # set method from the optparse object to parcer. allows for multiple arguments / values in cli.
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    #captures values / inputs for use
    ( options, arguments ) = parser.parse_args()

    # make sure user gives values or throw an error
    if not options.interface:
        parser.error("[-]Please specify an interface, use --help for more info ")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.  ")
        # options holds the values of the user inputs
    return options


def change_mac(interface , new_mac):
    print("[*] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    # this line is not from the demom
    # print("All done! The new MAC address is: " + new_mac)


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # this is where we use the "re" module and regeex to fiter out the MAC address
    mac_address_search_result = re.search(rb"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("That's weird... where the hell is the MAC Address? Double check the interface.")



# the options variable holds the returned values from the get_arguments() function above
options= get_arguments()
current_mac = get_current_mac(options.interface)
# in the below print statement, str() is used because "current_mac" is not a string
# and cannot be read.  str() converts the variable to a string and clears the error.
print("The current MAC ADDY is ===> " + str(current_mac) + " <===")
change_mac(options.interface, options.new_mac)
# the value of this variable should have changed to the new mac address
current_mac = get_current_mac(options.interface)
print(current_mac)
if current_mac == current_mac:
    print("[+] MAC address was successfully changed to:  ===>  " + str(current_mac) + " <===")
else:
    print("[+] MAC address did not change.  :-(")





# this function does exactly what is says. it runs ifconfig and captures the state/value of the
# selected hw component
# subprocess.check_output(["ifconfig", options.interface])



# print(ifconfig_result)
# print("All done! The new MAC address is: ")

# the return object will contain all of the stings that are found in groups.  if there are
# multiple matches, the firs one is .group(0)
# print(mac_address_search_result.group(0))