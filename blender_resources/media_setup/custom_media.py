import bpy.utils.previews
import os

icons_path = ""

thumbnails_path = ""

preview_collections = {}


# Icons   

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

    previews.load("logo", os.path.join(icons_path, "EZ Spin Icon.png"), "IMAGE")

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


def import_custom_icons():
    global icons_path
    icons_path = os.path.join(os.path.dirname(__file__), "icons")
    
    logo_icon()
    interpolation_icons()
    menu_icons()
    documentation_icon()

# Thumbnails

def import_thumbnails():
    global preview_collections
    
    global thumbnails_path
    thumbnails_path = os.path.join(os.path.dirname(__file__), "../../lighting_setup/thumbnails")
    
    previews = bpy.utils.previews.new()
    
    previews.load("gradient", os.path.join(thumbnails_path, "gradient.png"), "IMAGE")
    previews.load("hdr",      os.path.join(thumbnails_path, "studio_small_09.png"), "IMAGE")

    preview_collections["thumbnail"] = previews
    
