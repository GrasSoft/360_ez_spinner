import bpy
import subprocess

from ..naming_convetions import *

from .output import output_list

output_queue = []

def hide_render_others(name):
    # hide the objects first
    scene_collection = bpy.context.scene.collection
    for obj in bpy.context.scene.objects:
        # Get the collections that the object is in (excluding the scene collection)
        collections = [col for col in obj.users_collection if col != scene_collection]

        # If the object is only in the scene collection (no other collections), hide it from render
        if not collections:
            obj.hide_render = True

    # hide the other collections and make the current one visible

    for collection in bpy.data.collections:
        if collection.name != name:
            collection.hide_render = True
        else:
            collection.hide_render = False

def set_current_camera_as_render(name):
    collection = bpy.data.collections[name]

    for obj in collection.objects:
        if camera_object_name in obj.name:
            bpy.context.scene.camera = obj
            break

# unused
# def save_file():
#     # Define the command to run
#     blend_file = bpy.data.filepath  # Get the current blend file

#     if blend_file:
#         # Save the current .blend file
#         bpy.ops.wm.save_mainfile()
#     else:
#         # Save the current file under a new name
#         bpy.ops.wm.save_as_mainfile(filepath="/tmp/blender")

# unused
# def render_command(name):
#     global output_filepath
#     output_path = output_filepath + "/" + name + "/" + name + "_"
    
#     blend_file = bpy.data.filepath
    
#     file_format = "PNG"
#     render_command = [
#         bpy.app.binary_path,   # Path to Blender executable
#         "-b", blend_file,      # Background mode and input file
#         "-o", output_path,     # Output path
#         "-F", file_format,     # File format
#         "-x", "1",             # Use file extension
#         "-a"                   # Render animation
#     ]
    
#     return render_command


    # TODO, try to close the render window someday        
    # bpy.app.timers.register(shut_window, first_interval=2)

def shut_window():
    # Function to find and "close" the render window
    
    # Get the current screen
    screen = bpy.context.screen

    # Loop through each area in the screen
    # for area in screen.areas:
    #     # Check if the area is an image editor and is showing a render result
    #     if area.type == 'IMAGE_EDITOR' and area.spaces.active.mode == 'VIEW':
    #         # Override the context to close the area
    #         override = bpy.context.copy()
    #         override['area'] = area
    #         bpy.ops.screen.area_close(override)
    #         break  # Exit after closing the first found render editor
  
    # Iterate over all windows
    for window in bpy.context.window_manager.windows:
        # Iterate over all screen areas in the window
        for area in window.screen.areas:
            # Check if the area type is 'IMAGE_EDITOR'
            if area.type == 'IMAGE_EDITOR':
                # Access the area spaces
                # for space in area.spaces:
                #     # Check if the space is set to show the render result
                #     if space.type == 'IMAGE_EDITOR' and space.image and space.image.type == 'RENDER_RESULT':
                #         # Change area type to 'INFO' or any other area type to "close" the render window
                area.type = "VIEW_3D"
                        
                return
        
    return        

def enable_render_button(scene, ren):
    scene.spin_settings.enable_render = True
    bpy.app.handlers.render_complete.remove(enable_render_button)

def render(scene, rend):
    global output_filepath
    global output_queue
    
    print(output_queue)
    
    scene.spin_settings.current_rendered_collection = output_queue[0]
    
    # shut_window()
    # bpy.ops.render.view_cancel('INVOKE_DEFAULT')
            
    hide_render_others(output_queue[0])
    set_current_camera_as_render(output_queue[0])
    
    if len(output_queue) == 1:
        if render in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(render)
        bpy.app.handlers.render_complete.append(enable_render_button)
    
    output_path = output_filepath + "/" + output_queue[0] + "/" + output_queue[0] + "_"

    
    bpy.context.scene.render.image_settings.file_format = 'PNG'  # Output file format
    bpy.context.scene.render.filepath = output_path
    
    # remove after render, order matters
    output_queue.pop(0)
    
    # Perform the render
    bpy.ops.render.render("INVOKE_DEFAULT", write_still=True, animation=True)

def update_render_stats(scene):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':  # Choose the appropriate area type
                with bpy.context.temp_override(window=window,area=area):
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                return

class OBJECTE_OT_render(bpy.types.Operator):
    bl_idname = "object.render"
    bl_label = "Render the list"
    bl_description = "Render the list of output objects with the appropriate settings"    


    def execute(self, context):
        global output_list
        global output_queue
        
        output_queue = output_list.copy()
        
        # bpy.app.handlers.render_stats.append(update_render_stats)
        bpy.app.handlers.render_complete.append(render)
        # bpy.context.scene.spin_settings.enable_render = False
        render(context.scene, None)
            
        return {"FINISHED"}