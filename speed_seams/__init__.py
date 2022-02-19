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

import bpy
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from .panels import SpeedSeamsPanel, SpeedSeamsPie
from .op_apply_transforms import SPEEDSEAMS_OT_Apply_Transforms, SPEEDSEAMS_OT_ApplyLocation, SPEEDSEAMS_OT_ApplyRotation, SPEEDSEAMS_OT_ApplyScale
from .op_edge_marker import SPEEDSEAMS_OT_ClearSharpEdges, SPEEDSEAMS_OT_ClearSeams, SPEEDSEAMS_OT_MarkSharpAsSeams, SPEEDSEAMS_OT_UnwrapSelected, SPEEDSEAMS_OT_SharpenSlider, SPEEDSEAMS_OT_AutoSmooth
from .op_gpu_overlay import SPEEDSEAMS_OT_drawOverlay, SPEEDSEAMS_OT_removeOverlay

#-----------------------------------------------------#
#     Properties
#-----------------------------------------------------#

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
        name="Mark Sharp as Seams",
        description="Marks sharp edges as seams as angle slider updates",
        default=False
    )

    unwrapAlgorithm : bpy.props.EnumProperty(
        name="",
        description="Apply Data to attribute.",
        items=[('OP1', "Conformal", ""),
            ('OP2', "Angle-Based", ""),
            ]
    )

#-----------------------------------------------------#
#     Register the modules
#-----------------------------------------------------#

classes = (SpeedSeamsSettings, SpeedSeamsPanel, SpeedSeamsPie, SPEEDSEAMS_OT_Apply_Transforms, SPEEDSEAMS_OT_ApplyLocation, SPEEDSEAMS_OT_ApplyRotation, SPEEDSEAMS_OT_ApplyScale, SPEEDSEAMS_OT_ClearSharpEdges, SPEEDSEAMS_OT_ClearSeams, SPEEDSEAMS_OT_MarkSharpAsSeams, SPEEDSEAMS_OT_UnwrapSelected, SPEEDSEAMS_OT_SharpenSlider, SPEEDSEAMS_OT_AutoSmooth, SPEEDSEAMS_OT_drawOverlay, SPEEDSEAMS_OT_removeOverlay)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.ss_settings = bpy.props.PointerProperty(type=SpeedSeamsSettings)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.ss_settings

if __name__ == "__main__":
    register()