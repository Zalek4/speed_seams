# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

class SPEEDSEAMS_OT_SetTD(bpy.types.Operator):
    bl_idname = "set.td"
    bl_label = "Set Texel Density"
    bl_description = "Sets texel density of UVs"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        bpy.ops.object.texel_density_set()

        return{'FINISHED'}