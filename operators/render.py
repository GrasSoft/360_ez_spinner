import bpy
import subprocess

class OBJECTE_OT_render(bpy.types.Operator):
    bl_idname = "object.render"
    bl_label = "Render the list"
    bl_description = "Render the list of output objects with the appropriate settings"
    
    def execute(self, context):
        
        # Define the command to run
        blend_file = bpy.data.filepath  # Get the current blend file
        output_path = "/home/image.png"
        file_format = "PNG"
        render_command = [
            bpy.app.binary_path,  # Path to Blender executable
            "-b", blend_file,      # Background mode and input file
            "-o", output_path,     # Output path
            "-F", file_format,     # File format
            "-x", "1",             # Use file extension
            "-a"                   # Render animation
        ]

        try:
            # Run the command in the background
            subprocess.Popen(render_command)
            self.report({'INFO'}, "Render command is running in the background.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to sta")

        return {"FINISHED"}