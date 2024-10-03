import bpy

from .blender_resources.media_setup.custom_media import *
from .helper_functions import *
from .naming_convetions import *
from .helper_functions import *

from .lighting_setup.lighting_setup import *

from .stage_setup.stage_setup import *

from .settings.settings_defaults import *

#____________________________ FUNCTIONS RETURNING ITEMS

def spin_direction_items(self, context):
    return [
        ('right', "", "The object/s turn to the right", preview_collections["spin_direction"]["right"].icon_id, 0),
        ('left', "", "The object/s turn to the left", preview_collections["spin_direction"]["left"].icon_id, 1),
    ]

def interpolation_items(self, context):
    return  [
                ('LINEAR', "", "The animation moves at constant speed", preview_collections["interpolation"]["linear"].icon_id, 0),
                ('BEZIER_SLOW', "", "The animation start and ends fast",preview_collections["interpolation"]["bezier_fast"].icon_id, 1),
                ('BEZIER_FAST', "", "The animation start and ends slow",preview_collections["interpolation"]["bezier_slow"].icon_id, 2),               
        ]

def length_items(self, context):
    return [
            ('Keyframes', "By nr keyframes", "Set the number of keyframes of the animation",preview_collections["keyframes"]["nr_keyframes"].icon_id, 0),
            ('Degrees', "By degrees", "Set the number of keyframes by degrees",preview_collections["keyframes"]["degrees"].icon_id, 1),
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
    
def lighting_type_items(self, context):
    return [
        ("HDR", "HDR Lighting", "Set up the lighting with an HDR image",preview_collections["thumbnail"]["hdr"].icon_id, 0),
        ("GRADIENT", "Gradient Lighting", "Set up lighting with a gradient",preview_collections["thumbnail"]["gradient"].icon_id, 1),
    ]
    
def dynamic_dropdown_items(self, context):
    items = context.scene.collections_list
    
    dropdown_items = []
    
    for item in items:
        dropdown_items.append((item.name, item.name, ""))
        
    return dropdown_items
#____________________________ UPDATE FUNCTIONS

def update_spin_direction(self, context):
    update_interpolation(self, context)

def update_menu_options(self, context):
    global current_rename
    current_rename = None

def update_current_collection(self, context):
    collection = bpy.data.collections[self.dropdown_collections]
    
    pivot = None
    
    for obj in collection.objects:
        if pivot_object_name in obj.name:
            pivot = obj
            break
    
    # make the pivot as the selected object
    if pivot is not None and pivot not in context.selected_objects:
        make_obj_active(pivot)

def update_movement_type(self, context):
    scene = context.scene
    current_collection = get_current_collection()
    spin_settings = getattr(scene, get_current_collection().name)
    
    remove_camera()
    reset_anim()
    # reset_obj(context.object)
        
    if spin_settings.movement_type == "object":
        setup_spinobject()
        # this removes the keyframes from the other object
        
        pivot = get_current_camera_pivot()
        if pivot is not None:
            pivot.animation_data.action = None
    else:
        setup_spincamera()  

        pivot = get_current_pivot()
        if pivot is not None:
            pivot.animation_data.action = None
            

def update_adjust_keyframes(self, context):
    # these all work on actions
    remove_keyframes()
    add_keyframes()
    
    # update_movement_type(self, context)
    
    action = get_current_action()
    if self.movement_type == "object":
        pivot = get_current_pivot()
        pivot.animation_data.action = action 
    else:
        cam_pivot = get_current_camera_pivot()
        cam_pivot.animation_data.action = action
        

# give degrees, update nr of frames
def update_nr_frames(self, context):
    self.nr_frames = int(360 / int(self.degrees)) 


def update_start_frame(self, context):
    context.scene.frame_start = self.start_frame
    remove_keyframes()
    add_keyframes()


def slow_bezier(self, context):
    action = get_current_action()
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
    if self.spin_direction == "right":
        end_frame.handle_left.y = radians(360)
    else:
        end_frame.handle_left.y = radians(-360)
    end_frame.handle_right_type = "ALIGNED"
    end_frame.handle_right.x = self.nr_frames + 2
    if self.spin_direction == "right":
        end_frame.handle_right.y = radians(360)
    else:
        end_frame.handle_right.y = radians(-360)


def fast_bezier(self, context):
    action = get_current_action()
    fcurve = action.fcurves.find("rotation_euler", index=2)
    end_frame = fcurve.keyframe_points[1]

    start_frame = fcurve.keyframe_points[0]
    start_frame.handle_right_type = "ALIGNED"
    start_frame.handle_right.x = self.start_frame
    if self.spin_direction == "right":
        start_frame.handle_right.y = radians(180)
    else:
        start_frame.handle_right.y = radians(-180)

    start_frame.handle_left_type = "ALIGNED"
    start_frame.handle_left.x = self.start_frame
    if self.spin_direction == "right":
        start_frame.handle_left.y = radians(-1)
    else:
        start_frame.handle_left.y = radians(1)

    end_frame.handle_left_type = "ALIGNED"
    end_frame.handle_left.x = self.nr_frames + 1
    if self.spin_direction == "right":
        end_frame.handle_left.y = radians(180)
    else:
        end_frame.handle_left.y = radians(-180)

    end_frame.handle_right_type = "ALIGNED"
    end_frame.handle_right.x = self.nr_frames + 1
    if self.spin_direction == "right":
        end_frame.handle_right.y = radians(361)
    else:
        end_frame.handle_right.y = radians(-361)

def update_interpolation(self, context):
    # update the keyframes to have the other interpolation
    remove_keyframes()
    add_keyframes()


    if self.interpolation_type == "BEZIER_SLOW":
        slow_bezier(self, context)
        return
    
    if self.interpolation_type == "BEZIER_FAST":
        fast_bezier(self, context)
        return

#_________________________________ LIGHTING            

def update_lighting(self, context):
    if self.add_lighting_setup:
        import_world()
    else:
        reset_world()

def update_lighting_type(self, context):
    world = get_current_world()
    
    if world is None:
        return
    
    links = world.node_tree.links
    nodes = world.node_tree.nodes
    
    gradient_node = nodes["Background"]
    hdr_node = nodes["Background.001"]
    
    background = nodes["World Output"]
    
    if self.lighting_type == "HDR":
        links.new(hdr_node.outputs[0], background.inputs[0])
    else:
        links.new(gradient_node.outputs[0], background.inputs[0])
        
        
def update_lighting_hdr_rotation(self, context):
    world = get_current_world()

    if world is None:
        return
    
    nodes = world.node_tree.nodes
    
    nodes["Mapping"].inputs[2].default_value[2] = self.lighting_hdr_rotation
    
def update_lighting_hdr_strength(self, context):
    world = get_current_world()

    if world is None:
        return
    
    nodes = world.node_tree.nodes
    
    nodes["Background"].inputs[1].default_value = self.lighting_hdr_strength
    
def update_lighting_gradient_height(self, context):
    world = get_current_world()

    if world is None:
        return
    
    nodes = world.node_tree.nodes
    
    nodes["Gradient Height"].inputs[0].default_value = self.lighting_gradient_height

def update_lighting_gradient_scale(self, context):
    world = get_current_world()

    if world is None:
        return
    
    nodes = world.node_tree.nodes
    
    val = self.lighting_gradient_scale
    nodes["Mapping.001"].inputs[3].default_value = Vector((val, val, val))
    
    
#_________________________________ STAGE

def update_stage(self, context):
    if self.add_stage:
        import_stage()
        update_stage_height_offset(self, context)
        update_stage_subdivision(self, context)
    else:
        reset_stage()

def update_stage_height_offset(self, context):
    stage = get_current_stage()
    
    if self.add_stage:
        modifier = bpy.data.objects[stage.name].modifiers.get("SpinWiz_StageCTRL")
        modifier["Socket_3"] = self.stage_height_offset 
        
        bpy.data.objects[stage.name].data.update()               

def update_stage_subdivision(self, context):
    stage = get_current_stage()
    
    if self.add_stage:
        modifier = bpy.data.objects[stage.name].modifiers.get("SpinWiz_StageCTRL")
        modifier["Socket_5"] = self.stage_subdivision
         
        bpy.data.objects[stage.name].data.update() 
              
def update_stage_material(self, context):
    if self.add_stage:
        material = get_current_material()
        node = material.node_tree.nodes["BackgroundShader"]
        
        node.inputs[1].default_value = (*self.stage_material_color, 1.0)
        node.inputs[0].default_value = self.stage_material_roughness
        node.inputs[2].default_value = self.stage_material_reflection_intensity
        node.inputs[3].default_value = self.stage_material_contact_shadow

#________________________________ CAMERA

def update_camera_height(self, context):
    cam_obj = get_current_camera()
    
        
    if cam_obj is not None:
        cam_obj.location.z =  self.camera_height


def update_camera_distance(self, context):
    cam_obj = get_current_camera()
    
    if cam_obj is not None:
        cam_obj.location.x = self.camera_distance
        
def update_camera_focal_length(self, context):
    cam_obj = get_current_camera()
    
    if cam_obj is not None:
        cam_obj.data.lens = self.camera_focal_length
        
    
def update_lookat_pivot(self, context):
    lookat_pivot = get_current_lookat_pivot()
    
    lookat_pivot.location.z = self.camera_tracking_height_offset 
            
#____________________________ PROPERTY CLASSES

class SpinWiz_collection_properties(bpy.types.PropertyGroup):
         
    # animation settings
    spin_direction: bpy.props.EnumProperty(
        name = "Spin Direction",
        description = "Change the direciton of the spin",
        items=spin_direction_items,
        default=0,
        update = update_spin_direction,
    ) #type: ignore
    
    degrees: bpy.props.EnumProperty(
        name="Nr of degrees",
        description="Number of degrees between frames",
        items=degrees_items, 
        update=update_nr_frames,
        default=3,
    )# type: ignore

    nr_frames: bpy.props.IntProperty(
        name="# of frames",
        description="Number of keyframes",
        min=1,
        update=update_adjust_keyframes,
        default = default_length,
    )# type: ignore

    start_frame: bpy.props.IntProperty(
        name="Start frame",
        description="Starting keyframe",
        min=1,
        update=update_start_frame,
        default=default_start_frame,
    )# type: ignore
    
    movement_type : bpy.props.EnumProperty(
        name= "Movement type",
        description= "Select wether the objects or the camera spins.",
        items= movement_type_items,
        update=update_movement_type,
        default=0
    ) # type: ignore

    interpolation_type: bpy.props.EnumProperty(
        name= "Interpolation",
        description= "Select the interpolation between the keyframes.",
        items=interpolation_items,
        update=update_interpolation,
        default=0
    ) # type: ignore

    length_type: bpy.props.EnumProperty(
        name= "Length",
        description= "Select the start and end keyframes or by degrees.",
        items= length_items,
        default=0
    ) # type: ignore

    # lighting settings
    add_lighting_setup: bpy.props.BoolProperty(
        name="Add Lighting Setup",
        description="See lighting setup",
        update=update_lighting,
        default=default_has_lighting_setup
    ) # type: ignore
    
    lighting_type: bpy.props.EnumProperty(
        name= "Lighting type",
        description= "Chose the lighting type", 
        default= 1,
        items= lighting_type_items,
        update=update_lighting_type,
    ) # type: ignore
    
    lighting_hdr_rotation: bpy.props.FloatProperty(
        name= "Rotation",
        description = "Rotation of the HDRI",
        default= default_hdr_rotation,
        update=update_lighting_hdr_rotation
    ) # type: ignore
    
    lighting_hdr_strength: bpy.props.FloatProperty(
        name = "Strength",
        description = "Change the strenght of the HDRI",
        default= default_hdr_strength,
        update=update_lighting_hdr_strength          
    ) # type: ignore
    
    lighting_gradient_height: bpy.props.FloatProperty(
        name = "Height",
        description = "Height of the gradient",
        default= default_gradient_height,
        update=update_lighting_gradient_height
    ) # type: ignore
    
    lighting_gradient_scale: bpy.props.FloatProperty(
        name = "Scale",
        description = "Scale of the gradient",
        default= default_gradient_scale,
        update=update_lighting_gradient_scale
    ) # type: ignore
    
    #camera settings
    camera_height: bpy.props.FloatProperty(
        name= "Camera Height",
        description= "Sets the height of the camera",
        default = 0,
        subtype='DISTANCE',
        update = update_camera_height, 
    )# type: ignore

    camera_tracking_height_offset: bpy.props.FloatProperty(
        name= "Camera tracking height offset",
        description= "Set the offset height of where the camera is looking",
        default= 0,
        update=update_lookat_pivot
    )# type: ignore
    
    camera_distance: bpy.props.FloatProperty(
        name= "Camera Distance",
        description= "Sets the distance from the camera to the object",
        subtype='DISTANCE',
        default = 5,
        update= update_camera_distance
    )# type: ignore
    
    camera_focal_length: bpy.props.FloatProperty(
        name = "Camera Focal Length",
        description= "Sets the focal length of the camera",
        default= 50,
        update=update_camera_focal_length
    )# type: ignore

    # stage settings 
    add_stage: bpy.props.BoolProperty(
        name="Add Stage",
        description="See stage menu",
        update=update_stage,
        default=default_has_stage,
    )# type: ignore

    stage_height_offset: bpy.props.FloatProperty(
        name = "Stage Height Offset",
        description= "Sets the height of the stage",
        update=update_stage_height_offset,
        min = 0,
        default = 15,
    )# type: ignore

    stage_subdivision: bpy.props.IntProperty(
        name = "Stage Subdivisions",
        description = "Sets the number of subdivisions",
        min = 1,
        default = 2,
        update = update_stage_subdivision,
    )# type: ignore    
    
    stage_material_color: bpy.props.FloatVectorProperty(
        name = "Material Color",
        description= "Choose the color of the material",
        subtype= 'COLOR',
        default=default_color,
        update= update_stage_material 
    )# type: ignore
    
    stage_material_roughness: bpy.props.FloatProperty(
        name = "Material Roughness",
        description= "Choose material roughness",
        default= default_roughness,
        update= update_stage_material
    )# type: ignore
    
    stage_material_reflection_intensity: bpy.props.FloatProperty(
        name= "Material Reflection Intensity",
        description= "Choose material reflection intensity",
        default= default_reflection_intensity,
        update= update_stage_material,
    )# type: ignore
    
    stage_material_contact_shadow: bpy.props.FloatProperty(
        name= "Material Contact Shadow",
        description= "Choose material contact shadow",
        default= default_contact_shadow,
        update= update_stage_material,
    )# type: ignore





class SpinWiz_properties(bpy.types.PropertyGroup):   
     
    menu_options: bpy.props.EnumProperty(
        name="Menu Options",
        items=menu_items,
        default=0,
        update= update_menu_options, 
    )# type: ignore
    
    enable_render: bpy.props.BoolProperty(
        name = "Enable Render",
        description = "Enable render button after the last render is done",
        default= False,
    ) # type: ignore
    
    is_rendering: bpy.props.BoolProperty(
        name = "Is rendering",
        description= "This will be true when the add-on is rendering",
        default=False,
    ) # type: ignore
    
    current_rendered_collection: bpy.props.StringProperty(
        name = "Collection Name",
        description = "Name of current collection being rendered",
    ) # type: ignore

    output_filepath: bpy.props.StringProperty(
        name = "Output filepath",
        description = "The filepath where the rendered images will be saved",
        default= ""
    ) # type: ignore
    
    dropdown_collections: bpy.props.EnumProperty(
        name = "Dropdown Collection",
        description = "Dropdown to select the collection you want to work on",
        items = dynamic_dropdown_items,
        update= update_current_collection
    ) # type: ignore
  