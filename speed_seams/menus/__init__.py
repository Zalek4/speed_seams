import bpy
from .panels import SPEEDSEAMS_PT_MainPanel, SPEEDSEAMS_MT_PieMenu

classes = (SPEEDSEAMS_PT_MainPanel, SPEEDSEAMS_MT_PieMenu)


def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
