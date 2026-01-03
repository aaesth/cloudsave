import os
import time
import zipfile
import subprocess
import psutil
import paramiko
from paramiko import SSHClient
from scp import SCPClient

def load_config():
    config = {}
    with open('here.txt', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

def download_and_unzip(config):
    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(config['sftp_ip'], username=config['sftp_user'], password=config['sftp_pass'])
        
        with SCPClient(ssh.get_transport()) as scp:
            remote_path = os.path.join(config['sftp_dir'], 'backup.zip')
            local_zip = 'temp_backup.zip'
            scp.get(remote_path, local_zip)
        
        ssh.close()
        
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(config['local_dir'])
        
        os.remove(local_zip)
        print("downloaded and unzipped backup.")
    except Exception as e:
        print(f"failed to download backup: {e}")

def zip_and_upload(config):
    zip_name = 'backup.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        with open('this.txt', 'r') as f:
            for file in f:
                file = file.strip()
                file_path = os.path.join(config['local_dir'], file)
                if os.path.exists(file_path):
                    zipf.write(file_path, file)
    
    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(config['sftp_ip'], username=config['sftp_user'], password=config['sftp_pass'])
        
        with SCPClient(ssh.get_transport()) as scp:
            remote_path = os.path.join(config['sftp_dir'], zip_name)
            scp.put(zip_name, remote_path)

        ssh.close()
        os.remove(zip_name)
        print("zipped and uploaded backup.")
    except Exception as e:
        print(f"failed to upload backup: {e}")

def main():
    config = load_config()
    download_and_unzip(config)

    app_path = config['app_path']
    process = subprocess.Popen(app_path)
    proc = psutil.Process(process.pid)
    proc_name = proc.name()
    print("┏━╸╻  ┏━┓╻ ╻╺┳┓┏━┓┏━┓╻ ╻┏━╸")
    print("┃  ┃  ┃ ┃┃ ┃ ┃┃┗━┓┣━┫┃┏┛┣╸ ")
    print("┗━╸┗━╸┗━┛┗━┛╺┻┛┗━┛╹ ╹┗┛ ┗━╸")
    print("[cs] cloudsave is running and monitoring", proc_name)
    # shoutouts 746128427760746680
    while True:
        try:
            if not any(p.name() == proc_name for p in psutil.process_iter()):
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            break
        time.sleep(1)
    
    zip_and_upload(config)

if __name__ == "__main__":
    main()