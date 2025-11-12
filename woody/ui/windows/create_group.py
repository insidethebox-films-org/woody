from .. import style
from ...lib.folder import create_group_sequence_fd
from ...lib.mongodb import create_group_sequence_db
from ...tool.woody_instance import WoodyInstance

import os
import customtkinter as ctk

class CreateGroupWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Group")
        self.window.geometry("300x170")
        
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
            border_color="#b34555"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
        # Make entry unavalible if no group type is selected
        woody = WoodyInstance().browser_selection()
        
        if not woody or not woody.get("group_type"):
            self.groupNameEntry.delete(0, "end")
            self.groupNameEntry.insert(0, "Please select a group type in browser")
            self.groupNameEntry.configure(
                state="disabled",
                **style.BODY_DANGER
            )
            self.createGroupButton.configure(state="disabled")
    
    def create_group(self):
        
        woody = WoodyInstance().browser_selection()
        group_type = woody.get("group_type")
        
        create_group_sequence_fd(group_type, self.groupNameEntry.get())
        create_group_sequence_db(group_type, self.groupNameEntry.get())
        
    def create_widgets(self):
         
        # Create element label
        self.projectLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Group",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2)
        
        # Group name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Group Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=6, column=0, sticky="nw", padx=8)
        
        # Group Name
        self.groupNameEntry = ctk.CTkEntry(
            self.frame,
            height=25    
        )
        self.groupNameEntry.grid(row=7, column=0, sticky="new", padx=8)
        
        # Create Group button
        self.createGroupButton = ctk.CTkButton(
            self.frame,
            text="Create Group",
            **style.BUTTON_STYLE,
            
            command=self.create_group
        )
        self.createGroupButton.grid(row=8, sticky="nwe", padx=8, pady=8)
    
    def run(self):
        self.window.wait_window()