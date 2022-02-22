# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class SPEEDSEAMS_OT_Apply_Transforms(bpy.types.Operator):
    bl_idname = "apply.transforms"
    bl_label = "All Transforms"
    bl_description = "Applies all transforms for the selected object"

    def execute(self, context):

        if context.mode == 'OBJECT':
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True)

        else:
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True)
            bpy.ops.object.editmode_toggle()

        self.report({'INFO'}, "Applied All Transformations")

        return {'FINISHED'}

# Logic for "Apply Location" button


class SPEEDSEAMS_OT_ApplyLocation(bpy.types.Operator):
    bl_idname = "apply.location"
    bl_label = "Location"
    bl_description = "Applies the location of the selected object"

    def execute(self, context):

        if context.mode == 'OBJECT':
            bpy.ops.object.transform_apply(
                location=True, rotation=False, scale=False)

        else:
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.transform_apply(
                location=True, rotation=False, scale=False)
            bpy.ops.object.editmode_toggle()

        self.report({'INFO'}, "Applied Location")

        return {'FINISHED'}

# Logic for "Apply Rotation" button


class SPEEDSEAMS_OT_ApplyRotation(bpy.types.Operator):
    bl_idname = "apply.rotation"
    bl_label = "Rotation"
    bl_description = "Applies the rotation of the selected object"

    def execute(self, context):

        if context.mode == 'OBJECT':
            bpy.ops.object.transform_apply(
                location=False, rotation=True, scale=False)

        else:
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.transform_apply(
                location=False, rotation=True, scale=False)
            bpy.ops.object.editmode_toggle()

        self.report({'INFO'}, "Applied Rotation")

        return {'FINISHED'}

# Logic for "Apply Scale" button


class SPEEDSEAMS_OT_ApplyScale(bpy.types.Operator):
    bl_idname = "apply.scale"
    bl_label = "Scale"
    bl_description = "Applies the scale of the selected object"

    def execute(self, context):

        if context.mode == 'OBJECT':
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

        else:
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)
            bpy.ops.object.editmode_toggle()

        self.report({'INFO'}, "Applied Scale")

        return {'FINISHED'}
