import bpy

from ..helper_functions import *


#____________________________ PANEL FUNCTIONS

def output_row(panel, layout, name):
    scene = bpy.context.scene
    spin_settings = scene.spin_settings

    collection = get_current_collection()

    row = layout.row()    
    

    row.enabled = not spin_settings.is_rendering 
    
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
    
    output_list = bpy.data.scenes[0].output_list
    
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
        col.label(text=spin_settings.output_filepath)

        
        col = split.column()
        col.enabled = not spin_settings.is_rendering
        col.operator("wm.open_path", text="Output path")

        # begin render output
        layout.separator()
        
        if spin_settings.enable_render is False:
            layout.label(text= "Please select a valid path!")
        
        row = layout.row()
        row.operator("object.render", text="Render output queue")
        row.enabled = spin_settings.enable_render
        
        
#_____________________________ HELPER FUNCTIONS

def get_render_progress_icon():
    scene = bpy.context.scene
    
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



#_____________________________ CLASSES

class OBJECT_OT_open_path(bpy.types.Operator):
    bl_idname = "wm.open_path"
    bl_label = "Open Path"
    bl_description = "Open path where the renders will be saved"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        context.scene.spin_settings.output_filepath = self.filepath

        if self.filepath is not None:
            context.scene.spin_settings.enable_render = True

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
        camera = None
        
        for obj in collection.objects:
            if pivot_object_name in obj.name:
                pivot = obj
                break
        
        for obj in collection.objects:
            if camera_object_name in obj.name:
                camera = obj
                break
        
        # make the pivot as the selected object
        if pivot is not None:
            make_obj_active(pivot)
            
        if camera is not None:
            context.scene.camera = camera
        
        return {"FINISHED"}            

class OBJECT_OT_output(bpy.types.Operator):
    bl_idname = "object.output"
    bl_label = "To Output Queue"
    bl_description = "Send object and settings to output queue"

    def execute(self, context):
        output_list = bpy.data.scenes[0].output_list

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
        
        output_list = bpy.data.scenes[0].output_list
        
        output_list.remove(self.name)
        
        return {"FINISHED"}