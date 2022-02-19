# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------
import bpy
from bpy.types import Menu
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from ..operators import op_apply_transforms, op_edge_marker, op_gpu_overlay

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

# Builds a panel


class SPEEDSEAMS_PT_MainPanel(bpy.types.Panel):
    bl_label = "Speed Seams"
    bl_idname = "SPEEDSEAMS_PT_mainPanel"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        objs = context.selected_objects
        scene = context.scene
        ss = scene.ss_settings

        if obj is not None:

            if len(objs) is not 0:
                split = layout.box()
                cf = layout.box().column_flow(columns=2, align=True)
                cf2 = layout.box().column_flow(columns=2, align=True)
                scale = 1.3


                row = split.row(align=True)
                row.label(text="Smoothing and UVs")                

                row = split.row(align=True)
                row.prop(ss, "unwrapAlgorithm")
                row.operator(op_edge_marker.SPEEDSEAMS_OT_UnwrapSelected.bl_idname,
                             icon='MOD_UVPROJECT')
                row.scale_y = scale

                row = split.row(align=True)
                row.prop(ss, "seamBool")
                row.prop(ss, "packmasterBool")
                row.scale_y = scale / 1.3

                row = split.row(align=True)
                row.prop(ss, "smoothingAngle", slider=True)
                row.scale_y = scale


                cf.scale_y = scale
                cf.label(text="Edge Tools")
                cf.operator(op_edge_marker.SPEEDSEAMS_OT_AutoSmooth.bl_idname,
                             icon='PROP_CON')
                cf.operator(op_edge_marker.SPEEDSEAMS_OT_MarkSharpAsSeams.bl_idname,
                             icon='PMARKER_ACT')
                             
                if context.mode == 'EDIT_MESH':
                    cf.separator()
                    cf.operator(
                        op_gpu_overlay.SPEEDSEAMS_OT_drawOverlay.bl_idname, icon='MOD_SOLIDIFY')                 
                    cf.separator()
                    cf.separator()
                    cf.separator()
                else:
                    cf.separator()
                    cf.separator()
                    cf.separator()

                cf.operator(op_edge_marker.SPEEDSEAMS_OT_ClearSharpEdges.bl_idname,
                             icon='MARKER_HLT')
                cf.operator(
                    op_edge_marker.SPEEDSEAMS_OT_ClearSeams.bl_idname, icon='MARKER')

                if context.mode == 'EDIT_MESH':
                    cf.separator()
                    cf.operator(
                        op_gpu_overlay.SPEEDSEAMS_OT_removeOverlay.bl_idname, icon='MOD_SOLIDIFY')

                # Apply Transforms Buttons
                cf2.label(text="Apply Transforms")
                cf2.scale_y = scale
                cf2.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_Apply_Transforms.bl_idname, icon='STICKY_UVS_DISABLE')
                cf2.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_ApplyLocation.bl_idname, icon='ORIENTATION_VIEW')
                cf2.separator()
                cf2.separator()
                cf2.separator()
                cf2.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_ApplyRotation.bl_idname, icon='ORIENTATION_GIMBAL')
                cf2.operator(
                    op_apply_transforms.SPEEDSEAMS_OT_ApplyScale.bl_idname, icon='CON_CHILDOF')

            else:
                layout = self.layout
                box = layout.box()
                box.separator()
                box.label(text="Please select a mesh")
                box.scale_y = .1

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH', 'OBJECT'}


class SPEEDSEAMS_MT_PieMenu(Menu):
    bl_label = "Speed Seams"
    bl_idname = "SPEEDSEAMS_MT_pieMenu"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator_enum("mesh.select_mode", "type")
