# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from mathutils import Vector
from math import pi

bl_info = {
    "name" : "360_spinner",
    "author" : "Cristian Cutitei",
    "description" : "",
    "blender" : (4, 1, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

camera_object = None

class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "360 Spinner"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '360 Spinner'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Testicular Torsion!")

        print(camera_object)
        if camera_object:
            col = layout.column()
            col.prop(camera_object, "location", text="Location")
            col = layout.column()
            col.prop(camera_object, "rotation_euler", text="Rotation")

        layout.separator()
        row = layout.row()
        row.operator("object.add_360_spinner_camera",
                        text="Add 360 Spinner Camera")    




class OBJECT_OT_add_360_spinner_camera(bpy.types.Operator):
    bl_idname = "object.add_360_spinner_camera"
    bl_label = "Add 360 Spinner Camera"
    bl_description = "Add a camera at (0, 0, 0) with rotation (0, 0, 0) named '360 Spinner Camera'"

    def execute(self, context):
        # get selected object 
        obj = context.object
        

        global camera_object
        # Create a new camera object


        bpy.ops.object.camera_add(rotation=(pi/2,0,pi/2))
        camera_object = bpy.context.active_object

        dimension = max(obj.dimensions)/2
        render_settings = bpy.context.scene.render
        aspect_ratio = (render_settings.resolution_x / render_settings.resolution_y) / (camera_object.data.sensor_width/camera_object.data.sensor_height)
        print(aspect_ratio)
        sensor_width_half = camera_object.data.sensor_width/2/1000
        sensor_height_half = camera_object.data.sensor_height/2/1000
 
        distance_height = dimension/(sensor_height_half) * (camera_object.data.lens/1000) * aspect_ratio
        distance_width =  dimension/(sensor_width_half)  * (camera_object.data.lens/1000)

        distance = max(distance_height, distance_width)
        distance = distance_height
        camera_object.location = obj.location + Vector((distance + dimension, 0, 0))
        print(f"Distance_height: {distance_height}\nDistance_width: {distance_width}\nDimnesion_half: {dimension}")
        
        camera_object.name = "360 Spinner Camera"
        camera_object.data.name = "360 Spinner Camera"

        return {'FINISHED'}

class_list = [VIEW3D_PT_main_panel, OBJECT_OT_add_360_spinner_camera]

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)

    
def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
