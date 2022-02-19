
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
    "version": (0, 4, 3),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Speed Seams",
    "description": "",
    "category": "Tools",
    "wiki_url": "",
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
        description="Marks sharp edges as seams as angle slider updates",
        default=False
    )

    packmasterBool: bpy.props.BoolProperty(
        name="UVPackmaster",
        description="Uses UVPackmaster 2 or 3 if installed",
        default=False
    )

    unwrapAlgorithm : bpy.props.EnumProperty(
        name="",
        description="Apply Data to attribute.",
        items=[('UA1', "Conformal", ""),
               ('UA2', "Angle-Based", ""),
        ]
    )

#-----------------------------------------------------#
#     register the modules
#-----------------------------------------------------#


def register():
    from .register import register_addon
    register_addon()
    bpy.utils.register_class(SpeedSeamsSettings)
    bpy.types.Scene.ss_settings = PointerProperty(type=SpeedSeamsSettings)


def unregister():
    from .register import unregister_addon
    unregister_addon()
    del bpy.types.Scene.ss_settings
