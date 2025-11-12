"""
Asset loading utilities for the Woody Blender addon.
Contains functions to load different types of assets from blend files.
"""

import bpy


def load_collections(blend_path: str, context):
    """
    Load collections from blend file.
    
    Args:
        blend_path: Path to the blend file
        context: Blender context
        
    Returns:
        List of linked collection names
    """
    linked_items = []
    
    with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
        if data_from.collections:
            data_to.collections = data_from.collections

    # Make library paths relative for cross-platform compatibility
    bpy.ops.file.make_paths_relative()

    for col in data_to.collections:
        if col:
            context.scene.collection.children.link(col)
            linked_items.append(col.name)
    
    return linked_items


def load_materials(blend_path: str, context):
    """
    Load materials from blend file.
    
    Args:
        blend_path: Path to the blend file
        context: Blender context
        
    Returns:
        List of linked material names
    """
    linked_items = []
    
    with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
        if data_from.materials:
            data_to.materials = data_from.materials

    # Make library paths relative for cross-platform compatibility
    bpy.ops.file.make_paths_relative()

    for mat in data_to.materials:
        if mat:
            linked_items.append(mat.name)
    
    return linked_items


def load_objects(blend_path: str, context):
    """
    Load objects from blend file.
    
    Args:
        blend_path: Path to the blend file
        context: Blender context
        
    Returns:
        List of linked object names
    """
    linked_items = []
    
    with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
        if data_from.objects:
            data_to.objects = data_from.objects

    # Make library paths relative for cross-platform compatibility
    bpy.ops.file.make_paths_relative()

    for obj in data_to.objects:
        if obj:
            context.scene.collection.objects.link(obj)
            linked_items.append(obj.name)
    
    return linked_items


def load_meshes(blend_path: str, context):
    """
    Load meshes from blend file.
    
    Args:
        blend_path: Path to the blend file
        context: Blender context
        
    Returns:
        List of linked mesh names
    """
    linked_items = []
    
    with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
        if data_from.meshes:
            data_to.meshes = data_from.meshes

    # Make library paths relative for cross-platform compatibility
    bpy.ops.file.make_paths_relative()

    for mesh in data_to.meshes:
        if mesh:
            linked_items.append(mesh.name)
    
    return linked_items


def load_node_groups(blend_path: str, context):
    """
    Load node groups from blend file.
    
    Args:
        blend_path: Path to the blend file
        context: Blender context
        
    Returns:
        List of linked node group names
    """
    linked_items = []
    
    with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
        if data_from.node_groups:
            data_to.node_groups = data_from.node_groups

    # Make library paths relative for cross-platform compatibility
    bpy.ops.file.make_paths_relative()

    for node_group in data_to.node_groups:
        if node_group:
            linked_items.append(node_group.name)
    
    return linked_items


def load_by_type(blend_path: str, publish_type: str, context):
    """
    Load assets based on their publish type.
    
    Args:
        blend_path: Path to the blend file
        publish_type: Type of asset to load (collection, material, object, mesh)
        context: Blender context
        
    Returns:
        List of linked asset names
    """
    linked_items = []
    
    if publish_type.upper() == "COLLECTION":
        linked_items = load_collections(blend_path, context)
    elif publish_type.upper() == "MATERIAL":
        linked_items = load_materials(blend_path, context)
    elif publish_type.upper() == "OBJECT":
        linked_items = load_objects(blend_path, context)
    elif publish_type.upper() == "MESH":
        linked_items = load_meshes(blend_path, context)
    elif publish_type.upper() == "NODE_GROUP" or publish_type.upper() == "NODEGROUP":
        linked_items = load_node_groups(blend_path, context)
    else:
        # Fallback: try to load collections first, then other types
        linked_items = load_collections(blend_path, context)
        if not linked_items:
            linked_items = load_materials(blend_path, context)
        if not linked_items:
            linked_items = load_objects(blend_path, context)
    
    return linked_items