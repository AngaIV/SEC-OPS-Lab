import subprocess
import os

def run_local_module(script_name, argument):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(base_dir) == "scripts":
        script_path = os.path.join(base_dir, script_name)
    else:
        script_path = os.path.join(base_dir, "scripts", script_name)
    
    print(f"[*] Executing native script at: {script_path} against {argument}...")
    
    try:
        result = subprocess.run(
            ["sudo", script_path, argument],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, f"Execution failed with exit code {e.returncode}\nError: {e.stderr}"


stdout, stderr = run_local_module("vuln_scanner.sh", "127.0.0.1")

print("\n[+] System Output:")
print(stdout)

if stderr:
    print(f"\n[!] System Alerts:\n{stderr}")
