# ------------------------------------------------------------------------
#    Imports
# ------------------------------------------------------------------------
from re import search
import bpy
import bmesh
from mathutils import Vector
from ..utilities.utilities import traverse_tree, parent_lookup, progress_bar
import time
import random


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

class SPEEDSEAMS_OT_PairHighLowObjects(bpy.types.Operator):
    bl_idname = "pair.high_low_objects"
    bl_label = "Pair High/Low Meshes"
    bl_description = "Pairs high/low objects based on the amount they overlap"

    def execute(self, context):
        scene = context.scene
        ss = scene.ss_settings
        matchAccuracy = 85 * .01
        bg_name = ss.bakePrepAssetName + "_" + "bake_group"
        bg_low_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixLow
        bg_high_name = ss.bakePrepAssetName + "_" + ss.bakePrepSuffixHigh

        #Get collection names and print them
        bg_collection = bpy.data.collections.get(bg_name)
        bg_high_collection = bpy.data.collections.get(bg_high_name)
        bg_low_collection = bpy.data.collections.get(bg_low_name)

        #print settings to console
        print("-----------------------------------------------------------------")
        print("Using " + str(bg_low_collection.name) + " as Lowpoly collection")
        print("Using " + str(bg_high_collection.name) + " as Highpoly collection")
        print("Match Percentage: " + str(matchAccuracy) + "%")
        print("Search Distance : " + str(ss.searchDistance))
        print("-----------------------------------------------------------------")

        #Hide all high and low objects
        for lowObject in bg_low_collection.all_objects:
            lowObject.hide_set(True)

        for highObject in bg_high_collection.all_objects:
            highObject.hide_set(True)

        objectNumber = 0

        #Look at each mesh in the low collection
        for lowObject in bg_low_collection.all_objects:
            print("_________________________________________________________________")
            print("Looking for a match for: " + str(lowObject.name))
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

            #reset the variables
            objectNumber = objectNumber + 1
            normalList = []
            transformList = []
            vertexCount = 0

            #Set up proper object naming
            if objectNumber <= 9:
                mesh_low_name = ss.bakePrepAssetName + "_" + "00" + str(objectNumber) + "_" + ss.bakePrepSuffixLow
                mesh_high_name = ss.bakePrepAssetName + "_" + "00" + str(objectNumber) + "_" + ss.bakePrepSuffixHigh
            elif objectNumber > 9:
                mesh_low_name = ss.bakePrepAssetName + "_" + "0" + str(objectNumber) + "_" + ss.bakePrepSuffixLow
                mesh_high_name = ss.bakePrepAssetName + "_" + "0" + str(objectNumber) + "_" + ss.bakePrepSuffixHigh
            elif objectNumber > 99:
                mesh_low_name = ss.bakePrepAssetName + "_" + str(objectNumber) + "_" + ss.bakePrepSuffixLow
                mesh_high_name = ss.bakePrepAssetName + "_" + str(objectNumber) + "_" + ss.bakePrepSuffixHigh
            #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            
            #Get vertex data of current low mesh
            for v in lowObject.data.vertices:
                #get the vertex count
                vertexCount = vertexCount + 1
                #get the normal of the vertex and append it to the normal dictionary
                n = v.normal
                n = n * -1
                normalList.append(n)
                nOffset = n * 0.0001

                #get the location of the vertex and append it to the location dictionary
                coords = lowObject.matrix_world @ v.co
                offsetCoords = coords + nOffset
                transformList.append(offsetCoords)

            #Check if the data was actually generated
            if vertexCount:
                if normalList:
                    if transformList:
                        print("Generated data for " + str(lowObject.name))

            hitCount = 0
            searchingBool = 0
            badLowMatches = []
            badHighMatches = []
            
            #cycle through each high object and raycast onto each
            for highObject in bg_high_collection.all_objects:
                
                #only print 'searching' once
                if searchingBool < 1:
                    print("Searching...")
                searchingBool = 1

                #Do traces, and report the name of the object each hits
                hitCount = 0
                accuracy = 0
                indexCap = len(normalList)
                indexCap = indexCap - 1

                #Sets the limit for the number of random points we can select. Prevents small meshes from throwing an error.
                indexRange = round(vertexCount * 0.05)
                if indexRange < 30:
                    indexRange = vertexCount


                highObject.hide_set(False)

                for i in range(indexRange):
                    index = random.randint(0, indexCap)

                    hit, loc, norm, idx, ob, M = scene.ray_cast(context.evaluated_depsgraph_get(), transformList[index], normalList[index], distance=ss.searchDistance)

                    if hit:
                        #add 1 to the hitCount and print what we hit
                        hitCount = hitCount + 1

                    #add 1 to the index so we can move to the next object
                    index = index + 1
                    accuracy = hitCount/indexRange

                    #print a miss
                    #if not hit:
                        #print("Missed")

                    #compare the hit count with the vert count every check. If more than half the hits match a highpoly object, exit the loop.
                    if accuracy >= matchAccuracy:
                        print("More than " + str(matchAccuracy * 100) + "% of the lowpoly verts match " + str(highObject.name))
                        print("Checking for similar volume...")
                        rayVolMatch = False

                        bm = bmesh.new()
                        bm.from_mesh(lowObject.data)
                        #lowArea = sum(f.calc_area() for f in bm.faces)
                        lowVolume = bm.calc_volume(signed=True)
                        print("Low volume: " + str(lowVolume))
                        bm.free()
                        bm = bmesh.new()
                        bm.from_mesh(highObject.data)
                        #highArea = sum(f.calc_area() for f in bm.faces)
                        highVolume = bm.calc_volume(signed=True)
                        print("High volume: " + str(highVolume))
                        bm.free()
                        #areaDif = highArea/lowArea
                        #areaDif = areaDif - 1
                        volumeDif = highVolume/lowVolume
                        volumeDif = volumeDif - 1

                        if volumeDif < 0:
                            volumeDif = volumeDif * -1

                        if volumeDif <= 0.3:
                            print("Volume difference: " + str(volumeDif))
                            print("Volumes are similar")
                            rayVolMatch = True
                            break

                        else:
                            print("Volume difference: " + str(volumeDif))
                            print("Volume difference too high. Aborting match...")
                            accuracy = 0
                            break
                        
                        

                #compare the hit count with the vert count every highpoly object. If more than half the hits match a highpoly object, exit the loop.
                if accuracy >= matchAccuracy:
                    if rayVolMatch == True:
                        print("<<Matching " + str(lowObject.name) + " with " + str(highObject.name) + ">>")
                        lowObject.name = mesh_low_name
                        highObject.name = mesh_high_name
                        print("<<Converted to " + str(lowObject.name) + " and " + str(highObject.name) + ">>")
                        print("Moving to next object...")
                        break

                #hide the highpoly object
                highObject.hide_set(True)
                #time.sleep(0.1)

            #THIS IS A PROBLEM
            if accuracy < matchAccuracy:
                print("NO MATCH FOUND")
                badLowMatches.append(lowObject)
                badHighMatches.append(highObject)

        for ob in badLowMatches:
            for coll in ob.users_collection:
                # Unlink the object
                coll.objects.unlink(ob)
            bg_collection.objects.link(ob)

        for ob in badHighMatches:
            for coll in ob.users_collection:
                # Unlink the object
                coll.objects.unlink(ob)
            bg_collection.objects.link(ob)

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