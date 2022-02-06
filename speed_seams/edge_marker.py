# info for plugin
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from gpu_extras.batch import batch_for_shader
import gpu
import bgl
import bpy


# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

# Builds a panel
class QuickUnwrapPanel(bpy.types.Panel):
    bl_label = "Quick Unwrap WTF"
    bl_category = "Quick Unwrap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

        split = layout.split()
        col = split.column(align=True)

        if obj is not None:
            col.label(text="Smoothing and UVs")
            col.prop(obj, 'seamBool')
            col.prop(obj, 'realtimeUnwrap')
            col.prop(obj, 'smoothingAngle', slider=True)
            col.operator(AHAutoSmooth.bl_idname)
            col.separator()
            col.operator(ClearSharp.bl_idname)
            col.operator(ClearSeams.bl_idname)
            col.separator()
            col.prop(obj, 'unwrapAlgorithm')
            col.operator(UnwrapSelected.bl_idname)
            col.separator()
            col.label(text="Apply Transforms")
            col.operator(ApplyTransformsOperator.bl_idname)
            col.operator(ApplyLocationOperator.bl_idname)
            col.operator(ApplyRotationOperator.bl_idname)
            col.operator(ApplyScaleOperator.bl_idname)
            col.separator()
            # col.operator(JoinObjects.bl_idname)

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH', 'OBJECT'}

# Logic for "Clear Sharp" button


class ClearSharp(bpy.types.Operator):
    bl_idname = "do.clear_sharp"
    bl_label = "Clear Sharp"
    bl_description = "Clears the selected object's sharp edges"

    # Executes automation after button press
    def execute(self, context):

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
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

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        print("Cleared UV Seams")
        self.report({'INFO'}, "Cleared UV Seams")

        return {'FINISHED'}

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
        Var_RealtimeUnwrap = bpy.context.object.realtimeUnwrap

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

        # Unwrap the object if checkbox is filled
        if Var_RealtimeUnwrap == True:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            print("Realtime Unwrap Active")

        else:
            print("Realtime Unwrap is not checked")

        return None

# Logic for "Smooth All" button


class AHAutoSmooth(bpy.types.Operator):
    bl_idname = "do.ah_autosmooth"
    bl_label = "Smooth All"
    bl_description = "Enables Autosmooth at an angle of 180 degrees"

    def execute(self, context):
        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        self.report({'INFO'}, "Cleared Sharp Edges")
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 3.1459

        return {'FINISHED'}

# Logic for "Apply Transforms" button


class ApplyTransformsOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_transforms"
    bl_label = "All Transforms"
    bl_description = "Applies selected transforms for the selected object"

    def execute(self, context):

        bpy.ops.object.transform_apply(
            location=True, rotation=True, scale=True)
        self.report({'INFO'}, "Applied All Transformations")

        return {'FINISHED'}

# Logic for "Apply Location" button


class ApplyLocationOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_location"
    bl_label = "Location"
    bl_description = "Applies the location of the selected object"

    def execute(self, context):

        bpy.ops.object.transform_apply(
            location=True, rotation=False, scale=False)
        self.report({'INFO'}, "Applied Location")

        return {'FINISHED'}

# Logic for "Apply Rotation" button


class ApplyRotationOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_rotation"
    bl_label = "Rotation"
    bl_description = "Applies the rotation of the selected object"

    def execute(self, context):

        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=False)
        self.report({'INFO'}, "Applied Rotation")

        return {'FINISHED'}

# Logic for "Apply Scale" button


class ApplyScaleOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_scale"
    bl_label = "Scale"
    bl_description = "Applies the scale of the selected object"

    def execute(self, context):

        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)
        self.report({'INFO'}, "Applied Scale")

        return {'FINISHED'}


# Logic for "Join" button
"""class JoinObjects(bpy.types.Operator):
	bl_idname = "do.ah_join_objects"
	bl_label = "Join"
	bl_description = "Joins selected objects with active object"

	def execute(self, context):

		bpy.ops.object.join()
		self.report({'INFO'}, "Joined Objects")
		return {'FINISHED'}"""


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(QuickUnwrapPanel)
    bpy.utils.register_class(ClearSharp)
    bpy.utils.register_class(ClearSeams)
    bpy.utils.register_class(UnwrapSelected)
    bpy.utils.register_class(SharpenSlider)
    bpy.utils.register_class(AHAutoSmooth)
    bpy.utils.register_class(ApplyTransformsOperator)
    bpy.utils.register_class(ApplyLocationOperator)
    bpy.utils.register_class(ApplyRotationOperator)
    bpy.utils.register_class(ApplyScaleOperator)
    # bpy.utils.register_class(JoinObjects)

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
        update=SharpenSlider.execute
    )

    bpy.types.Object.seamBool = BoolProperty(
        name="Mark Sharp as Seams",
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
    # bpy.utils.unregister_class(DrawLines)
    bpy.utils.unregister_class(QuickUnwrapPanel)
    bpy.utils.unregister_class(ClearSharp)
    bpy.utils.unregister_class(ClearSeams)
    bpy.utils.unregister_class(UnwrapSelected)
    bpy.utils.unregister_class(SharpenSlider)
    bpy.utils.unregister_class(AHAutoSmooth)
    bpy.utils.unregister_class(ApplyTransformsOperator)
    bpy.utils.unregister_class(ApplyLocationOperator)
    bpy.utils.unregister_class(ApplyRotationOperator)
    bpy.utils.unregister_class(ApplyScaleOperator)
    """bpy.utils.unregister_class(JoinObjects)"""


# honestly not sure wtf this is
if __name__ == "__main__":
    register()
