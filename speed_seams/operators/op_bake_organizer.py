# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------

from bpy import context
import time
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
        scene = context.scene
        ss = scene.ss_settings
        matchAccuracy = ss.matchAccuracy * .01
        bg_low_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixLow
        bg_high_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixHigh

        #Get collection names and print them
        bg_high_collection = bpy.data.collections.get(bg_high_name)
        bg_low_collection = bpy.data.collections.get(bg_low_name)

        print("Using " + str(bg_low_collection.name) + " as Lowpoly collection")
        print("Using " + str(bg_high_collection.name) + " as Highpoly collection")

        #Hide all high and low objects
        for lowObject in bg_low_collection.all_objects:
            lowObject.hide_set(True)

        for highObject in bg_high_collection.all_objects:
            highObject.hide_set(True)

        print("Match Percentage: " + str(ss.matchAccuracy) + "%")

        #Look at each mesh in the low collection
        for lowObject in bg_low_collection.all_objects:

            #reset the variables
            normalList = []
            transformList = []
            vertexCount = 0
            
            #Get vertex data of current low mesh
            for v in lowObject.data.vertices:
                #get the vertex count
                vertexCount = vertexCount + 1
                #get the normal of the vertex and append it to the normal dictionary
                n = v.normal
                n = n * -1
                normalList.append(n)

                #get the location of the vertex and append it to the location dictionary
                coords = lowObject.matrix_world @ v.co
                transformList.append(coords)
            
            #print(lowObject.name)
            #print(lowObject.name + "'s Vertex Count: " + str(vertexCount))
            #print("Normal List: " + str(normalList))
            #print("Transform List: " + str(transformList))

            #cycle through each high object and raycast onto each
            for highObject in bg_high_collection.all_objects:

                #Do traces, and report the name of the object each hits
                index = 0
                hitCount = 0
                highObject.hide_set(False)

                print("Looking for the match for " + str(lowObject.name) + "...")

                for i in range(len(normalList)):

                    hit, loc, norm, idx, ob, M = scene.ray_cast(context.evaluated_depsgraph_get(), transformList[index], normalList[index], distance=0.3)
                    
                    #print("Raycast location: " + str(transformList[index]))
                    #print("Normal direction: " + str(normalList[index]))

                    if hit:
                        #add 1 to the hitCount and print what we hit
                        hitCount = hitCount + 1
                        print("Hit " + str(ob.name) + " - Total: " + str(hitCount))

                    #add 1 to the index so we can move to the next object
                    index = index + 1

                    #print a miss
                    if not hit:
                        print("Missed")

                    #compare the hit count with the vert count every check. If more than half the hits match a highpoly object, exit the loop.
                    if hitCount/vertexCount >= matchAccuracy:
                        matchAccuracy = matchAccuracy * 100
                        print("More than " + str(matchAccuracy) + "% of the lowpoly verts match " + str(highObject.name))
                        break
                
                #compare the hit count with the vert count every highpoly object. If more than half the hits match a highpoly object, exit the loop.
                if hitCount/vertexCount >= matchAccuracy:
                    print("Skipping all other HP checks")
                    break
                
                #hide the highpoly object
                highObject.hide_set(True)
                #time.sleep(0.1)

        #Unhide everything
        for lowObject in bg_low_collection.all_objects:
            lowObject.hide_set(False)

        for highObject in bg_high_collection.all_objects:
            highObject.hide_set(False)

        return{'FINISHED'}

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
                    print("Moved: ")
                    print(objs)
                    # Loop through all collections the obj is linked to
                    for coll in ob.users_collection:
                        # Unlink the object
                        coll.objects.unlink(ob)

                    # Link each object to the target collection
                    bg_high_collection.objects.link(ob)

        else:
            self.report({'ERROR'}, "Highpoly collection does not exist")

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
                    print("Moved: ")
                    print(objs)
                    # Loop through all collections the obj is linked to
                    for coll in ob.users_collection:
                        # Unlink the object
                        coll.objects.unlink(ob)

                    # Link each object to the target collection
                    bg_low_collection.objects.link(ob)

        else:
            self.report({'ERROR'}, "Lowpoly collection does not exist")

        return {'FINISHED'}