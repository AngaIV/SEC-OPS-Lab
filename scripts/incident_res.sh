#!/bin/bash

#ensure the script is run with root/sudo privileges to read system logs
if [ "$EUID" -ne 0 ]; then
  echo "[!] Error: Incident Response containment requires sudo privileges."
  exit 1
fi

COMMAND=$1

#identify the primary active network interface card
INTERFACE=$(ip -o -4 route show to default | awk '{print $5}' | head -n 1)

if [ -z "$INTERFACE" ] && [ "$COMMAND" != "restore" ]; then
    #fallback to general lookups if default route is tricky
    INTERFACE=$(ip link show | awk -F': ' '/valid_lft/ {print $2}' | grep -v "lo" | head -n 1)
fi

case "$COMMAND" in
    "isolate")
        echo "=================================================="
        echo "   CRITICAL INCIDENT RESPONSE CONTAINMENT ACTIVE  "
        echo "=================================================="
        echo "[!] SEVERING ACTIVE CORRUPT NETWORK LOGISTICS..."
        
        #take a snap-shot forensic print of active memory network connections before killing them
        mkdir -p ~/Desktop/IR_Forensics_Logs
        ss -tunapl > ~/Desktop/IR_Forensics_Logs/connections_snapshot.txt
        ps aux > ~/Desktop/IR_Forensics_Logs/process_snapshot.txt
        
        #shut down the network adapter link to completely isolate the machine
        if [ ! -z "$INTERFACE" ]; then
            echo "[*] Killing interface connection channel: $INTERFACE"
            #store the isolated interface identifier so we know what to restore later
            echo "$INTERFACE" > /tmp/isolated_interface.txt
            ip link set "$INTERFACE" down
            echo "[SUCCESS] Network link terminated. Target system is isolated."
        else
            echo "[!] Error: Could not accurately trace active network adapters."
        fi
        ;;
        
    "restore")
        echo "=================================================="
        echo "   RESTORING SYSTEM CONTEXT CONNECTIONS           "
        echo "=================================================="
        
        #retrieve the cached card configuration pointer
        if [ -f /tmp/isolated_interface.txt ]; then
            SAVED_INT=$(cat /tmp/isolated_interface.txt)
            echo "[*] Restoring network adapter link: $SAVED_INT"
            ip link set "$SAVED_INT" up
            rm /tmp/isolated_interface.txt
            echo "[SUCCESS] Network pipelines active."
        else
            #fallback: ring up all interfaces if cache is missing
            echo "[*] Restoring all network interface structures..."
            for int in $(ls /sys/class/net/ | grep -v lo); do
                ip link set "$int" up
            done
            echo "[SUCCESS] Adapters reactivated."
        fi
        ;;
        
    *)
        echo "Usage: $0 {isolate|restore}"
        exit 1
        ;;
esac
