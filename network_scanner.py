#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
    # Parser object to handle user inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Specify the IP address or the IP range")
    # Dest value of parser stores the values of corresponding arguments
    options = parser.parse_args()

    # Check for Error condition
    if not options.target:
        parser.error("[-] Please specify the IP, use --help for more information")
    else:
        return options.target

def scan(ip):
    #scapy.arping(ip)
    # scapy.ls(scapy.ARP()) // Gets the Information about ARP class
    # Replicate the above functionality of ARP ping

    # ARP instance for creating an ARP packet
    arp_request = scapy.ARP(pdst=ip)

    # Creating an ethernet packet with broadcast MAC address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # Create a combined packet with ARP and ethernet request
    arp_broadcast_packet = broadcast/arp_request

    # Send the newly created custom packet on the network and capture the response
    (answered_lists, unanswered_lists) = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)

    # Parse the response and extract IP and MAC address to store in a list of dictionary
    list_of_values = []

    for ans in answered_lists:
        values = {'ip':ans[1].psrc, 'mac':ans[1].hwsrc}
        list_of_values.append(values)

    return list_of_values

def print_result(results_list):
    print("IP\t\t\tMAC")
    print(50 * "-")

    for result in results_list:
        print(result['ip'] + "\t\t" + result['mac'])


ip_range = get_arguments()
scan_result = scan(ip_range)
print_result(scan_result)
