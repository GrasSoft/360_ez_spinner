import bpy


class OBJECT_OT_documentation(bpy.types.Operator):
    bl_idname = "object.documentation"
    bl_label = "Documentation"
    bl_description = "Go to documentation"

    def execute(self, context):
        return {"FINISHED"}

