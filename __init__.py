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

from .icon_setup.custom_icons import *

from .properties import *

from .operators.setup_spinwiz import OBJECT_OT_spin_wiz_setup 

from .operators.output import *

from .operators.render import *

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

current_pivot = None

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
        
def panel_camera_options(panel, layout):
    options = layout
    
    spin_settings = bpy.context.scene.spin_settings
                        
    # camera settings
    
    options.label(text="Current: " + get_current_camera().name)
    
    options.prop(spin_settings, "camera_height", text="Camera Height")

    row = options.row()
    col = row.column()
    col.prop(spin_settings, "camera_focal_length", text="Focal Length")
    col = row.column()
    col.prop(spin_settings, "camera_distance", text="Distance")

def no_selection_warning(panel, layout):
    row = layout.row(align=True)
    row.alignment = "CENTER"
    row.label(text="Please select a suitable object")  

def documentation(panel, layout):
    # documentation button
    row = layout.row()
    row.operator("wm.url_open",
                    text="Documentation",
                    icon_value=preview_collections["documentation"]["documentation"].icon_id).url = link_to_docs

def is_selection_valid():
    # Iterate through the selected objects

    for obj in bpy.context.view_layer.objects.selected:
        if (obj.type == 'MESH' or obj.type == "EMPTY") : # and not collection_name in [col.name for col in obj.users_collection]:
            # update the current context such that the UI reflects the selection

            return True
    return False



def is_selection_setup():
    obj =  bpy.context.active_object
    for name in [cam_pivot_object_name, pivot_object_name, camera_object_name, curve_object_name]:
        if name in obj.name:
            return True

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
            if not is_selection_setup():
                row = layout.row()
                row.operator("object.spin_wiz_setup",
                         text="Setup for Active Objects",
                         icon_value=preview_collections["logo"]["logo"].icon_id)
            else:
                global current_pivot

                if current_pivot is None:
                    current_pivot = get_current_pivot()

                if current_pivot is not None and bpy.context.view_layer.objects.active.name != current_pivot.name:
                    layout.separator()

                    row = layout.row(align=True)
                    row.label(text="The current selection has changed, refresh")
                    row.operator("object.refresh", icon="WORLD_DATA")
            
                else:
                    layout.separator()

                    # Motion and Output menu selectors 
                    # menu_items(self, layout)

                    row = layout.row()
                    row.prop(spin_settings, "menu_options", expand=True)

                    match spin_settings.menu_options:
                        case 'motion_setup':
                            layout.separator()


                            layout.label(text="Camera options")
                            # create the box where the options are
                            options = layout.box()
                            
                            # camera options
                            panel_camera_options(self, options)
                            
                            
                            layout.label(text="Animation options")
                            
                            options = layout.box()
                            
                            select_movement_type(self, options)
                            select_interpolation_type(self, options)
                            select_length_type(self, options)
                            
                        
                            # stage setup
                            panel_stage_setup(self, layout)                            

                            # lighting setup
                            panel_lighting_setup(self, layout)
                            
                            layout.separator()

                            panel_operator_add_to_output(self, layout)

                            layout.separator()

                        case 'output_setup':
                            layout.separator()
                            layout.label(text="Output menu")
                            
                            panel_output_list(self, layout)

                            layout.separator()

        # documentation button
        documentation(self, layout)   

class OBJECT_OT_refresh(bpy.types.Operator):
    bl_idname="object.refresh"
    bl_description="refreshes the entire panel"
    bl_label="Refresh"

    def execute(self, context):
        global current_pivot
        
        update_context()

        current_pivot = get_current_pivot()

        return {"FINISHED"}

class_list = [SpinWiz_properties, VIEW3D_PT_main_panel, OBJECT_OT_spin_wiz_setup, OBJECT_OT_output, OBJECT_OT_delete_output, OBJECT_OT_select, OBJECTE_OT_render, OBJECT_OT_open_path, OBJECT_OT_refresh]

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
