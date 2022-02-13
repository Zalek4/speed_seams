import bpy
import gpu
import bgl
from mathutils import Vector
from gpu_extras.batch import batch_for_shader
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       )
import bmesh
from struct import pack

# class DarrowToolPanel(bpy.types.Panel):
#     bl_label = "DarrowGL"
#     bl_category = "Darrow OpenGL"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_idname = "DARROW_PT_openGLPanel"

#     def draw(self, context):
#         layout = self.layout
#         objs = context.selected_objects
#         obj = context.active_object
#         Var_compactBool = True
#         if obj is not None:
#             split = layout.box()
#             col = split.column(align=True)
#             col.scale_y = 1.2
#             col.operator('remove.handle', icon="OUTLINER_COLLECTION")
#             col.operator('draw.handle', icon="OUTLINER_COLLECTION")

#-----------------------------------------------------#
#    handles
#-----------------------------------------------------#

class SPEEDSEAMS_OT_drawOverlay(bpy.types.Operator):
    bl_idname = "draw.gpu_handle"
    bl_description = ""
    bl_label = "Display Edges"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator
    

    def execute(self, context):
        shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
        ob = bpy.context.object
        mat = ob.matrix_world
        if bpy.context.mode != 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        bm = bmesh.from_edit_mesh(ob.data)
        bpy.ops.mesh.select_all(action='DESELECT')
        sel = []
        def get_coords():
            for e in bm.edges:
                if not e.smooth:
                    e.select = True
                    sel.append(e)
                else:
                    e.select = False
            list = [v for v in bm.verts if v.select]
            return [mat @ v.co for v in list]
        get_coords()

        edgeindices = [(v.index for v in e.verts) for e in bm.edges if e.select]
        batch = batch_for_shader(
            shader, 'LINES', {"pos": get_coords()}, indices=edgeindices)
        r, g, b, a = 1.0, 1.0, 0.0, 1.0
    
        try:
            bpy.types.SpaceView3D.draw_handler_remove(
                bpy._ahGLDrawing, 'WINDOW')
            print("Attempting to remove existing overlay")
        except:
            print("No drawing to remove")
                        
        def draw():
            if bpy.context.mode == 'EDIT_MESH':
                bgl.glLineWidth(10)
                shader.bind()
                color = shader.uniform_from_name("color")
                shader.uniform_vector_float(color, pack("4f", r, g, b, a), 4)
                batch.draw(shader)

        if len(get_coords()) is not 0: 
            bpy._ahGLDrawing = bpy.types.SpaceView3D.draw_handler_add(
                    draw, (), 'WINDOW', 'POST_VIEW')
        else:
            self.report({'INFO'}, "No conditions met to display overlay")
        return {'FINISHED'}

#-----------------------------------------------------#
#    handles removing
#-----------------------------------------------------#

class SPEEDSEAMS_OT_removeOverlay(bpy.types.Operator):
    bl_idname = "draw.remove_handle"
    bl_description = ""
    bl_label = "Remove Display"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator

    def execute(self, context):
        try:
            bpy.types.SpaceView3D.draw_handler_remove(
                bpy._ahGLDrawing, 'WINDOW')
            for area in bpy.context.window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        except:
            print("No drawing to remove")
        self.report({'INFO'}, "None overlay to remove")
        return {'FINISHED'}

#-----------------------------------------------------#
#   Registration classes
#-----------------------------------------------------#

classes = (SPEEDSEAMS_OT_drawOverlay, SPEEDSEAMS_OT_removeOverlay)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()


# import bpy
# import gpu
# import bgl
# import blf
# from gpu_extras.batch import batch_for_shader

# import bmesh


# class GpuOverlay(bpy.types.Operator):
#     bl_idname = "do.gpu_overlay"
#     bl_label = "GPU Overlay"
#     bl_description = "Uses the GPU api to draw lines in the viewport. Blender must be restarted to remove them."

#     #FloatValue = bpy.context.object.smoothingAngle
#     #print("Initial Button Value =", FloatValue)

#     # Executes automation after button press
#     def __init__(self, context, prop):
#         self.prop = prop
#         self.handle = bpy.types.SpaceView3D.draw_handler_add(
#             self.draw_text_callback, (context,),
#             'WINDOW', 'POST_PIXEL')

#     def draw_text_callback(self, context):
#         font_id = 0  # XXX, need to find out how best to get this.

#         # draw some text
#         blf.position(font_id, 15, 50, 0)
#         blf.size(font_id, 20, 72)
#         blf.draw(font_id, "%s %s" % (context.scene.name, self.prop))

#     def remove_handle(self):
#         bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')


# context = bpy.context
# dns = bpy.app.driver_namespace
# dns["dc"] = GpuOverlay(context, "Draw This On Screen")

# """def draw_lines(self, context):
#          data = bpy.context.active_object.data

#          bm = bmesh.from_edit_mesh(data)

#          faces = [f for f in bm.faces if f.select == True]

#          dbm = bmesh.new()
#          for face in faces:
#              dbm.faces.new((dbm.verts.new(v.co, v) for v in face.verts), face)
#          dbm.verts.index_update()

#          vertices = [v.co for v in dbm.verts]
#          faceindices = [(loop.vert.index for loop in looptris)
#                         for looptris in dbm.calc_loop_triangles()]
#          face_colors = [(0.9, 0.25, 0.25, 1) for _ in range(len(dbm.verts))]

#          edgeindices = [(v.index for v in e.verts) for e in dbm.edges]
#          edges_colors = [(0, 1.0, 0.25, 1) for _ in range(len(dbm.verts))]

#          shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
#          batch1 = batch_for_shader(
#              shader, 'TRIS',
#              {"pos": vertices, "color": face_colors},
#              indices=faceindices,
#          )
#          batch2 = batch_for_shader(
#              shader, 'LINES',
#              {"pos": vertices, "color": edges_colors},
#              indices=edgeindices,
#          )

#          bgl.glLineWidth(5)

#          def draw():
#              # batch1.draw(shader)
#              batch2.draw(shader)

#          my_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
#              draw, (), 'WINDOW', 'POST_VIEW')"""
# #bpy.types.SpaceView3D.draw_handler_remove(my_draw_handler, 'WINDOW')

# #self.report({'INFO'}, "Marked Edges!")
# # return {'FINISHED'}

# """def end(self, context):
#             context.space_data.draw_handler_remove("WINDOW")
#             context.area.tag_redraw()
#             print("Ran end function")
#             return {'FINISHED'}

#             edgeindices = []
#             vertices = []
#             shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
#             edges_colors = [(0.0, 1.0, 0.25, 1) for _ in range(len(dbm.verts))]

#             batch_clear = batch_for_shader(
#                 shader, 'LINES',
#                 {"pos": vertices, "color": edges_colors},
#                 indices=edgeindices,
#             )

#             def draw():
#                 batch_clear.draw(shader)

#             my_draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_VIEW')"""


# class GpuOverlayRemove(bpy.types.Operator):
#     bl_idname = "do.gpu_overlay_remove"
#     bl_label = "Remove GPU Overlay"
#     bl_description = "Uses the GPU api to draw lines in the viewport. Blender must be restarted to remove them."

#     #FloatValue = bpy.context.object.smoothingAngle
#     #print("Initial Button Value =", FloatValue)

#     # Executes automation after button press
#     def execute(self, context):

#         GpuOverlay.end(GpuOverlay(self), GpuOverlay(context))

#         self.report({'INFO'}, "Removed GPU Draw Handler")
#         return {'FINISHED'}


# classes = (GpuOverlay, GpuOverlayRemove)


# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)


# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)
