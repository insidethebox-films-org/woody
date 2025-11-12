import bpy
from pathlib import Path

class ElementGatherer:
    """Handles gathering of different asset types and their dependencies"""

    def get_collections_list(self):
        """Get list of collections in the scene"""
        try:
            items = []
            for col in bpy.data.collections:
                # Skip the default "Collection" if it's empty or you don't want it
                if col.name == "Collection" and len(col.objects) == 0:
                    continue
                    
                # Format: (identifier, name, description)
                items.append((
                    col.name,  # identifier (what gets stored)
                    col.name,  # display name
                    f"{len(col.objects)} objects"  # description
                ))
            
            # Always return at least one item to prevent enum errors
            if not items:
                return [("NONE", "No collections", "Create a collection first")]
                
            return items
            
        except Exception as e:
            print(f"Error getting collections: {e}")
            return [("ERROR", "Error loading collections", str(e))]

    def get_materials_list(self):
        """Get list of materials in the scene"""
        try:
            items = []
            for mat in bpy.data.materials:
                items.append((
                    mat.name,  # identifier
                    mat.name,  # display name
                    f"Material: {mat.name}"  # description
                ))
            
            if not items:
                return [("NONE", "No materials", "Create a material first")]
                
            return items
            
        except Exception as e:
            print(f"Error getting materials: {e}")
            return [("ERROR", "Error loading materials", str(e))]

    def get_meshes_list(self):
        """Get list of meshes in the scene"""
        try:
            items = []
            for mesh in bpy.data.meshes:
                items.append((
                    mesh.name,  # identifier
                    mesh.name,  # display name
                    f"Mesh: {mesh.name} ({len(mesh.vertices)} verts)"  # description
                ))
            
            if not items:
                return [("NONE", "No meshes", "Create a mesh first")]
                
            return items
            
        except Exception as e:
            print(f"Error getting meshes: {e}")
            return [("ERROR", "Error loading meshes", str(e))]

    def get_node_groups_list(self):
        """Get list of node groups in the scene"""
        try:
            items = []
            for ng in bpy.data.node_groups:
                ng_type = "Geometry" if ng.type == 'GEOMETRY' else "Shader" if ng.type == 'SHADER' else "Other"
                items.append((
                    ng.name,  # identifier
                    ng.name,  # display name
                    f"{ng_type} Node Group: {ng.name}"  # description
                ))
            
            if not items:
                return [("NONE", "No node groups", "Create a node group first")]
                
            return items
            
        except Exception as e:
            print(f"Error getting node groups: {e}")
            return [("ERROR", "Error loading node groups", str(e))]

    def get_objects_list(self):
        """Get list of objects in the scene"""
        try:
            items = []
            for obj in bpy.data.objects:
                items.append((
                    obj.name,  # identifier
                    obj.name,  # display name
                    f"{obj.type}: {obj.name}"  # description
                ))
            
            if not items:
                return [("NONE", "No objects", "Create an object first")]
                
            return items
            
        except Exception as e:
            print(f"Error getting objects: {e}")
            return [("ERROR", "Error loading objects", str(e))]

    def create_published_asset(self, publish_type: str, selected_item: str, output_path: Path) -> bool:
        """Create published asset based on selected type"""
        try:
            datablocks = set()
            
            if publish_type == 'COLLECTION':
                success, blocks = self.gather_collection_data(selected_item)
            elif publish_type == 'MATERIAL':
                success, blocks = self.gather_material_data(selected_item)
            elif publish_type == 'MESH':
                success, blocks = self.gather_mesh_data(selected_item)
            elif publish_type == 'NODE_GROUP':
                success, blocks = self.gather_node_group_data(selected_item)
            elif publish_type == 'OBJECT':
                success, blocks = self.gather_object_data(selected_item)
            else:
                return False
                
            if not success:
                return False
                
            datablocks.update(blocks)

            # Write the blend file
            bpy.data.libraries.write(
                str(output_path),
                datablocks,
                fake_user=True,
                compress=True
            )
            
            print(f"✅ Published {publish_type}: {len(datablocks)} data blocks")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create published asset: {e}")
            return False

    def gather_collection_data(self, collection_name: str):
        """Gather all data from a collection"""
        try:
            if collection_name not in bpy.data.collections:
                print(f"Collection '{collection_name}' not found")
                return False, set()
            
            collection = bpy.data.collections[collection_name]
            datablocks = {collection}
            
            # Add all objects in the collection
            for obj in collection.objects:
                datablocks.add(obj)
                
                # Add object data (mesh, curve, etc.)
                if obj.data:
                    datablocks.add(obj.data)
                    
                # Add materials
                if hasattr(obj.data, 'materials') and obj.data.materials:
                    for mat in obj.data.materials:
                        if mat:
                            datablocks.add(mat)
            
            return True, datablocks
            
        except Exception as e:
            print(f"Error gathering collection data: {e}")
            return False, set()

    def gather_material_data(self, material_name: str):
        """Gather material and its dependencies"""
        try:
            if material_name not in bpy.data.materials:
                print(f"Material '{material_name}' not found")
                return False, set()
            
            material = bpy.data.materials[material_name]
            datablocks = {material}
            
            # Add node groups and textures if material uses nodes
            if material.use_nodes and material.node_tree:
                datablocks.add(material.node_tree)
                
                for node in material.node_tree.nodes:
                    if hasattr(node, 'node_tree') and node.node_tree:
                        datablocks.add(node.node_tree)
                    if hasattr(node, 'image') and node.image:
                        datablocks.add(node.image)
            
            return True, datablocks
            
        except Exception as e:
            print(f"Error gathering material data: {e}")
            return False, set()

    def gather_mesh_data(self, mesh_name: str):
        """Gather mesh data"""
        try:
            if mesh_name not in bpy.data.meshes:
                print(f"Mesh '{mesh_name}' not found")
                return False, set()
            
            mesh = bpy.data.meshes[mesh_name]
            datablocks = {mesh}
            
            # Add materials used by the mesh
            if mesh.materials:
                for mat in mesh.materials:
                    if mat:
                        datablocks.add(mat)
            
            return True, datablocks
            
        except Exception as e:
            print(f"Error gathering mesh data: {e}")
            return False, set()

    def gather_node_group_data(self, node_group_name: str):
        """Gather node group data"""
        try:
            if node_group_name not in bpy.data.node_groups:
                print(f"Node group '{node_group_name}' not found")
                return False, set()
            
            node_group = bpy.data.node_groups[node_group_name]
            datablocks = {node_group}
            
            return True, datablocks
            
        except Exception as e:
            print(f"Error gathering node group data: {e}")
            return False, set()

    def gather_object_data(self, object_name: str):
        """Gather single object data"""
        try:
            if object_name not in bpy.data.objects:
                print(f"Object '{object_name}' not found")
                return False, set()
            
            obj = bpy.data.objects[object_name]
            datablocks = {obj}
            
            # Add object data
            if obj.data:
                datablocks.add(obj.data)
                
            # Add materials
            if hasattr(obj.data, 'materials') and obj.data.materials:
                for mat in obj.data.materials:
                    if mat:
                        datablocks.add(mat)
            
            return True, datablocks
            
        except Exception as e:
            print(f"Error gathering object data: {e}")
            return False, set()