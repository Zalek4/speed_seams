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
    bl_label = "Sharp to Seams"
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
    bl_label = "Mark Sharp"
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


class SPEEDSEAMS_OT_SharpenSliderReset(bpy.types.Operator):
    bl_idname = "slider.reset"
    bl_label = ""
    bl_description = "Resets 'Sharp Edge Angle' slider to 35 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        if ss.smoothingAngle == 35:
            self.report({'INFO'}, "Already default value")
        else:
            ss.smoothingAngle = 35
            self.report({'INFO'}, "Reset angle")

        return {'FINISHED'}


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


class SPEEDSEAMS_OT_QuickSharp15(bpy.types.Operator):
    bl_idname = "quick.sharp15"
    bl_label = "15"
    bl_description = "Marks edges sharp at 15 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        ss.smoothingAngle = 15

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}


class SPEEDSEAMS_OT_QuickSharp30(bpy.types.Operator):
    bl_idname = "quick.sharp30"
    bl_label = "30"
    bl_description = "Marks edges sharp at 30 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        ss.smoothingAngle = 30

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}


class SPEEDSEAMS_OT_QuickSharp45(bpy.types.Operator):
    bl_idname = "quick.sharp45"
    bl_label = "45"
    bl_description = "Marks edges sharp at 45 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        ss.smoothingAngle = 45

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}


class SPEEDSEAMS_OT_QuickSharp60(bpy.types.Operator):
    bl_idname = "quick.sharp60"
    bl_label = "60"
    bl_description = "Marks edges sharp at 60 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        ss.smoothingAngle = 60

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}


class SPEEDSEAMS_OT_QuickSharp75(bpy.types.Operator):
    bl_idname = "quick.sharp75"
    bl_label = "75"
    bl_description = "Marks edges sharp at 75 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        ss.smoothingAngle = 75

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}


class SPEEDSEAMS_OT_QuickSharp90(bpy.types.Operator):
    bl_idname = "quick.sharp90"
    bl_label = "90"
    bl_description = "Marks edges sharp at 90 degrees"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        ss.smoothingAngle = 90

        self.report({'INFO'}, "Smoothed!")
        return {'FINISHED'}
