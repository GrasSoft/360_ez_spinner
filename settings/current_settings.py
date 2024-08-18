import bpy

class CurrentSettings():
    
    def __init__(self, length_type="Keyframes", length=72, start_frame=1, interpolation_type="LINEAR", movement_type="object", has_stage=False, has_lighting_setup=False) -> None:     
        # related to nr of frames
        self.current_length_type = length_type
        self.current_length = length
        self.current_start_frame = start_frame

        # interpolation type 
        self.current_interpolation = interpolation_type

        # movement type
        self.current_movement_type = movement_type

        # has stage
        self.current_has_stage = has_stage

        # has lighting setup
        self.current_has_lighting_setup = has_lighting_setup



previous_settings = CurrentSettings()


#____________________________ Helper Functions


def update_current_settings():
    selected_obj = bpy.context.object
    spin_settings = bpy.context.scene.spin_settings

    if selected_obj:
            global previous_settings

            previous_settings = CurrentSettings(spin_settings.length_type, spin_settings.nr_frames, spin_settings.start_frame,
                                                spin_settings.interpolation_type, spin_settings.movement_type, spin_settings.add_stage, spin_settings.add_lighting_setup)

                        
def update_properties():
    spin_settings = bpy.context.scene.spin_settings
    
    global previous_settings
    
    spin_settings.nr_frames = previous_settings.current_length
    spin_settings.start_frame = previous_settings.current_start_frame
    spin_settings.add_stage = previous_settings.current_has_stage
    spin_settings.add_lighting_setup = previous_settings.current_has_lighting_setup
    spin_settings.movement_type = previous_settings.current_movement_type
    spin_settings.imterpolation_type = previous_settings.current_interpolation
    spin_settings.length_type = previous_settings.current_length_type
    