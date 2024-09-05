import bpy
import subprocess
import functools

from ..naming_convetions import *

from .output import output_list

output_queue = []

saved_window = None
saved_area = None
saved_screen = None

def hide_render_others(name, scene):

    # hide the objects first
    scene_collection = scene.collection
    for obj in scene.objects:
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

def set_current_camera_as_render(name, scene):

    collection = bpy.data.collections[name]

    for obj in collection.objects:
        if camera_object_name in obj.name:
            scene.camera = obj
            break
     

def enable_render_button(scene, ren):
    scene.spin_settings.enable_render = True
    bpy.app.handlers.render_complete.remove(enable_render_button)

# def render(idx, scene, rend):
#     global output_filepath
#     global output_queue
    
#     print(output_queue)
    
#     scene.spin_settings.current_rendered_collection = output_queue[0]
    
#     if len(output_queue) == 1:
#         if render in bpy.app.handlers.render_complete:
#             # TODO, FIX THIS< IT SHOULD REMOVE NOT POP< WE DONT KNOW WHAT IS IN THE QUEUE
#             bpy.app.handlers.render_complete.pop(0)
#         bpy.app.handlers.render_complete.append(enable_render_button)
    
#     output_path = output_filepath + "/" + output_queue[0] + "/" + output_queue[0] + "_"

    
#     scene.render.image_settings.file_format = 'PNG'  # Output file format
#     scene.render.filepath = output_path
    
#     window = bpy.context.window_manager.windows[idx]
#     screen = window.screen
    
#     views_3d = [a for a in screen.areas if a.type == 'VIEW_3D']
            
    
#     with bpy.context.temp_override(window=window , area=views_3d[0], screen=screen, scene=scene):
#         print(bpy.context.window)
        
#         hide_render_others(output_queue[0], scene)
#         set_current_camera_as_render(output_queue[0], scene)

#         # remove after render, order matters
#         output_queue.pop(0)

#         # Perform the render
#         bpy.ops.render.render("INVOKE_DEFAULT", animation=True, scene=scene.name)


class OBJECTE_OT_render(bpy.types.Operator):
    bl_idname = "object.render"
    bl_label = "Render the list"
    bl_description = "Render the list of output objects with the appropriate settings"    


    def execute(self, context):
        global output_list
        global output_queue
        
        output_queue = output_list.copy()
        
        # bpy.app.handlers.render_stats.append(update_render_stats)
        # bpy.context.scene.spin_settings.enable_render = False
        
        # idx = bpy.context.window_manager.windows[:].index(bpy.context.window)
        
        # bpy.app.handlers.render_complete.append(functools.partial(render, idx))
        
        # render(idx, context.scene, None)
        
        context.scene.use_nodes = True
        
        compositor_nodes = context.scene.node_tree.nodes
        compositor_links = context.scene.node_tree.links
                
        compositor_nodes.clear()
        compositor_links.clear()
        
        file_output_node = compositor_nodes.new(type='CompositorNodeOutputFile')
        
        index = 0
        for name in output_list:
            view_layer = context.scene.view_layers.new(name=name)
            hide_render_others(name, context.scene)
            set_current_camera_as_render(name, context.scene)
            
            render_layer = compositor_nodes.new(type="CompositorNodeRLayers")
            render_layer.layer = view_layer.name

            compositor_links.new(render_layer.outputs[0], file_output_node.inputs[index])
            
            file_output_node.file_slots.new("Image")
            
            index += 1 
                    
            
        return {"FINISHED"}