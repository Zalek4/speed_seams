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


class HighlightUnifiedEdges(bpy.types.Operator):
    bl_idname = "do.highlight_unified_edges"
    bl_label = "Highlight Unified Edges"
    bl_description = "Shows edges that are marked as both sharp and UV seams"

    # Executes automation after button press
    def execute(self, context):

        #collection = bpy.data.collections.new("MyTestCollection")
        # bpy.context.scene.collection.children.link(collection)
        active_object = bpy.context.selected_objects[0]

        if context.mode == 'OBJECT':
            obj = bpy.context.active_object
            me = bpy.context.object.data

            bpy.ops.object.editmode_toggle()
            bm = bmesh.from_edit_mesh(me)

            # Find and select edges that are both sharp and UV seams
            for e in bm.edges:
                if not e.smooth:
                    if e.seam:
                        e.select = True
            bmesh.update_edit_mesh(me)

            # Duplicate edges off, separate them, and convert them to a grease pencil object
            bpy.ops.mesh.duplicate_move()
            # bpy.ops.mesh.separate(type='SELECTED')
            # bpy.ops.object.editmode_toggle()

            org_obj_list = {obj.name for obj in context.selected_objects}
            # This is a Set comprehension in Python,
            # which create a set of name from the context.selected_objects
            # context.selected_objects will be a Iterable collection of some object

            bpy.ops.mesh.separate(type='SELECTED')
            # This will call the separate operator in your code directly
            # the type can be a enum string in ['SELECTED', 'LOOSE', 'MATERIAL']

            bpy.ops.object.editmode_toggle()
            # Switch back to object mode from edit mode

            # Those separated object will also be selected now
            # We then check if selected object is the one we saved before, then deselect it.
            for obj in context.selected_objects:
                if obj and obj.name in org_obj_list:
                    # Deselect selected object
                    obj.select_set(False)
                else:
                    # Set the new created object to active
                    context.view_layer.objects.active = obj

            bpy.ops.object.convert(target='GPENCIL')
            bpy.context.object.name = active_object.name + "_gp_highlights"
            #bpy.context.view_layer.objects.active = active_object.name + "_gp_highlights"

            C = bpy.context
            for i in range(1, len(C.object.material_slots)):
                C.object.active_material_index = 1
                bpy.ops.object.material_slot_remove()

            bpy.ops.gpencil.editmode_toggle()
            bpy.ops.gpencil.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.context.object.active_material.grease_pencil.color = (
                1, 1, 1, 1)
            bpy.ops.gpencil.editmode_toggle()
            context.view_layer.objects.active = active_object
            active_object.select_set(True)
            bpy.ops.object.parent_set(type='OBJECT')

        else:
            bpy.ops.object.editmode_toggle()
            obj = bpy.context.active_object
            me = bpy.context.object.data

            bpy.ops.object.editmode_toggle()
            bm = bmesh.from_edit_mesh(me)

            # Find and select edges that are both sharp and UV seams
            for e in bm.edges:
                if not e.smooth:
                    if e.seam:
                        e.select = True
            bmesh.update_edit_mesh(me)

            # Duplicate edges off, separate them, and convert them to a grease pencil object
            bpy.ops.mesh.duplicate_move()
            # bpy.ops.mesh.separate(type='SELECTED')
            # bpy.ops.object.editmode_toggle()

            org_obj_list = {obj.name for obj in context.selected_objects}
            # This is a Set comprehension in Python,
            # which create a set of name from the context.selected_objects
            # context.selected_objects will be a Iterable collection of some object

            bpy.ops.mesh.separate(type='SELECTED')
            # This will call the separate operator in your code directly
            # the type can be a enum string in ['SELECTED', 'LOOSE', 'MATERIAL']

            bpy.ops.object.editmode_toggle()
            # Switch back to object mode from edit mode

            # Those separated object will also be selected now
            # We then check if selected object is the one we saved before, then deselect it.
            for obj in context.selected_objects:
                if obj and obj.name in org_obj_list:
                    # Deselect selected object
                    obj.select_set(False)
                else:
                    # Set the new created object to active
                    context.view_layer.objects.active = obj

            bpy.ops.object.convert(target='GPENCIL')
            bpy.context.object.name = active_object.name + "_gp_highlights"
            #bpy.context.view_layer.objects.active = active_object.name + "_gp_highlights"

            C = bpy.context
            for i in range(1, len(C.object.material_slots)):
                C.object.active_material_index = 1
                bpy.ops.object.material_slot_remove()

            bpy.ops.gpencil.editmode_toggle()
            bpy.ops.gpencil.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.context.object.active_material.grease_pencil.color = (
                1, 1, 1, 1)

            bpy.ops.gpencil.editmode_toggle()
            context.view_layer.objects.active = active_object
            active_object.select_set(True)
            bpy.ops.object.parent_set(type='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            active_object.select_set(True)
            bpy.ops.object.editmode_toggle()

        self.report({'INFO'}, "Highlighted Unified Edges")
        return {'FINISHED'}


classes = (HighlightUnifiedEdges, )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
