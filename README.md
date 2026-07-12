# SEC-OPS-Lab: Enterprise Security Control Panel
**Modular Security Operations, Network Traffic Sniffing, and Automated Containment**

---

## About the Project

A security operations control panel that bridges custom Python orchestration with native Linux binaries. The system brings core defensive capabilities—including vulnerability scanning, real-time log monitoring, packet analysis, firewall hardening, and immediate network isolation—into a unified desktop interface for an Ubuntu deployment.

![Project Dashboard Overview](assets/image1.png)

---

## Core Components

| Component | Role |
|---|---|
| **Vulnerability Scanner** | Handles network footprinting sweeps using `nmap` to audit open ports and service banners. |
| **Log Monitor / IDS** | Parses `/var/log/auth.log` via a non-blocking asynchronous streaming worker to flag authentication failures instantly. |
| **Traffic Analyzer** | Utilizes a snapshot capture engine backed by `tcpdump` to extract connection tracking telemetry and flag traffic volume anomalies. |
| **System Hardening** | Interacts with the Uncomplicated Firewall (`ufw`) subsystem to enforce a default-deny inbound posture. |
| **Incident Response** | Functions as a network kill-switch to immediately isolate physical or virtual interface links during an active compromise. |

---

## Technical Architecture

A multi-threaded Python front-end built using `customtkinter` that spawns asynchronous subprocess pipelines to securely drive root-level system scripts.

![System Architecture and Process Routing](assets/image2.png)

---

## Configuration and Implementation

### 1. Snapshot Network Traffic Analysis

The traffic engine captures raw network packet frames directly from the active interface using a finite snapshot window before running statistical calculations to identify anomalies:

```bash
tcpdump -i "$INTERFACE" -c "$PACKET_COUNT" -nn -w "$CAPTURE_FILE" 2>/dev/null
```

Heuristic parsing instantly breaks down traffic protocols and reports top connection talkers to the interface display.

![Network Traffic Analyzer Interface](assets/image3.png)

### 2. Multi-Threaded Real-Time Log Monitoring

To keep the GUI responsive while streaming live data, the Intrusion Detection Module spans a background thread using Python's `threading` library, piping stdout sequentially from the core monitoring engine.

```python
self.monitor_thread = threading.Thread(target=self.log_stream_worker, daemon=True)
self.monitor_thread.start()
```

![Log Monitor Live Console Stream](assets/image4.png)

### 3. Incident Containment Network Kill-Switch

When system isolation is triggered, the response engine drops active network configuration bindings immediately via interface state control links:

```bash
sudo ip link set dev "$INTERFACE" down
```

This cuts off remote attacker persistence across compromised links instantly.

![Incident Response Containment View](assets/image5.png)

---

## Skills Applied

- Python multi-threading and GUI orchestration (`customtkinter`)
- Asynchronous subprocess pipeline handling
- Network packet sniffing and traffic telemetry (`tcpdump`)
- Linux authentication auditing (`auth.log`)
- Netfilter firewall policy enforcement (`ufw`)
- Incident response containment and interface isolation
- Bash scripting engineering and structural directory handling
- Linux permission privilege structures (`sudo` execution context)

---

## Prerequisites

The control panel relies on system binaries requiring root execution privileges. Ensure the following tools are installed on the host machine:

```bash
sudo apt update
sudo apt install nmap tcpdump ufw python3-pip python3-venv -y
```

---

## How to Replicate

### 1. Clone the Workspace
```bash
git clone git@github.com:AngaIV/SEC-OPS-Lab.git
cd SEC-OPS-Lab
```

### 2. Setup Isolated Environment
```bash
python3 -m venv env
source env/bin/activate
pip install customtkinter
```

### 3. Run the Control Panel
Because the application configures network cards and firewalls, execute the environment runner with root permissions:
```bash
sudo ./env/bin/python main.py
```

### 4. Optional: Compile standalone Binary
```bash
pip install pyinstaller
pyinstaller --clean --onefile --collect-all customtkinter --add-data "scripts:scripts" main.py
```
