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
from math import pi
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

camera_object = None

class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "360 Spinner"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '360 Spinner'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Testicular Torsion!")

        print(camera_object)
        if camera_object:
            col = layout.column()
            col.prop(camera_object, "location", text="Location")
            col = layout.column()
            col.prop(camera_object, "rotation_euler", text="Rotation")

        layout.separator()
        row = layout.row()
        row.operator("object.add_360_spinner_camera",
                        text="Add 360 Spinner Camera")    




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

        # Close the spline to make it cyclic
        spline.use_cyclic_u = True

        return curve_object

    def set_camera_track(self, camera, target):
        # Add a 'Track To' constraint to the camera
        track_to = camera.constraints.new(type='TRACK_TO')

        # Set the target of the constraint
        track_to.target = target

        # Configure the constraint
        track_to.track_axis = 'TRACK_NEGATIVE_Z'    # Camera looks along the -Z axis
        track_to.up_axis = 'UP_Y'                   # Y axis is considered up

    def set_camera_follow(self, camera, curve):
        # Add Follow Path constraint to the camera
        follow_path_constraint = camera.constraints.new(type='FOLLOW_PATH')
        follow_path_constraint.target = curve  # Set the curve as the target for the constraint
        follow_path_constraint.use_fixed_location = False  # Ensure the camera stays on the curve

        # Set keyframes for the constraint's offset property
        follow_path_constraint.offset = 0  # Start position at the beginning of the curve
        follow_path_constraint.keyframe_insert(data_path='offset', frame=1)  # Insert keyframe at frame 1

        # Move to the end of the animation (adjust frame number as needed)
        bpy.context.scene.frame_end = 250  # Example: set end frame

        follow_path_constraint.offset = 100  # End position at the end of the curve (adjust as needed)
        follow_path_constraint.keyframe_insert(data_path='offset', frame=250)  # Insert keyframe at frame 250



    def execute(self, context):
        # get selected object 
        obj = context.object
        

        global camera_object
        # Create a new camera object


        bpy.ops.object.camera_add(rotation=(pi/2,0,pi/2))
        camera_object = bpy.context.active_object

        dimension = max(obj.dimensions)/2
        render_settings = bpy.context.scene.render
        aspect_ratio = (render_settings.resolution_x / render_settings.resolution_y) / (camera_object.data.sensor_width/camera_object.data.sensor_height)
        sensor_width_half = camera_object.data.sensor_width/2/1000
        sensor_height_half = camera_object.data.sensor_height/2/1000
 
        # This only applies in the case wehre the aspect ratio of the camera makes it so the height is lower than the, width (TODO check different cases)
        # Increase the margins of the object by increasing the dimensions of the object with a certain amount
        dimension += 0.5
        distance_height = dimension/(sensor_height_half) * (camera_object.data.lens/1000) * aspect_ratio 
        distance_width =  dimension/(sensor_width_half)  * (camera_object.data.lens/1000)

        distance = max(distance_height, distance_width)


        camera_object.location = obj.location + Vector((distance + dimension, 0, 0))


        curve_object = self.create_bezier_circle(Vector((obj.location - camera_object.location)).length, obj.location)
        camera_object.location = obj.location

        self.set_camera_follow(camera_object, curve_object)
        
        self.set_camera_track(camera_object, obj)


        
        camera_object.name = "360 Spinner Camera"
        camera_object.data.name = "360 Spinner Camera"

        return {'FINISHED'}

class_list = [VIEW3D_PT_main_panel, OBJECT_OT_add_360_spinner_camera]

def register():
    for cls in class_list:
        bpy.utils.register_class(cls)

    
def unregister():
    for cls in class_list:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
