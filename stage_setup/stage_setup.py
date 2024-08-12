import bpy
import os

from ..naming_convetions import *

stage_name = "SpinWiz_Stage"

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

    add_camera()
     

def link_stage_to_collection():
    object = bpy.data.objects[stage_name]

    for col in object.users_collection:
        col.objects.unlink(object)  

    bpy.context.scene.collection.children[collection_name].objects.link(object)   

def add_camera():
    object = bpy.data.objects[stage_name]

    modifier = object.modifiers.get("SpinWiz_StageCTRL")

    modifier.node_group.nodes["Object Info"].inputs[0].default_value = bpy.data.objects[camera_object_name]
    

def reset_stage():
    if bpy.data.objects[stage_name] is not None:
        bpy.data.objects.remove(bpy.data.objects[stage_name])

    