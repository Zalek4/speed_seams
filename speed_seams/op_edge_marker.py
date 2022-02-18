# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy
import bmesh
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from . import SpeedSeamsSettings

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class SPEEDSEAMS_OT_ClearSharpEdges(bpy.types.Operator):
    bl_idname = "clear.sharp_edges"
    bl_label = "Clear Sharp"
    bl_description = "Clears the selected object's sharp edges"

    # Executes automation after button press
    def execute(self, context):

        if context.mode == 'OBJECT':

            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.editmode_toggle()
            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')

        self.report({'INFO'}, "Cleared Sharp Edges")
        return {'FINISHED'}


class SPEEDSEAMS_OT_ClearSeams(bpy.types.Operator):
    bl_idname = "clear.seams"
    bl_label = "Clear UV Seams"
    bl_description = "Clears the selected object's UV seams"

    # Executes automation after button press
    def execute(self, context):

        if context.mode == 'OBJECT':
            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_seam(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            print("Cleared UV Seams")

        else:
            bpy.ops.object.editmode_toggle()
            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_seam(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')

        self.report({'INFO'}, "Cleared UV Seams")
        return {'FINISHED'}


class SPEEDSEAMS_OT_MarkSharpAsSeams(bpy.types.Operator):
    bl_idname = "mark.sharp_as_seams"
    bl_label = "Mark Sharp as Seams"
    bl_description = "Marks current sharp edges as UV seams"

    # Executes automation after button press

    def execute(self, context):

        obj = bpy.context.active_object
        me = bpy.context.object.data
        #bm = bmesh.from_edit_mesh(me)

        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            bm = bmesh.from_edit_mesh(me)

            for e in bm.edges:
                if not e.smooth:
                    e.select = True
                    e.seam = True

            bmesh.update_edit_mesh(me)
            bpy.ops.object.editmode_toggle()

        else:
            bm = bmesh.from_edit_mesh(me)
            for e in bm.edges:
                if not e.smooth:
                    e.select = True
                    e.seam = True
            bmesh.update_edit_mesh(me)

        self.report({'INFO'}, "Marked Sharp Edges as Seams")
        return {'FINISHED'}


class SPEEDSEAMS_OT_UnwrapSelected(bpy.types.Operator):
    bl_idname = "unwrap.selected"
    bl_label = "Unwrap Object"
    bl_description = "Unwraps, averages, and packs UVs"

    def execute(self, context):

        Var_UnwrapMethod = SpeedSeamsSettings.unwrapAlgorithm
        print(Var_UnwrapMethod)

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)

        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        else:
            print("Context is not 'Object' it is", context.mode)

        if Var_UnwrapMethod == 'OP1':
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            print("UNWRAPPED UVS CONFORMAL")
            self.report({'INFO'}, "Unwrapped UVs -- Conformal")

        else:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            print("UNWRAPPED UVS ANGLE-BASED")
            self.report({'INFO'}, "Unwrapped UVs -- Angle-Based")

        return {'FINISHED'}


class SPEEDSEAMS_OT_SharpenSlider(bpy.types.Operator):
    bl_idname = "sharpen.slider"
    bl_label = "Smooth and Sharpen"
    bl_description = "Sets 'Autosmooth' and 'Sharp Edges' at slider angle"
    bl_context = 'mesh_edit'

    # Executes automation after button press
    def execute(self, context):

        # ------------------------------------------------------------------------
        #    Smoothing Logic
        # ------------------------------------------------------------------------

        # Variables
        Var_AngleValue = SpeedSeamsSettings.smoothingAngle
        Var_SeamBool = SpeedSeamsSettings.seamBool
        #Var_RealtimeUnwrap = bpy.context.object.realtimeUnwrap

        # Convert angle slider input to radians
        Var_NewAngle = Var_AngleValue * (3.1459/180)

        # Enable autosmooth at the defined angle
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 3.1459

        # Enter 'Edit Mode', deselect everything, and change selection setting to 'Edge'

        if context.mode == 'OBJECT':
            print("CONTEXT IS", context.mode)
            bpy.ops.object.shade_smooth()
            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.object.editmode_toggle()

        else:
            print("Context is not 'OBJECT' -- it is ", context.mode)

        bpy.ops.mesh.select_all(action='DESELECT')

        # Clear old sharp edges, and mark sharp edges based on the smoothing angle
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp(sharpness=Var_NewAngle)
        bpy.ops.mesh.mark_sharp()

        # Mark UV seams at sharp edges if the checkbox is filled
        if Var_SeamBool == True:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_seam(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=Var_NewAngle)
            bpy.ops.mesh.mark_seam(clear=False)
            print("MARKED UV SEAMS")

        else:
            print("DID NOT MARK UV SEAMS")

        return None


class SPEEDSEAMS_OT_AutoSmooth(bpy.types.Operator):
    bl_idname = "auto.smooth"
    bl_label = "Smooth All"
    bl_description = "Enables Autosmooth at an angle of 180 degrees"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.use_auto_smooth = True
            bpy.context.object.data.auto_smooth_angle = 3.1459

        else:
            bpy.context.scene.tool_settings.mesh_select_mode = (
                False, True, False)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.use_auto_smooth = True
            bpy.context.object.data.auto_smooth_angle = 3.1459

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Properties
# ------------------------------------------------------------------------

smoothingAngle = bpy.props.FloatProperty(
    name="Sharp Edge Angle",
    description="Angle to use for smoothing",
    default=35,
    min=1,
    max=180,
    step=0.5,
    update=SPEEDSEAMS_OT_SharpenSlider.execute
)

seamBool = bpy.props.BoolProperty(
    name="Mark Sharp as Seams",
    description="Marks sharp edges as seams as angle slider updates",
    default=False
)

unwrapAlgorithm = bpy.props.EnumProperty(
    name="",
    description="Apply Data to attribute.",
    items=[('OP1', "Conformal", ""),
           ('OP2', "Angle-Based", ""),
           ]
)
