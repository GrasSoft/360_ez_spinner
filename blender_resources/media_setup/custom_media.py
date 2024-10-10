import bpy.utils.previews
import os

icons_path = ""

thumbnails_path = ""

preview_collections = {}


# Icons   
def spin_direction_icons():
    previews = bpy.utils.previews.new()
    
    global icons_path
    global preview_collections
    
    previews.load("right", os.path.join(icons_path, "rotate-arrow-right.png"), "IMAGE")
    previews.load("left", os.path.join(icons_path, "rotate-arrow_left.png"), "IMAGE")

    preview_collections["spin_direction"] = previews    

def interpolation_icons():
    previews = bpy.utils.previews.new()
    global icons_path
    global preview_collections

    previews.load("linear", os.path.join(icons_path, "Lin Int.png"), "IMAGE")
    previews.load("bezier_fast", os.path.join(icons_path, "F-S-F Int.png"), "IMAGE")
    previews.load("bezier_slow", os.path.join(icons_path, "S-F-S Int.png"), "IMAGE")

    preview_collections["interpolation"] = previews

def logo_icon():
    previews = bpy.utils.previews.new()
    global icons_path
    global preview_collections

    previews.load("logo", os.path.join(icons_path, "SpinWiz_Icon.png"), "IMAGE")

    preview_collections["logo"] = previews

def documentation_icon():
    previews = bpy.utils.previews.new()
    global icons_path
    global preview_collections

    previews.load("documentation", os.path.join(icons_path, "Documentation.png"), "IMAGE")

    preview_collections["documentation"] = previews


def menu_icons():
    previews = bpy.utils.previews.new()
    global icons_path
    global preview_collections

    previews.load("motion_menu", os.path.join(icons_path, "Motion Setup.png"), "IMAGE")
    previews.load("output_menu", os.path.join(icons_path, "output.png"), "IMAGE")

    preview_collections["menu"] = previews

def keyframe_icons():
    previews = bpy.utils.previews.new()
    global icons_path
    global preview_collections

    previews.load("degrees", os.path.join(icons_path, "By angle.png"), "IMAGE")
    previews.load("nr_keyframes", os.path.join(icons_path, "By Number of Keyframes.png"), "IMAGE")

    preview_collections["keyframes"] = previews

def progress_icons():
    previews = bpy.utils.previews.new()
    global icons_path
    global preview_collections

    previews.load("prog_0", os.path.join(icons_path, "prog_0.png"), "IMAGE")
    previews.load("prog_25", os.path.join(icons_path, "prog_25.png"), "IMAGE")
    previews.load("prog_50", os.path.join(icons_path, "prog_50.png"), "IMAGE")
    previews.load("prog_75", os.path.join(icons_path, "prog_75.png"), "IMAGE")
    previews.load("prog_100", os.path.join(icons_path, "prog_100.png"), "IMAGE")

    preview_collections["progress"] = previews

def spinwiz_import_custom_icons():
    global icons_path
    icons_path = os.path.join(os.path.dirname(__file__), "icons")

    keyframe_icons()
    progress_icons()   
    spin_direction_icons() 
    logo_icon()
    interpolation_icons()
    menu_icons()
    documentation_icon()

# Thumbnails

def spinwiz_import_thumbnails():
    global preview_collections
    
    global thumbnails_path
    thumbnails_path = os.path.join(os.path.dirname(__file__), "../../lighting_setup/thumbnails")
    
    previews = bpy.utils.previews.new()
    
    previews.load("gradient", os.path.join(thumbnails_path, "gradient.png"), "IMAGE")
    previews.load("hdr",      os.path.join(thumbnails_path, "studio_small_09.png"), "IMAGE")

    preview_collections["thumbnail"] = previews
    
