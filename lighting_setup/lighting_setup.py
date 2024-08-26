import bpy
import os

from ..naming_convetions import *

from ..helper_functions import *

original_world = None
world_name = "SpinWiz_Wrld"

#_____________________________ HELPER FUNCTIONS
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
    
    if bpy.context.scene.world is not None:
        original_world = bpy.context.scene.world.name

    bpy.context.scene.world = bpy.data.worlds[world_name]

def reset_world():
    if original_world is None:
        bpy.context.scene.world = None
    else:
        bpy.context.scene.world = bpy.data.worlds[original_world]

    if world_name in bpy.data.worlds:
        world = bpy.data.worlds[world_name]
        bpy.data.worlds.remove(world)


def load_thumbnail_lighting():
    image_path = os.path.join(os.path.dirname(__file__), '../lighting_setup/thumbnails/studio_small_09.png')
    image = bpy.data.images.load(image_path)
    return image

#___________________________ PANEL FUNCTIONS

def panel_lighting_setup(panel, layout):
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
     
    ligthing_setup_box = layout.box()
    ligthing_setup_box.prop(spin_settings, "add_lighting_setup")           
    
    image = bpy.data.images.get("studio_small_09.png") or load_thumbnail_lighting()

    if spin_settings.add_lighting_setup:
        # thumbnail of the world used
        if image:           
            # Use template_ID to display the image data block
            ligthing_setup_box.template_preview(bpy.context.scene.world)

        ligthing_setup_box.label(text=bpy.context.scene.world.name)

        ligthing_setup_box.prop(bpy.data.worlds[world_name].node_tree.nodes["Mapping"].inputs[2], "default_value", index=2, text="Rotation")

        ligthing_setup_box.prop(bpy.data.worlds[world_name].node_tree.nodes["Background"].inputs[1], "default_value", text="Strength")
