import bpy
from .op_apply_transforms import SPEEDSEAMS_OT_Apply_Transforms, SPEEDSEAMS_OT_ApplyLocation, SPEEDSEAMS_OT_ApplyRotation, SPEEDSEAMS_OT_ApplyScale
from .op_edge_marker import SPEEDSEAMS_OT_ClearSharpEdges, SPEEDSEAMS_OT_ClearSeams, SPEEDSEAMS_OT_MarkSharpAsSeams, SPEEDSEAMS_OT_SharpenSlider, SPEEDSEAMS_OT_SharpenSliderButton, SPEEDSEAMS_OT_AutoSmooth, SPEEDSEAMS_OT_SharpenSliderReset, SPEEDSEAMS_OT_QuickSharp15, SPEEDSEAMS_OT_QuickSharp30, SPEEDSEAMS_OT_QuickSharp45, SPEEDSEAMS_OT_QuickSharp60, SPEEDSEAMS_OT_QuickSharp75, SPEEDSEAMS_OT_QuickSharp90
from .op_gpu_overlay import SPEEDSEAMS_OT_drawOverlay, SPEEDSEAMS_OT_removeOverlay
from .op_uv_unwrap import SPEEDSEAMS_OT_UnwrapSelected
from .op_bake_organizer import SPEEDSEAMS_OT_Organize_Objects, SPEEDSEAMS_OT_CreateHighLowCollections

classes = (SPEEDSEAMS_OT_Apply_Transforms, SPEEDSEAMS_OT_ApplyLocation, SPEEDSEAMS_OT_ApplyRotation, SPEEDSEAMS_OT_ApplyScale, SPEEDSEAMS_OT_AutoSmooth, SPEEDSEAMS_OT_ClearSeams,
           SPEEDSEAMS_OT_ClearSharpEdges, SPEEDSEAMS_OT_MarkSharpAsSeams, SPEEDSEAMS_OT_UnwrapSelected, SPEEDSEAMS_OT_SharpenSlider, SPEEDSEAMS_OT_SharpenSliderButton, SPEEDSEAMS_OT_SharpenSliderReset,
            SPEEDSEAMS_OT_QuickSharp15, SPEEDSEAMS_OT_QuickSharp30, SPEEDSEAMS_OT_QuickSharp45, SPEEDSEAMS_OT_QuickSharp60, SPEEDSEAMS_OT_QuickSharp75, SPEEDSEAMS_OT_QuickSharp90, SPEEDSEAMS_OT_drawOverlay,
             SPEEDSEAMS_OT_removeOverlay, SPEEDSEAMS_OT_Organize_Objects, SPEEDSEAMS_OT_CreateHighLowCollections)


def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)