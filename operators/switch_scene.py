import bpy
from ..naming_convetions import *
from ..helper_functions import get_spinwiz_scene

class OBJECT_OT_spinwiz_switch_scene(bpy.types.Operator):
    bl_idname = bl_idname_switch_scene
    bl_label = "Switch Scene"
    bl_description = "Switch between the SpinWiz scene and the old one"
    
    def execute(self, context):
        if context.scene == get_spinwiz_scene():
          
            bpy.context.window.scene = bpy.data.scenes[context.scene.spinwiz_old_scene]
        else:
                    
            get_spinwiz_scene().spinwiz_old_scene = bpy.context.scene.name
            bpy.context.window.scene = get_spinwiz_scene()       
        
        return {'FINISHED'}
    
