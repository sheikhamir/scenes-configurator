import platform
import subprocess
import socket
import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class InstallerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.title_label = Label(text="Pulse Control Server Installer", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title_label)
        
        self.device_ip_label = Label(text="Device IP:", size_hint=(1, 0.1))
        self.layout.add_widget(self.device_ip_label)
        self.device_ip_input = TextInput(multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.device_ip_input)
        
        self.device_port_label = Label(text="Device Port:", size_hint=(1, 0.1))
        self.layout.add_widget(self.device_port_label)
        self.device_port_input = TextInput(multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.device_port_input)
        
        self.server_ip_label = Label(text="Control Server IP:", size_hint=(1, 0.1))
        self.layout.add_widget(self.server_ip_label)
        self.server_ip_input = TextInput(text=self.get_ipv4_address(), multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.server_ip_input)
        
        self.install_button = Button(text="Install", size_hint=(1, 0.2), background_color=(0, 0, 1, 1))
        self.install_button.bind(on_press=self.create_compose_file)
        self.layout.add_widget(self.install_button)
        
        self.log_output = TextInput(readonly=True, size_hint=(1, 0.5))
        self.layout.add_widget(self.log_output)
        
        return self.layout

    def log_message(self, message):
        self.log_output.text += message + '\n'
    
    def detect_os(self):
        os_name = platform.system()
        if os_name == "Windows":
            return "windows"
        elif os_name == "Linux":
            return "linux"
        elif os_name == "Darwin":
            return "macos"
        else:
            return "unknown"
    
    def get_ipv4_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def install_docker_windows(self):
        docker_installer_url = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
        self.log_message("Downloading Docker for Windows...")
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {docker_installer_url} -OutFile DockerDesktopInstaller.exe"])
        self.log_message("Running Docker installer for Windows...")
        subprocess.run(["DockerDesktopInstaller.exe", "install"])
        self.log_message("Docker installation completed for Windows.")

    def install_docker_linux(self):
        self.log_message("Updating package list...")
        subprocess.run(["sudo", "apt-get", "update"])
        self.log_message("Installing Docker...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"])
        self.log_message("Docker installation completed for Linux.")

    def install_docker_macos(self):
        docker_installer_url = "https://desktop.docker.com/mac/stable/Docker.dmg"
        self.log_message("Downloading Docker for MacOS...")
        subprocess.run(["curl", "-L", "-o", "Docker.dmg", docker_installer_url])
        self.log_message("Mounting Docker installer...")
        subprocess.run(["hdiutil", "attach", "Docker.dmg"])
        self.log_message("Copying Docker app to Applications folder...")
        subprocess.run(["cp", "-R", "/Volumes/Docker/Docker.app", "/Applications"])
        subprocess.run(["hdiutil", "detach", "/Volumes/Docker"])
        self.log_message("Docker installation completed for MacOS.")

    def write_docker_compose(self, device_ip, device_port, server_ip):
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
        with open("docker-compose.yml", "w") as file:
            file.write(docker_compose_content)
        self.log_message("docker-compose.yml file created successfully.")

    def update_files(self, server_ip):
        frontend_app_env = "frontend/src/environments/environments.prod.ts"
        wrapper_file = "wrapper/index.html"
        self.log_message(f"Updating IP addresses in configuration files to {server_ip}...")
        if not self.replace_ip(frontend_app_env, server_ip):
            self.log_message(f"Failed to update IP address in {frontend_app_env}")
        if not self.replace_ip(wrapper_file, server_ip):
            self.log_message(f"Failed to update IP address in {wrapper_file}")

    def replace_ip(self, filepath, server_ip):
        if not os.path.isfile(filepath):
            return False
        with open(filepath, 'r') as file:
            file_content = file.read()
        updated_content = file_content.replace("INSTALL_SERVER_IP", server_ip)
        with open(filepath, 'w') as file:
            file.write(updated_content)
        return True

    def run_docker_compose(self):
        self.log_message("Running Docker Compose...")
        subprocess.run(["docker-compose", "up", "-d"])
        self.log_message("Docker Compose has been run successfully.")

    def create_delete_script(self):
        delete_script_content = f"""
import os
import time

time.sleep(5)

os.remove(r"{sys.argv[0]}")
"""
        with open("delete_self.py", "w") as file:
            file.write(delete_script_content)

    def create_compose_file(self, instance):
        device_ip = self.device_ip_input.text
        device_port = self.device_port_input.text
        server_ip = self.server_ip_input.text

        if not device_ip or not device_port or not server_ip:
            self.show_popup("Input Error", "All fields are required")
            return

        self.create_delete_script()
        self.log_message(f"Detected Server IP Address: {server_ip}")
        self.write_docker_compose(device_ip, device_port, server_ip)
        self.update_files(server_ip)
        
        os_type = self.detect_os()
        if os_type == "windows":
            self.install_docker_windows()
        elif os_type == "linux":
            self.install_docker_linux()
        elif os_type == "macos":
            self.install_docker_macos()
        else:
            self.show_popup("Error", "Unsupported OS")
            return
        
        self.run_docker_compose()
        self.show_popup("Success", "Docker Compose has been run successfully")

        subprocess.Popen([sys.executable, "delete_self.py"])

        self.stop()

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message)
        button = Button(text="OK", size_hint=(1, 0.2))
        layout.add_widget(label)
        layout.add_widget(button)
        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4))
        button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    InstallerApp().run()
