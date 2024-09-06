import bpy
from mathutils import Vector
from math import pi, radians
import math

from .naming_convetions import *

from .settings.settings_defaults import *

#__________________________________________ CONTEXT FUNCTIONS
# functions that help setup and update the correct objects and properties

# this function gets the current collection based on the selected object
def get_current_world():
    collection = get_current_collection()
   
    if "current_world" in collection: 
        return bpy.data.worlds[collection["current_world"]]

def get_original_world():
    collection = get_current_collection()

    if "original_world" in collection:    
        return bpy.data.worlds[collection["original_world"]]

def get_current_collection():
    if bpy.context.object is not None:
        return bpy.context.object.users_collection[0]

def get_current_stage():
    collection = get_current_collection()

    for obj in collection.objects:
        if stage_name in obj.name:
            return obj
    
    return None

def get_current_material():
    stage = get_current_stage()
    
    if stage is not None:
        return stage.modifiers["SpinWiz_StageCTRL"]["Socket_6"]

def get_current_camera():
    collection = get_current_collection()
        
    for obj in collection.objects:
        if camera_object_name in obj.name:
            return obj

    return None
  
def get_current_pivot():
    collection = get_current_collection()
        
    for obj in collection.objects:
        if pivot_object_name in obj.name:
            return obj

    return None

def get_current_camera_pivot():
    collection = get_current_collection()
        
    for obj in collection.objects:
        if cam_pivot_object_name in obj.name:
            return obj

    return None

def get_suffix_difference(str1, str2):
    # Find the common prefix length
    common_length = min(len(str1), len(str2))
    
    for i in range(common_length):
        if str1[i] != str2[i]:
            # Return the part of str2 that comes after the common prefix
            return str2[i:]
    
    # If one string is a prefix of the other, return the suffix of str2
    return str2[common_length:]

def get_current_action():
    collection = get_current_collection()
    
    name = collection["action"]
    
    return bpy.data.actions[name]    

#__________________________________________ HELPER FUNCTIONS

def hide_anything_but(new_collection):
    
    # Hide all collections except the new one
    for collection in bpy.context.scene.collection.children:
        # Hide the collection in the active view layer
        for view_layer in bpy.context.scene.view_layers:
            layer_collection = view_layer.layer_collection.children.get(collection.name)
        
            if layer_collection:
                if collection != new_collection:
                    layer_collection.hide_viewport = True
                else:
                    layer_collection.hide_viewport = False
            
            
       
       
    # Get the default "Scene Collection"
    scene_collection = bpy.context.scene.collection
   
    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is only in the "Scene Collection" and not in any other collections
        if len(obj.users_collection) == 1 and scene_collection in obj.users_collection:
            # Hide the object from the viewport using hide_set
            obj.hide_set(True)
 
def get_collection_origin(pivot):
    x, y, z = 0,0,0

    for obj in pivot.children:
        x += obj.location.x
        y += obj.location.y
        z += obj.location.z
    l = len(pivot.children)

    return (x/l, y/l, z/l)

# the min and max coordinates in any direction, return a tuple    
def get_collection_bounding_box(pivot):
    # Initialize min and max values using the first corner
    min_corner = list(pivot.location)
    max_corner = list(pivot.location)

    for obj in pivot.children:
        bounding_box = obj.bound_box

        for corner in bounding_box:
            for i in range(3):  # X, Y, Z axes
                min_corner[i] = min(min_corner[i], corner[i])
                max_corner[i] = max(max_corner[i], corner[i])

    return (min_corner, max_corner)



def reset_obj(obj):
    obj.rotation_euler = (0,0,0)     
    
def reset_anim():
    bpy.context.scene.frame_set(0)



def delete_obj(obj):
    obj = bpy.data.objects[obj]

    # Remove object from all collections it is linked to
    for collection in obj.users_collection:
        collection.objects.unlink(obj)
    
    # Delete the object if it has no other users
    if obj.users == 0:
        bpy.data.objects.remove(obj)
                
# Function to check if the object is valid
def is_object_valid(object_name):
    return object_name in bpy.data.objects


def remove_camera():
    cam_pivot = get_current_camera_pivot()
    camera = get_current_camera()
    
    if cam_pivot is not None:
        delete_obj(cam_pivot.name)

    if camera is not None:
        delete_obj(camera.name)

def create_cam_pivot():
    collection = get_current_collection()
    
    # Create an empty object
    bpy.ops.object.empty_add(location=bpy.context.object.location)  # Location of the other pivot
    
    empty_obj = bpy.context.object

    empty_obj.name = cam_pivot_object_name

    # remove object from any collection it is currently in
    for col in empty_obj.users_collection:
        col.objects.unlink(empty_obj)  
    
    collection.objects.link(empty_obj)
    
    return empty_obj

def make_obj_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def setup_spincamera():  
    # camera that will rotate around the object
    create_camera()
    
    camera = get_current_camera()

    # the pivot, parent of the camera
    pivot = create_cam_pivot()

    if pivot.animation_data is None:
        pivot.animation_data_create()
    
    pivot.animation_data.action = get_current_action()

    # TODO: temp change
    # radius = get_track_radius(obj)
    # create_bezier_circle(radius, obj.location)
    radius = get_track_radius()
    if camera.location.x < pivot.location.x + radius: 
        camera.location = pivot.location + Vector((radius, 0, 0))

    # set the pivot point as the parent so that the rotation is the same
    camera.parent = pivot

    set_camera_track(pivot)

    make_obj_active(get_current_pivot())


def setup_spinobject():
    create_camera()

    camera = get_current_camera()

    pivot = get_current_pivot()

    if pivot.animation_data is None:
        pivot.animation_data_create()

    pivot.animation_data.action = get_current_action() 

    # TODO: temp change
    #radius = get_track_radius(obj)
    radius = get_track_radius()
    if camera.location.x < pivot.location.x + radius: 
        camera.location = pivot.location + Vector((radius, 0, 0)) 

    set_camera_track(pivot)

    make_obj_active(pivot)

 
def add_keyframes(): 
    spin_settings = getattr(bpy.context.scene, get_current_collection().name)
    
    num_frames = (spin_settings.nr_frames)
    action = get_current_action()
    
    # offset is the offset of the start frame of the animation
    offset = int(spin_settings.start_frame)

    # Create keyframes
    fcurve = action.fcurves.find("rotation_euler", index=2)
    if fcurve is None:
        fcurve = action.fcurves.new(data_path="rotation_euler", index=2)

    # initial frame
    rotation_value = radians(0)
    keyframe_point = fcurve.keyframe_points.insert(offset, rotation_value)
    keyframe_point.interpolation = spin_settings.interpolation_type

    # end frame    
    rotation_value = radians(360)
    keyframe_point = fcurve.keyframe_points.insert(num_frames + offset + 1, rotation_value)
    keyframe_point.interpolation = spin_settings.interpolation_type

    # Set the scene's end frame
    bpy.context.scene.frame_start = offset
    bpy.context.scene.frame_end = num_frames + offset

def remove_keyframes():
    action = get_current_action()

    fcurve = action.fcurves.find("rotation_euler", index=2)
    if fcurve is None:
        return 
    else:
        fcurve.keyframe_points.clear()


def set_camera_track(target):
    camera_object = get_current_camera()
    # Add a 'Track To' constraint to the camera
    track_to = camera_object.constraints.new(type='TRACK_TO')

    # Set the target of the constraint
    track_to.target = target

    # Configure the constraint
    track_to.track_axis = 'TRACK_NEGATIVE_Z'    # Camera looks along the -Z axis
    track_to.up_axis = 'UP_Y'                   # Y axis is considered up


def get_camera_information():
    camera_object = get_current_camera()

    render_settings = bpy.context.scene.render

    # this is the aspect ratio of the redner resolution divided by the aspect ratio of the sensor, used to scale the height of the image        
    aspect_ratio_correction = (render_settings.resolution_x / render_settings.resolution_y) / (camera_object.data.sensor_width/camera_object.data.sensor_height)
    
    # half of the sensor width, scaled to mm
    sensor_width_half = camera_object.data.sensor_width/2/1000

    # half of the sensor height, scaled to mm
    sensor_height_half = camera_object.data.sensor_height/2/1000

    return (aspect_ratio_correction, sensor_width_half, sensor_height_half)


def get_track_radius():
    camera_object = get_current_camera()

    (aspect_ratio_correction, sensor_width_half, sensor_height_half) = get_camera_information()

    (min_corner, max_corner) = get_collection_bounding_box(get_current_pivot())

    dimensions = [max_corner[0] - min_corner[0], max_corner[1] - min_corner[1], max_corner[2] - min_corner[2]]
    dimension = max(dimensions)/2
    # This only applies in the case wehre the aspect ratio of the camera makes it so the height is lower than the, width (TODO check different cases)
    # Increase the margins of the object by increasing the dimensions of the object with a certain amount
    dimension += 0.5
    distance_height = dimension/(sensor_height_half) * (camera_object.data.lens/1000) * aspect_ratio_correction
    distance_width =  dimension/(sensor_width_half)  * (camera_object.data.lens/1000)

    # take the maximum distance out out of the 2 so we make sure every part of the object is in the frame
    return max(distance_height, distance_width)

def create_camera():
    camera_settings = getattr(bpy.context.scene, get_current_collection().name)
    
    # Store references to the currently selected and active objects
    selected_objects = bpy.context.selected_objects
    active_objects = bpy.context.view_layer.objects.active

    # get the collection name from the collection of the current selected object
    collection = get_current_collection()
    collection_name = collection.name
    

    bpy.ops.object.camera_add()
    camera_object = bpy.context.active_object

    camera_object.name = camera_object_name
    camera_object.data.name = camera_object_name
    
    # add properties
    
    camera_object.data.lens = camera_settings.camera_focal_length
    camera_object.location = (camera_settings.camera_distance, 0, camera_settings.camera_height)

    for col in camera_object.users_collection:
        col.objects.unlink(camera_object)   
           
    collection.objects.link(camera_object)

    # Restore the selection and active object
    for obj in selected_objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = active_objects
    if active_objects:
        active_objects.select_set(True)
        
def use_settings_of_other(collection_name):
    prev_settings = getattr(bpy.context.scene, collection_name)
    
    current_collection = get_current_collection()
    current_settings = getattr(bpy.context.scene, current_collection.name)
    
    # collection name 
    current_settings.collection_name = current_collection.name
    
    # animation settings
    current_settings.movement_type = prev_settings.movement_type
    current_settings.degrees = prev_settings.degrees
    current_settings.nr_frames = prev_settings.nr_frames
    current_settings.start_frame = prev_settings.start_frame
    current_settings.interpolation_type = prev_settings.interpolation_type
    current_settings.length_type = prev_settings.length_type
    
    # lighting settings
    current_settings.add_lighting_setup = prev_settings.add_lighting_setup
    current_settings.lighting_type = prev_settings.lighting_type
    current_settings.lighting_hdr_strength = prev_settings.lighting_hdr_strength
    current_settings.lighting_hdr_rotation = prev_settings.lighting_hdr_rotation
    current_settings.lighting_gradient_height = prev_settings.lighting_gradient_height
    current_settings.lighting_gradient_scale = prev_settings.lighting_gradient_scale
    
    # camera settings
    current_settings.camera_height = prev_settings.camera_height
    current_settings.camera_focal_length = prev_settings.camera_focal_length
    current_settings.camera_distance = get_current_camera().location.x
    
    # stage settings
    current_settings.add_stage = prev_settings.add_stage
    current_settings.stage_height_offset = prev_settings.stage_height_offset
    current_settings.stage_subdivision = prev_settings.stage_subdivision
    
    # stage material
    current_settings.stage_material_color = prev_settings.stage_material_color
    current_settings.stage_material_roughness = prev_settings.stage_material_roughness
    current_settings.stage_material_reflection_intensity = prev_settings.stage_material_reflection_intensity
    current_settings.stage_material_contact_shadow = prev_settings.stage_material_contact_shadow
    
    
def reset_default_settings():
    current_collection = get_current_collection()
    current_settings = getattr(bpy.context.scene, current_collection.name)
    
    # animation settings
    current_settings.movement_type = default_movement_type
    current_settings.degrees = default_degrees
    current_settings.nr_frames = default_length
    current_settings.start_frame = default_start_frame
    current_settings.interpolation_type = default_interpolation
    current_settings.length_type = default_length_type
    
    #lighting settings
    current_settings.add_lighting_setup = default_has_lighting_setup
    current_settings.lighting_type = default_lighting_type
    current_settings.lighting_hdr_rotation = default_hdr_rotation
    current_settings.lighting_hdr_strength = default_hdr_strength
    current_settings.lighting_gradient_height = default_gradient_height
    current_settings.lighting_gradient_scale = default_gradient_scale
    
    # camera settings
    current_settings.camera_height = default_camera_height
    current_settings.camera_focal_length = default_camera_focal_length
    
    # stage settings
    current_settings.add_stage = default_has_stage
    current_settings.stage_height_offset = default_stage_height_offset
    current_settings.stage_subdivision = default_stage_subdivision   

    # stage material
    current_settings.stage_material_color = default_color
    current_settings.stage_material_roughness = default_roughness
    current_settings.stage_material_reflection_intensity = default_reflection_intensity
    current_settings.stage_material_contact_shadow = default_contact_shadow
    