import bpy
from ..helper_functions import get_current_collection, use_settings_of_other
from ..naming_convetions import *


class OBJECT_OT_spinwiz_copy(bpy.types.Operator):
    bl_idname = bl_idname_copy
    bl_label = "Copy"
    bl_description = "Copy collection settings"
    
    def execute(self, context):
        context.scene.spinwiz_copy_collection_name = get_current_collection().name
        return {"FINISHED"}
    
class OBJECT_OT_spinwiz_paste(bpy.types.Operator):
    bl_idname = bl_idname_paste
    bl_label = "Paste"
    bl_description = "Paste collection settings"
    
    def execute(self, context):
        use_settings_of_other(context.scene.spinwiz_copy_collection_name)
        
        return {"FINISHED"}