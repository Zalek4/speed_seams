import bpy
from .panels import SPEEDSEAMS_PT_MainPanel, SPEEDSEAMS_MT_QuickSharpPie, SPEEDSEAMS_MT_EdgeToolsPie, SPEEDSEAMS_MT_TransformsToolsPie, SPEEDSEAMS_MT_HighLowPie

classes = (SPEEDSEAMS_PT_MainPanel, SPEEDSEAMS_MT_QuickSharpPie, SPEEDSEAMS_MT_EdgeToolsPie, SPEEDSEAMS_MT_TransformsToolsPie, SPEEDSEAMS_MT_HighLowPie)


def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
