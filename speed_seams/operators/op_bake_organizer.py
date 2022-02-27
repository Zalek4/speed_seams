# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

import bpy

# ------------------------------------------------------------------------
#    Classes
# ------------------------------------------------------------------------


class SPEEDSEAMS_OT_OrganizeHighLowCollections(bpy.types.Operator):
    bl_idname = "create.high_low_collections"
    bl_label = "Organize High/Low Collections"
    bl_description = "Sets up bake collections for high/low object sets"

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings
        bg_name = ss.bakePrepAssetName + "_" + "bake_group"
        bg_low_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixLow
        bg_high_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixHigh

        # Get all collections of the scene and their parents in a dict
        coll_scene = bpy.context.scene.collection
        coll_parents = parent_lookup(coll_scene)

        #Check to see if the bake group exists
        bg_collection = bpy.data.collections.get(bg_name)
        if bg_collection:
            print("'Bake Group' collection already exists")

            #Check to see if the High collection exists. Make it if it doesn't
            bg_high_collection = bpy.data.collections.get(bg_high_name)
            if bg_high_collection:
                print("'High' collection already exists. Moving it to proper collection...")

                bg_high_collection_parent = coll_parents.get(bg_high_collection.name)

                if bg_high_collection_parent:
                    #unlink
                    bg_high_collection_parent.children.unlink(bg_high_collection)

                    #relink
                    bg_collection.children.link(bg_high_collection)

            else:
                print("'High' collection doesn't exist. Creating it...")
                bg_high_collection = bpy.data.collections.new(bg_high_name)
                bg_collection.children.link(bg_high_collection)

            #Check to see if the Low collection exists. Make it if it doesn't
            bg_low_collection = bpy.data.collections.get(bg_low_name)
            if bg_low_collection:
                print("'Low' collection already exists. Moving it to proper collection...")

                bg_low_collection_parent = coll_parents.get(bg_low_collection.name)

                if bg_low_collection_parent:
                    #unlink
                    bg_low_collection_parent.children.unlink(bg_low_collection)

                    #relink
                    bg_collection.children.link(bg_low_collection)

            else:
                print("'Low' collection doesn't exist. Creating it...")
                bg_low_collection = bpy.data.collections.new(bg_low_name)
                bg_collection.children.link(bg_low_collection)

        else:
            print("'Bake Group' collection doesn't exist. Creating it...")
            bg_collection = bpy.data.collections.new(bg_name)
            bpy.context.scene.collection.children.link(bg_collection)
            bg_collection = bpy.data.collections.get(bg_name)

            bg_high_collection = bpy.data.collections.get(bg_high_name)
            if bg_high_collection:
                print("'High' collection already exists. Moving it to proper collection...")

                bg_high_collection_parent = coll_parents.get(bg_high_collection.name)

                if bg_high_collection_parent:
                    #unlink
                    bg_high_collection_parent.children.unlink(bg_high_collection)

                    #relink
                    bg_collection.children.link(bg_high_collection)
            else:
                print("'High' collection doesn't exist. Creating it...")
                bg_high_collection = bpy.data.collections.new(bg_high_name)
                bg_collection.children.link(bg_high_collection)

            bg_low_collection = bpy.data.collections.get(bg_low_name)
            if bg_low_collection:
                print("'Low' collection already exists. Moving it to proper collection...")

                bg_low_collection_parent = coll_parents.get(bg_low_collection.name)

                if bg_low_collection_parent:
                    #unlink
                    bg_low_collection_parent.children.unlink(bg_low_collection)

                    #relink
                    bg_collection.children.link(bg_low_collection)
            else:
                print("'Low' collection doesn't exist. Creating it...")
                bg_low_collection = bpy.data.collections.new(bg_low_name)
                bg_collection.children.link(bg_low_collection)

        scene.ss_collection_high = bg_high_collection
        scene.ss_collection_low = bg_low_collection

        return {'FINISHED'}


def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)


def parent_lookup(coll):
    parent_lookup = {}
    for coll in traverse_tree(coll):
        for c in coll.children.keys():
            parent_lookup.setdefault(c, coll)
    print(parent_lookup)
    return parent_lookup

class SPEEDSEAMS_OT_PairHighLowObjects(bpy.types.Operator):
    bl_idname = "pair.high_low_objects"
    bl_label = "Pair High/Low Meshes"
    bl_description = "Not super sure what this does yet"

    def execute(self, context):

        for obj in bpy.data.scenes["Scene"].ss_collection_high.all_objects:
            print("high obj: ", obj.name)

        for obj in bpy.data.scenes["Scene"].ss_collection_low.all_objects:
            print("low obj: ", obj.name)

        self.report({'INFO'}, "Ran organization op")

        return {'FINISHED'}
