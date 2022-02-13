# imports
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from ..operators import op_edge_marker


class SPEEDSEAMS_Global_Properties(bpy.types.PropertyGroup):

    smoothingAngle = FloatProperty(
        name="Sharp Edge Angle",
        description="Angle to use for smoothing",
        default=35,
        min=1,
        max=180,
        step=0.5,
        update=op_edge_marker.SPEEDSEAMS_OT_SharpenSlider.execute
    )

    unwrapBool = BoolProperty(
        name="Unwrap Selected Objects",
        description="Unwraps the selected objects and packs them conformally",
        default=False
    )

    unwrapAlgorithm = EnumProperty(
        name="",
        description="Apply Data to attribute.",
        items=[('OP1', "Conformal", ""),
               ('OP2', "Angle-Based", ""),
               ]
    )
