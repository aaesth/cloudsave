# cloudsave
python program for cloud saving i guess

only tested on mwc and on windows

## setup

1. install dependencies: `pip install -r requirements.txt`

2. edit `here.txt` with your configuration:
   - `app_path`: path to the application executable.
   - `sftp_ip`: sftp server IP address.
   - `sftp_user`: sftp username.
   - `sftp_pass`: sftp password.
   - `sftp_dir`: directory on SFTP server.
   - `local_dir`: local directory where the save files are at.

3. edit `this.txt` with the list of files to backup, one file per line.

## usage

running `python cloudsave.py` will:
- download the latest backup from SFTP and unzip to `local_dir`.
- launch the application.
- monitor the application; when it closes, zips the specified files and upload to sftp.

## notes

- make sure the sftp server allows connections and the credentials are correct.
- the backup zip is named `backup.zip`.
- if no backup exists on sftp, the download step will fail but it doesnt stop the entire propcess.

## credits
github copilot - it kept crashing i didnt know how to fix it bro

