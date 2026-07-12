#!/bin/bash

#Ensure the script is run with root/sudo privileges to read system logs
if [ "$EUID" -ne 0 ]; then
  echo "[!] Error: This hardening module requires sudo privileges."
  exit 1
fi

COMMAND=$1

case "$COMMAND" in
    "status")
        echo "=================================================="
        echo "          CURRENT FIREWALL STATUS           "
        echo "=================================================="
        ufw status verbose
        ;;
        
    "enforce")
        echo "=================================================="
        echo "          APPLYING SYSTEM HARDENING RULES         "
        echo "=================================================="
        
        #Turn on UFW if it's disabled
        echo "[*] Enabling Uncomplicated Firewall (UFW)..."
        ufw --force enable
        
        #Set strict default policies
        echo "[*] Setting default baseline: Deny Incoming, Allow Outgoing..."
        ufw default deny incoming
        ufw default allow outgoing
        
        #Allow clean essential management traffic
        echo "[*] Hardening rules applied successfully."
        ufw reload
        ;;
        
    "disable")
        echo "[WARNING] Disabling firewall defenses..."
        ufw disable
        ;;
        
    *)
        echo "Usage: $0 {status|enforce|disable}"
        exit 1
        ;;
esac
