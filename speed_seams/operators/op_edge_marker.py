# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy
import bmesh
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class SPEEDSEAMS_OT_ClearSharpEdges(bpy.types.Operator):
    bl_idname = "clear.sharp_edges"
    bl_label = "Clear Sharp"
    bl_description = "Clears the selected object's sharp edges"

    @classmethod
    def poll(cls, context):
        return context.object is not None

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

    @classmethod
    def poll(cls, context):
        return context.object is not None

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

    @classmethod
    def poll(cls, context):
        return context.object is not None

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

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        Var_UnwrapMethod = ss.unwrapAlgorithm

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)

        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        if Var_UnwrapMethod == 'OP1':
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            self.report({'INFO'}, "Unwrapped UVs -- Conformal")

        else:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            self.report({'INFO'}, "Unwrapped UVs -- Angle-Based")

        return {'FINISHED'}


class SPEEDSEAMS_OT_SharpenSlider(bpy.types.Operator):
    bl_idname = "sharpen.slider"
    bl_label = "Smooth and Sharpen"
    bl_description = "Sets 'Autosmooth' and 'Sharp Edges' at slider angle"
    bl_context = 'mesh_edit'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    # Executes automation after button press
    def execute(self, context):

        scene = context.scene
        ss = scene.ss_settings

        # Variables
        Var_AngleValue = ss.smoothingAngle
        Var_SeamBool = ss.seamBool
        #Var_RealtimeUnwrap = bpy.context.object.realtimeUnwrap

        # Convert angle slider input to radians
        Var_NewAngle = Var_AngleValue * (3.1459/180)

        if context.object is not None:
            # Enable autosmooth at the defined angle
            bpy.context.object.data.use_auto_smooth = True
            bpy.context.object.data.auto_smooth_angle = 3.1459

            # Enter 'Edit Mode', deselect everything, and change selection setting to 'Edge'

            if context.mode == 'OBJECT':
                bpy.ops.object.shade_smooth()
                bpy.context.scene.tool_settings.mesh_select_mode = (
                    False, True, False)
                bpy.ops.object.editmode_toggle()

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

            return None
            

        else:
            #print("No object is active")
            return None


class SPEEDSEAMS_OT_SharpenSliderButton(bpy.types.Operator):
    bl_idname = "sharpen.slider_button"
    bl_label = ""
    bl_description = "Sets 'Autosmooth' and 'Sharp Edges' at slider angle"
    bl_context = 'mesh_edit'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    # Executes automation after button press
    def execute(self, context):

        scene = context.scene
        ss = scene.ss_settings

        # Variables
        Var_AngleValue = ss.smoothingAngle
        Var_SeamBool = ss.seamBool
        #Var_RealtimeUnwrap = bpy.context.object.realtimeUnwrap

        # Convert angle slider input to radians
        Var_NewAngle = Var_AngleValue * (3.1459/180)

        if context.object is not None:
            # Enable autosmooth at the defined angle
            bpy.context.object.data.use_auto_smooth = True
            bpy.context.object.data.auto_smooth_angle = 3.1459

            # Enter 'Edit Mode', deselect everything, and change selection setting to 'Edge'

            if context.mode == 'OBJECT':
                bpy.ops.object.shade_smooth()
                bpy.context.scene.tool_settings.mesh_select_mode = (
                    False, True, False)
                bpy.ops.object.editmode_toggle()

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

            return {'FINISHED'}

        else:
            #print("No object is active")
            return None

class SPEEDSEAMS_OT_AutoSmooth(bpy.types.Operator):
    bl_idname = "auto.smooth"
    bl_label = "Smooth All"
    bl_description = "Clears sharp edges and enables Autosmooth at an angle of 180 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

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