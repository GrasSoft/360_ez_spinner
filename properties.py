import bpy
from .custom_icons import *
from .helper_functions import *
from .naming_convetions import *
from .helper_functions import *

#____________________________ FUNCTIONS RETURNING ITEMS

def interpolation_items(self, context):
    return  [
                ('LINEAR', "", "The animation moves at constant speed", preview_collections["interpolation"]["linear"].icon_id, 0),
                ('Bezier_fast', "", "The animation start and ends fast",preview_collections["interpolation"]["bezier_fast"].icon_id, 1),
                ('Bezier_slow', "", "The animation start and ends slow",preview_collections["interpolation"]["bezier_slow"].icon_id, 2),               
        ]

def length_items(self, context):
    return [
            ('Keyframes', "", "",'WORLD_DATA', 0),
            ('Degrees', "", "",'WORLD_DATA', 1),
        ]

def degrees_items(self, context):
    return [
                ('1', "1", ""),
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
        ]

def movement_type_items(self, context):
    return [
            ('object', "Object rotates", "The camera stays in place and object rotates",0),
            ('camera', "Camera rotates", "The object stays in place and camera rotates",1),    
        ]


#____________________________ UPDATE FUNCTIONS


def update_movement_type(self, context):
    scene = context.scene
    spin_settings = scene.spin_settings
    
    remove_camera()
    reset_anim()
    # reset_obj(context.object)
        
    if spin_settings.movement_type == "object":
        setup_spinobject()
        # this removes the keyframes from the other object
        if is_object_valid(cam_pivot_object_name) :
            bpy.data.objects[cam_pivot_object_name].animation_data.action = None
    else:
        setup_spincamera()  

        if is_object_valid(pivot_object_name):
            bpy.data.objects[pivot_object_name].animation_data.action = None
    


def update_adjust_keyframes(self, context):
    # these all work on actions
    remove_keyframes()
    add_keyframes()
    update_movement_type(self, context)




# give degrees, update nr of frames
def update_nr_frames(self, context):
    self.nr_frames = int(360 / int(self.degrees))    



def update_start_frame(self, context):
    context.scene.frame_start = self.start_frame
#____________________________ PROPERTY CLASSES

class SpinWiz_properties(bpy.types.PropertyGroup):
    degrees: bpy.props.EnumProperty(
        name="Nr of degrees",
        description="Number of degrees between frames",
        items=degrees_items, 
        default=3,
        update=update_nr_frames
    )# type: ignore

    nr_frames: bpy.props.IntProperty(
        name="# of frames",
        description="Number of keyframes",
        default = 72,
        update=update_adjust_keyframes
    )# type: ignore

    start_frame: bpy.props.IntProperty(
        name="Start frame",
        description="Starting keyframe",
        default = 0,
        min=0,
        update=update_start_frame
    )# type: ignore

    add_stage: bpy.props.BoolProperty(
        name="Add Stage",
        description="See stage menu",
        default=False
    )# type: ignore

    add_lighting_setup: bpy.props.BoolProperty(
        name="Add Lighting Setup",
        description="See lighting setup",
        default=False
    ) # type: ignore

    movement_type : bpy.props.EnumProperty(
        name= "Movement type",
        description= "Select wether the objects or the camera spins.",
        items= movement_type_items,
        update=update_movement_type
    ) # type: ignore


    interpolation_type: bpy.props.EnumProperty(
        name= "Interpolation",
        description= "Select the interpolation between the keyframes.",
        items=interpolation_items
    ) # type: ignore

    length_type: bpy.props.EnumProperty(
        name= "Length",
        description= "Select the start and end keyframes or by degrees.",
        items= length_items
    ) # type: ignore


