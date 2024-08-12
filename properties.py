import bpy
from .icon_setup.custom_icons import *
from .helper_functions import *
from .naming_convetions import *
from .helper_functions import *

from .lighting_setup.lighting_setup import *

from .stage_setup.stage_setup import *

from .settings.current_settings import *

#____________________________ FUNCTIONS RETURNING ITEMS

def interpolation_items(self, context):
    return  [
                ('LINEAR', "", "The animation moves at constant speed", preview_collections["interpolation"]["linear"].icon_id, 0),
                ('BEZIER', "", "The animation start and ends fast",preview_collections["interpolation"]["bezier_fast"].icon_id, 1),
                ('BEZIER', "", "The animation start and ends slow",preview_collections["interpolation"]["bezier_slow"].icon_id, 2),               
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

def menu_items(self, context):
    return [
        ('motion_setup', "Motion Setup", "Here is a panel with all the options regarding the 360 movement", preview_collections["menu"]["motion_menu"].icon_id, 0),
        ('output_setup', "Output Setup", "Here is a panel with all the options regarding 360 output", preview_collections["menu"]["output_menu"].icon_id, 1),
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
    remove_keyframes()
    add_keyframes()



def slow_bezier(self, context):
    action = bpy.data.actions[action_name]
    fcurve = action.fcurves.find("rotation_euler", index=2)
    end_frame = fcurve.keyframe_points[1]

    start_frame = fcurve.keyframe_points[0]
    start_frame.handle_right_type = "ALIGNED"
    start_frame.handle_right.x = int(self.nr_frames / 2)
    start_frame.handle_right.y = 0

    start_frame.handle_left_type = "ALIGNED"
    start_frame.handle_left.x = self.start_frame - 1
    start_frame.handle_left.y = 0


    end_frame.handle_left_type = "ALIGNED"
    end_frame.handle_left.x = int(self.nr_frames / 2)
    end_frame.handle_left.y = radians(360)

    end_frame.handle_right_type = "ALIGNED"
    end_frame.handle_right.x = self.nr_frames + 2
    end_frame.handle_right.y = radians(360)


def update_interpolation(self, context):
    # update the keyframes to have the other interpolation
    remove_keyframes()
    add_keyframes()

    for item in interpolation_items(self, context):
        if self.interpolation_type == item[0]:
            if item[4] == 1:
                slow_bezier(self, context)
            elif item[4] == 2: 
                return  

def update_lighting(self, context):
    if self.add_lighting_setup:
        import_world()
    else:
        reset_world()

def update_stage(self, context):
    if self.add_stage:
        import_stage()
    else:
        reset_stage()

#____________________________ PROPERTY CLASSES

class SpinWiz_properties(bpy.types.PropertyGroup):
    menu_options: bpy.props.EnumProperty(
        name="Menu Options",
        items=menu_items,
        default=0
    )# type: ignore

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
        default = current_length,
        min=1,
        update=update_adjust_keyframes
    )# type: ignore

    start_frame: bpy.props.IntProperty(
        name="Start frame",
        description="Starting keyframe",
        min=1,
        update=update_start_frame,
        default=current_start_frame,
    )# type: ignore

    add_stage: bpy.props.BoolProperty(
        name="Add Stage",
        description="See stage menu",
        default=current_has_stage,
        update=update_stage
    )# type: ignore

    add_lighting_setup: bpy.props.BoolProperty(
        name="Add Lighting Setup",
        description="See lighting setup",
        update=update_lighting,
        default=current_has_lighting_setup
    ) # type: ignore

    movement_type : bpy.props.EnumProperty(
        name= "Movement type",
        description= "Select wether the objects or the camera spins.",
        items= movement_type_items,
        update=update_movement_type,
        default=current_movement_type
    ) # type: ignore


    interpolation_type: bpy.props.EnumProperty(
        name= "Interpolation",
        description= "Select the interpolation between the keyframes.",
        items=interpolation_items,
        update=update_interpolation,
        default=current_interpolation
    ) # type: ignore

    length_type: bpy.props.EnumProperty(
        name= "Length",
        description= "Select the start and end keyframes or by degrees.",
        items= length_items,
        default=current_length_type
    ) # type: ignore


