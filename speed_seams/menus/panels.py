# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------
import bpy
from bpy.types import Menu
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from ..operators import op_apply_transforms, op_edge_marker, op_gpu_overlay, op_bake_organizer

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

        #if len(objs) is not 0:
        #UV Tools --------------------------------------------------------------
        box = layout.box()
        scale = 1.2
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        row.label(text="Smoothing and UV Tools")

        row = col.row(align=True)
        row.scale_y = scale

        if context.object is not None:
            row.prop(ss, "unwrapAlgorithm")
        else:
            row.active = False
            row.prop(ss, "unwrapAlgorithm")

        row.operator(op_edge_marker.SPEEDSEAMS_OT_UnwrapSelected.bl_idname,
                    icon='MOD_UVPROJECT')
        col.separator()

        row = col.row(align=True)

        if context.object is not None:
            row.prop(ss, "seamBool")
            row.prop(ss, "packmasterBool")
        else:
            row.active = False
            row.prop(ss, "seamBool")
            row.prop(ss, "packmasterBool")

        col.separator()

        row = col.row(align=True)
        row.scale_y = scale

        if context.object is not None:
            row.prop(ss, "smoothingAngle", slider=True)
        else:
            row.active = False
            row.prop(ss, "smoothingAngle", slider=True)
        

        #Edge Tools --------------------------------------------------------------
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        row.label(text="Edge Tools")
        row = col.row(align=True)
        row.scale_y = scale
        row.operator(op_edge_marker.SPEEDSEAMS_OT_AutoSmooth.bl_idname,
                        icon='PROP_CON')
        row.operator(op_edge_marker.SPEEDSEAMS_OT_MarkSharpAsSeams.bl_idname,
                        icon='PMARKER_ACT')
                        

        row = col.row(align=True)
        row.scale_y = scale
        row.operator(op_edge_marker.SPEEDSEAMS_OT_ClearSharpEdges.bl_idname,
                        icon='MARKER_HLT')
        row.operator(
            op_edge_marker.SPEEDSEAMS_OT_ClearSeams.bl_idname, icon='MARKER')

        if context.mode == 'EDIT_MESH':
            row = col.row(align=True)
            row.scale_y = scale
            row.operator(
                op_gpu_overlay.SPEEDSEAMS_OT_drawOverlay.bl_idname, icon='MOD_SOLIDIFY')
            row.operator(
                op_gpu_overlay.SPEEDSEAMS_OT_removeOverlay.bl_idname, icon='MOD_SOLIDIFY')

        #Transforms Tools ---------------------------------------------------------
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        row.label(text="Transforms Tools")

        row = col.row(align=True)
        row.scale_y = scale
        row.operator(
            op_apply_transforms.SPEEDSEAMS_OT_Apply_Transforms.bl_idname, icon='STICKY_UVS_DISABLE')

        row = col.row(align=True)
        row.scale_y = scale
        row.operator(
            op_apply_transforms.SPEEDSEAMS_OT_ApplyLocation.bl_idname, icon='ORIENTATION_VIEW')
        row.operator(
            op_apply_transforms.SPEEDSEAMS_OT_ApplyRotation.bl_idname, icon='ORIENTATION_GIMBAL')
        row.operator(
            op_apply_transforms.SPEEDSEAMS_OT_ApplyScale.bl_idname, icon='CON_CHILDOF')

        #Bake Prep Tools ---------------------------------------------------------
        box = layout.box()
        scale = 1.2
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        # Set up bake groups
        row = col.row(align=True)
        row.label(text="Bake Prep Tools")
        row.scale_y = scale

        row = col.row(align=True)
        row.scale_y = scale
        row.operator(
            op_bake_organizer.SPEEDSEAMS_OT_Organize_Objects.bl_idname, icon='NEWFOLDER')

        row = col.row(align=True)
        row.scale_y = scale
        row.prop(scene, "ss_collection_high")

        row = col.row(align=True)
        row.scale_y = scale
        row.prop(scene, "ss_collection_low")

        col.separator()
        row = col.row(align=True)
        row.prop(ss, "renameCollectionsBool")
        row.prop(ss, "renameObjectsBool")
            

    def draw_uv_tools(self, context, layout):
        scene = context.scene
        ss = scene.ss_settings


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
