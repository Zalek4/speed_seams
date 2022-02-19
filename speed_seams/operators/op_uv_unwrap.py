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
        print(Var_UnwrapMethod)

        bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)

        if context.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        else:
            print("Context is not 'Object' it is", context.mode)

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
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.unwrap(method='CONFORMAL', margin=0.01)
                bpy.ops.uvpackmaster3.pack(
                    mode_id="pack.single_tile", pack_to_others=False)
                self.report({'INFO'}, "Unwrapped UVs -- UVPackmaster")
                
            except:
                self.report({'ERROR'}, "UVPackmaster is not installed, or is unable to be found")
            
            

        else:
            self.report({'ERROR'}, "Unknown unwrap algorithm")

        return {'FINISHED'}


