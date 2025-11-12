from .. import style
from ...utils.format_date import format_date
from ...tool.woody_instance import WoodyInstance
from ...tool.event_bus import event_bus

import customtkinter as ctk

class AssetDetailsFrame:
    def __init__(self, parent):
        self.parent = parent
        self.detail_widgets = []
        
        self.create_frame()
        self.create_widgets()
        
        event_bus.subscribe('browser_selection_changed', self.get_asset_details)
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
        )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        
    def get_asset_details(self, new_browser_selection):
        
        if not new_browser_selection:
            print("asset_details: Received None selection")
            return
        
        if not new_browser_selection.get("group"):
            self.title_label.configure(text="Select an item")
            
            for widget in self.asset_details_frame.winfo_children():
                widget.destroy()
            return
        
        asset_details = WoodyInstance().asset_details()
        
        if not asset_details:
            print("asset_details: No asset details available")
            return
        
        # Update title
        if new_browser_selection.get("group_type") == "Assets Group":
            root = "assets"
            group = new_browser_selection.get("group")
        else:
            root = "shots"
            group = new_browser_selection.get("group")
        
        name = new_browser_selection.get("element")
        path = f"{root}/{group}/{name}" if group and name else f"{root}/{group}"
        self.title_label.configure(text=path)
              
        # Dynamic detail fields create
        for widget in self.asset_details_frame.winfo_children():
            widget.destroy()
        
        exclude_fields = ["_id", "assets", "shots"]
        
        current_row = 0
        
        for key, value in asset_details.items():
            if key in exclude_fields:
                continue
            
            field_frame = ctk.CTkFrame(
                self.asset_details_frame,
                corner_radius=5,
                fg_color="#252525",
                height=40
            )
            field_frame.grid(row=current_row, pady=(0,3), sticky="ew")
            field_frame.grid_columnconfigure(1, weight=1)
            field_frame.grid_rowconfigure(0, weight=1)
            field_frame.grid_propagate(False)
            
            label = ctk.CTkLabel(
                field_frame,
                text=f"{key.replace('_', ' ').title()}:",
                width=120,
                anchor="w",
                **style.BODY_LABEL
            )
            label.grid(row=0, column=0, padx=(12, 5), sticky="w")
            
            display_value = format_date(key, value)
            
            entry = ctk.CTkEntry(
                field_frame,
                placeholder_text=display_value if display_value else "None",
                fg_color="#1F1F1F",
                border_width=0
            )
            entry.insert(0, display_value)
            entry.grid(row=0, column=1, padx=(5, 12), sticky="ew")
            entry.configure(state="readonly")
            
            current_row += 1

    def create_widgets(self):
        
        # Header
        self.header_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.header_frame.grid(row=0, pady=(7, 3), padx=7, sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Details:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, pady=7, padx=12, sticky="w")
        
        # Title
        self.title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.title_frame.grid(row=1, padx=7, pady=(0, 3), sticky="ew")
        self.title_frame.grid_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Select an item",
            **style.SUB_HEADER_LABEL
        )
        self.title_label.grid(row=0, padx=12, sticky="w")
        
        # Dynamic asset details frame
        self.asset_details_frame = ctk.CTkScrollableFrame(
            self.frame,
            corner_radius=5,
            fg_color="transparent",      
            border_width=2,
            
        )
        self.asset_details_frame.grid(row=2, padx=7, pady=(3,7), sticky="nsew")
        self.asset_details_frame.grid_columnconfigure(0, weight=1)
        self.asset_details_frame._scrollbar.grid(padx=(0, 3), pady=3)