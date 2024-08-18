import bpy

# array where all the names of collections will be kept with output files wiht settings will be kept
output_list = []

#____________________________ HELPER FUNCTIONS

def get_current_collection(context):
    selected_obj = context.object
    
    if selected_obj is not None:
        return selected_obj.users_collection[0].name


#____________________________ PANEL FUNCTIONS

def output_row(panel, layout, name):
    row = layout.row()    
    
    col = row.column()
    col.operator("object.documentation", text=name)
    col.enabled = False
    
    col = row.column()
    op = row.operator("object.remove_output", text="", icon="TRASH")
    op.name = name
    
def panel_operator_add_to_output(panel, layout):
    # send to output button
    row = layout.row()
    row.operator("object.output", 
                    text="Send to output queue",)

def panel_output_list(panel, layout):
    
    
    global output_list
    
    if len(output_list) == 0:
        layout.label(text="There are not items in the queue")
    else:
        box = layout.box()
        for name in output_list:
            output_row(panel, box, name)
        

#_____________________________ CLASS

class OBJECT_OT_output(bpy.types.Operator):
    bl_idname = "object.output"
    bl_label = "To Output Queue"
    bl_description = "Send object and settings to output queue"

    def execute(self, context):

        global output_list
        
        output_list.append(get_current_collection(context))        
        
        return {"FINISHED"}
    
    
class OBJECT_OT_delete_output(bpy.types.Operator):
    bl_idname = "object.remove_output"
    bl_label = "Remove output item"
    bl_description = "Remove collection from output queue"
    
    name: bpy.props.StringProperty()
    
    def execute(self, context):
        
        global output_list
        
        output_list.remove(self.name)
        
        return {"FINISHED"}