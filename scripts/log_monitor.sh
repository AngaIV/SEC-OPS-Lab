#!/bin/bash

#Ensure the script is run with root/sudo privileges to read system logs
if [ "$EUID" -ne 0 ]; then
  echo "[!] Error: Please run this monitor script with sudo."
  exit 1
fi

echo "=================================================="
echo "   REAL-TIME LOG MONITOR & IDS AGENT ACTIVE       "
echo "   Monitoring: SSH & Local Authentication Failures "
echo "=================================================="
echo "[*] Operational mode: Streaming live security events..."
echo "--------------------------------------------------"

#stream the latest systemd authentication logs in real-time
#-u ssh: filters for SSH service logs
#-f: tails/follows the log live
#grep: extracts lines containing "Failed password" or "authentication failure"
journalctl -u ssh -f | grep --line-buffered -E "Failed password|authentication failure|invalid user" | while read -r line
do
    #extract structural details out of the log line for human-readable output
    TIMESTAMP=$(echo "$line" | awk '{print $1" "$2" "$3}')
    ATTACKER_IP=$(echo "$line" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1)
    USER_TARGET=$(echo "$line" | grep -oP 'for (invalid user )?\K\S+')

    if [ -z "$ATTACKER_IP" ]; then
        ATTACKER_IP="Local/Internal Console"
    fi

    #trigger visual alert structure
    echo "[ALERT] Security Anomaly Detected!"
    echo "  Time:    $TIMESTAMP"
    echo "  Target:  User account '$USER_TARGET'"
    echo "  Source:  $ATTACKER_IP"
    echo "--------------------------------------------------"
done
