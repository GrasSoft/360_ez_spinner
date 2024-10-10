import bpy
import subprocess
import functools

from ..naming_convetions import *
from ..helper_functions import hide_anything_but, update_scene_frame, update_current_world, update_current_stage


def hide_render_others(name, scene):

    # hide them in the view port
    hide_anything_but(bpy.data.collections[name])

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
            bpy.context.scene.camera = obj
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            break
     

def enable_render_button(scene):
    # renable render button
    scene.spinwiz_spin_settings.enable_render = True
    scene.spinwiz_spin_settings.is_rendering = False

    
def make_all_objects_not_selectable():
    for obj in bpy.data.objects:
        obj.hide_select = True

def make_all_objects_selectable(not_selectable):
    for obj in bpy.data.objects:
        if obj not in not_selectable:
            obj.hide_select = False
        
def get_not_selectable_objects():
    not_selectable_objects = [obj for obj in bpy.data.objects if obj.hide_select]
    return not_selectable_objects

class OBJECTE_OT_spinwiz_render(bpy.types.Operator):
    bl_idname = bl_idname_render
    bl_label = "Render the list"
    bl_description = "Render the list of output objects with the appropriate settings"   
    
    rendering = False
    render_queue = []
    _timer = None
    stop = False
    
    not_selectable = None
    
    initial_selection = None
    initial_active = None
    
    def restore_initial_selection(self):
        # Loop through all objects in the scene and deselect them
        for obj in bpy.data.objects:
            obj.select_set(False)
        
        for obj in self.initial_selection:
            obj.select_set(True)
            
        bpy.context.view_layer.objects.active = self.initial_active
    
    def render_cancel(self, dummy, thrd):
        self.stop = True
    
    def render_pre(self, dummy, thrd):
        self.rendering = True
        
    def render_post(self, dummy, thrd):
        scene = bpy.context.scene
        
        if scene.frame_current == scene.frame_end:
            self.rendering = False
        
    def modal(self, context, event):
        scene = context.scene
        
        if event.type == "ESC":
            # remove the timer
            bpy.context.window_manager.event_timer_remove(self._timer)
        
            # remove the handlers
            bpy.app.handlers.render_pre.remove(self.render_pre)
            bpy.app.handlers.render_post.remove(self.render_post)
            bpy.app.handlers.render_cancel.remove(self.render_cancel) 

            make_all_objects_selectable(self.not_selectable)
            self.restore_initial_selection()
            
            # enable the render button after canceling
            enable_render_button(context.scene)
            return {"CANCELLED"}
        
        if event.type == "TIMER":
            # rendering has been cancelled
            if self.stop:
                 # remove the timer
                bpy.context.window_manager.event_timer_remove(self._timer)
                
                # remove the handlers
                bpy.app.handlers.render_pre.remove(self.render_pre)
                bpy.app.handlers.render_post.remove(self.render_post)   
                bpy.app.handlers.render_cancel.remove(self.render_cancel) 
                
                make_all_objects_selectable(self.not_selectable)
                self.restore_initial_selection()
                
                # enable the render button after queue is done rendering
                enable_render_button(context.scene)                                                               

                return {"CANCELLED"}
                
            # rendering is done
            if len(self.render_queue) == 0 and self.rendering is False:
                # remove the timer
                bpy.context.window_manager.event_timer_remove(self._timer)
                
                # remove the handlers
                bpy.app.handlers.render_pre.remove(self.render_pre)
                bpy.app.handlers.render_post.remove(self.render_post)
                bpy.app.handlers.render_cancel.remove(self.render_cancel) 
    
                make_all_objects_selectable(self.not_selectable)
                self.restore_initial_selection()
                
                # enable the render button after queue is done rendering
                enable_render_button(context.scene)                                                               

                return {"FINISHED"}

            elif self.rendering is False:
                # get fist element of the queue
                collection_name = self.render_queue.pop(0)
                
                # adjust settings for new render
                hide_render_others(collection_name, context.scene)
                set_current_camera_as_render(collection_name, context.scene)
                update_scene_frame(collection_name, context.scene)
                update_current_world(collection_name, context.scene)
                update_current_stage(collection_name, context.scene)
                
                bpy.context.scene.render.filepath = scene.spinwiz_spin_settings.spinwiz_output_filepath + "/" + collection_name + "/" + collection_name + "_"
                
                # begin the next render
                bpy.ops.render.render("INVOKE_DEFAULT", animation=True)
                
        return {"PASS_THROUGH"}
                
    def execute(self, context):
        # disable the render button until the render ends
        context.scene.spinwiz_spin_settings.enable_render = False
        context.scene.spinwiz_spin_settings.is_rendering = True
        
        bpy.app.handlers.render_pre.append(self.render_pre)
        bpy.app.handlers.render_post.append(self.render_post)   
        bpy.app.handlers.render_cancel.append(self.render_cancel) 
   
   
        # get original not selectable objects to restore them to previous state
        self.not_selectable = get_not_selectable_objects()
        
        # so the user can not mess with rendering
        make_all_objects_not_selectable()
        
        self.initial_active = bpy.context.view_layer.objects.active
        self.initial_selection = bpy.context.selected_objects
        
        output_list = [item.name for item in context.scene.spinwiz_output_list]
        
        self.render_queue = output_list.copy()
        
        self.rendering = False
        
        self._timer = bpy.context.window_manager.event_timer_add(0.5, window=bpy.context.window)
        bpy.context.window_manager.modal_handler_add(self)
            
        return {"RUNNING_MODAL"}
    
    def invoke(self, context, event):
        return self.execute(context)