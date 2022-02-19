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

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)

        if Var_UnwrapMethod == 'UA1':

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            self.report({'INFO'}, "Unwrapped UVs -- Conformal")

        elif Var_UnwrapMethod == 'UA2':
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.01)
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands(rotate=True, margin=0.01)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.context.scene.tool_settings.uv_select_mode = ('ISLAND')
            self.report({'INFO'}, "Unwrapped UVs -- Angle-Based")

        elif Var_UnwrapMethod == 'UA3':

            try:

                #tries this first just to throw the except if it doesn't exist
                bpy.ops.uvpackmaster3.pack(
                    mode_id="pack.single_tile", pack_to_others=False)

                #Does the real thing if it doesn't fail
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
                bpy.ops.uvpackmaster3.pack(
                    mode_id="pack.single_tile", pack_to_others=False)
                self.report(
                    {'WARNING'}, "Unwraped and packed with UVPackmaster3")
                
            except:

                try:
                    #tries this first just to throw the except if it doesn't exist
                    bpy.ops.uvpackmaster2.uv_pack()

                    #Does the real thing if it doesn't fail
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
                    bpy.ops.uvpackmaster2.uv_pack()
                    self.report(
                        {'WARNING'}, "Unwraped and packed with UVPackmaster2")

                except:
                    self.report(
                        {'ERROR'}, "No version of UVPackmaster is installed")

        else:
            self.report({'ERROR'}, "Unknown unwrap algorithm")

        return {'FINISHED'}


