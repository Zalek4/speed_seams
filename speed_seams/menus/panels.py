# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------
import bpy
from bpy.types import Menu
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from ..operators import op_apply_transforms, op_edge_marker, op_gpu_overlay, op_uv_unwrap, op_texel_density_checker
from os.path import exists
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

        #Texel Density Checker Integration --------------------------------------------------------------
        box = layout.box()
        scale = 1.2
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        row = col.row(align=True)
        row.scale_y = scale
        try:
            td = scene.td
            if context.object is not None:
                row.label(text="Texel Density Checker")
            else:
                row.active = False
                row.label(text="Texel Density Checker")

            row = col.row(align=True)
            row.scale_y = scale
            if context.object is not None:
                row.label(text="Units:")
                row.prop(td, "units")
            else:
                row.active = False
                row.label(text="Units:")
                row.prop(td, "units")

            row = col.row(align=True)
            row.scale_y = scale
            if context.object is not None:
                row.label(text="Texture Size:")
                row.prop(td, "texture_size")
            else:
                row.active = False
                row.label(text="Texture Size:")
                row.prop(td, "texture_size")

            row = col.row(align=True)
            row.scale_y = scale
            if context.object is not None:
                row.label(text="Set TD:")
                row.prop(td, "density_set")
            else:
                row.active = False
                row.label(text="Set TD:")
                row.prop(td, "density_set")

            row = col.row(align=True)
            row.scale_y = scale
            row.operator(op_texel_density_checker.SPEEDSEAMS_OT_SetTD.bl_idname, icon='TEXTURE_DATA')

            row = col.row(align=True)
            row.scale_y = scale
            if context.object is not None:
                if td.units == '0':
                    row.operator("object.preset_set", text="20.48").td_value = "20.48"
                    row.operator("object.preset_set", text="10.24").td_value = "10.24"
                    row.operator("object.preset_set", text="5.12").td_value = "5.12"
                if td.units == '1':
                    row.operator("object.preset_set", text="2048").td_value="2048"
                    row.operator("object.preset_set", text="1024").td_value="1024"
                    row.operator("object.preset_set", text="512").td_value="512"
                if td.units == '2':
                    row.operator("object.preset_set", text="52.019").td_value="52.019"
                    row.operator("object.preset_set", text="26.01").td_value="26.01"
                    row.operator("object.preset_set", text="13.005").td_value="13.005"
                if td.units == '3':
                    row.operator("object.preset_set", text="624.23").td_value="624.23"
                    row.operator("object.preset_set", text="312.115").td_value="312.115"
                    row.operator("object.preset_set", text="156.058").td_value="156.058"

            else:
                row.active = False
                if td.units == '0':
                    row.operator("object.preset_set", text="20.48").td_value = "20.48"
                    row.operator("object.preset_set", text="10.24").td_value = "10.24"
                    row.operator("object.preset_set", text="5.12").td_value = "5.12"
                if td.units == '1':
                    row.operator("object.preset_set", text="2048").td_value="2048"
                    row.operator("object.preset_set", text="1024").td_value="1024"
                    row.operator("object.preset_set", text="512").td_value="512"
                if td.units == '2':
                    row.operator("object.preset_set", text="52.019").td_value="52.019"
                    row.operator("object.preset_set", text="26.01").td_value="26.01"
                    row.operator("object.preset_set", text="13.005").td_value="13.005"
                if td.units == '3':
                    row.operator("object.preset_set", text="624.23").td_value="624.23"
                    row.operator("object.preset_set", text="312.115").td_value="312.115"
                    row.operator("object.preset_set", text="156.058").td_value="156.058"

            row = col.row(align=True)
            row.scale_y = scale
            if context.object is not None:
                if td.units == '0':
                    row.operator("object.preset_set", text="2.56").td_value = "2.56"
                    row.operator("object.preset_set", text="1.28").td_value = "1.28"
                    row.operator("object.preset_set", text="0.64").td_value = "0.64"
                if td.units == '1':
                    row.operator("object.preset_set", text="256").td_value="256"
                    row.operator("object.preset_set", text="128").td_value="128"
                    row.operator("object.preset_set", text="64").td_value="64"
                if td.units == '2':
                    row.operator("object.preset_set", text="6.502").td_value="6.502"
                    row.operator("object.preset_set", text="3.251").td_value="3.251"
                    row.operator("object.preset_set", text="1.626").td_value="1.626"
                if td.units == '3':
                    row.operator("object.preset_set", text="78.029").td_value="78.029"
                    row.operator("object.preset_set", text="39.014").td_value="39.014"
                    row.operator("object.preset_set", text="19.507").td_value="19.507"

            else:
                row.active = False
                if td.units == '0':
                    row.operator("object.preset_set", text="2.56").td_value = "2.56"
                    row.operator("object.preset_set", text="1.28").td_value = "1.28"
                    row.operator("object.preset_set", text="0.64").td_value = "0.64"
                if td.units == '1':
                    row.operator("object.preset_set", text="256").td_value="256"
                    row.operator("object.preset_set", text="128").td_value="128"
                    row.operator("object.preset_set", text="64").td_value="64"
                if td.units == '2':
                    row.operator("object.preset_set", text="6.502").td_value="6.502"
                    row.operator("object.preset_set", text="3.251").td_value="3.251"
                    row.operator("object.preset_set", text="1.626").td_value="1.626"
                if td.units == '3':
                    row.operator("object.preset_set", text="78.029").td_value="78.029"
                    row.operator("object.preset_set", text="39.014").td_value="39.014"
                    row.operator("object.preset_set", text="19.507").td_value="19.507"
        except:
            row.label(text="Texel Density Checker 3.3 not installed/enabled")

        #UV Tools --------------------------------------------------------------

        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        if context.object is not None:
            row.label(text="UV Tools")

        else:
            row.active = False
            row.label(text="UV Tools")

        row = col.row(align=True)
        row.scale_y = scale
        if context.object is not None:
            row.prop(ss, "uvTextureRes")
        else:
            row.active = False
            row.prop(ss, "uvTextureRes")
        if context.object is not None:
            row.prop(ss, "uvTextureType")
        else:
            row.active = False
            row.prop(ss, "uvTextureType")
        row.operator(op_uv_unwrap.SPEEDSEAMS_OT_AddUVTexture.bl_idname, icon='TEXTURE_DATA')

        row = col.row(align=True)
        row.scale_y = scale

        if context.object is not None:
            row.prop(ss, "unwrapAlgorithm")
        else:
            row.active = False
            row.prop(ss, "unwrapAlgorithm")

        row.operator(op_edge_marker.SPEEDSEAMS_OT_UnwrapSelected.bl_idname,
                     icon='MOD_EXPLODE')
        col.separator()

        row = col.row(align=True)

        if context.object is not None:
            row.prop(ss, "packmasterBool")
        else:
            row.active = False
            row.prop(ss, "packmasterBool")
        

        #Edge Tools --------------------------------------------------------------
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        if context.object is not None:
            row.label(text="Edge Tools")
        else:
            row.active = False
            row.label(text="Edge Tools")

        row = col.row(align=True)
        row.scale_y = scale
        row.operator(
            op_edge_marker.SPEEDSEAMS_OT_SharpenSliderButton.bl_idname, icon='FILE_3D')

        row = col.row(align=True)
        row.scale_y = scale
        if context.object is not None:
            row.prop(ss, "smoothingAngle", slider=True)
            row.operator(
                op_edge_marker.SPEEDSEAMS_OT_SharpenSliderReset.bl_idname, icon='LOOP_BACK')

        else:
            row.active = False
            row.prop(ss, "smoothingAngle", slider=True)
            row.operator(
                op_edge_marker.SPEEDSEAMS_OT_SharpenSliderReset.bl_idname, icon='LOOP_BACK')
        col.separator()

        row = col.row(align=True)
        if context.object is not None:
            row.prop(ss, "seamBool")
        else:
            row.active = False
            row.prop(ss, "seamBool")
        col.separator()
        
        row = col.row(align=True)
        row.scale_y = scale
        row.operator(op_edge_marker.SPEEDSEAMS_OT_AutoSmooth.bl_idname,
                        icon='PROP_CON')
        row.operator(op_edge_marker.SPEEDSEAMS_OT_MarkSharpAsSeams.bl_idname,
                     icon='MATCUBE')
                        

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

        if context.object is not None:
            row.label(text="Transforms Tools")

        else:
            row.active = False
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

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH', 'OBJECT'}