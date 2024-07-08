import customtkinter
import os
import socket
import sys
from PIL import Image

# Constants
PAD = 5
VERSION = "v1.0 BETA"
COPYRIGHT = "Pulse Middle East Trading LLC \u00A9 2024. All rights reserved."
FOOTER_FONT_SIZE = 10
LOG_FONT_SIZE = 12
WINDOW_SIZE = "500x650"
ICON_SIZE = (26, 26)
LOGO_SIZE = (200, 87)

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # Set up theme and window properties
        self.setup_theme()
        self.setup_window()

        # Load images
        self.load_images()

        # Set up layout
        self.setup_layout()

    def setup_theme(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

    def setup_window(self):
        self.title("Pulse Control Server Setup")
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)
        self.configure(fg_color='#000')
        self.iconbitmap(self.resource_path("favicon.xbm"))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def load_images(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media")
        self.image_icon = customtkinter.CTkImage(Image.open(self.resource_path("icon.png")), size=ICON_SIZE)
        self.image_logo = customtkinter.CTkImage(Image.open(self.resource_path("pulse-logo.png")), size=LOGO_SIZE)

    def setup_layout(self):
        self.create_main_frame()
        self.add_logo()
        self.add_title()
        self.add_input_fields()
        self.add_save_button()
        self.add_footer()
        self.add_log_textbox()

    def create_main_frame(self):
        self.frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame.grid(row=0, column=0, padx=100, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

    def add_logo(self):
        self.frame_logo = customtkinter.CTkLabel(self.frame, text="", image=self.image_logo)
        self.frame_logo.grid(row=0, column=0, pady=20)

    def add_title(self):
        self.label_title = customtkinter.CTkLabel(master=self.frame, text="Control Server Setup", font=customtkinter.CTkFont(size=22))
        self.label_title.grid(row=1, column=0, pady=(0, PAD * 4), sticky="ew")

    def add_input_fields(self):
        # Server IP
        self.label_server_ip = self.create_label(self.frame, "Enter Server IP Address", 15, "bold")
        self.label_server_ip.grid(row=2, column=0, sticky="ew")
        self.input_server_ip = self.create_entry(self.frame, "Example: 192.168.xxx.xxx")
        self.input_server_ip.grid(row=3, column=0, pady=(0, PAD * 3), sticky="ew")
        self.input_server_ip.insert(0, self.get_ip_address())

        # Device IP
        self.label_device_ip = self.create_label(self.frame, "Enter Device IP Address", 15, "bold")
        self.label_device_ip.grid(row=4, column=0, sticky="ew")
        self.input_device_ip = self.create_entry(self.frame, "Example: 192.168.xxx.xxx")
        self.input_device_ip.grid(row=5, column=0, pady=(0, PAD * 3), sticky="ew")

        # Device Port
        self.label_device_port = self.create_label(self.frame, "Enter Device Port", 15, "bold")
        self.label_device_port.grid(row=6, column=0, sticky="ew")
        self.input_device_port = self.create_entry(self.frame, "Example: 48631")
        self.input_device_port.grid(row=7, column=0, pady=(0, PAD * 3), sticky="ew")

    def create_label(self, master, text, size, weight):
        return customtkinter.CTkLabel(master, text=text, font=customtkinter.CTkFont(size=size, weight=weight), anchor="w")

    def create_entry(self, master, placeholder):
        return customtkinter.CTkEntry(master, placeholder_text=placeholder, font=customtkinter.CTkFont(size=22), height=40)

    def add_save_button(self):
        self.button_save = customtkinter.CTkButton(master=self.frame, text="Save and run", font=customtkinter.CTkFont(size=22), height=50, fg_color="#AF8D61", hover_color="#C7975E", text_color="#000", command=self.submit, corner_radius=0)
        self.button_save.grid(row=8, column=0, pady=(PAD * 4, 0), sticky="ew")

    def add_footer(self):
        self.label_version = customtkinter.CTkLabel(master=self, text=VERSION, font=customtkinter.CTkFont(size=FOOTER_FONT_SIZE), anchor="e", text_color="gray20")
        self.label_version.grid(row=2, column=0, padx=(0, PAD * 2), sticky="e")

        self.label_copyright = customtkinter.CTkLabel(master=self, text=COPYRIGHT, font=customtkinter.CTkFont(size=FOOTER_FONT_SIZE), anchor="w", text_color="gray20")
        self.label_copyright.grid(row=2, column=0, padx=(PAD * 2, 0), sticky="w")

    def add_progress_bar(self):
        self.progress_bar = customtkinter.CTkProgressBar(master=self.frame, orientation="horizontal", corner_radius=0)
        self.progress_bar.grid(row=9, column=0, sticky="ew")

    def add_log_textbox(self):
        self.textbox_log = customtkinter.CTkTextbox(master=self.frame, height=100, wrap='word', font=customtkinter.CTkFont(size=LOG_FONT_SIZE), state='disabled', corner_radius=0, fg_color="transparent", text_color="gray35")
        self.textbox_log.grid(row=10, column=0, pady=(PAD * 3.5, 0), sticky="ew")

    def log_message(self, message):
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert(customtkinter.END, message + "\n")
        self.textbox_log.yview(customtkinter.END)  # Scroll to the end
        self.textbox_log.configure(state="disabled")

    def start_progress_bar(self):
        self.progress_bar.configure(mode="indeterminnate")
        self.progress_bar.start()

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def submit(self):
        self.add_progress_bar()
        self.start_progress_bar()
        self.log_message("Login button pressed")
        print("Login")

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()
