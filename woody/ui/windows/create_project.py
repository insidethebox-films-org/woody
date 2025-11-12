from .. import style
from ...tool.woody_instance import WoodyInstance
from ...lib.folder import create_project_fd
from ...lib.mongodb import create_project_db
from ...plugins.blender.install_blender_libraries import install_blender_libraries
from ...plugins.blender.operations.copy_prefs_to_addon import copy_prefs_to_addon

import os
import customtkinter as ctk

class CreateProjectWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Project")
        self.window.geometry("300x275")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
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
            border_color="#b59630"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_project(self):
        project_name=self.projectNameEntry.get().strip()
        project_host_address=self.projectHostAddressEntry.get().strip()
        project_directory=self.projectDirectoryEntry.get().strip()
        
        # Create project folders and database
        print("Project name:", project_name)
        print("Project directory:", project_directory) #TODO creates folders in wrong location
        if create_project_db(project_name, project_host_address, project_directory):
            create_project_fd(project_name)
        else:
            print(f"Error: Project creation failed, database already exists for {project_name}")
            return

        # Install Blender libraries
        blender_executable_path = WoodyInstance().blenderExecutable.strip()
        if blender_executable_path:
            print("Installing required libraries into Blender...")
            if install_blender_libraries(blender_executable_path):
                print("Blender libraries installed successfully!")
            else:
                print("Warning: Library installation failed")
        
        # Copy prefs to addon
        copy_prefs_to_addon()  #TODO remove
        
        print(f"Project '{self.projectNameEntry.get()}' created successfully!")
        self.window.destroy()
    
    def create_widgets(self):
        
        # Preferences label
        self.preferancesLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Project",
            **style.HEADER_LABEL
        )
        self.preferancesLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 
        

        # Project name label
        self.projectNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Project Name",
            **style.BODY_LABEL
        )
        self.projectNameLabel.grid(row=2, column=0, sticky="nw", padx=8)

        # Project name entry
        self.projectNameEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.projectNameEntry.grid(row=3, column=0, sticky="new", padx=8, columnspan=2)
        
        # Project host address label
        self.projectHostAddressLabel = ctk.CTkLabel(
            self.frame, 
            text="Host Address",
            **style.BODY_LABEL
        )
        self.projectHostAddressLabel.grid(row=4, column=0, sticky="nw", padx=8)

        # Project host address entry
        self.projectHostAddressEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.projectHostAddressEntry.grid(row=5, column=0, sticky="new", padx=8, columnspan=2)
        
        # Project directory label
        self.projectDirectoryLabel = ctk.CTkLabel(
            self.frame, 
            text="Project Directory",
            **style.BODY_LABEL
        )
        self.projectDirectoryLabel.grid(row=6, column=0, sticky="nw", padx=8)

        # Project name entry
        self.projectDirectoryEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.projectDirectoryEntry.grid(row=7, column=0, sticky="new", padx=8, columnspan=2)
        
        # Create project button
        self.createProjectButton = ctk.CTkButton(
            self.frame,
            text="Create Project",
            **style.BUTTON_STYLE,
            
            command=self.create_project
        )
        self.createProjectButton.grid(row=8, column=0, sticky="nwe", padx=8, pady=8)
    
    def run(self):
        self.window.wait_window()