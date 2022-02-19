import bpy
from .op_apply_transforms import SPEEDSEAMS_OT_Apply_Transforms, SPEEDSEAMS_OT_ApplyLocation, SPEEDSEAMS_OT_ApplyRotation, SPEEDSEAMS_OT_ApplyScale
from .op_edge_marker import SPEEDSEAMS_OT_ClearSharpEdges, SPEEDSEAMS_OT_ClearSeams, SPEEDSEAMS_OT_MarkSharpAsSeams, SPEEDSEAMS_OT_SharpenSlider, SPEEDSEAMS_OT_AutoSmooth
from .op_gpu_overlay import SPEEDSEAMS_OT_drawOverlay, SPEEDSEAMS_OT_removeOverlay
from .op_uv_unwrap import SPEEDSEAMS_OT_UnwrapSelected

classes = (SPEEDSEAMS_OT_Apply_Transforms, SPEEDSEAMS_OT_ApplyLocation, SPEEDSEAMS_OT_ApplyRotation, SPEEDSEAMS_OT_ApplyScale, SPEEDSEAMS_OT_AutoSmooth, SPEEDSEAMS_OT_ClearSeams,
           SPEEDSEAMS_OT_ClearSharpEdges, SPEEDSEAMS_OT_MarkSharpAsSeams, SPEEDSEAMS_OT_UnwrapSelected, SPEEDSEAMS_OT_SharpenSlider, SPEEDSEAMS_OT_drawOverlay, SPEEDSEAMS_OT_removeOverlay)


def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
