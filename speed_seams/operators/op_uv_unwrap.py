# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------

class SPEEDSEAMS_OT_UnwrapSelected(bpy.types.Operator):
    bl_idname = "unwrap.selected"
    bl_label = "Unwrap Object"
    bl_description = "Unwraps, averages, and packs UVs"

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings

        Var_UnwrapMethod = ss.unwrapAlgorithm
        Var_Packmaster = ss.packmasterBool

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)

        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        else:
            print("")

        if Var_UnwrapMethod == 'UA1':

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')

            if ss.packmasterBool == True:
                self.packmaster(context)

            else:
                self.report({'INFO'}, "Unwrapped UVs -- Conformal")
                return {'FINISHED'}

        elif Var_UnwrapMethod == 'UA2':

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            self.report({'INFO'}, "Unwrapped UVs -- Angle-Based")

            if ss.packmasterBool == True:
                self.packmaster(context)

            else:
                self.report({'INFO'}, "Unwrapped UVs -- Angle-Based")
                return {'FINISHED'}

        else:
            self.report({'ERROR'}, "Unknown unwrap algorithm")

        return {'FINISHED'}

    def packmaster(self, context):
        scene = context.scene
        ss = scene.ss_settings
        Var_UnwrapMethod = ss.unwrapAlgorithm
        Var_Packmaster = ss.packmasterBool

        print("hello I'm working")
        try:
            #tries this first just to throw the except if it doesn't exist
            bpy.ops.uvpackmaster3.pack(
                mode_id="pack.single_tile", pack_to_others=False)

            #Does the real thing if it doesn't fail
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.select_all(action='SELECT')

            if Var_UnwrapMethod == 'UA1':
                bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
            else:
                bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)

            bpy.ops.uvpackmaster3.pack(
                mode_id="pack.single_tile", pack_to_others=False)

            if Var_UnwrapMethod == 'UA1':
                self.report({'INFO'}, "Unwraped UVs -- Conformal -- UVPackmaster3")
            else:
                self.report({'INFO'}, "Unwraped UVs -- Angle-Based -- UVPackmaster3")

        except:

            try:
                #tries this first just to throw the except if it doesn't exist
                bpy.ops.uvpackmaster2.uv_pack()

                #Does the real thing if it doesn't fail
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.select_all(action='SELECT')

                if Var_UnwrapMethod == 'UA1':
                    bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
                else:
                    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)

                bpy.ops.uvpackmaster2.uv_pack()

                if Var_UnwrapMethod == 'UA1':
                    self.report({'INFO'}, "Unwraped UVs -- Conformal -- UVPackmaster2")
                else:
                    self.report({'INFO'}, "Unwraped UVs -- Angle-Based -- UVPackmaster2")

            except:
                self.report(
                    {'ERROR'}, "No version of UVPackmaster is installed")