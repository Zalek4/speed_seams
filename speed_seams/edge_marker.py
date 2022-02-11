# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy
import bmesh
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

# Logic for "Clear Sharp" button


class ClearSharp(bpy.types.Operator):
    bl_idname = "do.clear_sharp"
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

# Logic for "Clear UV Seams" button


class ClearSeams(bpy.types.Operator):
    bl_idname = "do.clear_seams"
    bl_label = "Clear UV Seams"
    bl_description = "Clears the selected object's UV seams"

    #FloatValue = bpy.context.object.smoothingAngle
    #print("Initial Button Value =", FloatValue)

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


class MarkSharpAsSeams(bpy.types.Operator):
    bl_idname = "do.mark_sharp_as_seams"
    bl_label = "Mark Sharp as Seams"
    bl_description = "Marks current sharp edges as UV seams"

    #FloatValue = bpy.context.object.smoothingAngle
    #print("Initial Button Value =", FloatValue)

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


"""class MarkSeamsAsSharp(bpy.types.Operator):
    bl_idname = "do.mark_seams_as_sharp"
    bl_label = "Mark Seams as Sharp"
    bl_description = "Marks current UV seams as sharp edges"

    #FloatValue = bpy.context.object.smoothingAngle
    #print("Initial Button Value =", FloatValue)

    # Executes automation after button press

    def execute(self, context):

        obj = bpy.context.active_object
        me = bpy.context.object.data
        #bm = bmesh.from_edit_mesh(me)

        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            bm = bmesh.from_edit_mesh(me)

            for e in bm.edges:
                if e.seam:
                    e.select = True
                    e.smooth = False

            bmesh.update_edit_mesh(me, False)
            bpy.ops.object.editmode_toggle()

        else:
            bm = bmesh.from_edit_mesh(me)
            for e in bm.edges:
                if e.seam:
                    e.select = True
                    e.smooth = False
            bmesh.update_edit_mesh(me, False)

        self.report({'INFO'}, "Marked Seams as Sharp")
        return {'FINISHED'}"""

# Logic for "Unwrap the Selected Object" button


class UnwrapSelected(bpy.types.Operator):
    bl_idname = "do.ah_unwrap"
    bl_label = "Unwrap Object"
    bl_description = "Unwraps, averages, and packs UVs"

    def execute(self, context):

        Var_UnwrapMethod = bpy.context.object.unwrapAlgorithm
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

# Logic for "Smoothing Angle" slider


class SharpenSlider(bpy.types.Operator):
    bl_idname = "do.ah_smooth"
    bl_label = "Smooth and Sharpen"
    bl_description = "Sets 'Autosmooth' and 'Sharp Edges' at slider angle"
    bl_context = 'mesh_edit'

    #FloatValue = bpy.context.object.smoothingAngle
    #print("Initial Button Value =", FloatValue)

    # Executes automation after button press
    def execute(self, context):

        # ------------------------------------------------------------------------
        #    Smoothing Logic
        # ------------------------------------------------------------------------

        # Variables
        Var_AngleValue = bpy.context.object.smoothingAngle
        Var_SeamBool = bpy.context.object.seamBool
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

# Logic for "Smooth All" button


class AHAutoSmooth(bpy.types.Operator):
    bl_idname = "do.ah_autosmooth"
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


classes = (AHAutoSmooth, SharpenSlider, UnwrapSelected,
           ClearSeams, ClearSharp, MarkSharpAsSeams, )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
