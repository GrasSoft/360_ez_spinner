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

class MyProperties(bpy.types.PropertyGroup):
    object_up_axis: bpy.props.EnumProperty(
        name= "Object UP axis",
        description= "In case you object is not alligned with the camera, change the up axis.", 
        items= [('X', "X", "The up axis will become X."),
                ('Y', "Y", "The up axis will become Y."),        
                ('Z', "Z", "The up axis will become Z.")
        ]
    )

    movement_type : bpy.props.EnumProperty(
        name= "Movement type",
        description= "Select wether the objects or the camera spins.",
        items= [('OP1', "Object rotates", "The camera stays in place and object rotates",'WORLD_DATA', 0),
                ('OP2', "Camera rotates", "The object stays in place and camera rotates",'WORLD_DATA', 1),
               
        ]
    )

class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "SpinWiz"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SpinWiz'

    def draw(self, context):
        scene = context.scene
        spin_settings = scene.spin_settings

        layout = self.layout
        layout.scale_y = 1.5
        

        if len(bpy.context.selected_objects) == 0:
            row = layout.row(align=True)
            row.alignment = "CENTER"
            row.label(text="Please select a suitable object")        
        else:
            # if is_object_valid(camera_object_name):
            #     camera_object = bpy.data.objects[camera_object_name]
            #     col = layout.column()
            #     col.prop(camera_object, "location", text="Location")
            #     col = layout.column()
            #     col.prop(camera_object, "rotation_euler", text="Rotation")

            layout.separator()
            row = layout.row()
            column = row.column()
            column.operator("object.documentation", text="Motion Setup")
            column = row.column()
            column.operator("object.documentation", text="Output")
            layout.separator()

            box = layout.box()
            box.prop(spin_settings, "movement_type")

            row = box.row(align=True)
            row.label(text="Interpolation")
            row.prop(spin_settings, "movement_type", expand=True, icon_only=True, icon="BLENDER")

            


            row = layout.row()
            row.operator("object.spin_object",
                            text="Spin selected object")    
            
            layout.separator()
        # documentation button
        row = layout.row()
        row.operator("object.documentation",
                        text="Documentation")    


class OBJECT_OT_documentation(bpy.types.Operator):
    bl_idname = "object.documentation"
    bl_label = "Documentation"
    bl_description = "Go to documentation"

    def execute(self, context):
        return {"FINISHED"}


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


class_list = [MyProperties, VIEW3D_PT_main_panel, OBJECT_OT_add_360_spinner_camera, OBJECT_OT_spin_object, OBJECT_OT_documentation]

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)

        bpy.types.Scene.spin_settings = bpy.props.PointerProperty(type= MyProperties)

    
def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)
        #del bpy.types.Scene.spin_settings
if __name__ == "__main__":
    register()
