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

from .operators.setup_spinwiz import OBJECT_OT_spin_wiz_setup
from .operators.documentation import OBJECT_OT_documentation

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
    row = layout.row()
    preview_menu = preview_collections["menu"]

    column = row.column()
    column.operator("object.documentation", text="Motion Setup", icon_value=preview_menu["motion_menu"].icon_id)
    column = row.column()
    column.operator("object.documentation", text="Output", icon_value=preview_menu["output_menu"].icon_id)

def select_movement_type(panel, layout):
    spin_settings = bpy.context.scene.spin_settings

    split = layout.split(factor=0.5)
    col = split.column()
    col.label(text="Movement type")
    col = split.column()
    col.prop(spin_settings, "movement_type", text="")

def select_interpolation_type(panel, layout):
    spin_settings = bpy.context.scene.spin_settings
    
    row = layout.row(align=True)
    row.scale_x = 1.6
    row.label(text="Interpolation")
    row.prop(spin_settings, "interpolation_type", expand=True, icon_only=True)

def select_length_type(panel, layout):
    spin_settings = bpy.context.scene.spin_settings
    options = layout

    row = options.row(align=True)
    row.label(text="Length")
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

def no_selection_warning(panel, layout):
    row = layout.row(align=True)
    row.alignment = "CENTER"
    row.label(text="Please select a suitable object")  

def documentation(panel, layout):
    # documentation button
    row = layout.row()
    row.operator("object.documentation",
                    text="Documentation",
                    icon_value=preview_collections["documentation"]["documentation"].icon_id) 

def is_selection_valid():
    # Iterate through the selected objects
    
    for obj in bpy.context.selected_objects:
        print([col.name for col in obj.users_collection])
        if (obj.type == 'MESH' or obj.type == "EMPTY") : # and not collection_name in [col.name for col in obj.users_collection]:
            return True
    return False

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
        
        # check if there are any selected objects (TODO: check if the selected object is an actual object)
        if not is_selection_valid():
            no_selection_warning(self, layout)      
        else:
            row = layout.row()
            row.operator("object.spin_wiz_setup",
                         text="Setup for Active Objects",
                         icon_value=preview_collections["logo"]["logo"].icon_id)

            layout.separator()

            # Motion and Output menu selectors 
            menu_items(self, layout)
            
            layout.separator()

            # create the box where the options are
            options = layout.box()

            select_movement_type(self, options)
            select_interpolation_type(self, options)
            select_length_type(self, options)

                            
            add_stage = layout.box()
            add_stage.prop(spin_settings, "add_stage")
            
            add_ligthing_setup = layout.box()
            add_ligthing_setup.prop(spin_settings, "add_lighting_setup")
            
        # documentation button
        documentation(self, layout)   

class_list = [SpinWiz_properties, VIEW3D_PT_main_panel, OBJECT_OT_documentation, OBJECT_OT_spin_wiz_setup]

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
