import bpy

from ..helper_functions import *

# array where all the names of collections will be kept with output files wiht settings will be kept
output_list = []

#____________________________ HELPER FUNCTIONS

def get_current_collection(context):
    selected_obj = context.object
    
    if selected_obj is not None:
        return selected_obj.users_collection[0].name


#____________________________ PANEL FUNCTIONS

def output_row(panel, layout, name):
    row = layout.row()    
    
    col = row.column()
    op = col.operator("object.select", text=name)
    op.name = name
    
    col = row.column()
    op = row.operator("object.remove_output", text="", icon="TRASH")
    op.name = name
    
def panel_operator_add_to_output(panel, layout):
    # send to output button
    row = layout.row()
    row.operator("object.output", 
                    text="Send to output queue",)

def panel_output_list(panel, layout):
    
    
    global output_list
    
    if len(output_list) == 0:
        layout.label(text="There are not items in the queue")
    else:
        box = layout.box()
        for name in output_list:
            output_row(panel, box, name)

        # output path selection            
        layout.separator()

        box = layout.box()
        split = box.split(factor=0.75)
        col = split.column()
        col.label(text=output_filepath)

        col = split.column()
        col.operator("wm.open_path", text="Output path")

        # begin render output
        layout.separator()
        layout.operator("object.render", text="Render output queue")
        

#_____________________________ CLASSES

class OBJECT_OT_open_path(bpy.types.Operator):
    bl_idname = "wm.open_path"
    bl_label = "Open Path"
    bl_description = "Open path where the renders will be saved"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        global output_filepath

        output_filepath = self.filepath

        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OBJECT_OT_select(bpy.types.Operator):
    bl_idname = "object.select"
    bl_label = "Select Item"
    bl_description = "Select the item to be able to modify the settings again"
    
    name: bpy.props.StringProperty()
    
    def execute(self, context):
        collection = bpy.data.collections[self.name]
        
        pivot = None
        
        for obj in collection.objects:
            if pivot_object_name in obj.name:
                pivot = obj
                break
        
        # make the pivot as the selected object
        if pivot is not None:
            make_obj_active(pivot)
            
        # update the settings such that htey reflect the selection
        spin_settings = context.scene.spin_settings
        spin_settings.menu_options = "motion_setup"
        
        # select camera
        camera = None
        for obj in collection.objects:
            if camera_object_name in obj.name:
                camera = obj
                
        spin_settings.camera_height = camera.location.z
        spin_settings.camera_distance = camera.location.x
        spin_settings.camera_focal_length = camera.data.lens
        
        # Hide all collections except the current one, make that vissible
        for coll in bpy.context.scene.collection.children:
            if collection != coll:
                # Hide the collection in the active view layer
                for view_layer in bpy.context.scene.view_layers:
                    layer_collection = view_layer.layer_collection.children.get(coll.name)
                
                    if layer_collection:
                        layer_collection.hide_viewport = True
            else:
                for view_layer in bpy.context.scene.view_layers:
                    layer_collection = view_layer.layer_collection.children.get(coll.name)
                
                    if layer_collection:
                        layer_collection.hide_viewport = False
        
        
        # Get the default "Scene Collection"
        scene_collection = bpy.context.scene.collection
    
        # Iterate through all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is only in the "Scene Collection" and not in any other collections
            if len(obj.users_collection) == 1 and scene_collection in obj.users_collection:
                # Hide the object from the viewport using hide_set
                obj.hide_set(True)
            
        
        return {"FINISHED"}            

class OBJECT_OT_output(bpy.types.Operator):
    bl_idname = "object.output"
    bl_label = "To Output Queue"
    bl_description = "Send object and settings to output queue"

    def execute(self, context):

        global output_list
        
        if get_current_collection(context) not in output_list:
            output_list.append(get_current_collection(context))        
        
        return {"FINISHED"}
    
    
class OBJECT_OT_delete_output(bpy.types.Operator):
    bl_idname = "object.remove_output"
    bl_label = "Remove output item"
    bl_description = "Remove collection from output queue"
    
    name: bpy.props.StringProperty()
    
    def execute(self, context):
        
        global output_list
        
        output_list.remove(self.name)
        
        return {"FINISHED"}