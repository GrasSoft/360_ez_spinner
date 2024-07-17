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
        if len(bpy.context.selected_objects) == 0:
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


class OBJECT_OT_documentation(bpy.types.Operator):
    bl_idname = "object.documentation"
    bl_label = "Documentation"
    bl_description = "Go to documentation"

    def execute(self, context):
        return {"FINISHED"}

def create_pivot(collection):
    # Store originally selected objects
    original_selection = bpy.context.selected_objects[:]

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')

    # Select objects that do not have parents
    objects_to_parent = [obj for obj in original_selection if obj.parent is None]

    # Create an empty object
    bpy.ops.object.empty_add(location=(0, 0, 0))  # You can adjust the location as needed
    empty_obj = bpy.context.object

    #unlink from scene collection
    bpy.context.scene.collection.objects.unlink(empty_obj)
    collection.objects.link(empty_obj)


    # Make the empty object the parent of each selected object
    for obj in objects_to_parent:
        obj.select_set(True)
        obj.parent = empty_obj

    # Deselect all objects at the end
    bpy.ops.object.select_all(action='DESELECT')

# create a new collection, copy the selected objects inside it and hide the rest of the scene objects  
def create_copy_and_hide():
    # Create a new collection for the copied objects
    new_collection = bpy.data.collections.new("SpinWiz")
    bpy.context.scene.collection.children.link(new_collection)

    # Get selected objects
    selected_objects = bpy.context.selected_objects
    
    for original_obj in selected_objects: 
        # Create a new object by copying the original
        new_obj = original_obj.copy()
        new_obj.data = original_obj.data.copy()  # Also copy mesh data if needed
        
        # Remove the new object from all collections it is currently part of
        for col in new_obj.users_collection:
            col.objects.unlink(new_obj)  
        
        # Link the new object to the new collection
        new_collection.objects.link(new_obj)
        
        # Optionally, you can make the new object the active object
        bpy.context.view_layer.objects.active = new_obj
        new_obj.select_set(True)
       
    # Hide all collections except the new one
    for collection in bpy.context.scene.collection.children:
        if collection != new_collection:
            collection.hide_viewport = True
            collection.hide_render = True
    
            
    # Hide all objects in the scene of the current context, that are not in any collection
    for obj in bpy.context.scene.collection.objects:
        obj.hide_viewport = True
        obj.hide_render = True

    return new_collection

class OBJECT_OT_spin_wiz_setup(bpy.types.Operator):
    bl_idname = "object.spin_wiz_setup"
    bl_label = "Spin Wiz Setup"
    bl_description = "This operator creates the setup for Spin Wiz"

    def execute(self, context):
        collection = create_copy_and_hide()
        # create_pivot(collection)

        return {"FINISHED"}

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
