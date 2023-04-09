import datetime
import paramiko
import time

# List of devices
devices = [
    {'hostname': 'switch1.example.com', 'ip': '192.168.1.1', 'username': 'admin', 'password': 'password'},
    {'hostname': 'switch2.example.com', 'ip': '192.168.1.2', 'username': 'admin', 'password': 'password'},
    {'hostname': 'switch3.example.com', 'ip': '192.168.1.3', 'username': 'admin', 'password': 'password'}
]

# Date
date = datetime.datetime.now().strftime('%Y-%m-%d')

# File name
filename = f'backup_{date}.txt'

# Open the file for writing
with open(filename, 'w') as f:

    # Loop through each device
    for device in devices:
        print(f"Connecting to {device['hostname']}...")

        # Create SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=device['ip'], username=device['username'], password=device['password'])

        # Create shell object
        shell = ssh.invoke_shell()

        # Send command to backup running configuration
        shell.send('copy running-config tftp://10.0.0.1/running-config\n')
        time.sleep(2)
        shell.send('\n')

        # Receive output of backup running configuration
        output = ''
        while not output.endswith('#'):
            time.sleep(1)
            output += shell.recv(65535).decode()

        # Write backup running configuration to file
        f.write(f"-----------------------------------\n")
        f.write(f"Device: {device['hostname']} - {date}\n")
        f.write(f"-----------------------------------\n\n")
        f.write(f"Backup running configuration...\n\n")
        f.write(f"{output}\n")

        # Send command to show STP status
        shell.send('show spanning-tree\n')
        time.sleep(2)

        # Receive output of STP status
        output = ''
        while not output.endswith('#'):
            time.sleep(1)
            output += shell.recv(65535).decode()

        # Write STP status to file
        f.write(f"\nSTP status...\n\n")
        f.write(f"{output}\n")

        # Send command to show environment status
        shell.send('show environment\n')
        time.sleep(2)

        # Receive output of environment status
        output = ''
        while not output.endswith('#'):
            time.sleep(1)
            output += shell.recv(65535).decode()

        # Write environment status to file
        f.write(f"\nBackup environment status...\n\n")
        f.write(f"{output}\n")

        # Close SSH connection
        ssh.close()

    # Write success message to file
    f.write(f"\nBackup successful!")

print(f"\nBackup successful! Filename: {filename}")
