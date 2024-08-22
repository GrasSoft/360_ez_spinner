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

    link_stage_to_collection()

    set_origin()

    add_camera()
     

def link_stage_to_collection():
    object = None
    for obj in bpy.context.scene.objects:
        if len(obj.users_collection) == 1 and obj.users_collection[0] == bpy.context.scene.collection and stage_name in obj.name:
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
    if stage_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[stage_name])

#______________________________________________ PANEL FUNCTIONS 

def panel_stage_setup(panel, layout):
    spin_settings = bpy.context.scene.spin_settings

    add_stage = layout.box()
    add_stage.prop(spin_settings, "add_stage")

    if spin_settings.add_stage:
        add_stage.label(text="Stage Shape")
        add_stage.prop(spin_settings, "stage_height_offset", text="Stage Height")
        add_stage.prop(spin_settings, "stage_subdivision", text="Subdivisions")


        add_stage.separator()
        add_stage.label(text="Stage Material")

        node = bpy.data.materials["SpinWiz_Stage_Mtl"].node_tree.nodes["BackgroundShader"]

        add_stage.prop(node.inputs[1], "default_value")
        add_stage.prop(node.inputs[0], "default_value", text="Roughness")
        add_stage.prop(node.inputs[2], "default_value", text="Reflection Intensity") 
        add_stage.prop(node.inputs[3], "default_value", text="Contact Shadow")                           

        bpy.data.objects[stage_name].data.update()   