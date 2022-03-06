# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------
import bpy
from bpy.types import Menu
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from ..operators import op_apply_transforms, op_edge_marker

class SPEEDSEAMS_MT_EdgeToolsPie(Menu):
    bl_label = "Edge Tools"
    bl_idname = "SPEEDSEAMS_MT_EdgeToolsPie"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator(op_edge_marker.SPEEDSEAMS_OT_ClearSeams.bl_idname,
                     icon='MARKER')
        pie.operator(op_edge_marker.SPEEDSEAMS_OT_ClearSharpEdges.bl_idname,
                     icon='MARKER_HLT')
        pie.operator(op_edge_marker.SPEEDSEAMS_OT_MarkSharpAsSeams.bl_idname,
                     icon='MATCUBE')
        pie.operator(op_edge_marker.SPEEDSEAMS_OT_AutoSmooth.bl_idname,
                     icon='PROP_CON')


class SPEEDSEAMS_MT_TransformsToolsPie(Menu):
    bl_label = "Transforms Tools"
    bl_idname = "SPEEDSEAMS_MT_TransformsToolsPie"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator(
            op_apply_transforms.SPEEDSEAMS_OT_ApplyLocation.bl_idname, icon='ORIENTATION_VIEW')
        pie.operator(
            op_apply_transforms.SPEEDSEAMS_OT_ApplyScale.bl_idname, icon='CON_CHILDOF')
        pie.operator(
            op_apply_transforms.SPEEDSEAMS_OT_ApplyRotation.bl_idname, icon='ORIENTATION_GIMBAL')
        pie.operator(
            op_apply_transforms.SPEEDSEAMS_OT_Apply_Transforms.bl_idname, icon='STICKY_UVS_DISABLE')


class SPEEDSEAMS_MT_QuickSharpPie(Menu):
    bl_label = "Quick Sharp"
    bl_idname = "SPEEDSEAMS_MT_QuickSharpPie"
    bl_category = "Speed Seams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator(
            op_edge_marker.SPEEDSEAMS_OT_QuickSharp15.bl_idname, icon='CON_SHRINKWRAP')
        pie.operator(
            op_edge_marker.SPEEDSEAMS_OT_QuickSharp75.bl_idname, icon='CON_SHRINKWRAP')
        pie.operator(
            op_edge_marker.SPEEDSEAMS_OT_QuickSharp90.bl_idname, icon='CON_SHRINKWRAP')
        pie.operator(
            op_edge_marker.SPEEDSEAMS_OT_QuickSharp45.bl_idname, icon='CON_SHRINKWRAP')
        pie.operator(
            op_edge_marker.SPEEDSEAMS_OT_QuickSharp30.bl_idname, icon='CON_SHRINKWRAP')
        pie.operator(
            op_edge_marker.SPEEDSEAMS_OT_QuickSharp60.bl_idname, icon='CON_SHRINKWRAP')
