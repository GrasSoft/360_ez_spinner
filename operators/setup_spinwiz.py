import bpy
from mathutils import Vector

from ..naming_convetions import *

from ..helper_functions import get_current_collection, add_keyframes, hide_anything_but, reset_default_settings, \
    get_collection_origin, set_active_collection, create_spinwiz_scene, get_spinwiz_scene

from ..properties import  SpinWiz_collection_properties

from ..lighting_setup.lighting_setup import import_world


def create_action(collection = None):
    # Create a new action
    action = bpy.data.actions.new(name=action_name)

    if collection is None:
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



def get_parent_chain(obj, parent_set=None):
    if parent_set is None:
        parent_set = set()
    
    # Check if the object has a parent
    if obj.parent and obj.parent not in parent_set:
        parent_set.add(obj.parent)
        # Recursively call this function for the parent
        get_parent_chain(obj.parent, parent_set)
    
    return parent_set


# create a new collection, copy the selected objects inside it and hide the rest of the scene objects  
def create_copy_and_hide():
    scene = get_spinwiz_scene()
    
    # Create a new collection for the copied objects
    new_collection = bpy.data.collections.new(collection_name + bpy.context.selected_objects[0].name)
    bpy.context.scene.collection.children.link(new_collection)  
    
    # add collection to collection list
    item = scene.spinwiz_collections_list.add()
    item.name = new_collection.name

    # Get selected objects without parents
    selected_objects = bpy.context.selected_objects
    all_parents = set(selected_objects)

    for obj in selected_objects:
        parent_chain = get_parent_chain(obj)
        all_parents.update(parent_chain)

    # Convert the set to a list if needed
    all_parents_list = list(all_parents)
        
    pivot = create_pivot(new_collection, pivot_object_name, (0, 0, 0))
    pivot.empty_display_type = "ARROWS"
    
    # the pivot we look at is different than the pivot that holds the objects
    look_at_pivot = create_pivot(new_collection, pivot_track_name,  get_collection_origin(all_parents_list)) 
    
    bpy.ops.object.select_all(action="DESELECT")
    
    # first select all objects we want to copy
    for obj in all_parents_list:
        obj.select_set(True)
        
    # this will copy all selected objects
    bpy.ops.object.duplicate()
    
    # get selected objects which are duplicated now
    copied_objects = bpy.context.selected_objects

    
    no_parent_obj = [obj for obj in copied_objects if obj.parent == None]

    collection_to_remove = [col for col in copied_objects[0].users_collection if col != new_collection][0]
    
    for obj in copied_objects:
        new_collection.objects.link(obj)
        collection_to_remove.objects.unlink(obj)
        
    # set the parent to the others     
    for obj in no_parent_obj:
        obj.parent = pivot
           
                                   
    return new_collection



class OBJECT_OT_spinwiz_setup(bpy.types.Operator):
    bl_idname = bl_idname_setup
    bl_label = "Spin Wiz Setup"
    bl_description = "This operator creates the setup for Spin Wiz"

    def execute(self, context):
        
        scene = create_spinwiz_scene()
        
     
          
        scene.spinwiz_is_setting_up = True
                
        scene.spinwiz_spin_settings.menu_options = "motion_setup"
        
        collection = create_copy_and_hide()
    
        # order matters
        setattr(bpy.types.Scene, collection.name, bpy.props.PointerProperty(type=SpinWiz_collection_properties))    

        create_action()
        
        import_world()
        
        # use global settings
        # use_settings_of_other(collection_name)
        reset_default_settings()
                
        # set_active_collection(collection)
        
        scene.collection.children.link(collection)
        
        context.scene.collection.children.unlink(collection)

        if len(scene.spinwiz_collections_list) == 1:
            scene.spinwiz_spin_settings.dropdown_collections = "NONE"
        
        # hide_anything_but(collection)
        
        scene.spinwiz_is_setting_up = False
        

        return {"FINISHED"}

