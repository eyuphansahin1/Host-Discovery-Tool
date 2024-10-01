import argparse
import re
from scapy.all import ICMP, IP, sr1
import concurrent.futures

ip_list = []

def get_ip_range():
    parser = argparse.ArgumentParser(description="Performs host discovery using ping")
    parser.add_argument("-i", "--ip", required=True, metavar="START_IP", help="Enter the start IP address in a /24 range")
    args = parser.parse_args()

    start_ip = args.ip
    
    ip_pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
                            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
                            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.0$")
    
    if not ip_pattern.match(start_ip):
        print("Error: IP address must be in the format x.x.x.0 where x is between 0 and 255 (e.g., 192.168.1.0)")
        exit(1)

    base_ip = ".".join(start_ip.split(".")[:-1])  
    return base_ip

def create_ping_packet(ip):
    icmp = ICMP()
    ip_layer = IP(dst=ip)
    ping_packet = ip_layer / icmp
    response = sr1(ping_packet, timeout=0.1, verbose=False)
    if response:
        return ip
    return None

def ping_ips(base_ip):
    ip_range = [f"{base_ip}.{i}" for i in range(256)]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(create_ping_packet, ip_range)
    
    return [ip for ip in results if ip]

base_ip = get_ip_range()
ip_list = ping_ips(base_ip)

print(ip_list)
