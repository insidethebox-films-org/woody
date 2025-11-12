from .. import style
from ...utils import save_settings_json, load_settings_json
from ...plugins.blender.blender_instance import BlenderInstance
from ...tool.woody_instance import WoodyInstance
from ...plugins.blender.install_blender_libraries import install_blender_libraries

import os
import customtkinter as ctk

class SettingsWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x315")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
        self.blender = BlenderInstance()
        
        # Set icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "icons",
            "woodyIcon.ico"
        )
        self.window.after(201, lambda: self.window.iconbitmap(icon_path))
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#5a5a5a"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.load_settings()
        
    def load_settings(self):
        preferences = load_settings_json()
        self.mongoDBAddressEntry.insert(0, preferences.get("mongoDBAddress", ""))
        self.blenderExecutableEntry.insert(1, preferences.get("blenderExecutable", ""))
    
    def save_settings(self):
        mongoDBAddress = self.mongoDBAddressEntry.get()
        blenderExecutable = self.blenderExecutableEntry.get()
        
        print(f"Saving settings:\nMongoDB Address: {mongoDBAddress}\nBlender Executable: {blenderExecutable}")
        save_settings_json(mongoDBAddress=mongoDBAddress, blenderExecutable=blenderExecutable)
        self.window.destroy()
    
    def install_blender(self):
        blender_executable_path = WoodyInstance().blenderExecutable.strip()
        install_blender_libraries(blender_executable_path)
    
    def dev_update(self):
        if self.blender.dev_update():
            print("Dev Update Complete", "Addon zip has been recreated successfully!")
        else:
            print("Dev Update Failed", "Failed to recreate addon zip. Check the console for details.")
    
    def create_widgets(self):
        # Settings Label
        self.settingsLabel = ctk.CTkLabel(
            self.frame,
            text="Settings",
            **style.HEADER_LABEL
        )
        self.settingsLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))
        
        # Separator
        self.separator = ctk.CTkFrame(
            self.frame,
            height=2,
            fg_color="#414141"
        )
        self.separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8))

        # MongoDB Address
        self.mongoDBAddressLabel = ctk.CTkLabel(
            self.frame,
            text="MongoDB Address",
            **style.BODY_LABEL
        )
        self.mongoDBAddressLabel.grid(row=2, column=0, sticky="nw", padx=8)
        
        self.mongoDBAddressEntry = ctk.CTkEntry(
            self.frame,
        )
        self.mongoDBAddressEntry.grid(row=3, column=0, sticky="ew", padx=8)

        # Blender executable label
        self.blenderExecutableLabel = ctk.CTkLabel(
            self.frame, 
            text="Blender Executable",
            **style.BODY_LABEL
        )
        self.blenderExecutableLabel.grid(row=4, column=0, sticky="nw", padx=8)

        # Blender executable entry
        self.blenderExecutableEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.blenderExecutableEntry.grid(row=5, column=0, sticky="new", padx=8, columnspan=2)
        
        # Save settings button
        self.saveSettingsButton = ctk.CTkButton(
            self.frame,
            text="Save Settings",
            **style.BUTTON_STYLE,
            
            command=self.save_settings
        )
        self.saveSettingsButton.grid(row=6, column=0, sticky="nwe", padx=8, pady=8)
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=7, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2)
        
        self.blenderInstallButton = ctk.CTkButton(
            self.frame,
            text="Install Blender Addon and Dependencies",
            **style.BUTTON_STYLE,
            command=self.install_blender
            )
        self.blenderInstallButton.grid(row=8, sticky="nwe", padx=8, pady=(0,8))
        
        self.devUpdateButton = ctk.CTkButton(
            self.frame,
            text="Dev Update",
            **style.BUTTON_STYLE,
            command=self.dev_update
            )
        self.devUpdateButton.grid(row=9, sticky="nwe", padx=8, pady=(0,8))
    
    def run(self):
        self.window.wait_window()