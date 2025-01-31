import threading
import subprocess
import sys

def run_ocp_vscode():
    subprocess.run([sys.executable, '-m', 'ocp_vscode'])

# Create a thread for running ocp_vscode
ocp_thread = threading.Thread(target=run_ocp_vscode,  daemon=True)

# Start the ocp_vscode thread
ocp_thread.start()

subprocess.run([sys.executable, 'cadviewer.py'])