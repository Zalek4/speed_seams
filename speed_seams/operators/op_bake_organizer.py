# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

from bpy import context
import bmesh
import bpy
from mathutils.bvhtree import BVHTree
from mathutils import Vector

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
    bl_description = "Pairs high/low objects based on the amount they overlap"

    def execute(self, context):

        #These would need to be the locations of the high and low meshes
        a = Vector((-5, 0, 0))
        b = Vector((5, 0, 0))

        scene = context.scene

        #WTAF
        while True:
            hit, loc, norm, idx, ob, M = scene.ray_cast(context.evaluated_depsgraph_get(), 
            a, (b - a), distance=(b - a).length,)
            if hit:
                #Here, we could add a value to 1 and compare the end sum to the number of verts on the low
                #If the number of hits is within 1 percent of the number of LP verts, then match the objects
                print(f"Hit, removing {ob.name}")
                #bpy.data.objects.remove(ob)
                continue
            break

        return {'FINISHED'}

        #for obj in bpy.data.scenes["Scene"].ss_collection_high.all_objects:
            #print("high obj: ", obj.name)

        #for obj in bpy.data.scenes["Scene"].ss_collection_low.all_objects:
            #print("low obj: ", obj.name)

        #globalcoordinate = Vector((x, y, z))
        #localcoordinateforobject = (globalcoordinate - object.location) * object.matrix_world.inverted()

        #C = bpy.context

        # Build BVH once
        #bvh = BVHTree.FromObject(C.object, C.evaluated_depsgraph_get())

        #for i in range(999999):
            # Slower, this possibly builds BVH everytime
            # C.object.ray_cast((0, 0, 0), (0, 0, -1))

            # Faster
        #bvh.ray_cast((0, 0, 0), (0, 0, -1))
        #print (bvh.ray_cast((0, 0, 0), (0, 0, -1)))

        #return {'FINISHED'}


class SPEEDSEAMS_OT_SortHighObjects(bpy.types.Operator):
    bl_idname = "sort.high_objects"
    bl_label = "Add to HP collection"
    bl_description = "Adds the selected objects to the Highpoly collection of current bake group"

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings
        bg_high_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixHigh

        # List of object references
        objs = bpy.context.selected_objects

        # Set target collection to a known collection        

        bg_high_collection = bpy.data.collections.get(bg_high_name)
        print(bg_high_collection)
        print(objs)

        # If target found and object list not empty
        if bg_high_collection:
            print("Target collection is: " + bg_high_name)
            if objs:
                print("Moving objects...")

                # Loop through all objects
                for ob in objs:
                    print(objs)
                    # Loop through all collections the obj is linked to
                    for coll in ob.users_collection:
                        # Unlink the object
                        coll.objects.unlink(ob)

                    # Link each object to the target collection
                    bg_high_collection.objects.link(ob)

        return {'FINISHED'}


class SPEEDSEAMS_OT_SortLowObjects(bpy.types.Operator):
    bl_idname = "sort.low_objects"
    bl_label = "Add to LP collection"
    bl_description = "Adds the selected objects to the Lowpoly collection of current bake group"

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings
        bg_low_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixLow

        # List of object references
        objs = bpy.context.selected_objects

        # Set target collection to a known collection

        bg_low_collection = bpy.data.collections.get(bg_low_name)
        print(bg_low_collection)
        print(objs)

        # If target found and object list not empty
        if bg_low_collection:
            print("Target collection is: " + bg_low_name)
            if objs:
                print("Moving objects...")

                # Loop through all objects
                for ob in objs:
                    print(objs)
                    # Loop through all collections the obj is linked to
                    for coll in ob.users_collection:
                        # Unlink the object
                        coll.objects.unlink(ob)

                    # Link each object to the target collection
                    bg_low_collection.objects.link(ob)

        return {'FINISHED'}
