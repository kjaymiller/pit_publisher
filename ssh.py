from config import SSH_PATH, SSH_USERNAME
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

def ssh(filename, path):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(SSH_PATH, username=SSH_USERNAME)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(filename, path)
