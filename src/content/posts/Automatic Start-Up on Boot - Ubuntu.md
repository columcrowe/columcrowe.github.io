---
title: 'Automatic Start-Up on Boot: Ubuntu'
description: ''
pubDate: 'Jun 26 2025'
---
###### Notes
- Replace vim with a text editor you're comfortable using (e.g., nano, gedit, or others).
- Ensure all file paths, environment names, and user names are accurate for your setup.
  - Replace 192.168.1.x with the IP address for that specific device
- To stop the service if needed:
  ```bash 
  systemctl stop service_name
  ```

## Instructions
### Step 1: Configure Automatic Login
Open the GDM configuration file (replace \`vim\` with your preferred editor, such as nano or gedit):
```bash
sudo vim /etc/gdm3/custom.conf
```
Insert or update the following lines under the \[daemon\] section:
```bash
\[daemon\]

AutomaticLoginEnable = true

AutomaticLogin = user
```

### Step 2: Create the Service Startup Script
Open the script file for editing:
```bash
vim /home/user/run_service_name.sh
```
Insert the following script content (Example: running a python script):
```bash
#! /bin/bash

# Source the conda environment setup
source /home/user/miniconda3/etc/profile.d/conda.sh

# Navigate to the working directory
cd
/home/user/Documents/ToF_python/ToF/build/bindings/python/examples/first_frame/

# Activate the Conda environment and run the Python script
conda activate pytorch

# Replace 192.168.1.x with the IP address for that specific Device
python3 main.py 192.168.1.15 192.168.1.x
```
Change the script permissions to make it executable:
```bash
chmod +x /home/user/run_service_name.sh
```

### Step 3: Create the Systemd Service File
Open the service file for editing:
```bash
sudo vim /etc/systemd/system/service_name.service
```
Insert the following content:
```bash
\[Unit\]

Description=service_name

After=graphical.target

After=multi-user.target

After=network-online.target

\[Service\]

Type=idle

ExecStart=/home/user/run_service_name.sh

User=user

StandardOutput=journal+console

\[Install\]

WantedBy=multi-user.target
```
Adjust permissions for the service file:
```bash
sudo chmod 644 /etc/systemd/system/service_name.service

sudo chmod +x /etc/systemd/system/service_name.service
```

### Step 4: Enable and Start the Service
Reload systemd to update its internal data:
```bash
systemctl daemon-reload
```
Enable the service to start at boot:
```bash
systemctl enable service_name
```
Start the service immediately:
```bash
systemctl start service_name
```

### Step 5: Verify the Service
Check the status of the service:
```bash
systemctl status service_name
```

View logs for the service:
```bash
journalctl -u service_name
```