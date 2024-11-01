import bpy

from bpy.app.handlers import persistent

from mathutils import Vector
from math import pi, radians
import math

from .naming_convetions import *

from .settings.settings_defaults import *

current_rename = None

#__________________________________________ CONTEXT FUNCTIONS
# functions that help setup and update the correct objects and properties

def switch_to_spinwiz():
                
    scene = get_spinwiz_scene()
        
    scene.spinwiz_old_scene = bpy.context.scene.name

    bpy.context.window.scene = scene

    change_perspective()
    
    str = scene.spinwiz_last_looked
    
    
    
    if len(scene.collection.children) > 0: 
        pivot = None
        for obj in bpy.data.collections[str].objects:
            if pivot_object_name in obj.name:
                pivot = obj
                break
        
        if pivot is not None:
            make_obj_active(pivot)
            return 
    

    scene.spinwiz_spin_settings.dropdown_collections = "None"        
        # hide_anything_but(scene.collection.children[0])

        # hide_anything_but(bpy.data.collections[ str ])
                            
   
              

def get_spinwiz_scene():
    if scene_name in bpy.data.scenes:
        return bpy.data.scenes[scene_name] 
    return None

def create_spinwiz_scene():
    # Check if the scene exists
    if scene_name not in bpy.data.scenes:
        
        # get the current scene
        source_scene = bpy.context.scene
        
        # Create the scene if it does not exist
        bpy.data.scenes.new(name=scene_name)
        
        # set target scene
        target_scene = bpy.data.scenes[scene_name]
        
        # copy the render settings of old scenes
        
        # Copy Render Engine
        target_scene.render.engine = source_scene.render.engine
        
        # Check if the source scene uses Cycles before copying Cycles settings
        if source_scene.render.engine == 'CYCLES':
            # Copy Feature Set (SUPPORTED or EXPERIMENTAL)
            target_scene.cycles.feature_set = source_scene.cycles.feature_set
            
            # Copy Device (CPU or GPU)
            target_scene.cycles.device = source_scene.cycles.device
            
            target_scene.cycles.use_preview_adaptive_sampling = source_scene.cycles.use_preview_adaptive_sampling
            target_scene.cycles.preview_adaptive_threshold = source_scene.cycles.preview_adaptive_threshold
            target_scene.cycles.preview_samples = source_scene.cycles.preview_samples
            target_scene.cycles.preview_adaptive_min_samples = source_scene.cycles.preview_adaptive_min_samples
            
            target_scene.cycles.use_preview_denoising = source_scene.cycles.use_preview_denoising
            target_scene.cycles.preview_denoiser = source_scene.cycles.preview_denoiser
            target_scene.cycles.preview_denoising_input_passes = source_scene.cycles.preview_denoising_input_passes
            target_scene.cycles.preview_denoising_start_sample = source_scene.cycles.preview_denoising_start_sample
            
            target_scene.cycles.use_adaptive_sampling = source_scene.cycles.use_adaptive_sampling
            target_scene.cycles.adaptive_threshold = source_scene.cycles.adaptive_threshold
            target_scene.cycles.samples = source_scene.cycles.samples
            target_scene.cycles.adaptive_min_samples = source_scene.cycles.adaptive_min_samples
            target_scene.cycles.time_limit = source_scene.cycles.time_limit
            
            target_scene.cycles.use_denoising = source_scene.cycles.use_denoising
            target_scene.cycles.denoiser = source_scene.cycles.denoiser
            target_scene.cycles.denoising_input_passes = source_scene.cycles.denoising_input_passes
            target_scene.cycles.denoising_prefilter = source_scene.cycles.denoising_prefilter
            target_scene.cycles.denoising_use_gpu = source_scene.cycles.denoising_use_gpu
            
        if source_scene.render.engine == "EEVEE":
            target_scene.eevee.taa_render_samples = source_scene.eevee.taa_render_samples
            target_scene.eevee.taa_samples = source_scene.eevee.taa_samples
            target_scene.eevee.use_taa_reprojection = source_scene.eevee.use_taa_reprojection

                
    return bpy.data.scenes[scene_name]


def get_current_lookat_pivot():
    collection = get_current_collection()
    
    for obj in collection.objects:
        if pivot_track_name in obj.name:
            return obj
        
    return None

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
    active_collection = bpy.context.view_layer.active_layer_collection
    
    if active_collection is not None and not bpy.context.scene.collection:
        return bpy.data.collections[active_collection.name]
    
    
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

    if collection is not None:        
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

def hide_anything_but(new_collection, only_collections = False):
    
    if new_collection is None:
        change_perspective('PERSP')
    
    scene = get_spinwiz_scene()
    # Hide all collections except the new one
    for collection in scene.collection.children:
        # Hide the collection in the active view layer
        for view_layer in scene.view_layers:
            layer_collection = view_layer.layer_collection.children.get(collection.name)
        
            if layer_collection:
                if collection != new_collection:
                    layer_collection.hide_viewport = True
                    collection.hide_render = True
                else:
                    layer_collection.hide_viewport = False
                    collection.hide_render = False
            
            
    if not only_collections:   
        
        # Get the default "Scene Collection"
        scene_collection = scene.collection
    
        # Iterate through all objects in the scene
        for obj in scene.objects:
            # Check if the object is only in the "Scene Collection" and not in any other collections
            if len(obj.users_collection) == 1 and scene_collection in obj.users_collection:
                # Hide the object from the viewport using hide_set
                obj.hide_set(True)
                obj.hide_render = True
 
 
def get_collection_origin(objects):
    if len(objects) == 0:
        return (0,0,0)
    
    # Initialize variables to sum up vertex positions
    total_vertices = 0
    total_position = Vector((0.0, 0.0, 0.0))

    for obj in objects:
        if obj.type == 'MESH' and obj.data is not None and hasattr(obj.data, 'vertices'):
            for vertex in obj.data.vertices:
                total_position += obj.matrix_world @ vertex.co
                total_vertices += 1

    if total_vertices == 0:
        return (0, 0, 0)
    
    return total_position / total_vertices 

# the min and max coordinates in any direction, return a tuple    
def get_collection_bounding_box(pivot):
    # Initialize min and max values using the first corner
    min_corner = [float('inf'), float('inf'), float('inf')]
    max_corner = [-float('inf'), -float('inf'), -float('inf')]

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
    bpy.ops.object.select_all(action='DESELECT')
    if obj is not None:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    

old_collection_names = []    
old_selection = None

def move_item(collection, from_index, to_index):
    if from_index < 0 or from_index >= len(collection) or to_index < 0 or to_index >= len(collection):
        print(f"Invalid move from {from_index} to {to_index}. Index out of bounds.")
        return
    
    # Create a temporary list of items to reorder
    items = [item for item in collection]
    
    collection.move(from_index, to_index)
                    

def change_perspective(perspective = 'CAMERA'):
    bpy.context.scene.camera = get_current_camera()
    
    # Iterate through all areas in the current screen
    for area in bpy.context.screen.areas:
        # Check if the area is a 3D view
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Change the view to camera perspective
                    space.region_3d.view_perspective = perspective
                    break

old_collection = None

def update_scene_frame(collection_name = None, scene = None):
    global old_collection
    
    if old_collection == get_current_collection().name: 
        return 

    old_collection = get_current_collection().name
    
    if collection_name is None:
        collection_name = get_current_collection().name
    
    if scene is None:
        scene = bpy.context.scene
    
    spin_settings = getattr(scene, collection_name)

    scene.frame_current = spin_settings.start_frame
    scene.frame_start = spin_settings.start_frame
    scene.frame_end = spin_settings.start_frame + spin_settings.nr_frames - 1 
    
def update_current_world(collection_name = None, scene = None):
        
    if collection_name is None:
        collection_name = get_current_collection().name
    
    if scene is None:
        scene = bpy.context.scene
        
    spin_settings = getattr(scene, collection_name)
    
    spin_settings.add_lighting_setup = spin_settings.add_lighting_setup

  
    
def update_current_stage(collection_name = None, scene = None):
           
    if collection_name is None:
        collection_name = get_current_collection().name
    
    if scene is None:
        scene = bpy.context.scene
        
    spin_settings = getattr(scene, collection_name)

    if spin_settings.add_stage:
        spin_settings.stage_height_offset = spin_settings.stage_height_offset
        spin_settings.stage_subdivision = spin_settings.stage_subdivision
        spin_settings.stage_material_color = spin_settings.stage_material_color
        spin_settings.stage_material_roughness = spin_settings.stage_material_roughness
        spin_settings.stage_material_reflection_intensity = spin_settings.stage_material_reflection_intensity
        spin_settings.stage_material_contact_shadow = spin_settings.stage_material_contact_shadow

@persistent
def spinwiz_frame_change_handler(scene): 
    
    if not scene.spinwiz_spin_settings.is_rendering:
        # only run it if the are any setups in the addon
        if len(scene.spinwiz_collections_list) > 0:   
            if get_current_collection():
                spin_settings = getattr(scene, get_current_collection().name) 
                spin_settings.camera_height = spin_settings.camera_height
                spin_settings.camera_tracking_height_offset = spin_settings.camera_tracking_height_offset
                spin_settings.camera_distance = spin_settings.camera_distance
    return 

@persistent
def spinwiz_update_current_selection(scene):
    
    if scene.name == scene_name:
        global current_rename
        current_rename = None

        current_collection_names = [col.name for col in scene.collection.children]

        if len(current_collection_names) !=  len(scene.spinwiz_collections_list):
            # check if old collections are still here
            for index, item in enumerate(scene.spinwiz_collections_list):
                if item.name not in current_collection_names:
                    delattr(bpy.types.Scene, item.name)
                    scene.spinwiz_collections_list.remove(index)
                    

            for index, item in enumerate(scene.spinwiz_old_collections):
                if item not in current_collection_names:
                    scene.spinwiz_old_collections.remove(index)

            # in the case where the collection removed is the one we looked at, it will not siplay anything so by defalut we 
            # switch the dropdown value to please select a collection so we dont display garbage
            scene.spinwiz_spin_settings.dropdown_collections = "NONE"

        if len(scene.spinwiz_collections_list) > 0:
            current_collection_names = [col.name for col in scene.collection.children]

            if len(scene.spinwiz_old_collections) == 0:
                for name in current_collection_names:
                    item = scene.spinwiz_old_collections.add()
                    item.name = name

            old_collection_names = [item.name for item in scene.spinwiz_old_collections]


            current = set(current_collection_names)
            old = set(old_collection_names)

            if current != old:

                scene.spinwiz_old_collections.clear()

                for item in current_collection_names:
                    nig = scene.spinwiz_old_collections.add()
                    nig.name = item

                # Find unique elements
                new_name = current - old
                old_name = old     - current

              
                    
                if len(old_name) > 0 and len(new_name) > 0:
                    new_name = list(new_name)[0]
                    old_name = list(old_name)[0]
                    
                    scene.spinwiz_last_looked = new_name


                    if hasattr(bpy.types.Scene, old_name):
                        new_item = scene.spinwiz_collections_list.add()
                        new_item.name = new_name

                        for index, item in enumerate(scene.spinwiz_collections_list):
                            if item.name == old_name:
                                move_item(scene.spinwiz_collections_list, len(scene.spinwiz_collections_list) - 1, index)
                                scene.spinwiz_collections_list.remove(index + 1)
                                break

                        spin_settings = getattr(scene, old_name)
                        setattr(bpy.types.Scene, new_name, spin_settings)
                        delattr(bpy.types.Scene, old_name)


                        for index, item in enumerate(scene.spinwiz_output_list):
                            if item.name == old_name:
                                new_item = scene.spinwiz_output_list.add()
                                new_item.name = new_name

                                move_item(scene.spinwiz_output_list, len(scene.spinwiz_output_list) - 1, index)
                                scene.spinwiz_output_list.remove(index + 1)
                                break


            current_selection = bpy.context.view_layer.objects.active

            global old_selection

            if old_selection != current_selection and not scene.spinwiz_is_setting_up:

                if is_selection_setup(current_selection):
                    hide_anything_but(current_selection.users_collection[0])

                    update_scene_frame()

                    update_current_world()

                    update_current_stage()
                    
                    set_active_collection(get_current_collection())

                    change_perspective()

                    scene.spinwiz_spin_settings.dropdown_collections = current_selection.users_collection[0].name
                    
                elif current_selection:
                    
                    hide_anything_but(current_selection.users_collection[0], True)

                    current_selection.hide_set(False)

                old_selection = current_selection
            
def is_selection_valid():
    
    # Iterate through the selected objects
    correct_selection = True
    
    if is_selection_setup(bpy.context.active_object) and len(bpy.context.scene.spinwiz_collections_list) > 0:
        return True
    
    if len(bpy.context.view_layer.objects.selected) == 0:
        return False
    
    for obj in bpy.context.view_layer.objects.selected:
        if not (obj.type in ["MESH", "CURVE", "CURVES", "EMPTY", "ARMATURE", "SURFACE", "TEXT", "POINTCLOUD"]) or not (obj.name in bpy.context.scene.objects): # and not collection_name in [col.name for col in obj.users_collection]:
            # update the current context such that the UI reflects the selection
            print(obj.type)
            correct_selection = False
    
    if get_spinwiz_scene() is not None and get_spinwiz_scene().spinwiz_spin_settings.dropdown_collections == "NONE" and bpy.context.scene == get_spinwiz_scene():
        return False
            
    return correct_selection


def is_selection_setup(current_selection):
    
    if current_selection is not None:
        current_obj = current_selection
        
        # Traverse up the hierarchy until an object without a parent is found
        while current_obj.parent is not None:
            current_obj = current_obj.parent
        
        for name in [cam_pivot_object_name, pivot_object_name, camera_object_name, curve_object_name, stage_name, pivot_track_name]:
            if name in current_obj.name:
                return True
        
    return False

def is_camera(current_selection):
    return current_selection.type == "CAMERA" or cam_pivot_object_name in current_selection.name

def is_pivot(current_selection):
    parent = current_selection
    while parent.parent is not None:
        parent = parent.parent
        
    return parent.type == "EMPTY" and pivot_object_name in parent.name

def is_stage(current_selection):
    return stage_name in current_selection.name
        
def set_active_collection(collection):
    if collection:

        # Find the collection in the current view layer and set it as active
        for layer_collection in bpy.context.view_layer.layer_collection.children:
            if layer_collection.collection == collection:
                bpy.context.view_layer.active_layer_collection = layer_collection
                layer_collection.exclude = False  # Make sure it's not hidden
                return





def setup_spincamera():  
    # camera that will rotate around the object
    create_camera()
    
    camera = get_current_camera()

    # the pivot, parent of the camera
    pivot = create_cam_pivot()

    if pivot.animation_data is None:
        pivot.animation_data_create()
    
    pivot.animation_data.action = get_current_action()

    radius = get_track_radius()
    if camera.location.x < pivot.location.x + radius: 
        camera.location = pivot.location + Vector((radius, 0, get_current_lookat_pivot().location.z))
        
    # set the pivot point as the parent so that the rotation is the same
    camera.parent = pivot

    set_camera_track()

    make_obj_active(get_current_pivot())


def setup_spinobject():
    
    create_camera()

    camera = get_current_camera()

    pivot = get_current_pivot()

    if pivot.animation_data is None:
        pivot.animation_data_create()

    pivot.animation_data.action = get_current_action() 

    radius = get_track_radius()
    if camera.location.x < pivot.location.x + radius: 
        camera.location = pivot.location + Vector((radius, 0, get_current_lookat_pivot().location.z)) 

    set_camera_track()

    make_obj_active(pivot)
 
def add_keyframes(): 
    spin_settings = getattr(get_spinwiz_scene(), get_current_collection().name)
    
    num_frames = (spin_settings.nr_frames)
    action = get_current_action()
    
    # offset is the offset of the start frame of the animation
    offset = int(spin_settings.start_frame)

    # Create keyframes
    fcurve = action.fcurves.find("rotation_euler", index=2)
    if fcurve is None:
        fcurve = action.fcurves.new(data_path="rotation_euler", index=2)

    interpolation_type = "LINEAR"
    if "BEZIER" in spin_settings.interpolation_type:
        interpolation_type = "BEZIER"
        

    # initial frame
    rotation_value = radians(0)
    keyframe_point = fcurve.keyframe_points.insert(offset, rotation_value)
    keyframe_point.interpolation = interpolation_type

    # end frame   
    if spin_settings.spin_direction == "right": 
        rotation_value = radians(360)
    else:
        rotation_value = radians(-360)
        
    rotation_value = rotation_value * spin_settings.spin_amount
    
    num_frames = num_frames * spin_settings.spin_amount
            
    keyframe_point = fcurve.keyframe_points.insert(num_frames + offset , rotation_value)
    
    keyframe_point.interpolation = interpolation_type

    # Set the scene's end frame
    get_spinwiz_scene().frame_start = offset
    get_spinwiz_scene().frame_end = num_frames

def remove_keyframes():
    action = get_current_action()

    fcurve = action.fcurves.find("rotation_euler", index=2)
    if fcurve is None:
        return 
    else:
        fcurve.keyframe_points.clear()


def set_camera_track():
    target = get_current_lookat_pivot()
    
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

    dimensions = [max_corner[0] - min_corner[0] , max_corner[1] - min_corner[1], max_corner[2] - min_corner[2]]
    
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
    

    bpy.ops.object.camera_add(location= get_collection_origin(get_current_collection().objects))
    camera_object = bpy.context.active_object
    

    camera_object.name = camera_object_name
    camera_object.data.name = camera_object_name
    
    # add properties
    
    camera_object.data.lens = camera_settings.camera_focal_length
    # camera_object.location += Vector((camera_settings.camera_distance, 0, camera_settings.camera_height))


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
    prev_settings = getattr(get_spinwiz_scene(), collection_name)
    

    current_collection = get_current_collection()
    current_settings = getattr(get_spinwiz_scene(), current_collection.name)
    
    current_settings.spin_direction = prev_settings.spin_direction
    
    # animation settings
    current_settings.movement_type = prev_settings.movement_type
    current_settings.degrees = prev_settings.degrees
    current_settings.nr_frames = prev_settings.nr_frames
    current_settings.start_frame = prev_settings.start_frame
    current_settings.interpolation_type = prev_settings.interpolation_type
    current_settings.length_type = prev_settings.length_type
    current_settings.spin_amount = prev_settings.spin_amount
    
    # lighting settings
    if prev_settings.add_lighting_setup:
        current_settings.add_lighting_setup = prev_settings.add_lighting_setup
    current_settings.lighting_type = prev_settings.lighting_type
    current_settings.lighting_hdr_strength = prev_settings.lighting_hdr_strength
    current_settings.lighting_hdr_rotation = prev_settings.lighting_hdr_rotation
    current_settings.lighting_gradient_height = prev_settings.lighting_gradient_height
    current_settings.lighting_gradient_scale = prev_settings.lighting_gradient_scale
    
    # camera settings
    current_settings.camera_height = prev_settings.camera_height # get_current_camera().location.z
    current_settings.camera_focal_length = prev_settings.camera_focal_length
    current_settings.camera_distance = prev_settings.camera_distance # get_current_camera().location.x
    current_settings.camera_tracking_height_offset = prev_settings.camera_tracking_height_offset # get_current_camera().location.z
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
    
    current_settings = getattr(get_spinwiz_scene(), current_collection.name)
    
    # animation settings
    current_settings.movement_type = default_movement_type
    current_settings.degrees = default_degrees
    current_settings.nr_frames = default_length
    current_settings.start_frame = default_start_frame
    current_settings.interpolation_type = default_interpolation
    current_settings.length_type = default_length_type
    current_settings.spin_amount = default_spin_amount
    
    #lighting settings
    current_settings.add_lighting_setup = default_has_lighting_setup
    current_settings.lighting_type = default_lighting_type
    current_settings.lighting_hdr_rotation = default_hdr_rotation
    current_settings.lighting_hdr_strength = default_hdr_strength
    current_settings.lighting_gradient_height = default_gradient_height
    current_settings.lighting_gradient_scale = default_gradient_scale
    
    # camera settings
    current_settings.camera_height = get_current_camera().location.z
    current_settings.camera_focal_length = default_camera_focal_length
    current_settings.camera_distance = get_current_camera().location.x
    current_settings.camera_tracking_height_offset = get_current_camera().location.z
    
    # stage settings
    current_settings.add_stage = default_has_stage
    current_settings.stage_height_offset = default_stage_height_offset
    current_settings.stage_subdivision = default_stage_subdivision   

    # stage material
    current_settings.stage_material_color = default_color
    current_settings.stage_material_roughness = default_roughness
    current_settings.stage_material_reflection_intensity = default_reflection_intensity
    current_settings.stage_material_contact_shadow = default_contact_shadow
    