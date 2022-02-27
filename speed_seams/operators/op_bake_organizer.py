# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class SPEEDSEAMS_OT_CreateHighLowCollections(bpy.types.Operator):
    bl_idname = "create.high_low_collections"
    bl_label = "Create High/Low Collections"
    bl_description = "Sets up bake collections for high/low object sets"

    def execute(self, context):
        bg_name = "Bake Group"
        bg_low_name = "Low"
        bg_high_name = "High"
        scene_collection_name = "Scene Collection"
        scene = context.scene

        scene_collection = bpy.context.scene.collection.children.get(scene_collection_name)
        bg_collection = bpy.context.scene.collection.children.get(bg_name)
        if bg_collection:
            print("'Bake Group' collection already exists")

            bg_high_collection = bpy.context.scene.collection.children.get(bg_high_name)
            if bg_high_collection:
                print("'High' collection already exists")
                scene.collection.children.unlink(bg_high_collection)
                bg_collection.children.link(bg_high_collection)
            else:
                print("'High' collection doesn't exist!!!")
                bg_high_collection = bpy.data.collections.new(bg_high_name)
                bg_collection.children.link(bg_high_collection)

            bg_low_collection = bpy.context.scene.collection.children.get(bg_low_name)
            if bg_low_collection:
                print("'Low' collection already exists")
                scene.collection.children.unlink(bg_low_collection)
                bg_collection.children.link(bg_low_collection)
            else:
                print("'Low' collection doesn't exist!!!")
                bg_low_collection = bpy.data.collections.new(bg_low_name)
                bg_collection.children.link(bg_low_collection)

        else:
            print("'Bake Group' collection doesn't exist. Creating it...")
            bg_collection = bpy.data.collections.new(bg_name)
            bpy.context.scene.collection.children.link(bg_collection)
            bg_collection = bpy.context.scene.collection.children.get(bg_name)


            bg_high_collection = bpy.context.scene.collection.children.get(bg_high_name)
            if bg_high_collection:
                print("'High' collection already exists")
                scene.collection.children.unlink(bg_high_collection)
                bg_collection.children.link(bg_high_collection)
            else:
                print("'High' collection doesn't exist. Creating it...")
                bg_high_collection = bpy.data.collections.new(bg_high_name)
                bg_collection.children.link(bg_high_collection)


            bg_low_collection = bpy.context.scene.collection.children.get(bg_low_name)
            if bg_low_collection:
                print("'Low' collection already exists")
                scene.collection.children.unlink(bg_low_collection)
                bg_collection.children.link(bg_low_collection)
            else:
                print("'Low' collection doesn't exist. Creating it...")
                bg_low_collection = bpy.data.collections.new(bg_low_name)
                bg_collection.children.link(bg_low_collection)
        

        """for obj in scene:
            if obj.type == "EMPTY":
                for coll in obj.users_collection:
                    coll.objects.unlink(obj)
                bpy.data.collections[empty_collection_name].objects.link(obj)
                obj.hide_set(True)

        vlayer = bpy.context.scene.view_layers["View Layer"]
        vlayer.layer_collection.children[empty_collection_name].hide_viewport = True
        bpy.data.collections[empty_collection_name].color_tag = 'COLOR_01'
        bpy.ops.object.select_all(action='DESELECT')

        for x in old_obj:
            x.select_set(state=True)"""


        return {'FINISHED'}


class SPEEDSEAMS_OT_Organize_Objects(bpy.types.Operator):
    bl_idname = "organize.objects"
    bl_label = "Organize"
    bl_description = "Not super sure what this does yet"

    def execute(self, context):

        for obj in bpy.data.scenes["Scene"].ss_collection_high.all_objects:
            print("high obj: ", obj.name)

        for obj in bpy.data.scenes["Scene"].ss_collection_low.all_objects:
            print("low obj: ", obj.name)

        self.report({'INFO'}, "Ran organization op")

        return {'FINISHED'}
