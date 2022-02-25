
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
from .operators import SPEEDSEAMS_OT_SharpenSlider

bl_info = {
    "name": "Speed Seams",
    "author": "Alex Hallenbeck, Blake Darrow",
    "version": (0, 4, 2),
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

#-----------------------------------------------------#
#     register the modules
#-----------------------------------------------------#


def register():
    from .register import register_addon
    register_addon()
    bpy.utils.register_class(SpeedSeamsSettings)
    bpy.types.Scene.ss_settings = PointerProperty(type=SpeedSeamsSettings)
    bpy.types.Scene.ss_collection_high = PointerProperty(name="Highpoly", type=bpy.types.Collection)
    bpy.types.Scene.ss_collection_low = PointerProperty(name="Lowpoly", type=bpy.types.Collection)


def unregister():
    from .register import unregister_addon
    unregister_addon()
    del bpy.types.Scene.ss_settings
    del bpy.types.Scene.ss_collection_high
    del bpy.types.Scene.ss_collection_low