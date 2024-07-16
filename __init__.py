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
from bpy.types import Context
from mathutils import Vector
from math import pi, radians
import math
from .helper_functions import *
from .custom_icons import *
from .properties import *


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

def menu_items(panel, layout):


class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "SpinWiz"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SpinWiz'

    def draw_header(self, context: Context):
        self.layout.label(text="", icon_value=preview_collections["logo"]["logo"].icon_id)
    
    def draw(self, context):
        scene = context.scene
        spin_settings = scene.spin_settings

        layout = self.layout
        layout.scale_y = 1.2
        

        if len(bpy.context.selected_objects) == 0:
            row = layout.row(align=True)
            row.alignment = "CENTER"
            row.label(text="Please select a suitable object")        
        else:
            layout.separator()
            row = layout.row()

            preview_menu = preview_collections["menu"]

            column = row.column()
            column.operator("object.documentation", text="Motion Setup", icon_value=preview_menu["motion_menu"].icon_id)
            column = row.column()
            column.operator("object.documentation", text="Output", icon_value=preview_menu["output_menu"].icon_id)
            layout.separator()

            options = layout.box()
            split = options.split(factor=0.5)
            col = split.column()
            col.label(text="Movement type")
            col = split.column()
            col.prop(spin_settings, "movement_type", text="")
            

            row = options.row(align=True)
            row.scale_x = 1.6
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
                
            add_stage = layout.box()
            add_stage.prop(spin_settings, "add_stage")
            
            add_ligthing_setup = layout.box()
            add_ligthing_setup.prop(spin_settings, "add_lighting_setup")
            

        # documentation button
        row = layout.row()
        row.operator("object.documentation",
                        text="Documentation",
                        icon_value=preview_collections["documentation"]["documentation"].icon_id)    


class OBJECT_OT_documentation(bpy.types.Operator):
    bl_idname = "object.documentation"
    bl_label = "Documentation"
    bl_description = "Go to documentation"

    def execute(self, context):
        return {"FINISHED"}



class_list = [SpinWiz_properties, VIEW3D_PT_main_panel, OBJECT_OT_documentation]

def register():
    import_custom_icons()

    for cls in class_list:
        bpy.utils.register_class(cls)

        bpy.types.Scene.spin_settings = bpy.props.PointerProperty(type= SpinWiz_properties)


def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)
        #del bpy.types.Scene.spin_settings

    global preview_collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
if __name__ == "__main__":
    register()
