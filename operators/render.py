import bpy
import subprocess
import functools

from ..naming_convetions import *


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



def create_view_layers(context):
    output_list = bpy.data.scenes[0].output_list
 
    context.scene.use_nodes = True
        
    compositor_nodes = context.scene.node_tree.nodes
    compositor_links = context.scene.node_tree.links

    # clear existing nodes            
    compositor_nodes.clear()
    compositor_links.clear()

    
    # for every item in output_list, create a view_layer where only the objects that is visible in render is the current one     
    for index, name in enumerate(output_list):

        file_output_node = compositor_nodes.new(type='CompositorNodeOutputFile')
    
        global output_filepath
        file_output_node.base_path = output_filepath + "/" + name

        view_layer = context.scene.view_layers.new(name=name)
        hide_render_others(name, context.scene)
        set_current_camera_as_render(name, context.scene)
        
        render_layer = compositor_nodes.new(type="CompositorNodeRLayers")
        render_layer.layer = view_layer.name

        compositor_links.new(render_layer.outputs[0], file_output_node.inputs[0])

            
            

class OBJECTE_OT_render(bpy.types.Operator):
    bl_idname = "object.render"
    bl_label = "Render the list"
    bl_description = "Render the list of output objects with the appropriate settings"    


    def execute(self, context):
        
        create_view_layers(context)
        
        # disable the render button until the render ends
        context.scene.spin_settings.enable_render = False
        
        bpy.app.handlers.render_complete.append(enable_render_button)
                    
        bpy.ops.render.render("INVOKE_DEFAULT", animation=True)
            
        return {"FINISHED"}