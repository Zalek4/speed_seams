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
        split = layout.box()
        col = split.column(align=True)
        split = layout.box()
        row = split.row(align=True)
        scale = 1.3

        if obj is not None:

            if len(objs) is not 0:

                col.label(text="Smoothing and UVs")
                col.scale_y = .3
                row.prop(obj, 'unwrapAlgorithm')
                row.operator(edge_marker.UnwrapSelected.bl_idname,
                             icon='MOD_UVPROJECT')
                row.scale_y = scale

                row = split.row(align=False)
                row.prop(obj, 'smoothingAngle', slider=True)
                row.scale_y = scale

                row = split.row(align=True)
                row.prop(obj, 'seamBool')
                row.prop(obj, 'realtimeUnwrap')
                #col.scale_y = 1
                row.scale_y = scale / 1.2

                row = split.row(align=False)
                col = split.column(align=True)
                col.operator(edge_marker.AHAutoSmooth.bl_idname,
                             icon='PROP_CON')
                col.operator(edge_marker.MarkSharpAsSeams.bl_idname,
                             icon='PMARKER_ACT')
                # col.operator(edge_marker.MarkSeamsAsSharp.bl_idname)
                col.operator(edge_marker.ClearSharp.bl_idname,
                             icon='MARKER_HLT')
                col.operator(edge_marker.ClearSeams.bl_idname, icon='MARKER')
                col.separator()

                # Apply Transforms Buttons
                col.label(text="Apply Transforms")
                col.scale_y = scale
                col.operator(
                    apply_transforms.ApplyTransformsOperator.bl_idname, icon='STICKY_UVS_DISABLE')
                col.operator(
                    apply_transforms.ApplyLocationOperator.bl_idname, icon='ORIENTATION_VIEW')
                col.operator(
                    apply_transforms.ApplyRotationOperator.bl_idname, icon='ORIENTATION_GIMBAL')
                col.operator(
                    apply_transforms.ApplyScaleOperator.bl_idname, icon='CON_CHILDOF')
                col.separator()

            else:
                layout = self.layout
                box = layout.box()
                # box.separator()
                box.label(text="Please select a mesh")
                box.scale_y = .1
                # box.separator()

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
