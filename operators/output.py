import bpy

from ..helper_functions import *

# array where all the names of collections will be kept with output files wiht settings will be kept
output_list = []


#____________________________ PANEL FUNCTIONS

def output_row(panel, layout, name):
    scene = bpy.context.scene
    spin_settings = scene.spin_settings

    collection = get_current_collection()

    row = layout.row()    
    
    col = row.column()

    if collection.name == name:
        if spin_settings.current_rendered_collection != name:
            op = col.operator("object.select", text=name, depress=True)
        else:
            op = col.operator("object.select", text=name, depress=True, icon=get_render_progress_icon())
    else:
        if spin_settings.current_rendered_collection != name:
            op = col.operator("object.select", text=name)
        else:
            op = col.operator("object.select", text=name, icon=get_render_progress_icon())

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
    spin_settings = bpy.context.scene.spin_settings    
    
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
        row = layout.row()
        op = row.operator("object.render", text="Render output queue")
        row.enabled = spin_settings.enable_render
        
#_____________________________ HELPER FUNCTIONS

def get_render_progress_icon():
    scene = bpy.context.scene
    
    print("nigger")
    
    # Get the start, end, and current frames
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    current_frame = scene.frame_current
    
    # Calculate the total number of frames
    total_frames = end_frame - start_frame + 1
    
    # Determine the progress range based on the current frame
    if current_frame < start_frame + 0.25 * total_frames:
        # Less than a quarter of the way
        return "OUTLINER_OB_CAMERA"
    elif current_frame < start_frame + 0.5 * total_frames:
        # Between a quarter and half of the way
        return "RENDER_ANIMATION"
    elif current_frame < start_frame + 0.75 * total_frames:
        # Between half and three-quarters of the way
        return "MODIFIER"
    else:
        # Between three-quarters and the end
        return "FILE_TICK"

def update_context():
    collection = get_current_collection()

    # update the settings such that htey reflect the selection
    spin_settings = bpy.context.scene.spin_settings
    spin_settings.menu_options = "motion_setup"
    
    # select camera
    camera = get_current_camera()
            
    spin_settings.camera_height = camera.location.z
    spin_settings.camera_distance = camera.location.x
    spin_settings.camera_focal_length = camera.data.lens

    # select stage
    stage = get_current_stage()

    if stage is not None:
        spin_settings.has_stage = (stage is not None)
        spin_settings.stage_height_offset = stage.modifiers.get("SpinWiz_StageCTRL")["Socket_3"]
        spin_settings.stage_subdivision = stage.modifiers.get("SpinWiz_StageCTRL")["Socket_5"]

    
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
            
       
        
        return {"FINISHED"}            

class OBJECT_OT_output(bpy.types.Operator):
    bl_idname = "object.output"
    bl_label = "To Output Queue"
    bl_description = "Send object and settings to output queue"

    def execute(self, context):

        global output_list
        
        collection_name = get_current_collection().name
        if collection_name not in output_list:
            output_list.append(collection_name)        
        
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