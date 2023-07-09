import os
import paramiko
from dotenv import load_dotenv

def run_lynis_scan(hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ssh.connect(hostname, port=port, username=username, password=password)

    # Check if Lynis is installed
    stdin, stdout, stderr = ssh.exec_command("command -v lynis")
    if stdout.channel.recv_exit_status() != 0:  # Command failed, Lynis not installed
        # Install Lynis
        print(f"Installing Lynis on {hostname}...")
        stdin, stdout, stderr = ssh.exec_command("yum install lynis -y")
        if stdout.channel.recv_exit_status() != 0:  # Command failed
            print(f"Failed to install Lynis on {hostname}: {stderr.read().decode('utf-8')}")
            return
        print(f"Lynis installed on {hostname}")

    # Run Lynis scan
    print(f"Running Lynis scan on {hostname}...")
    stdin, stdout, stderr = ssh.exec_command("lynis audit system")

    output = stdout.readlines()

    ssh.close()

    return output

load_dotenv()  # Load environment variables from .env file

hostname = 'fedora'
port = 22
username = os.getenv('un_fedora')
password = os.getenv('pw_fedora')

output = run_lynis_scan(hostname, port, username, password)

print(output)
