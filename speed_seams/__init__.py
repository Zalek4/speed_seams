
import importlib
import sys
import bpy
bl_info = {
    "name": "Speed Seams",
    "author": "Alex Hallenbeck, Blake Darrow",
    "version": (0, 4, 3),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Speed Seams",
    "description": "",
    "category": "Tools",
    "wiki_url": "",
}

#-----------------------------------------------------#
#     register the modules
#-----------------------------------------------------#


def register():
    from .register import register_addon
    register_addon()


def unregister():
    from .register import unregister_addon
    unregister_addon()
