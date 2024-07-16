import bpy
from mathutils import Vector
from math import pi, radians
import math

camera_object_name = "360 Spinner Camera"
curve_object_name = "Camera Track Curve"

def reset_obj(obj):
    obj.rotation_euler = (0,0,0)     

def delete_obj(obj):
    # Remove object from all collections it is linked to
    for collection in obj.users_collection:
        collection.objects.unlink(obj)
    
    # Delete the object if it has no other users
    if obj.users == 0:
        bpy.data.objects.remove(obj)

def reset_anim():
    bpy.context.scene.frame_set(0)

def remove_all_keyframes(obj):
    # Check if the object has animation data
    if obj.animation_data:
        action = obj.animation_data.action
        if action:
            # Iterate through each FCurve and remove it
            for fcurve in action.fcurves:
                action.fcurves.remove(fcurve)


def remove_spincamera():
    if is_object_valid(camera_object_name):
        delete_obj(bpy.data.objects[camera_object_name])
    if is_object_valid(curve_object_name):
        delete_obj(bpy.data.objects[curve_object_name])

def setup_spincamera():
    # get selected object 
    obj = bpy.context.object
    
    create_camera()

    radius = get_track_radius(obj)
    create_bezier_circle(radius, obj.location)
    
    # order matters
    set_camera_follow()
    
    set_camera_track(obj)

def setup_spinobject():
    obj = bpy.context.object

    add_keyframes(obj, 100)

    create_camera()

    radius = get_track_radius(obj)
    bpy.data.objects[camera_object_name].location = obj.location + Vector((radius, 0, 0)) 

    set_camera_track(obj)

def add_keyframes(obj, num_frames):
    # Convert rotation amount to radians
    rotation_amount_radians = radians(360)

    # Create keyframes
    for frame in range(num_frames + 1):
        bpy.context.scene.frame_set(frame)
        obj.rotation_euler[2] = rotation_amount_radians * frame / num_frames
        obj.keyframe_insert(data_path="rotation_euler", index=2)

    # Set the scene's end frame
    bpy.context.scene.frame_end = num_frames



# Function to check if the object is valid
def is_object_valid(object_name):
    return object_name in bpy.data.objects


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

def set_camera_track(target):

    camera_object = bpy.data.objects[camera_object_name]
    # Add a 'Track To' constraint to the camera
    track_to = camera_object.constraints.new(type='TRACK_TO')

    # Set the target of the constraint
    track_to.target = target

    # Configure the constraint
    track_to.track_axis = 'TRACK_NEGATIVE_Z'    # Camera looks along the -Z axis
    track_to.up_axis = 'UP_Y'                   # Y axis is considered up

def set_camera_follow():
    
    camera_object = bpy.data.objects[camera_object_name]
    curve = bpy.data.objects[curve_object_name]

    # Add Follow Path constraint to the camera
    follow_path_constraint = camera_object.constraints.new(type='FOLLOW_PATH')
    follow_path_constraint.target = curve  # Set the curve as the target for the constraint
    follow_path_constraint.use_fixed_location = False  # Ensure the camera stays on the curve

    # Set keyframes for the constraint's offset property
    follow_path_constraint.offset = 0  # Start position at the beginning of the curve
    follow_path_constraint.keyframe_insert(data_path='offset', frame=1)  # Insert keyframe at frame 1

    # Move to the end of the animation (adjust frame number as needed)
    bpy.context.scene.frame_end = 250  # Example: set end frame

    follow_path_constraint.offset = 100  # End position at the end of the curve (adjust as needed)
    follow_path_constraint.keyframe_insert(data_path='offset', frame=250)  # Insert keyframe at frame 250

    # Set interpolation type to Linear for both keyframes
    action = camera_object.animation_data.action
    if action:
        for fcurve in action.fcurves:
            if fcurve.data_path == f'constraints["{follow_path_constraint.name}"].offset':
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'LINEAR'


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

    # Restore the selection and active object
    for obj in selected_objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = active_objects
    if active_objects:
        active_objects.select_set(True)

