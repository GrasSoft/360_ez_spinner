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

from .blender_resources.media_setup.custom_media import *

from .properties import *

from .operators.setup_spinwiz import OBJECT_OT_spin_wiz_setup 

from .operators.output import *

from .operators.render import *

from . import addon_updater_ops



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

current_selection = None

def menu_items(panel, layout):
    row = layout.row()
    preview_menu = preview_collections["menu"]

    column = row.column()
    column.operator("object.documentation", text="Motion Setup", icon_value=preview_menu["motion_menu"].icon_id)
    column = row.column()
    column.operator("object.documentation", text="Output", icon_value=preview_menu["output_menu"].icon_id)

def select_movement_type(panel, layout):
    current_collection = get_current_collection()
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)

    split = layout.split(factor=0.5)
    col = split.column()
    col.label(text="Movement type")
    col = split.column()
    col.prop(spin_settings, "movement_type", text="")

def select_interpolation_type(panel, layout):
    current_collection = get_current_collection()
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
    
    row = layout.row(align=True)
    row.scale_x = 1.6
    row.label(text="Interpolation")
    row.prop(spin_settings, "interpolation_type", expand=True, icon_only=True)

def select_length_type(panel, layout):
    current_collection = get_current_collection()
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
    
    options = layout

    row = options.row(align=True)
    row.scale_x = 1.6 
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
    layout.label(text="Camera options")
     
    # create the box where the options are
    options = layout.box()
                                    
    current_collection = get_current_collection()
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
                        
    # camera settings
    
    options.label(text="Current: " + get_current_camera().name)
    
    options.prop(spin_settings, "camera_height", text="Camera Height")

    row = options.row()
    col = row.column()
    col.prop(spin_settings, "camera_focal_length", text="Focal Length")
    col = row.column()
    col.prop(spin_settings, "camera_distance", text="Distance")
    
    row = options.row()
    row.prop(spin_settings, "camera_tracking_height_offset", text="Height of lookat point")

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


        
    

class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "SpinWiz"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SpinWiz'


    def draw_header(self, context: Context):
        self.layout.label(text="", icon_value=preview_collections["logo"]["logo"].icon_id)
    
    def draw(self, context):
        
        # check for update in background
        addon_updater_ops.check_for_update_background()
        
        scene = context.scene
        spin_settings = scene.spin_settings
                
        current_selection = bpy.context.active_object

        collection_settings = getattr(scene, get_current_collection().name, None)
        
        layout = self.layout
        
        layout.scale_y = 1.2
        
        # check if there are any selected objects (TODO: check if the selected object is an actual object)
        if not is_selection_valid():
            no_selection_warning(self, layout)      
        else:
            if not is_selection_setup(current_selection):
                row = layout.row()
                row.operator("object.spin_wiz_setup",
                         text="Setup for Active Objects",
                         icon_value=preview_collections["logo"]["logo"].icon_id)
            else:
                layout.separator()

                row = layout.row()
                row.prop(spin_settings, "menu_options", expand=True)   
                
                match spin_settings.menu_options:
                    case 'motion_setup':
                        if spin_settings.is_rendering:
                            layout.label(text= "The add-on is currently rendering")
                            layout.label(text= "Settings can not be changed during")
                            layout.label(text= "To cancel, close the render window")
                        else:
                            layout.separator()
                    
                            box = layout.box()
                            row = box.row()
                            row.prop(collection_settings, "collection_name", text="")     
                            
                            box = layout.box()
                            box.prop(collection_settings, "use_global_settings", text="Use global settings, unchecking returns to defaults")
                            
                            if is_pivot(current_selection) or is_camera(current_selection):
                                
                                # camera options
                                panel_camera_options(self, layout)
                                
                            if is_pivot(current_selection):  
                                    
                                layout.label(text="Animation options")
                                
                                options = layout.box()
                                
                                select_movement_type(self, options)
                                select_interpolation_type(self, options)
                                select_length_type(self, options)
                                
                                
                            if is_pivot(current_selection) or is_stage(current_selection):
                                add_stage = layout.box()
                                if is_pivot(current_selection):
                                    add_stage.prop(collection_settings, "add_stage")
                                # stage setup
                                panel_stage_setup(self, add_stage)                            

                            if is_pivot(current_selection):
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
                        
        #automatic update function 
        layout.separator()
        
        update_setup_box = layout.box()
        update_setup_box.prop(spin_settings, "show_update_window")     
        
        if spin_settings.show_update_window:       
            addon_updater_ops.update_settings_ui(self,context)
        
        addon_updater_ops.update_notice_box_ui(self, context)
        
        # documentation button
        documentation(self, layout)   



class UpdatePreferences(bpy.types.AddonPreferences):
	"""Demo bare-bones preferences"""
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update: bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=True
    ) # type: ignore

	updater_interval_months: bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0
    ) # type: ignore


	updater_interval_days: bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=1,
		min=0,
		max=31
    ) # type: ignore


	updater_interval_hours: bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23
    ) # type: ignore


	updater_interval_minutes: bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59
    ) # type: ignore


	

class_list = [UpdatePreferences, SpinWiz_properties, SpinWiz_collection_properties, VIEW3D_PT_main_panel, OBJECT_OT_spin_wiz_setup, OBJECT_OT_up_down, OBJECT_OT_output, OBJECT_OT_delete_output, OBJECT_OT_select, OBJECTE_OT_render, OBJECT_OT_open_path]

        

def register():
    addon_updater_ops.register(bl_info)
    
    import_custom_icons()
    import_thumbnails()

    for cls in class_list:
        bpy.utils.register_class(cls)
        
        
    bpy.types.Scene.output_list = []
    
    bpy.types.Scene.spin_settings = bpy.props.PointerProperty(type= SpinWiz_properties)
    
    bpy.app.handlers.depsgraph_update_post.append(update_current_selection)


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
