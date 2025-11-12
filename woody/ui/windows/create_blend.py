from .. import style
from ...lib.mongodb import create_blend_db
from ...plugins.blender.blender_instance import BlenderInstance
from ...tool.woody_instance import WoodyInstance

import re
import os
import customtkinter as ctk

class CreateBlendWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Blender Scene")
        self.window.geometry("300x170")
        
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
            border_color="#e97824"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
        # Make entry unavalible if no element is selected
        woody = WoodyInstance().browser_selection()
        
        if not woody or not woody.get("element"):
            self.blendNameEntry.delete(0, "end")
            self.blendNameEntry.insert(0, "Please select an element in browser")
            self.blendNameEntry.configure(
                state="disabled",
                **style.BODY_DANGER
            )
            self.createBlendButton.configure(state="disabled")

    def _create_blend_file(self):
        
        woody = WoodyInstance().browser_selection()
        group_type_selection = woody.get("group_type")
        group_selection = woody.get("group")
        element_selection = woody.get("element")
        
        blend_name = self.blendNameEntry.get().strip()
        # Validate blend name - prevent _latest and _v* patterns
        if self._is_invalid_blend_name(blend_name):
            print(
                "Invalid Name", 
                "Blend name cannot contain '_latest' or version suffixes like '_v1', '_v2', etc.\n"
                "These suffixes are reserved for the versioning system."
            )
            return
        
        # Append _latest to the blend name for file creation
        blend_name_with_latest = f"{blend_name}_latest.blend"
        group_type = "assets" if group_type_selection == "Assets Group" else "shots"
        
        # Try to create the database entry first
        if create_blend_db(group_type, group_selection, element_selection, blend_name):
            # Only create the file if database entry was successful
            success = self.blender.create_file(
                group_type,
                group_selection,
                element_selection,
                blend_name_with_latest
            )
            
            if success:
                print(f"Blend file created successfully: {blend_name_with_latest}")
            else:
                print("Failed to create blend file")
        else:
            print("Failed to create database entry - blend file not created")
       
    def _is_invalid_blend_name(self, name: str) -> bool:
        """Check if blend name contains reserved suffixes"""
        if "_latest" in name:
            return True
        if re.search(r"_v\d+", name):
            return True
        return False
        
    def create_widgets(self):
        
        # Project label
        self.projectLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Blender Scene",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 

        # Blend name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Blend File Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=2, column=0, sticky="nw", padx=8)
        
        # Blend Name
        self.blendNameEntry = ctk.CTkEntry(
            self.frame,
            height=25    
        )
        self.blendNameEntry.grid(row=3, column=0, sticky="new", padx=8)

        # Add Blender buttons
        self.createBlendButton = ctk.CTkButton(
            self.frame,
            text="Create Blend File",
            **style.BUTTON_STYLE,
            command=self._create_blend_file
        )
        self.createBlendButton.grid(row=4, sticky="nwe", padx=8, pady=8)

    def run(self):
        self.window.wait_window()