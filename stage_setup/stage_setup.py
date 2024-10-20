import bpy
import os

from ..naming_convetions import *
from ..helper_functions import *


#_____________________________________________________ HELPER FUNCTIONS

def import_stage():
    blender_file_path = os.path.join(os.path.dirname(__file__), '../blender_resources/SpinWiz_Master.blend')
    
    directory = blender_file_path + "/Object/"
    
    bpy.ops.wm.append(
        filepath = directory + stage_name,
        directory = directory,
        filename = stage_name,
        link = False,
        autoselect = False
    )

    # link_stage_to_collection()

    set_origin()

    add_camera()

     

def link_stage_to_collection():
    object = None
    for obj in get_spinwiz_scene().objects:
        if len(obj.users_collection) == 1 and obj.users_collection[0] == get_spinwiz_scene().collection and stage_name in obj.name:
            object = obj
            break

    for col in object.users_collection:
        col.objects.unlink(object)  

    get_current_collection().objects.link(object)   

def add_camera():
    object = get_current_stage() 

    modifier = object.modifiers.get("SpinWiz_StageCTRL")

    modifier.node_group.nodes["Object Info"].inputs[0].default_value = get_current_camera()

def set_origin():
    (min_corner, _) = get_collection_bounding_box(get_current_pivot())
    
    stage = get_current_stage()
    stage.location.z = min_corner[2]

def reset_stage():
    stage =  get_current_stage()
    if stage is not None:
        bpy.data.objects.remove(stage)

#______________________________________________ PANEL FUNCTIONS 

def panel_stage_setup(panel, layout):
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)

    add_stage = layout

    if spin_settings.add_stage:
        add_stage.label(text="Stage Shape")
        add_stage.prop(spin_settings, "stage_height_offset", text="Stage Height")
        add_stage.prop(spin_settings, "stage_subdivision", text="Subdivisions")


        add_stage.separator()
        add_stage.label(text="Stage Material")

        add_stage.prop(spin_settings, "stage_material_color")
        add_stage.prop(spin_settings, "stage_material_roughness", text="Roughness")
        add_stage.prop(spin_settings, "stage_material_reflection_intensity", text="Reflection Intensity") 
        add_stage.prop(spin_settings, "stage_material_contact_shadow", text="Contact Shadow")                           

