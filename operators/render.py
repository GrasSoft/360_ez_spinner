import bpy
import subprocess

from ..naming_convetions import *

from .output import output_list

def hide_render_others(name):
    for collection in bpy.data.collections:
        if collection.name != name:
            collection.hide_render = True
        else:
            collection.hide_render = False

def set_current_camera_as_render(name):
    collection = bpy.data.collections[name]

    for obj in collection.objects:
        if camera_object_name in obj.name:
            print("Nigger")
            bpy.context.scene.camera = obj
            break

def run_subprocess(name):
    # Define the command to run
    blend_file = bpy.data.filepath  # Get the current blend file

    if blend_file:
        # Save the current .blend file
        bpy.ops.wm.save_mainfile()
    else:
        # Save the current file under a new name
        bpy.ops.wm.save_as_mainfile()

    output_path = "/tmp/" + name + "/" + name + "_"
    file_format = "PNG"
    render_command = [
        bpy.app.binary_path,   # Path to Blender executable
        "-b", blend_file,      # Background mode and input file
        "-o", output_path,     # Output path
        "-F", file_format,     # File format
        "-x", "1",             # Use file extension
        "-a"                   # Render animation
    ]

    try:
        # Run the command in the background
        subprocess.Popen(render_command)
        print({'INFO'}, "Render command is running in the background.")
    except Exception as e:
        print({'ERROR'}, f"Failed to start subprocess")

class OBJECTE_OT_render(bpy.types.Operator):
    bl_idname = "object.render"
    bl_label = "Render the list"
    bl_description = "Render the list of output objects with the appropriate settings"    


    def execute(self, context):
       global output_list
       print(output_list)
       for collection_name in output_list:
           hide_render_others(collection_name)
           set_current_camera_as_render(collection_name)
           run_subprocess(collection_name)

       return {"FINISHED"}