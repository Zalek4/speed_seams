# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------
import bpy
from bpy.types import Menu
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from ..operators import op_apply_transforms, op_edge_marker, op_gpu_overlay, op_grease_pencil
from ..operators.op_edge_marker import seamBool, unwrapAlgorithm, smoothingAngle

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

# Builds a panel


class SpeedSeamsPanel(bpy.types.Panel):
    bl_label = "Speed Seams"
    bl_idname = "SPEEDSEAMS_PT_mainPanel"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        objs = context.selected_objects

        if obj is not None:

            if len(objs) is not 0:

                split = layout.box()
                col = split.column(align=True)
                split = layout.box()
                row = split.row(align=True)
                scale = 1.3

                col.label(text="Smoothing and UVs")
                row.prop(obj, 'unwrapAlgorithm')
                row.operator(op_edge_marker.SPEEDSEAMS_OT_UnwrapSelected.bl_idname,
                             icon='MOD_UVPROJECT')
                row.scale_y = scale

                row = split.row(align=False)
                row.prop(obj, 'smoothingAngle', slider=True)
                row.scale_y = scale

                row = split.row(align=True)
                row.prop(obj, 'seamBool')
                row.scale_y = scale / 1.2

                row = split.row(align=False)
                col = split.column(align=True)
                col.operator(op_edge_marker.SPEEDSEAMS_OT_AutoSmooth.bl_idname,
                             icon='PROP_CON')
                col.operator(op_edge_marker.SPEEDSEAMS_OT_MarkSharpAsSeams.bl_idname,
                             icon='PMARKER_ACT')
                col.operator(op_edge_marker.SPEEDSEAMS_OT_ClearSharpEdges.bl_idname,
                             icon='MARKER_HLT')
                col.operator(
                    op_edge_marker.SPEEDSEAMS_OT_ClearSeams.bl_idname, icon='MARKER')
                col.separator()
                if context.mode == 'EDIT_MESH':
                    col.operator(
                        op_gpu_overlay.SPEEDSEAMS_OT_drawOverlay.bl_idname, icon='MOD_SOLIDIFY')

                    col.operator(
                        op_gpu_overlay.SPEEDSEAMS_OT_removeOverlay.bl_idname, icon='MOD_SOLIDIFY')

                # Apply Transforms Buttons
                col.label(text="Apply Transforms")
                col.scale_y = scale
                row = split.row(align=True)
                row.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_Apply_Transforms.bl_idname, icon='STICKY_UVS_DISABLE')
                row.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_ApplyLocation.bl_idname, icon='ORIENTATION_VIEW')
                row.scale_y = scale
                row = split.row(align=True)
                row.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_ApplyRotation.bl_idname, icon='ORIENTATION_GIMBAL')
                row.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_ApplyScale.bl_idname, icon='CON_CHILDOF')
                row.scale_y = scale

            else:
                layout = self.layout
                box = layout.box()
                box.separator()
                box.label(text="Please select a mesh")
                box.scale_y = .1
                # box.separator()

            # col.operator(JoinObjects.bl_idname)

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH', 'OBJECT'}


class SpeedSeamsPie(Menu):
    bl_label = "Speed Seams"
    bl_idname = "SPEEDSEAMS_PT_pieMenu"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator_enum("mesh.select_mode", "type")
