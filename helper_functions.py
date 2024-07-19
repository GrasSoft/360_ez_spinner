import bpy
from mathutils import Vector
from math import pi, radians
import math

from .naming_convetions import *

def reset_obj(obj):
    obj.rotation_euler = (0,0,0)     

def delete_obj(obj):
    obj = bpy.data.objects[obj]

    # Remove object from all collections it is linked to
    for collection in obj.users_collection:
        collection.objects.unlink(obj)
    
    # Delete the object if it has no other users
    if obj.users == 0:
        bpy.data.objects.remove(obj)

def reset_anim():
    bpy.context.scene.frame_set(0)

def remove_camera():
    if is_object_valid(cam_pivot_object_name):
        delete_obj(cam_pivot_object_name)
    if is_object_valid(camera_object_name):
        delete_obj(camera_object_name)
    if is_object_valid(curve_object_name):
        delete_obj(curve_object_name)

def create_cam_pivot():
    # Create an empty object
    bpy.ops.object.empty_add(location=bpy.data.objects[pivot_object_name].location)  # Location of the other pivot
    empty_obj = bpy.context.object

    empty_obj.name = cam_pivot_object_name

    # remove object from any collection it is currently in
    for col in empty_obj.users_collection:
        col.objects.unlink(empty_obj)  
    
    bpy.data.collections[collection_name].objects.link(empty_obj)

    return empty_obj

def make_obj_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def setup_spincamera():
    # camera that will rotate around the object
    create_camera()

    # the pivot, parent of the camera
    pivot = create_cam_pivot()

    if pivot.animation_data is None:
        pivot.animation_data_create()
    
    pivot.animation_data.action = bpy.data.actions[action_name]

    # TODO: temp change
    # radius = get_track_radius(obj)
    # create_bezier_circle(radius, obj.location)
    radius = 5
    bpy.data.objects[camera_object_name].location = pivot.location + Vector((radius, 0, 0))

    # set the pivot point as the parent so that the rotation is the same
    bpy.data.objects[camera_object_name].parent = pivot

    set_camera_track(pivot)

    make_obj_active(pivot)


def setup_spinobject():
    create_camera()

    pivot = bpy.data.objects[pivot_object_name] 

    if pivot.animation_data is None:
        pivot.animation_data_create()

    pivot.animation_data.action = bpy.data.actions[action_name]   

    # TODO: temp change
    #radius = get_track_radius(obj)
    radius = 5
    bpy.data.objects[camera_object_name].location = pivot.location + Vector((radius, 0, 0)) 

    set_camera_track(pivot)

    make_obj_active(pivot)

def add_keyframes():
    spin_settings = bpy.context.scene.spin_settings
    num_frames = (spin_settings.nr_frames)
    action = bpy.data.actions[action_name]

    # Convert rotation amount to radians
    rotation_amount_radians = radians(360)

    # Create keyframes
    for frame in range(num_frames + 1):
        fcurve = action.fcurves.find("rotation_euler", index=2)
        if fcurve is None:
            fcurve = action.fcurves.new(data_path="rotation_euler", index=2)
        
        rotation_value = rotation_amount_radians * frame / num_frames
        keyframe_point = fcurve.keyframe_points.insert(frame, rotation_value)
        keyframe_point.interpolation = spin_settings.interpolation_type

    # Set the scene's end frame
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = num_frames

def remove_keyframes():
    action = bpy.data.actions[action_name]

    fcurve = action.fcurves.find("rotation_euler", index=2)
    if fcurve is None:
        return 
    else:
        fcurve.keyframe_points.clear()



# Function to check if the object is valid
def is_object_valid(object_name):
    return object_name in bpy.data.objects

def set_camera_track(target):

    camera_object = bpy.data.objects[camera_object_name]
    # Add a 'Track To' constraint to the camera
    track_to = camera_object.constraints.new(type='TRACK_TO')

    # Set the target of the constraint
    track_to.target = target

    # Configure the constraint
    track_to.track_axis = 'TRACK_NEGATIVE_Z'    # Camera looks along the -Z axis
    track_to.up_axis = 'UP_Y'                   # Y axis is considered up

def get_camera_information():
    camera_object = bpy.data.objects[camera_object_name]

    render_settings = bpy.context.scene.render

    # this is the aspect ratio of the redner resolution divided by the aspect ratio of the sensor, used to scale the height of the image        
    aspect_ratio_correction = (render_settings.resolution_x / render_settings.resolution_y) / (camera_object.data.sensor_width/camera_object.data.sensor_height)
    
    # half of the sensor width, scaled to mm
    sensor_width_half = camera_object.data.sensor_width/2/1000

    # half of the sensor height, scaled to mm
    sensor_height_half = camera_object.data.sensor_height/2/1000

    return (aspect_ratio_correction, sensor_width_half, sensor_height_half)

def get_track_radius(obj):
    camera_object = bpy.data.objects[camera_object_name]


    (aspect_ratio_correction, sensor_width_half, sensor_height_half) = get_camera_information()

    dimension = max(obj.dimensions)/2
    # This only applies in the case wehre the aspect ratio of the camera makes it so the height is lower than the, width (TODO check different cases)
    # Increase the margins of the object by increasing the dimensions of the object with a certain amount
    dimension += 0.5
    distance_height = dimension/(sensor_height_half) * (camera_object.data.lens/1000) * aspect_ratio_correction
    distance_width =  dimension/(sensor_width_half)  * (camera_object.data.lens/1000)

    # take the maximum distance out out of the 2 so we make sure every part of the object is in the frame
    return max(distance_height, distance_width)

def create_camera():
    # Store references to the currently selected and active objects
    selected_objects = bpy.context.selected_objects
    active_objects = bpy.context.view_layer.objects.active

    bpy.ops.object.camera_add()
    camera_object = bpy.context.active_object

    camera_object.name = camera_object_name
    camera_object.data.name = camera_object_name

    for col in camera_object.users_collection:
        col.objects.unlink(camera_object)    
        
    bpy.data.collections[collection_name].objects.link(camera_object)

    # Restore the selection and active object
    for obj in selected_objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = active_objects
    if active_objects:
        active_objects.select_set(True)

def create_bezier_circle(radius, origin):

    selected_objects = bpy.context.selectable_objects
    active_objects = bpy.context.view_layer.objects.active

    # Calculate control points
    control_point = radius * (4 * (math.sqrt(2) - 1) / 3)

    # Create a new Bezier curve
    curve_data = bpy.data.curves.new('BezierCircle', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 64

    # Create a new object with the curve data
    curve_object = bpy.data.objects.new('BezierCircle', curve_data)
    bpy.context.collection.objects.link(curve_object)

    # Create a spline for the Bezier curve
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(3)  # Total 4 points for a circle

    points = spline.bezier_points

    # Define the points for the circle
    points[0].co = (radius, 0.0, 0.0)
    points[0].handle_right = (radius, control_point, 0.0)
    points[0].handle_left = (radius, -control_point, 0.0)

    points[1].co = (0.0, radius, 0.0)
    points[1].handle_right = (-control_point, radius, 0.0)
    points[1].handle_left = (control_point, radius, 0.0)

    points[2].co = (-radius, 0.0, 0.0)
    points[2].handle_right = (-radius, -control_point, 0.0)
    points[2].handle_left = (-radius, control_point, 0.0)

    points[3].co = (0.0, -radius, 0.0)
    points[3].handle_right = (control_point, -radius, 0.0)
    points[3].handle_left = (-control_point, -radius, 0.0)

    # Set the origin of the curve
    curve_object.location = origin

    curve_object.name = curve_object_name
    curve_object.data.name = curve_object_name

    # Close the spline to make it cyclic
    spline.use_cyclic_u = True

    # Restore the selection and active object
    for obj in selected_objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = active_objects
    if active_objects:
        active_objects.select_set(True)

    return curve_object

