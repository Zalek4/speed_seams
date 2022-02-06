# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class ApplyTransformsOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_transforms"
    bl_label = "All Transforms"
    bl_description = "Applies selected transforms for the selected object"

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


class ApplyLocationOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_location"
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


class ApplyRotationOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_rotation"
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


class ApplyScaleOperator(bpy.types.Operator):
    bl_idname = "do.ah_apply_scale"
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


classes = (ApplyTransformsOperator, ApplyLocationOperator,
           ApplyRotationOperator, ApplyScaleOperator)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


# honestly not sure wtf this is
if __name__ == "__main__":
    register()
