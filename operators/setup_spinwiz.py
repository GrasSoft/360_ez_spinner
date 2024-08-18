import bpy

from ..naming_convetions import *
from ..helper_functions import *
from ..properties import update_movement_type

from ..settings.current_settings import list_current_settings, previous_settings, update_properties

def create_action():
    # Create a new action
    bpy.data.actions.new(name=action_name)

    add_keyframes()

def create_pivot(collection):
    # Create an empty object
    bpy.ops.object.empty_add(location=(0, 0, 0))  # You can adjust the location as needed
    empty_obj = bpy.context.object

    empty_obj.name = pivot_object_name

    for col in empty_obj.users_collection:
        col.objects.unlink(empty_obj)  
    

    collection.objects.link(empty_obj)

    return empty_obj


def duplicate_object_with_hierarchy(obj, parent=None, collection=None):
    # Duplicate the object
    duplicate_obj = obj.copy()
    duplicate_obj.data = obj.data.copy() if obj.data else None


    # Remove the new object from all collections it is currently part of
    # for col in duplicate_obj.users_collection:
    #     col.objects.unlink(duplicate_obj)  
    
    # Link the duplicate object to the collection
    collection.objects.link(duplicate_obj)

    # Preserve the transformation
    duplicate_obj.location = obj.location
    duplicate_obj.rotation_euler = obj.rotation_euler
    duplicate_obj.scale = obj.scale
    
    # Set the parent for the duplicate object if provided
    if parent:
        duplicate_obj.parent = parent
        # Preserve the relative transformation to the parent
        duplicate_obj.matrix_parent_inverse = obj.matrix_parent_inverse
    
    # Recursively duplicate children
    for child in obj.children:
        print(child)
        duplicate_object_with_hierarchy(child, parent=duplicate_obj, collection=collection)
    
    return duplicate_obj    

# create a new collection, copy the selected objects inside it and hide the rest of the scene objects  
def create_copy_and_hide():

    # Create a new collection for the copied objects
    new_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(new_collection)

    # Get selected objects without parents
    selected_objects = bpy.context.selected_objects
    selected_objects = [obj for obj in selected_objects if obj.parent is None]

    pivot = create_pivot(new_collection)

    for original_obj in selected_objects: 
        # Create a new object by copying the original
        duplicate_object_with_hierarchy(original_obj, parent=pivot, collection=new_collection) 
               
    # Hide all collections except the new one
    for collection in bpy.context.scene.collection.children:
        if collection != new_collection:
            # Hide the collection in the active view layer
            for view_layer in bpy.context.scene.view_layers:
                layer_collection = view_layer.layer_collection.children.get(collection.name)
            
                if layer_collection:
                    layer_collection.hide_viewport = True
            collection.hide_render = True
       
       
    # Get the default "Scene Collection"
    scene_collection = bpy.context.scene.collection
   
    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
         # Check if the object is only in the "Scene Collection" and not in any other collections
        if len(obj.users_collection) == 1 and scene_collection in obj.users_collection:
            # Hide the object from the viewport using hide_set
            obj.hide_set(True)
            obj.hide_render = True
                
    return new_collection

def add_settings(name):
    list_current_settings[name] = previous_settings

class OBJECT_OT_spin_wiz_setup(bpy.types.Operator):
    bl_idname = "object.spin_wiz_setup"
    bl_label = "Spin Wiz Setup"
    bl_description = "This operator creates the setup for Spin Wiz"

    def execute(self, context):
        collection = create_copy_and_hide()
        
        add_settings(collection.name)
        
        create_action()

        update_properties()             

        return {"FINISHED"}

