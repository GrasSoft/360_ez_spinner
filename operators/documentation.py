import bpy

from ..settings.current_settings import list_current_settings

class OBJECT_OT_documentation(bpy.types.Operator):
    bl_idname = "object.documentation"
    bl_label = "Documentation"
    bl_description = "Go to documentation"

    def execute(self, context):
        
        for key in list_current_settings.keys():
            print(key+"\n")
        return {"FINISHED"}

