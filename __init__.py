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
from mathutils import Vector
from math import pi, radians
import math

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

camera_object_name = "360 Spinner Camera"
curve_object_name = "Camera Track Curve"

# Function to check if the object is valid
def is_object_valid(object_name):
    return object_name in bpy.data.objects

class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "360 Spinner"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '360 Spinner'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Testicular Torsion!")

        if is_object_valid(camera_object_name):
            camera_object = bpy.data.objects[camera_object_name]
            col = layout.column()
            col.prop(camera_object, "location", text="Location")
            col = layout.column()
            col.prop(camera_object, "rotation_euler", text="Rotation")

        layout.separator()
        row = layout.row()
        row.operator("object.add_360_spinner_camera",
                        text="Add 360 Spinner Camera")
        row = layout.row()
        row.operator("object.spin_object",
                        text="Spin selected object")    

class OBJECT_OT_spin_object(bpy.types.Operator):
    bl_idname = "object.spin_object"
    bl_label = "Spin object"
    bl_description = "Spin the object around by 360 degrees"

    def add_keyframes(self, obj, num_frames):
        # Convert rotation amount to radians
        rotation_amount_radians = radians(360)

        # Create keyframes
        for frame in range(num_frames + 1):
            bpy.context.scene.frame_set(frame)
            obj.rotation_euler[2] = rotation_amount_radians * frame / num_frames
            obj.keyframe_insert(data_path="rotation_euler", index=2)

        # Set the scene's end frame
        bpy.context.scene.frame_end = num_frames

    def execute(self, context):
        obj = context.object

        self.add_keyframes(obj, 100)

        return {'FINISHED'}


class OBJECT_OT_add_360_spinner_camera(bpy.types.Operator):
    bl_idname = "object.add_360_spinner_camera"
    bl_label = "Add 360 Spinner Camera"
    bl_description = "Add a camera at (0, 0, 0) with rotation (0, 0, 0) named '360 Spinner Camera'"

    def create_bezier_circle(self, radius, origin):
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

        return curve_object

    def set_camera_track(self, target):

        camera_object = bpy.data.objects[camera_object_name]
        # Add a 'Track To' constraint to the camera
        track_to = camera_object.constraints.new(type='TRACK_TO')

        # Set the target of the constraint
        track_to.target = target

        # Configure the constraint
        track_to.track_axis = 'TRACK_NEGATIVE_Z'    # Camera looks along the -Z axis
        track_to.up_axis = 'UP_Y'                   # Y axis is considered up

    def set_camera_follow(self):
     
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

    def get_camera_information(self):
        camera_object = bpy.data.objects[camera_object_name]

        render_settings = bpy.context.scene.render

        # this is the aspect ratio of the redner resolution divided by the aspect ratio of the sensor, used to scale the height of the image        
        aspect_ratio_correction = (render_settings.resolution_x / render_settings.resolution_y) / (camera_object.data.sensor_width/camera_object.data.sensor_height)
        
        # half of the sensor width, scaled to mm
        sensor_width_half = camera_object.data.sensor_width/2/1000
 
        # half of the sensor height, scaled to mm
        sensor_height_half = camera_object.data.sensor_height/2/1000

        return (aspect_ratio_correction, sensor_width_half, sensor_height_half)

    def get_track_radius(self, obj):
        camera_object = bpy.data.objects[camera_object_name]


        (aspect_ratio_correction, sensor_width_half, sensor_height_half) = self.get_camera_information()

        dimension = max(obj.dimensions)/2
        # This only applies in the case wehre the aspect ratio of the camera makes it so the height is lower than the, width (TODO check different cases)
        # Increase the margins of the object by increasing the dimensions of the object with a certain amount
        dimension += 0.5
        distance_height = dimension/(sensor_height_half) * (camera_object.data.lens/1000) * aspect_ratio_correction
        distance_width =  dimension/(sensor_width_half)  * (camera_object.data.lens/1000)

        # take the maximum distance out out of the 2 so we make sure every part of the object is in the frame
        return max(distance_height, distance_width)

    def create_camera(self):
        bpy.ops.object.camera_add()
        camera_object = bpy.context.active_object

        camera_object.name = camera_object_name
        camera_object.data.name = camera_object_name



    def execute(self, context):
        # get selected object 
        obj = context.object
        
        global camera_object
        self.create_camera()

   
        radius = self.get_track_radius(obj)
        self.create_bezier_circle(radius, obj.location)
        
        
        # order matters
        self.set_camera_follow()
        
        self.set_camera_track(obj)

        return {'FINISHED'}

class_list = [VIEW3D_PT_main_panel, OBJECT_OT_add_360_spinner_camera, OBJECT_OT_spin_object]

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)

    
def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
