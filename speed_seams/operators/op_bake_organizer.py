# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class SPEEDSEAMS_OT_Organize_Objects(bpy.types.Operator):
    bl_idname = "organize.objects"
    bl_label = "Organize"
    bl_description = "Sets up bake collections for high/low object sets"

    def execute(self, context):

        for obj in bpy.data.scenes["Scene"].ss_collection_high.all_objects:
            print("high obj: ", obj.name)

        for obj in bpy.data.scenes["Scene"].ss_collection_low.all_objects:
            print("low obj: ", obj.name)

        self.report({'INFO'}, "Ran organization op")

        return {'FINISHED'}
