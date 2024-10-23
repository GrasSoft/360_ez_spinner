import bpy
from ..naming_convetions import *
from ..helper_functions import get_spinwiz_scene, change_perspective, hide_anything_but, get_current_collection

class OBJECT_OT_spinwiz_switch_scene(bpy.types.Operator):
    bl_idname = bl_idname_switch_scene
    bl_label = "Switch Scene"
    bl_description = "Switch between the SpinWiz scene and the old one"
    
    def execute(self, context):
        if context.scene == get_spinwiz_scene():
          
            bpy.context.window.scene = bpy.data.scenes[context.scene.spinwiz_old_scene]
 
            change_perspective("PERSP")
            
            self.report({'INFO'}, "Switched to scene you were previously in: "+ context.scene.spinwiz_old_scene)
        else:
                    
            scene = get_spinwiz_scene()
            
            scene.spinwiz_old_scene = bpy.context.scene.name

            change_perspective()
            
            str = scene.spinwiz_last_looked
            
            if str == "NONE" or str == "":
                hide_anything_but(None)
            else:
                hide_anything_but(bpy.data.collections[ str ])
                                    
            bpy.context.window.scene = scene
            
            self.report({'INFO'}, "Switched to SpinWiz_Scene")      
        
        return {'FINISHED'}
    
