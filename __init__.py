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
from math import pi, radians
import math
from .helper_functions import *

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

class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "360 Spinner"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '360 Spinner'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Testicular Torsion!")

        # if is_object_valid(camera_object_name):
        #     camera_object = bpy.data.objects[camera_object_name]
        #     col = layout.column()
        #     col.prop(camera_object, "location", text="Location")
        #     col = layout.column()
        #     col.prop(camera_object, "rotation_euler", text="Rotation")

        if is_object_valid(curve_object_name):
            camera_object = bpy.data.objects[curve_object_name]
            col = layout.column()
            col.prop(camera_object, "location", text="Location")
            col = layout.column()
            col.prop(camera_object, "rotation_euler", text="Rotation")
        layout.separator()
        row = layout.row()
        row.operator("object.add_360_spinner_camera",
                        text="Add 360 Spinner Camera")
        row = layout.row()
        row.operator("object.spin_object",
                        text="Spin selected object")    

class OBJECT_OT_spin_object(bpy.types.Operator):
    bl_idname = "object.spin_object"
    bl_label = "Spin object"
    bl_description = "Spin the object around by 360 degrees"

    def add_keyframes(self, obj, num_frames):
        # Convert rotation amount to radians
        rotation_amount_radians = radians(360)

        # Create keyframes
        for frame in range(num_frames + 1):
            bpy.context.scene.frame_set(frame)
            obj.rotation_euler[2] = rotation_amount_radians * frame / num_frames
            obj.keyframe_insert(data_path="rotation_euler", index=2)

        # Set the scene's end frame
        bpy.context.scene.frame_end = num_frames

    def execute(self, context):
        obj = context.object

        self.add_keyframes(obj, 100)

        create_camera()

        radius = get_track_radius(obj)
        bpy.data.objects[camera_object_name].location = obj.location + Vector((radius, 0, 0)) 

        set_camera_track(obj)



        return {'FINISHED'}


class OBJECT_OT_add_360_spinner_camera(bpy.types.Operator):
    bl_idname = "object.add_360_spinner_camera"
    bl_label = "Add 360 Spinner Camera"
    bl_description = "Add a camera at (0, 0, 0) with rotation (0, 0, 0) named '360 Spinner Camera'"


    def execute(self, context):
        # get selected object 
        obj = context.object
        
        create_camera()

   
        radius = get_track_radius(obj)
        create_bezier_circle(radius, obj.location)
        
        
        # order matters
        set_camera_follow()
        
        set_camera_track(obj)

        return {'FINISHED'}


class_list = [VIEW3D_PT_main_panel, OBJECT_OT_add_360_spinner_camera, OBJECT_OT_spin_object]

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)

    
def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
