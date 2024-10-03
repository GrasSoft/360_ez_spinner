import bpy

from ..naming_convetions import *

from ..helper_functions import *

from ..properties import  SpinWiz_collection_properties, SpinWiz_properties
 

def create_action():
    # Create a new action
    action = bpy.data.actions.new(name=action_name)

    collection = get_current_collection()
    collection["action"] = action.name
    
    add_keyframes()

def create_pivot(collection, name, location):
    # Create an empty object
    bpy.ops.object.empty_add(location= location)  # You can adjust the location as needed
    empty_obj = bpy.context.object

    empty_obj.name = name

    for col in empty_obj.users_collection:
        col.objects.unlink(empty_obj)  
    

    collection.objects.link(empty_obj)

    return empty_obj


def duplicate_object_with_hierarchy(obj, parent=None, collection=None):
    # Duplicate the object
    duplicate_obj = obj.copy()
    duplicate_obj.location = Vector()
    duplicate_obj.data = obj.data.copy() if obj.data else None


    # Remove the new object from all collections it is currently part of
    # for col in duplicate_obj.users_collection:
    #     col.objects.unlink(duplicate_obj)  
    
    # Link the duplicate object to the collection
    collection.objects.link(duplicate_obj)

    # Preserve the transformation
    # duplicate_obj.location = obj.location
    # duplicate_obj.rotation_euler = obj.rotation_euler
    # duplicate_obj.scale = obj.scale
    
    # Set the parent for the duplicate object if provided
    if parent:
        duplicate_obj.parent = parent
        # Preserve the relative transformation to the parent
        # duplicate_obj.matrix_parent_inverse = obj.matrix_parent_inverse
    
    # Recursively duplicate children
    for child in obj.children:
        duplicate_object_with_hierarchy(child, parent=duplicate_obj, collection=collection)
    
    return duplicate_obj    

# create a new collection, copy the selected objects inside it and hide the rest of the scene objects  
def create_copy_and_hide():

    # Create a new collection for the copied objects
    new_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(new_collection)
    
    # add collection to collection list
    item = bpy.context.scene.collections_list.add()
    item.name = new_collection.name

    # Get selected objects without parents
    selected_objects = bpy.context.selected_objects
    selected_objects = [obj for obj in selected_objects if obj.parent is None]

    pivot = create_pivot(new_collection, pivot_object_name, get_collection_origin(bpy.context.selected_objects))
    
    # the pivot we look at is different than the pivot that holds the objects
    look_at_pivot = create_pivot(new_collection, pivot_track_name, get_collection_origin(bpy.context.selected_objects))

    for original_obj in selected_objects: 
        # Create a new object by copying the original
        duplicate_object_with_hierarchy(original_obj, parent=pivot, collection=new_collection) 
             
               
    hide_anything_but(new_collection)
                
    return new_collection



class OBJECT_OT_spin_wiz_setup(bpy.types.Operator):
    bl_idname = "object.spin_wiz_setup"
    bl_label = "Spin Wiz Setup"
    bl_description = "This operator creates the setup for Spin Wiz"

    def execute(self, context):
          
        context.scene.is_setting_up = True 
                
        context.scene.spin_settings.menu_options = "motion_setup"
        
        collection = create_copy_and_hide()
        
        # order matters
        setattr(bpy.types.Scene, get_current_collection().name, bpy.props.PointerProperty(type=SpinWiz_collection_properties))

        create_action()
        
        # use global settings
        # use_settings_of_other(collection_name)
        reset_default_settings()
        
        change_perspective()
        
        context.scene.is_setting_up = False

        return {"FINISHED"}

