
import bpy

class VIEW3D_PT_context(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_woody_context"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Woody Pipeline"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout
        
        # Woody Tools Section
        rootBox = layout.box()
        rootBox.label(text="Woody Tools", icon="OUTLINER")
        rootBox.scale_y = 0.75
        
        # Add Version Up button
        row = rootBox.row()
        row.operator("woody.version_up", text="Version Up", icon="FILE_REFRESH")
        #Add Publish button
        row = rootBox.row()
        row.operator("woody.publish", text="Publish", icon="FILE_REFRESH")
        
        # Load Publishes Section
        layout.separator()
        loadBox = layout.box()
        loadBox.label(text="Load Publishes", icon="LINK_BLEND")
        
        # Publish ID input field (clipboard format)
        row = loadBox.row()
        row.prop(context.scene, "woody_publish_id", text="Publish ID#ver:version")
        
        # Load button
        row = loadBox.row()
        row.operator("woody.load_publish", text="Load Publish", icon="LIBRARY_DATA_DIRECT")
        
        # Loaded publishes info
        layout.separator()
        infoBox = layout.box()
        infoBox.label(text="Scene Publishes", icon="OUTLINER_COLLECTION")
        
        # Show count of loaded publishes
        loaded_count = getattr(context.scene, 'woody_loaded_publishes_count', 0)
        row = infoBox.row()
        row.label(text=f"Total: {loaded_count} published assets")
        
        # Show list of loaded publishes separated by status
        loaded_publishes_data = getattr(context.scene, 'woody_loaded_publishes_data', '[]')
        if loaded_count > 0:
            import json
            try:
                publishes = json.loads(loaded_publishes_data)
                
                # Separate into linked and overridden
                linked_publishes = [pub for pub in publishes if pub.get('override_status') == 'linked']
                overridden_publishes = [pub for pub in publishes if pub.get('override_status') == 'overridden']
                
                # Linked Section
                if linked_publishes:
                    infoBox.separator()
                    linkedBox = infoBox.box()
                    linkedBox.label(text=f"Linked: ({len(linked_publishes)})", icon="LINKED")
                    
                    for pub in linked_publishes:
                        row = linkedBox.row()
                        # Display name without status icon since section is clear
                        row.label(text=pub['display_name'])
                        
                        # Only show override button for asset types that support overrides
                        # Materials and Node Groups can't be meaningfully overridden
                        publish_type = pub.get('publish_type', 'UNKNOWN').upper()
                        if publish_type not in ['MATERIAL', 'NODE_GROUP']:
                            # Override button
                            override_btn = row.operator("woody.override_publish", text="Override", icon="UNLOCKED")
                            override_btn.library_path = pub['library_path']
                        else:
                            # Show info icon for non-overrideable types
                            row.label(text="", icon="INFO")
                        
                        # Delete button for all types
                        delete_btn = row.operator("woody.delete_publish", text="Delete", icon="TRASH")
                        delete_btn.library_path = pub['library_path']
                
                # Overridden Section
                if overridden_publishes:
                    infoBox.separator()
                    overriddenBox = infoBox.box()
                    overriddenBox.label(text=f"Overridden: ({len(overridden_publishes)})", icon="LIBRARY_DATA_OVERRIDE")
                    
                    for pub in overridden_publishes:
                        row = overriddenBox.row()
                        # Display name without status icon since section is clear
                        row.label(text=pub['display_name'])
                        # Show overridden status (no override button needed since already overridden)
                        row.label(text="", icon="LOCKED")
                        # Delete button for overridden items too
                        delete_btn = row.operator("woody.delete_publish", text="Delete", icon="TRASH")
                        delete_btn.library_path = pub['library_path']
                
            except (json.JSONDecodeError, KeyError) as e:
                # Fallback to simple display if JSON parsing fails
                display_text = getattr(context.scene, 'woody_loaded_publishes_display', "No published assets loaded")
                for line in display_text.split('\n'):
                    if line.strip():
                        row = infoBox.row()
                        row.label(text=f"  • {line}", icon="LINKED")
        else:
            row = infoBox.row()
            row.label(text="No published assets loaded")
        
        # Refresh button
        infoBox.separator()
        row = infoBox.row()
        row.operator("woody.refresh_loaded_publishes", text="Refresh List", icon="FILE_REFRESH")