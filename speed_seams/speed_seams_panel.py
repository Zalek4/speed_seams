# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from . import edge_marker, apply_transforms

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

# Builds a panel


class SpeedSeamsPanel(bpy.types.Panel):
    bl_label = "Speed Seams"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        objs = context.selected_objects
        row = layout.row()

        split = layout.split()
        col = split.column(align=True)

        print("WTF")

        if obj is not None:
            col.scale_y = 1.3
            if len(objs) is not 0:
                col.enabled = True

            else:
                col.enabled = False
            col.label(text="Smoothing and UVs")
            col.prop(obj, 'seamBool')
            col.prop(obj, 'realtimeUnwrap')
            col.prop(obj, 'smoothingAngle', slider=True)
            col.operator(edge_marker.AHAutoSmooth.bl_idname)
            col.separator()
            col.operator(edge_marker.MarkSharpAsSeams.bl_idname)
            col.operator(edge_marker.MarkSeamsAsSharp.bl_idname)
            col.separator()
            col.operator(edge_marker.ClearSharp.bl_idname, icon='PMARKER_SEL')
            col.operator(edge_marker.ClearSeams.bl_idname, icon='PMARKER_ACT')
            col.separator()
            col.prop(obj, 'unwrapAlgorithm')
            col.operator(edge_marker.UnwrapSelected.bl_idname,
                         icon='MOD_UVPROJECT')
            col.separator()

            # Apply Transforms Buttons
            col.label(text="Apply Transforms")
            col.operator(apply_transforms.ApplyTransformsOperator.bl_idname)
            col.operator(apply_transforms.ApplyLocationOperator.bl_idname)
            col.operator(apply_transforms.ApplyRotationOperator.bl_idname)
            col.operator(apply_transforms.ApplyScaleOperator.bl_idname)
            col.separator()
            # col.operator(JoinObjects.bl_idname)

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH', 'OBJECT'}


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


classes = (SpeedSeamsPanel,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # ------------------------------------------------------------------------
    #    Properties
    # ------------------------------------------------------------------------
    bpy.types.Object.smoothingAngle = FloatProperty(
        name="Sharp Edge Angle",
        description="Angle to use for smoothing",
        default=35,
        min=1,
        max=180,
        step=0.5,
        update=edge_marker.SharpenSlider.execute
    )

    bpy.types.Object.seamBool = BoolProperty(
        name="Mark Seams",
        description="Marks 'Smooth and Sharpen' edges as UV seams",
        default=False
    )

    bpy.types.Object.realtimeUnwrap = BoolProperty(
        name="Realtime Unwrap",
        description="Unwraps UVs as 'Smoothing Angle' changes",
        default=False
    )

    bpy.types.Object.unwrapBool = BoolProperty(
        name="Unwrap Selected Objects",
        description="Unwraps the selected objects and packs them conformally",
        default=False
    )

    bpy.types.Object.unwrapAlgorithm = EnumProperty(
        name="",
        description="Apply Data to attribute.",
        items=[('OP1', "Conformal", ""),
               ('OP2', "Angle-Based", ""),
               ]
    )


# ------------------------------------------------------------------------
#    Unregistration
# ------------------------------------------------------------------------
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


# honestly not sure wtf this is
if __name__ == "__main__":
    register()
