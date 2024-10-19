import bpy

from ..naming_convetions import *
from ..helper_functions import get_current_collection, move_item, make_obj_active
from ..blender_resources.media_setup.custom_media import *


#____________________________ PANEL FUNCTIONS

def output_row(panel, layout, name):
    scene = bpy.context.scene
    spin_settings = scene.spinwiz_spin_settings

    collection = get_current_collection()
    collection_settings = getattr(bpy.context.scene, get_current_collection().name)
                

    row = layout.row()    
    
    row.enabled = not spin_settings.is_rendering 
    
    up_down = row.row(align=True)
    up = up_down.column()
    
    index = 0
    for i, item in enumerate(scene.spinwiz_output_list):
        if item.name == name:
            index = i
            break
    
    up.enabled = (index > 0)
    op = up.operator(bl_idname_up_down, depress= (collection.name == name), icon= "TRIA_UP", text="")
    op.name = name
    op.up_down = True
    
    down = up_down.column()
    down.enabled = (index < len(scene.spinwiz_output_list) - 1)
    op = down.operator(bl_idname_up_down, depress= (collection.name == name), icon = "TRIA_DOWN", text="")
    op.name = name
    op.up_down = False
    
    col = row.column() 
    if spin_settings.is_rendering:
        op = col.operator(bl_idname_select, depress= (collection.name == name), text=name, icon_value=get_render_progress_icon(name, collection.name))
    else:
        global current_rename
        if current_rename == name:
            col.prop(get_current_collection(), "name", text="")     
        else:
            if collection.name == name:
                op = col.operator(bl_idname_rename, depress= (collection.name == name), text=name)
            else:
                op = col.operator(bl_idname_select, text=name)
    op.name = name

    col = row.column()
    op = row.operator(bl_idname_remove_output, text="", icon="TRASH", depress= (collection.name == name))
    op.name = name
    
def panel_operator_add_to_output(panel, layout):
    spin_settings = bpy.context.scene.spinwiz_spin_settings
    
    # render current item butt = 
    row = layout.row()
    
    col =  row.column()
    col.enabled = spin_settings.enable_render
    op = col.operator(bl_idname_render,
                    text="Render Current", icon = "RESTRICT_RENDER_OFF")
    op.name = get_current_collection().name
    
    # send to output button
    row.operator(bl_idname_output,
                    text="Send to Queue", icon = "RESTRICT_RENDER_OFF")
    
    
    text = "Please select a valid path" if not spin_settings.enable_render else ""
    row = layout.row()
    row.label(text= text)
    row.label(text="Currently in queue: "+ str(len(bpy.context.scene.spinwiz_output_list)))

def panel_output_list(panel, layout):
    spin_settings = bpy.context.scene.spinwiz_spin_settings
    
    output_list = bpy.data.scenes[0].spinwiz_output_list
    
    if len(output_list) == 0:
        layout.label(text="There are not items in the queue")
    else:
        box = layout.box()
        for item in output_list:
            output_row(panel, box, item.name)

        # output path selection            
        layout.separator()

        box = layout.box()
        split = box.split(factor=0.75)
        col = split.column()
        col.label(text=spin_settings.spinwiz_output_filepath)

        
        col = split.column()
        col.enabled = not spin_settings.is_rendering
        col.operator(bl_idname_open_path, text="Output path")

        # begin render output
        layout.separator()
        
        if spin_settings.enable_render is False and spin_settings.is_rendering is False:
            layout.label(text= "Please select a valid path!")
        
        row = layout.row()
        op = row.operator(bl_idname_render, text="Render output queue")
        op.render_queue =  [item.name for item in bpy.context.scene.spinwiz_output_list].copy()

        row.enabled = spin_settings.enable_render
        
        
#_____________________________ HELPER FUNCTIONS

def get_render_progress_icon(name, current_name):
    output_list = bpy.context.scene.spinwiz_output_list
    
    just_item = 0
    current_item = 0
    
    for index, item in enumerate(output_list):
        if item.name == name:
            just_item = index
        if item.name == current_name:
            current_item = index
    
    if just_item < current_item :
        return preview_collections["progress"]["prog_100"].icon_id

    if name != current_name:
        return preview_collections["progress"]["prog_0"].icon_id
 
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
        return preview_collections["progress"]["prog_0"].icon_id
    elif current_frame < start_frame + 0.5 * total_frames:
        # Between a quarter and half of the way
        return  preview_collections["progress"]["prog_25"].icon_id
    elif current_frame < start_frame + 0.75 * total_frames:
        # Between half and three-quarters of the way
        return  preview_collections["progress"]["prog_50"].icon_id
    elif current_frame < start_frame + (1 * total_frames) - 4:
        # Between three-quarters and end of the way
        return  preview_collections["progress"]["prog_75"].icon_id
    else:
        return preview_collections["progress"]["prog_100"].icon_id



#_____________________________ CLASSES

class OBJECT_OT_spinwiz_up_down(bpy.types.Operator):
    bl_idname = bl_idname_up_down
    bl_label = "Move the output"
    bl_description = "Move the output up and down the queue"
    
    name: bpy.props.StringProperty()
    up_down : bpy.props.BoolProperty()
    
    def execute(self, context):
        
        output_list = bpy.data.scenes[0].spinwiz_output_list
        
        # Find the index of the string
        index = 0
        for i, item in enumerate(output_list):
            if item.name == self.name:
                index = i
                break
            
        if self.up_down:
            # If it's not the first element, swap it with the previous element
            move_item(output_list, index, index-1)
    
        else:
            # If it's not the last element, swap it with the previous element
            move_item(output_list, index, index+1)
       
            
        return {'FINISHED'}

class OBJECT_OT_spinwiz_open_path(bpy.types.Operator):
    bl_idname = bl_idname_open_path
    bl_label = "Open Path"
    bl_description = "Open path where the renders will be saved"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        context.scene.spinwiz_spin_settings.spinwiz_output_filepath = self.filepath

        if self.filepath is not None:
            context.scene.spinwiz_spin_settings.enable_render = True

        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



class OBJECT_OT_spinwiz_rename(bpy.types.Operator):
    bl_idname = bl_idname_rename
    bl_label = "Rename Object"
    bl_description = "Rename the current selected collection"
    
    name: bpy.props.StringProperty()
    
    def execute(self, context):
        global current_rename
        current_rename = self.name
        
        return {'FINISHED'}



class OBJECT_OT_spinwiz_select(bpy.types.Operator):
    bl_idname = bl_idname_select
    bl_label = "Select Item"
    bl_description = "Select the item to be able to modify the settings again"
    
    name: bpy.props.StringProperty()
    is_selected: bpy.props.BoolProperty()
    
    def execute(self, context):
        
        global current_rename
        current_rename = None
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

class OBJECT_OT_spinwiz_output(bpy.types.Operator):
    bl_idname = bl_idname_output
    bl_label = "To Output Queue"
    bl_description = "Send object and settings to output queue"

    def execute(self, context):
        output_list = bpy.data.scenes[0].spinwiz_output_list

        collection_name = get_current_collection().name
        
        ok = True
        for item in output_list:
            if item.name == collection_name:
                ok = False
        
        if ok:
            item = output_list.add()
            item.name = collection_name        
        
        return {"FINISHED"}
    
    
class OBJECT_OT_spinwiz_delete_output(bpy.types.Operator):
    bl_idname = bl_idname_remove_output
    bl_label = "Remove output item"
    bl_description = "Remove collection from output queue"
    
    name: bpy.props.StringProperty()
    
    def execute(self, context):
        
        output_list = bpy.data.scenes[0].spinwiz_output_list
        
        for i, item in enumerate(output_list):
            if item.name == self.name:
                output_list.remove(i)
                break
        
        
        return {"FINISHED"}