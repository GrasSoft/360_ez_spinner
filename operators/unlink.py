import bpy
from ..naming_convetions import bl_idname_unlink, pivot_object_name
from ..helper_functions import get_current_collection, make_obj_active

class OBJECT_OT_spinwiz_unlinked(bpy.types.Operator):
    bl_idname = bl_idname_unlink
    bl_label = "Unlink"
    bl_description = "Unlinks the objects in the collection permanently"
        
    def execute(self, context):
        collection = get_current_collection()
        
        spin_settings = getattr(context.scene, collection.name)
        
        spin_settings.unlinked = True
        
        pivot = None
        for obj in collection.objects:
            if pivot_object_name in obj.name:
                pivot = obj
                break
        
        if pivot is not None:
            # Apply the operations recursively
            self.make_single_user_recursive(pivot)
            
            make_obj_active(pivot)
            return {'FINISHED'}
        
        return {'CANCELLED'}
    
    def make_single_user_recursive(self, obj):
        # Make Single User for the current object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.make_single_user(type='ALL', object=True)

        # Recursively call for all children
        for child in obj.children:
            self.make_single_user_recursive(child)
