# Host-Discovery-Tool

This tool performs network host discovery by sending ICMP ping requests to all IP addresses in a given /24 network range. It uses Scapy for sending and receiving ping responses, and utilizes Python's concurrent.futures module to perform parallelized ping requests, significantly reducing scan time.

Features:
Sends ICMP ping requests to each IP in the specified /24 range.
Collects responses from active hosts (those that reply to the ping).
Uses multithreading to scan multiple IP addresses concurrently, improving performance.
Simple and efficient for quick network scans.

Run the tool with the following command:
python host_discovery.py -i 192.168.1.0

Requirements:
Python 3.x
Scapy
