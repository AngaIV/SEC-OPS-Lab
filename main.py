import customtkinter as ctk
import subprocess
import os
import sys
import threading

#Global theme styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def get_script_path(script_name):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "scripts", script_name)
    #fallback to standard directory trees during active development
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", script_name)


class SecurityControlPanel(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configurations
        self.title("Enterprise Security Control Panel")
        self.geometry("1000x650")
        self.resizable(False, False)

        # Configure 2-column grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Threading & Process tracking states
        self.monitor_thread = None
        self.monitor_process = None
        self.is_monitoring = False

        # ================= SIDEBAR NAVIGATION LAYER =================
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="SECURITY PANEL", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Sidebar Navigation Buttons
        self.btn_vuln = ctk.CTkButton(self.sidebar_frame, text="Vulnerability Scanner", command=lambda: self.switch_view("vuln"))
        self.btn_vuln.grid(row=1, column=0, padx=20, pady=10)

        self.btn_log = ctk.CTkButton(self.sidebar_frame, text="Log Monitor / IDS", command=lambda: self.switch_view("log"))
        self.btn_log.grid(row=2, column=0, padx=20, pady=10)

        self.btn_traffic = ctk.CTkButton(self.sidebar_frame, text="Traffic Analyzer", command=lambda: self.switch_view("traffic"))
        self.btn_traffic.grid(row=3, column=0, padx=20, pady=10)

        self.btn_harden = ctk.CTkButton(self.sidebar_frame, text="System Hardening", command=lambda: self.switch_view("harden"))
        self.btn_harden.grid(row=4, column=0, padx=20, pady=10)

        self.btn_ir = ctk.CTkButton(self.sidebar_frame, text="Incident Response", fg_color="#C0392B", hover_color="#94281B", command=lambda: self.switch_view("ir"))
        self.btn_ir.grid(row=5, column=0, padx=20, pady=10)

        # ================= MAIN CONTENT WINDOW INTERFACE =================
        self.content_frame = ctk.CTkFrame(self, corner_radius=15)
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Header Title
        self.view_title = ctk.CTkLabel(self.content_frame, text="Welcome Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.view_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Dynamic Interactive Controls Layout Box
        self.controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.controls_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Main Terminal Console Text Output Panel
        self.terminal_output = ctk.CTkTextbox(self.content_frame, height=380, font=ctk.CTkFont(family="monospace", size=12))
        self.terminal_output.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Open Default State Tab View
        self.switch_view("vuln")

        # Hook Window Close Button to prevent hanging zombie processes
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def clear_controls(self):
        """Cleans up the top interactive frame layout when switching tabs."""
        for widget in self.controls_frame.winfo_children():
            widget.destroy()

    def log_to_terminal(self, text):
        """Appends output data straight into the text console interface safely."""
        self.terminal_output.insert("end", text + "\n")
        self.terminal_output.see("end")

    def switch_view(self, view_name):
        """Maintains clean state transitions when changing modules."""
        self.clear_controls()
        self.terminal_output.delete("0.0", "end")
        
        # MODULE 1: VULNERABILITY SCANNER
        if view_name == "vuln":
            self.view_title.configure(text="Module 1: Automated Vulnerability Assessment")
            self.target_entry = ctk.CTkEntry(self.controls_frame, placeholder_text="Target IP", width=250)
            self.target_entry.grid(row=0, column=0, padx=(0, 10), pady=10)
            self.target_entry.insert(0, "127.0.0.1")
            
            self.run_btn = ctk.CTkButton(self.controls_frame, text="Execute Scan", command=self.execute_vuln_scan)
            self.run_btn.grid(row=0, column=1, padx=10, pady=10)
            self.log_to_terminal("[Ready] Enter a target host and click 'Execute Scan' to run Nmap...")

        # MODULE 2: LOG MONITOR / IDS
        elif view_name == "log":
            self.view_title.configure(text="Module 2: Real-time Log Monitoring & IDS")
            if not self.is_monitoring:
                self.toggle_btn = ctk.CTkButton(self.controls_frame, text="Start IDS Monitor", fg_color="#27AE60", hover_color="#219653", command=self.start_log_monitoring)
            else:
                self.toggle_btn = ctk.CTkButton(self.controls_frame, text="Stop IDS Monitor", fg_color="#E67E22", hover_color="#D35400", command=self.stop_log_monitoring)
            self.toggle_btn.grid(row=0, column=0, pady=10)
            self.log_to_terminal("[Status] IDS ready...")

        # MODULE 3: TRAFFIC ANALYZER (SNAPSHOT MODEL)
        elif view_name == "traffic":
            self.view_title.configure(text="Module 3: Live Network Traffic Analysis")
            self.btn_sniff = ctk.CTkButton(self.controls_frame, text="Capture & Analyze Packets", fg_color="#2980B9", hover_color="#2471A3", command=self.execute_traffic_analysis)
            self.btn_sniff.grid(row=0, column=0, pady=10)
            self.log_to_terminal("[Ready] Click 'Capture & Analyze Packets' to run a snapshot traffic scan via tcpdump...")

        # MODULE 4: SYSTEM HARDENING
        elif view_name == "harden":
            self.view_title.configure(text="Module 4: Security Hardening & Firewalls")
            self.btn_status = ctk.CTkButton(self.controls_frame, text="Check Status", command=lambda: self.execute_hardening("status"))
            self.btn_status.grid(row=0, column=0, padx=5, pady=10)
            self.btn_enforce = ctk.CTkButton(self.controls_frame, text="Enforce Hardening Baseline", fg_color="#27AE60", hover_color="#219653", command=lambda: self.execute_hardening("enforce"))
            self.btn_enforce.grid(row=0, column=1, padx=5, pady=10)
            self.btn_disable = ctk.CTkButton(self.controls_frame, text="Disable Firewall", fg_color="#7F8C8D", hover_color="#616A6B", command=lambda: self.execute_hardening("disable"))
            self.btn_disable.grid(row=0, column=2, padx=5, pady=10)
            self.log_to_terminal("[Ready] Audit operational firewalls or enforce default deny incoming rules...")

        # MODULE 5: INCIDENT RESPONSE
        elif view_name == "ir":
            self.view_title.configure(text="Module 5: Incident Response & Containment")
            self.btn_isolate = ctk.CTkButton(self.controls_frame, text="ISOLATE SYSTEM", fg_color="#E74C3C", hover_color="#C0392B", font=ctk.CTkFont(weight="bold"), command=lambda: self.execute_incident_response("isolate"))
            self.btn_isolate.grid(row=0, column=0, padx=10, pady=10)
            self.btn_restore = ctk.CTkButton(self.controls_frame, text="Restore Connectivity", fg_color="#34495E", hover_color="#2C3E50", command=lambda: self.execute_incident_response("restore"))
            self.btn_restore.grid(row=0, column=1, padx=10, pady=10)
            self.log_to_terminal("[WARNING] Triggering System Isolation will instantaneously break active network links.")

    # ==================== MODULE 1 ENGINE ====================
    def execute_vuln_scan(self):
        target = self.target_entry.get().strip()
        if not target: return
        self.log_to_terminal(f"[*] Starting Vulnerability Scan against target: {target}...")
        self.update()
        script_path = get_script_path("vuln_scanner.sh")
        try:
            result = subprocess.run(["sudo", script_path, target], capture_output=True, text=True, timeout=60)
            if result.stdout: self.log_to_terminal("\n[+] Scan Results:\n" + result.stdout)
        except Exception as e: self.log_to_terminal(f"[!] Error: {str(e)}")

    # ==================== MODULE 2 ENGINE ====================
    def start_log_monitoring(self):
        self.is_monitoring = True
        self.switch_view("log")
        self.monitor_thread = threading.Thread(target=self.log_stream_worker, daemon=True)
        self.monitor_thread.start()

    def log_stream_worker(self):
        script_path = get_script_path("log_monitor.sh")
        self.monitor_process = subprocess.Popen(["sudo", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        for line in iter(self.monitor_process.stdout.readline, ""):
            if not self.is_monitoring: break
            self.after(0, self.log_to_terminal, line.strip())
        self.monitor_process.stdout.close()

    def stop_log_monitoring(self):
        self.is_monitoring = False
        if self.monitor_process:
            subprocess.run(["sudo", "pkill", "-P", str(self.monitor_process.pid)])
            self.monitor_process.terminate()
        self.switch_view("log")

    # ==================== MODULE 3 ENGINE ====================
    def execute_traffic_analysis(self):
        self.log_to_terminal("[*] Sniffing live packet data... Please generate network activity...")
        self.update()
        script_path = get_script_path("traffic_analysis.sh")
        try:
            result = subprocess.run(["sudo", script_path], capture_output=True, text=True, timeout=40)
            if result.stdout: self.log_to_terminal("\n" + result.stdout)
        except Exception as e: self.log_to_terminal(f"[!] Error: {str(e)}")

    # ==================== MODULE 4 ENGINE ====================
    def execute_hardening(self, action):
        self.log_to_terminal(f"[*] Loading hardening command: [{action}]...")
        self.update()
        script_path = get_script_path("hardening.sh")
        try:
            result = subprocess.run(["sudo", script_path, action], capture_output=True, text=True, timeout=30)
            if result.stdout: self.log_to_terminal("\n" + result.stdout)
        except Exception as e: self.log_to_terminal(f"[!] Error: {str(e)}")

    # ==================== MODULE 5 ENGINE ====================
    def execute_incident_response(self, action):
        self.log_to_terminal(f"[*] Initiating Containment: [{action.upper()}]...")
        self.update()
        script_path = get_script_path("incident_res.sh")
        try:
            result = subprocess.run(["sudo", script_path, action], capture_output=True, text=True, timeout=30)
            if result.stdout: self.log_to_terminal("\n" + result.stdout)
        except Exception as e: self.log_to_terminal(f"[!] Error: {str(e)}")

    def on_closing(self):
        """Ensures clean shutdown sequences when closing window interface entirely."""
        self.stop_log_monitoring()
        self.destroy()

if __name__ == "__main__":
    app = SecurityControlPanel()
    app.mainloop()
