#!/usr/bin/env python

# Module to run system commands
import subprocess
# Get arguments from user and parse the values
import optparse
# Module for regular expressions
import re

def get_arguments():
    # Parser object to handle user inputs
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    # Dest value of parser stores the values of corresponding arguments
    (options,arguments) = parser.parse_args()

    # Check for Error condition
    if not options.interface:
        parser.error("[-] Please specify the interface, use --help for more information")
    elif not options.new_mac:
        parser.error("[-] Please specify the MAC address, use --help for more information")
    else:
        return options

def change_mac(interface, new_mac):
    print("Changing MAC address for " + interface)
    # Always use the following process for executing shell commands
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search:
        return mac_address_search.group(0)
    else:
        print("Could not read MAC address")

# Get the User input arguments from the function
options = get_arguments()
current_mac = get_current_mac(options.interface)
#change_mac(options.interface, options.new_mac)


