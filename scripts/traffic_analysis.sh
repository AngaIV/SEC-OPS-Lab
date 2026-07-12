#!/bin/bash

#Ensure the script is run with root/sudo privileges to read system logs
if [ "$EUID" -ne 0 ]; then
  echo "[!] Error: Traffic Analysis requires sudo privileges."
  exit 1
fi

#find the primary active interface
INTERFACE=$(ip -o -4 route show to default | awk '{print $5}' | head -n 1)
if [ -z "$INTERFACE" ]; then
    INTERFACE=$(ls /sys/class/net/ | grep -v lo | head -n 1)
fi

PACKET_COUNT=50
CAPTURE_FILE="/tmp/live_capture.pcap"

echo "=================================================="
echo "    LIVE NETWORK TRAFFIC ANALYZER          "
echo "    Interface: $INTERFACE | Capture Window: $PACKET_COUNT Packets"
echo "=================================================="
echo "[*] Initializing sniffer..."

#capture traffic silently to a PCAP file
tcpdump -i "$INTERFACE" -c "$PACKET_COUNT" -nn -w "$CAPTURE_FILE" 2>/dev/null

echo "[+] Capture complete! Processing security analysis..."
echo "--------------------------------------------------"

#run heuristic analytics on the captured raw trace
echo ">>> Top Traffic Talkers (Source IP -> Connections):"
tcpdump -r "$CAPTURE_FILE" -nn | awk '{print $3}' | awk -F. '{print $1"."$2"."$3"."$4}' | sort | uniq -c | sort -nr | head -n 5
echo ""

echo ">>> Protocol Breakdown Summary:"
echo "    TCP Packets: $(tcpdump -r "$CAPTURE_FILE" -nn tcp 2>/dev/null | wc -l)"
echo "    UDP Packets: $(tcpdump -r "$CAPTURE_FILE" -nn udp 2>/dev/null | wc -l)"
echo "    ICMP (Ping): $(tcpdump -r "$CAPTURE_FILE" -nn icmp 2>/dev/null | wc -l)"
echo "--------------------------------------------------"

#quick Signature Check
ICMP_COUNT=$(tcpdump -r "$CAPTURE_FILE" -nn icmp 2>/dev/null | wc -l)
if [ "$ICMP_COUNT" -gt 10 ]; then
    echo "[ALERT] Anomalous ICMP (Ping) volume detected! Potential scanning activity."
fi

#clean up temporary capture footprint safely
rm -f "$CAPTURE_FILE"
