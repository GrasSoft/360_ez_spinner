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

def delete_obj(obj):
    obj = bpy.data.objects[camera_object_name]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.delete()


def remove_spincamera():
    if is_object_valid(camera_object_name):
        delete_obj(bpy.data.objects[camera_object_name])
    if is_object_valid(curve_object_name):
        delete_obj(bpy.data.objects[curve_object_name])

def setup_spincamera(self, context):
    # get selected object 
    obj = bpy.context.object
    
    create_camera()

    radius = get_track_radius(obj)
    create_bezier_circle(radius, obj.location)
    
    # order matters
    set_camera_follow()
    
    set_camera_track(obj)

def setup_spinobject():
    obj = bpy.context.object

    add_keyframes(obj, 100)

    create_camera()

    radius = get_track_radius(obj)
    bpy.data.objects[camera_object_name].location = obj.location + Vector((radius, 0, 0)) 

    set_camera_track(obj)

def add_keyframes(obj, num_frames):
    # Convert rotation amount to radians
    rotation_amount_radians = radians(360)

    # Create keyframes
    for frame in range(num_frames + 1):
        bpy.context.scene.frame_set(frame)
        obj.rotation_euler[2] = rotation_amount_radians * frame / num_frames
        obj.keyframe_insert(data_path="rotation_euler", index=2)

    # Set the scene's end frame
    bpy.context.scene.frame_end = num_frames


class MyProperties(bpy.types.PropertyGroup):
    degrees: bpy.props.EnumProperty(
        name="Nr of degrees",
        description="Number of degrees between frames",
        items= [('1', "1", ""),
                ('2', "2", ""),
                ('3', "3", ""),
                ('5', "5", ""),
                ('6', "6", ""),
                ('8', "8", ""),
                ('10', "10", ""),
                ('15', "15", ""),
                ('30', "30", ""),
                ('45', "45", ""),
                ('60', "60", ""),
                ('90', "90", ""),
        ],
        default=3
    )

    adjust_timeline: bpy.props.BoolProperty(
        name="Adjust timeline Start/End",
        description= "Adjust the length of the timeline",
        default=True,
    )

    nr_frames: bpy.props.IntProperty(
        name="# of frames",
        description="Number of keyframes",
        default = 100,
    )

    start_frame: bpy.props.IntProperty(
        name="Start frame",
        description="Starting keyframe",
        default = 1
    )

    add_stage: bpy.props.BoolProperty(
        name="Add Stage",
        description="See stage menu",
        default=False
    )

    add_lighting_setup: bpy.props.BoolProperty(
        name="Add Lighting Setup",
        description="See lighting setup",
        default=False
    )

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
        items= [('OP1', "Object rotates", "The camera stays in place and object rotates",0),
                ('OP2', "Camera rotates", "The object stays in place and camera rotates",1),    
        ],
        update=setup_spincamera
    )


    interpolation_type: bpy.props.EnumProperty(
        name= "Interpolation",
        description= "Select the interpolation between the keyframes.",
        items= [('Linear', "", "The animation moves at constant speed",'WORLD_DATA', 0),
                ('Bezier_fast', "", "The animation start and ends fast",'WORLD_DATA', 1),
                ('Bezier_slow', "", "The animation start and ends slow",'WORLD_DATA', 1),               
        ]
    )

    length_type: bpy.props.EnumProperty(
        name= "Length",
        description= "Select the start and end keyframes or by degrees.",
        items= [('Keyframes', "", "",'WORLD_DATA', 0),
                ('Degrees', "", "",'WORLD_DATA', 1),
        ]
    ) # type: ignore



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

            options = layout.box()
            split = options.split(factor=0.5)
            col = split.column()
            col.label(text="Movement type")
            col = split.column()
            col.prop(spin_settings, "movement_type", text="")
            
            split = options.split(factor=0.75)
            col = split.column()
            col.label(text="Object UP axis")
            col = split.column()
            col.prop(spin_settings, "object_up_axis", text="")

            row = options.row(align=True)
            row.label(text="Interpolation")
            row.prop(spin_settings, "interpolation_type", expand=True, icon_only=True)

            row = options.row(align=True)
            row.label(text="Lenght")
            row.prop(spin_settings, "length_type", expand=True, icon_only=True)

            if spin_settings.length_type == "Keyframes":
                options.label(text="by Number of Keyframes")
                row = options.row(align=True)
                row.prop(spin_settings, "nr_frames")
                row.separator()
                row.prop(spin_settings, "start_frame")

            else:   
                options.label(text="by Degrees")
                row = options.row(align=True)
                split = row.split(factor=0.75)
                col = split.column()
                col.label(text="Nr of degrees")
                col = split.column()
                col.prop(spin_settings, "degrees", text="")

                options.label(text="This will generate "+ str(int(360 / int(spin_settings.degrees))) +" frames")
                
            options.prop(spin_settings, "adjust_timeline")

            add_stage = layout.box()
            add_stage.prop(spin_settings, "add_stage")
            
            add_ligthing_setup = layout.box()
            add_ligthing_setup.prop(spin_settings, "add_lighting_setup")
            

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



class_list = [MyProperties, VIEW3D_PT_main_panel, OBJECT_OT_documentation]

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
