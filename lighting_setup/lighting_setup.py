import bpy
import os

from ..naming_convetions import *

from ..helper_functions import *

original_world = None
world_name = "SpinWiz_Wrld"

#_____________________________ HELPER FUNCTIONS
def import_world(collection = None):
    blender_file_path = os.path.join(os.path.dirname(__file__), '../blender_resources/SpinWiz_Master.blend')
    
    # List of objects before appending
    objects_before = set(bpy.data.worlds)
    
    directory = blender_file_path + "/World/"
    # TODO, this does not return anything, on setup just add a world for each object and set it as the default world when selected or not 
    bpy.ops.wm.append(
        filepath = directory + world_name,
        directory = directory,
        filename = world_name,
        link = False,
        autoselect = False
    )
    
    # get appended world by checking the difference between the 2 lists
    current_world = (list(set(bpy.data.worlds) - objects_before))[0]
    
    if collection is None:
        collection = get_current_collection()
    
    if bpy.context.scene.world is not None:
        collection["original_world"] = bpy.context.scene.world.name

    bpy.context.scene.world = current_world
    collection["current_world"] = current_world.name
    
def apply_world():
    world = get_current_world()
    bpy.context.scene.world = world

def reset_world():
    original_world = get_original_world()
    
    if original_world is None:
        bpy.context.scene.world = None
    else:
        bpy.context.scene.world = original_world


#___________________________ PANEL FUNCTIONS

def panel_lighting_setup(panel, layout):

    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
     
    ligthing_setup_box = layout.box()
    ligthing_setup_box.prop(spin_settings, "add_lighting_setup")           
    
    if spin_settings.add_lighting_setup:
                
        world = get_current_world()

        ligthing_setup_box.template_icon_view(spin_settings, "lighting_type", show_labels=True)

        ligthing_setup_box.label(text=bpy.context.scene.world.name)
        
        nodes = world.node_tree.nodes
        
        if spin_settings.lighting_type == "HDR":

            ligthing_setup_box.prop(spin_settings, "lighting_hdr_rotation", text="Rotation")

            ligthing_setup_box.prop(spin_settings, "lighting_hdr_strength", text="Strength")
        else:
            
            ligthing_setup_box.prop(spin_settings, "lighting_gradient_height", text="Gradient Height")
            
            ligthing_setup_box.prop(spin_settings, "lighting_gradient_scale", text="Gradient Scale")