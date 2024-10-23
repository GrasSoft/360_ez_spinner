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

from bpy.app.handlers import persistent

from .helper_functions import spinwiz_frame_change_handler, spinwiz_update_current_selection, is_selection_valid, is_selection_setup, is_pivot, \
    is_camera, is_stage, get_spinwiz_scene
from .lighting_setup.lighting_setup import panel_lighting_setup
from .stage_setup.stage_setup import panel_stage_setup
from .properties import *

from .operators.setup_spinwiz import OBJECT_OT_spinwiz_setup

from .operators.copy_paste import OBJECT_OT_spinwiz_copy, OBJECT_OT_spinwiz_paste

from .operators.output import panel_output_list, panel_operator_add_to_output, OBJECT_OT_spinwiz_rename, \
    OBJECT_OT_spinwiz_up_down, OBJECT_OT_spinwiz_output, OBJECT_OT_spinwiz_delete_output, OBJECT_OT_spinwiz_select, \
    OBJECT_OT_spinwiz_open_path

from .operators.render import OBJECTE_OT_spinwiz_render

from .operators.switch_scene import OBJECT_OT_spinwiz_switch_scene

from . import addon_updater_ops



bl_info = {
    "name" : "SpinWiz",
    "author" : "Blender Might",
    "description" : "",
    "blender" : (4, 2, 0),
    "version" : (1, 0, 0),
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

def select_spin_direction(panel, layout):
    current_collection = get_current_collection()
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
    
    row = layout.row(align=True)
    row.scale_x = 1.6
    row.label(text="Spin Direction")
    row.prop(spin_settings, "spin_direction", expand=True, icon_only=True)

    
    

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

def select_spin_amount(panel, layout):
    current_collection = get_current_collection()
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)

    row = layout.split(factor=0.8)
    row.label(text = "Number of spins")
    row.prop(spin_settings, "spin_amount", text="")

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
    
    options.prop(spin_settings, "camera_tracking_height_offset", text="Target Height")

    row = options.row()
    col = row.column()
    col.prop(spin_settings, "camera_focal_length", text="Focal Length")
    col = row.column()
    col.prop(spin_settings, "camera_distance", text="Distance")
    
    

def no_selection_warning(panel, layout):
    row = layout.row(align=True)
    row.alignment = "CENTER"
    row.label(text="Please select a suitable object")  
    
def dropdown_collection(panel, layout, no_copy_paste = False):
    scene = bpy.context.scene
    spin_settings = scene.spinwiz_spin_settings


    if not no_copy_paste:    
        if scene.spinwiz_copy_collection_name != "":
            layout.label(text="The current coppied collection is: " + scene.spinwiz_copy_collection_name)
    

    layout.label(text="Select a spinwiz collection")
                                
    row = layout.row()
    row.prop(spin_settings, "dropdown_collections", text="")

    if not no_copy_paste:        
        copy_paste = row.row(align=True)
        copy_paste.scale_x = 1.4
        copy_paste.operator(bl_idname_copy, text="", icon = "COPYDOWN", depress=scene.spinwiz_copy_collection_name == get_current_collection().name)
        copy_paste.operator(bl_idname_paste, text="", icon = "PASTEDOWN")

def documentation(panel, layout):
    # documentation button
    row = layout.row()
    row.operator("wm.url_open",
                    text="Documentation",
                    icon_value=preview_collections["documentation"]["documentation"].icon_id).url = link_to_docs

class VIEW3D_PT_spinwiz_mainpanel(bpy.types.Panel):
    bl_label = "SpinWiz"
    bl_idname = bl_idname_mainpanel
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SpinWiz'


    def draw_header(self, context):
        self.layout.label(text="", icon_value=preview_collections["logo"]["logo"].icon_id)
    
    def draw(self, context):
        
        # check for update in background
        addon_updater_ops.check_for_update_background()
        
        scene = context.scene
        spin_settings = scene.spinwiz_spin_settings
                
        current_selection = bpy.context.active_object
        
        
        if get_current_collection() is not None:
            collection_settings = getattr(scene, get_current_collection().name, None)
        
        layout = self.layout
        
        layout.scale_y = 1.2
        
        if get_spinwiz_scene() is not None and (len(get_spinwiz_scene().spinwiz_collections_list) > 0 or bpy.context.scene == get_spinwiz_scene()):
            row = layout.row()
            
            row.operator(bl_idname_switch_scene, text= "Switch to old scene" if bpy.context.scene == get_spinwiz_scene() else "Switch to SpinWiz scene", icon_value=preview_collections["menu"]["switch_scene"].icon_id)
            layout.separator()
            
        
        if not is_selection_valid():
            if scene == get_spinwiz_scene():
                dropdown_collection(self, layout, True) 
                layout.separator()
            else:
                no_selection_warning(self, layout)      
        else:
            if not is_selection_setup(current_selection):
                row = layout.row()
                row.operator(bl_idname_setup,
                         text="Set up for Selected Object(s)",
                         icon_value=preview_collections["logo"]["logo"].icon_id)
                row = layout.row(align=True)
                row.label(text= str(len(get_spinwiz_scene().spinwiz_collections_list) if get_spinwiz_scene() is not None else 0)  + " Setups in current blend file")
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
                            
                            dropdown_collection(self, layout)
                            
                            if is_pivot(current_selection) or is_camera(current_selection):
                                
                                # camera options
                                panel_camera_options(self, layout)
                                
                            if is_pivot(current_selection):  
                                    
                                layout.label(text="Animation options")
                                
                                options = layout.box()
                                
                                select_movement_type(self, options)
                                select_spin_direction(self, options)
                                select_interpolation_type(self, options)
                                select_spin_amount(self, options)
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
                            
                            layout.label(text="Change the current collection name")
                            box = layout.box()
                            row = box.row()
                            row.prop(get_current_collection(), "name", text="")

                            layout.separator()

                            panel_operator_add_to_output(self, layout)                            

                            layout.separator()

                    case 'output_setup':
                        layout.separator()
                        layout.label(text="Output menu")
                        
                        panel_output_list(self, layout)

                        layout.separator()
                                
        addon_updater_ops.update_notice_box_ui(self, context)
        
        # documentation button
        documentation(self, layout)   



        

# Define a PropertyGroup for the list items
class SpinWiz_ListCollection(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Item Name")

class_list = [
    SpinWiz_ListCollection,
    SpinWiz_UpdatePreferences,
    SpinWiz_properties,
    SpinWiz_collection_properties,
    VIEW3D_PT_spinwiz_mainpanel,
    OBJECT_OT_spinwiz_setup,
    OBJECT_OT_spinwiz_paste,
    OBJECT_OT_spinwiz_copy,
    OBJECT_OT_spinwiz_rename,
    OBJECT_OT_spinwiz_up_down,
    OBJECT_OT_spinwiz_output,
    OBJECT_OT_spinwiz_delete_output,
    OBJECT_OT_spinwiz_select,
    OBJECTE_OT_spinwiz_render,
    OBJECT_OT_spinwiz_open_path,
    OBJECT_OT_spinwiz_switch_scene
    
]


def register():    
    addon_updater_ops.register(bl_info)
    
    spinwiz_import_custom_icons()
    spinwiz_import_thumbnails()

    for cls in class_list:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.spinwiz_last_looked = bpy.props.StringProperty()
        
    bpy.types.Scene.spinwiz_old_scene = bpy.props.StringProperty()
        
    bpy.types.Scene.spinwiz_copy_collection_name = bpy.props.StringProperty()
        
    bpy.types.Scene.spinwiz_is_setting_up = bpy.props.BoolProperty()
                
    bpy.types.Scene.spinwiz_spin_settings = bpy.props.PointerProperty(type= SpinWiz_properties)
    
    bpy.types.Scene.spinwiz_old_collections = bpy.props.CollectionProperty(type= SpinWiz_ListCollection)
    
    bpy.types.Scene.spinwiz_collections_list = bpy.props.CollectionProperty(type=SpinWiz_ListCollection)
     
    bpy.types.Scene.spinwiz_output_list = bpy.props.CollectionProperty(type=SpinWiz_ListCollection)
     
    bpy.types.Scene.spinwiz_output_filepath = bpy.props.StringProperty()
    
    bpy.app.handlers.depsgraph_update_post.append(spinwiz_update_current_selection)
    
    bpy.app.handlers.load_post.append(spinwiz_on_load_post_handler)
   
    bpy.app.handlers.frame_change_post.append(spinwiz_frame_change_handler) 
    
    
# Timer function to delay the registration of dynamic properties
def delayed_property_registration():
    # Ensure the attribute is present and populated with items before registering
    scene = bpy.context.scene
    if hasattr(scene, 'spinwiz_collections_list') and len(scene.spinwiz_collections_list) > 0:
        register_dynamic_properties()
        return None  # Stop the timer once registration is complete
    else:
        return 1.0  # Repeat after 1 second



# Function to register dynamic properties based on the items in collections_list
def register_dynamic_properties():
    scene = bpy.context.scene
    if not hasattr(scene, 'collections_list'):
        print("collections_list not found in scene.")
        return
    
    if not scene.spinwiz_collections_list:
        print("collections_list is present but empty. No properties to register.")
        return

    # Iterate through the collections list and register dynamic properties
    for item in scene.spinwiz_collections_list:
        prop_name = item.name
        try:
            if not hasattr(bpy.types.Scene, prop_name):
                setattr(bpy.types.Scene, prop_name, bpy.props.PointerProperty(type=SpinWiz_collection_properties))
                print(f"Successfully registered dynamic property: {prop_name}")
        except Exception as e:
            print(f"Failed to register property {prop_name}: {e}")

@persistent
def spinwiz_on_load_post_handler(dummy):
    print("A .blend file has been loaded. Starting delayed property registration...")
    bpy.app.timers.register(delayed_property_registration)
    
def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)
        #del bpy.types.Scene.spin_settings

    global preview_collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
        
    preview_collections.clear()
    
    if hasattr(bpy.types.Scene, "spinwiz_last_looked"):
        del bpy.types.Scene.spinwiz_last_looked
    
    if hasattr(bpy.types.Scene, "spinwiz_old_scene"):
        del bpy.types.Scene.spinwiz_old_scene
    
    if hasattr(bpy.types.Scene, "spinwiz_copy_collection_name"):
        del bpy.types.Scene.spinwiz_copy_collection_name
    
    if hasattr(bpy.types.Scene, "spinwiz_is_setting_up"):
        del bpy.types.Scene.spinwiz_is_setting_up
    
    if hasattr(bpy.types.Scene, "spinwiz_spin_settings"):
        del bpy.types.Scene.spinwiz_spin_settings
    
    if hasattr(bpy.types.Scene, "spinwiz_collections_list"):
        # delete every item in collections list first
        
        for item in bpy.context.scene.spinwiz_collections_list:
            delattr(bpy.types.Scene, item.name)
        
        del bpy.types.Scene.spinwiz_collections_list
    
    if hasattr(bpy.types.Scene, "spinwiz_output_list"):
        del bpy.types.Scene.spinwiz_output_list
        
    if hasattr(bpy.types.Scene, "spinwiz_output_filepath"):
        del bpy.types.Scene.spinwiz_output_filepath
    
    if spinwiz_update_current_selection in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(spinwiz_update_current_selection)
        
    if spinwiz_on_load_post_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.load_post.remove(spinwiz_on_load_post_handler)
    
    if spinwiz_frame_change_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(spinwiz_frame_change_handler)
    
    
if __name__ == "__main__":
    register()
