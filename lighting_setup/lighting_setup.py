import bpy
import os

from ..naming_convetions import *

original_world = None
world_name = "SpinWiz_Wrld"


def import_world():
    blender_file_path = os.path.join(os.path.dirname(__file__), '../blender_resources/SpinWiz_Master.blend')
    
    directory = blender_file_path + "/World/"
    
    bpy.ops.wm.append(
        filepath = directory + world_name,
        directory = directory,
        filename = world_name,
        link = False,
        autoselect = False
    )
    global original_world
    original_world = bpy.context.scene.world.name

    bpy.context.scene.world = bpy.data.worlds[world_name]

def reset_world():
    if original_world is None:
        bpy.context.scene.world = None
    else:
        bpy.context.scene.world = bpy.data.worlds[original_world]

    world = bpy.data.worlds[world_name]
    bpy.data.worlds.remove(world)
    
