import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
import socket
import os
import sys

def detect_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Linux":
        return "linux"
    elif os_name == "Darwin":
        return "macos"
    else:
        return "unknown"

def get_ipv4_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)
    app.update()

def install_docker_windows():
    docker_installer_url = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
    log_message("Downloading Docker for Windows...")
    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {docker_installer_url} -OutFile DockerDesktopInstaller.exe"])
    log_message("Running Docker installer for Windows...")
    subprocess.run(["DockerDesktopInstaller.exe", "install"])
    log_message("Docker installation completed for Windows.")

def install_docker_linux():
    log_message("Updating package list...")
    subprocess.run(["sudo", "apt-get", "update"])
    log_message("Installing Docker...")
    subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"])
    log_message("Docker installation completed for Linux.")

def install_docker_macos():
    docker_installer_url = "https://desktop.docker.com/mac/stable/Docker.dmg"
    log_message("Downloading Docker for MacOS...")
    subprocess.run(["curl", "-L", "-o", "Docker.dmg", docker_installer_url])
    log_message("Mounting Docker installer...")
    subprocess.run(["hdiutil", "attach", "Docker.dmg"])
    log_message("Copying Docker app to Applications folder...")
    subprocess.run(["cp", "-R", "/Volumes/Docker/Docker.app", "/Applications"])
    subprocess.run(["hdiutil", "detach", "/Volumes/Docker"])
    log_message("Docker installation completed for MacOS.")

def write_docker_compose(device_ip, device_port, server_ip):
    docker_compose_content = f"""
version: '3'

services:
  bridge:
    restart: always
    build:
      context: ./bridge
      args:
        TAG: v1
    command: "80 {device_ip}:{device_port}"
    ports:
      - "8300:80"
  backend:
    restart: always
    build:
      context: ./backend
      args:
        TAG: v1
    ports:
      - "8000:80"
  frontend:
    restart: always
    build:
      context: ./frontend
      args:
        TAG: v1
    ports:
      - "8200:80"
  admin:
    restart: always
    build:
      context: ./admin-v2
      args:
        TAG: v1
    ports:
      - "9000:80"
  wrapper:
    restart: always
    build:
      context: ./wrapper
      args:
        TAG: v1
    ports:
      - "8201:80"
"""
    # docker_compose_content = f"""
    # version: '3'
    # services:
    #   {service_name}:
    #     image: {image_name}
    #     ports:
    #       - "{port_mapping}"
    # """
    with open("docker-compose.yml", "w") as file:
        file.write(docker_compose_content)
    log_message("docker-compose.yml file created successfully.")

def update_files(server_ip):
    frontend_app_env = "frontend/src/environments/environments.prod.ts"
    wrapper_file = "wrapper/index.html"

    # Replaces the IP address to the defined IP address
    replace_ip(frontend_app_env, server_ip)
    replace_ip(wrapper_file, server_ip)

def replace_ip(filepath, server_ip):
    # Check if the file exists
    if os.path.isfile(filepath) == False:
        return False
    # Read the content of the file
    with open(filepath, 'r') as file:
        file_content = file.read()
    # Replace the placeholder with the custom server IP
    updated_content = file_content.replace("INSTALL_SERVER_IP", server_ip)

    # Write the updated content back to the file
    with open(filepath, 'w') as file:
        file.write(updated_content)

def run_docker_compose():
    log_message("Running Docker Compose...")
    subprocess.run(["docker-compose", "up", "-d"])
    log_message("Docker Compose has been run successfully.")

def create_delete_script():
    delete_script_content = f"""
import os
import time

# Path to the current file
file_path = __file__

# Function to delete the file
def delete_self():
    os.remove(file_path)

# Wait for a few seconds to ensure the main executable has exited
time.sleep(1)

# Delete the main executable
os.remove(r"{sys.argv[0]}")

time.sleep(1)

# Call the function to delete the file
delete_self()
"""
    with open("delete_self.py", "w") as file:
        file.write(delete_script_content)

def create_compose_file():
    device_ip = device_ip_entry.get()
    device_port = device_port_entry.get()
    server_ip = server_ip_entry.get()

    # Create the delete script
    create_delete_script()
    
    if not device_ip or not device_port or not server_ip:
        messagebox.showerror("Input Error", "All fields are required")
        return
    
    write_docker_compose(device_ip, device_port, server_ip)
    # Updates the IP address inside the files
    update_files(server_ip)
    
    os_type = detect_os()
    if os_type == "windows":
        install_docker_windows()
    elif os_type == "linux":
        install_docker_linux()
    elif os_type == "macos":
        install_docker_macos()
    else:
        messagebox.showerror("Error", "Unsupported OS")
        return
    
    # run_docker_compose()
    messagebox.showinfo("Success", "Docker Compose has been run successfully")
    
    # Run the delete script
    subprocess.Popen([sys.executable, "delete_self.py"])

    # Close the GUI
    app.destroy()
    

# Create the main window
app = tk.Tk()
app.title("Pulse Control Server")
app.geometry("400x400")  # Set window size

# Add a title label
title_label = tk.Label(app, text="Pulse Control Server Installer", font=("Helvetica", 16))
title_label.grid(row=0, columnspan=2, pady=10)

# Add input fields and labels
tk.Label(app, text="Device IP:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Label(app, text="Device Port:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Label(app, text="Control Server IP:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

device_ip_entry = tk.Entry(app, width=30)
device_port_entry = tk.Entry(app, width=30)
server_ip_entry = tk.Entry(app, width=30)
server_ip_entry.insert(0, get_ipv4_address())

device_ip_entry.grid(row=1, column=1, padx=5, pady=5)
device_port_entry.grid(row=2, column=1, padx=5, pady=5)
server_ip_entry.grid(row=3, column=1, padx=5, pady=5)

# Add a create and run button
create_run_button = tk.Button(app, text="Install", command=create_compose_file, bg="blue", fg="white")
create_run_button.grid(row=4, columnspan=2, pady=10)

# Add a scrolled text widget for logging
log_text = scrolledtext.ScrolledText(app, width=60, height=10, state=tk.DISABLED)
log_text.grid(row=5, columnspan=2, padx=10, pady=10)

# Start the main loop
app.mainloop()
