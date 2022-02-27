
import bpy
import importlib
import sys
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from .menus.panels import SPEEDSEAMS_MT_EdgeToolsPie, SPEEDSEAMS_MT_QuickSharpPie, SPEEDSEAMS_MT_TransformsToolsPie
from .operators import SPEEDSEAMS_OT_SharpenSlider

bl_info = {
    "name": "Speed Seams",
    "author": "Alex Hallenbeck, Blake Darrow",
    "version": (0, 5, 3),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Speed Seams",
    "description": "",
    "category": "Tools",
    "wiki_url": "",
    "warning": "GPU OVERLAYS ARE EXPERIMENTAL AND SHOULD NOT BE USED"
}


class SpeedSeamsSettings(bpy.types.PropertyGroup):
    smoothingAngle : bpy.props.FloatProperty(
        name="Sharp Edge Angle",
        description="Angle to use for smoothing",
        default=35,
        min=1,
        max=180,
        step=0.5,
        update=SPEEDSEAMS_OT_SharpenSlider.execute
    )

    seamBool : bpy.props.BoolProperty(
        name="Mark Seams",
        description="Marks sharp edges as seams as the 'Sharp Edge Angle' slider is updated",
        default=False
    )

    packmasterBool: bpy.props.BoolProperty(
        name="UVPackmaster",
        description="Uses UVPackmaster 2 or 3 if installed",
        default=False
    )

    unwrapAlgorithm : bpy.props.EnumProperty(
        name="",
        description="Blender algorithm to use for unwraping UVs",
        items=[('UA1', "Conformal", ""),
               ('UA2', "Angle-Based", ""),
        ]
    )

    renameCollectionsBool: bpy.props.BoolProperty(
        name="Rename Collections",
        description="Gives the option to rename the high and low input collections.",
        default=False
    )

    renameObjectsBool: bpy.props.BoolProperty(
        name="Rename Objects",
        description="Gives the option to rename each object pair as bake groups are made.",
        default=False
    )

    bakePrepAssetName: bpy.props.StringProperty(
        name="",
        description="The asset name used to name bake prep collections",
        default=""
    )

    bakePrepSuffixHigh: bpy.props.StringProperty(
        name="",
        description="The highpoly suffix to use for objects and high/low collections",
        default="high"
    )

    bakePrepSuffixLow: bpy.props.StringProperty(
        name="",
        description="The lowpoly suffix to use for objects and high/low collections",
        default="low"
    )

#-----------------------------------------------------#
#     register the modules
#-----------------------------------------------------#

addon_keymaps = []

def register():
    from .register import register_addon
    register_addon()
    bpy.utils.register_class(SpeedSeamsSettings)
    bpy.types.Scene.ss_settings = PointerProperty(type=SpeedSeamsSettings)
    bpy.types.Scene.ss_collection_high = PointerProperty(name="", type=bpy.types.Collection)
    bpy.types.Scene.ss_collection_low = PointerProperty(name="", type=bpy.types.Collection)

    #Register Keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_edge_tools_pie = km.keymap_items.new("wm.call_menu_pie", "D", "PRESS", shift=True)
    kmi_edge_tools_pie.properties.name = SPEEDSEAMS_MT_EdgeToolsPie.bl_idname

    kmi_transforms_pie = km.keymap_items.new("wm.call_menu_pie", "D", "PRESS", shift=True, ctrl=True)
    kmi_transforms_pie.properties.name = SPEEDSEAMS_MT_TransformsToolsPie.bl_idname

    kmi_quick_sharp_pie = km.keymap_items.new("wm.call_menu_pie", "X", "PRESS", shift=True, ctrl=True)
    kmi_quick_sharp_pie.properties.name = SPEEDSEAMS_MT_QuickSharpPie.bl_idname

    addon_keymaps.append((km, kmi_edge_tools_pie, kmi_quick_sharp_pie, kmi_transforms_pie))

def unregister():
    from .register import unregister_addon
    unregister_addon()
    del bpy.types.Scene.ss_settings
    del bpy.types.Scene.ss_collection_high
    del bpy.types.Scene.ss_collection_low

    #Unregister Keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi_edge_tools_pie, kmi_quick_sharp_pie, kmi_transforms_pie in addon_keymaps:
            km.keymap_items.remove(kmi_edge_tools_pie)
            km.keymap_items.remove(kmi_quick_sharp_pie)
            km.keymap_items.remove(kmi_transforms_pie)
    addon_keymaps.clear()
