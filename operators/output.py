import bpy

class OBJECT_OT_output(bpy.types.Operator):
    bl_idname = "object.output"
    bl_label = "To Output Queue"
    bl_description = "Send object and settings to output queue"

    def execute(self, context):
        return {"FINISHED"}