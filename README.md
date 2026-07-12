# SEC-OPS-Lab: Security Operations Lab
**Simple Security Operations, Network Traffic Sniffing, and Automated Containment**

---

## About the Project

A security operations control panel that bridges custom Python orchestration with native Linux binaries. The system brings core defensive capabilities like vulnerability scanning, real-time log monitoring, packet analysis, firewall hardening, and immediate network isolation into a unified desktop interface for an Ubuntu deployment.


---

## Core Components

| Component | Role |
|---|---|
| **Vulnerability Scanner** | Handles network footprinting sweeps using `nmap` to audit open ports and service banners. |
| **Log Monitor / IDS** | Parses `/var/log/auth.log` via a non-blocking asynchronous streaming worker to flag authentication failures instantly. |
| **Traffic Analyzer** | Utilizes a snapshot capture engine backed by `tcpdump` to extract connection tracking telemetry and flag traffic volume anomalies. |
| **System Hardening** | Interacts with the Uncomplicated Firewall `(ufw)` subsystem to enforce a default-deny inbound posture. |
| **Incident Response** | Functions as a network kill-switch to immediately isolate physical or virtual interface links during an active compromise. |

---

## Technical Architecture

A multi-threaded Python front-end built using customtkinter that spawns asynchronous subprocess pipelines to securely drive root-level system scripts.

```text
                           [ Security Operations Lab GUI ]
                                         │
        ┌───────────────┬────────────────┼───────────────┬───────────────┐
        ▼               ▼                ▼               ▼               ▼
   [ Module 1 ]    [ Module 2 ]     [ Module 3 ]    [ Module 4 ]    [ Module 5 ]
   Vuln Scanner    Log Monitor    Traffic Analyzer   Hardening    Incident Response
        │               │                │               │               │
        ▼               ▼                ▼               ▼               ▼
     (nmap)       (auth.log)        (tcpdump)          (ufw)        (ip link)
```
---

## Configuration and Implementation

### 1. Automated Vulnerability Assessment

The scanning engine launches non-destructive network footprinting sweeps against specified target hosts to map the active attack surface and audit open port states:

```bash
nmap -sV -p- --open "$TARGET_IP" -oN "$SCAN_OUTPUT_FILE"
```

The application parses the output to display live port metrics and service configurations directly onto the dashboard.

![Vulnerability Scanner Interface](assets/image3.png)

### 2. Multi-Threaded Real-Time Log Monitoring

To keep the GUI fluid and responsive while processing continuous file streams, the Intrusion Detection module offloads execution to a background worker thread, sequentially tracking system authentication logs:

```python
self.monitor_thread = threading.Thread(target=self.log_stream_worker, daemon=True)
self.monitor_thread.start()
```

The underlying script continuously tails /var/log/auth.log to parse and highlight active authentication failures.

![Log Monitor Live Console Stream](assets/image4.png)

### 3. Snapshot Network Traffic Analysis

The traffic engine captures raw network packet frames over a finite evaluation window before running statistical calculations to flag volume anomalies or high-frequency network talkers:

```bash
tcpdump -i "$INTERFACE" -c "$PACKET_COUNT" -nn -w "$CAPTURE_FILE" 2>/dev/null
```

The captured telemetry is parsed systematically to extract protocols, source/destination IPs, and payload data sizes.

![Network Traffic Analyzer Interface](assets/image5.png)

### 4. Firewall Rule Hardening Execution

The hardening utility interfaces natively with the Uncomplicated Firewall (ufw) subsystem to control perimeter parameters and switch the local network posture between open and default-deny configurations:

```bash
sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw enable
```

Administrators can use the interface to safely apply strict access control list adjustments dynamically.

![Firewall Hardening Panel](assets/image6.png)

### 5. Incident Containment Network Kill-Switch

When an active host compromise is verified, the response engine drops active layer-2 and layer-3 configurations completely to isolate the machine from the physical or virtual segment:

```bash
sudo ip link set dev "$INTERFACE" down
```

This immediately severs remote command-and-control persistence loops and protects adjacent network assets from lateral movement.

![Incident Response Containment View](assets/image7.png)

---

## Skills Applied

- Python multi-threading and GUI orchestration `(customtkinter)`
- Asynchronous subprocess pipeline handling
- Network packet sniffing and traffic telemetry `(tcpdump)`
- Linux authentication auditing `(auth.log)`
- Netfilter firewall policy enforcement `(ufw)`
- Incident response containment and interface isolation
- Bash scripting engineering and structural directory handling
- Linux permission privilege structures (sudo execution context)

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
