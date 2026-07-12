#!/bin/bash

#get the first argument passed by Python
TARGET=$1

#fall back to localhost or throw an error if argument is not passed
if [ -z "$TARGET" ]; then
    echo "[!] Error: No target specified. Usage: ./vuln_scanner.sh <target-ip>"
    exit 1
fi

echo "=================================================="
echo "   LINUX VULNERABILITY SCANNER ACTIVE      "
echo "   Target Asset: $TARGET"
echo "=================================================="

echo "[*] Initiating fast port discovery scan..."
nmap -F "$TARGET"
