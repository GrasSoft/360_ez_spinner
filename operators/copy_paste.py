import bpy
from ..helper_functions import get_current_collection, use_settings_of_other

class OBJECT_OT_copy(bpy.types.Operator):
    bl_idname = "object.copy"
    bl_label = "Copy"
    bl_description = "Copy collection settings"
    
    def execute(self, context):
        context.scene.copy_collection_name = get_current_collection().name
        return {"FINISHED"}
    
class OBJECT_OT_paste(bpy.types.Operator):
    bl_idname = "object.paste"
    bl_label = "Paste"
    bl_description = "Paste collection settings"
    
    def execute(self, context):
        use_settings_of_other(context.scene.copy_collection_name)
        
        return {"FINISHED"}