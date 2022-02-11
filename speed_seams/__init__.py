
import importlib
import sys
import bpy
bl_info = {
    "name": "Speed Seams",
    "author": "Alex Hallenbeck",
    "version": (0, 4, 3),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Speed Seams",
    "description": "",
    "category": "Tools",
    "wiki_url": "",
}

#-----------------------------------------------------#
#     add all new scripts to this string
#-----------------------------------------------------#

if __package__ != "speed_seams":
    sys.modules["speed_seams"] = sys.modules[__package__]

modulesNames = ['panels', 'op_edge_marker',
                'op_apply_transforms', 'op_grease_pencil','op_gpu_overlay' ]

#-----------------------------------------------------#
#     imports
#-----------------------------------------------------#
#-----------------------------------------------------#
#     create a dictonary for module names
#-----------------------------------------------------#

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = (
        '{}.{}'.format(__name__, currentModuleName))

#-----------------------------------------------------#
#     import new modules to addon using full name from above
#-----------------------------------------------------#
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(
            currentModuleFullName)
        setattr(globals()[currentModuleFullName],
                'modulesNames', modulesFullNames)

#-----------------------------------------------------#
#     register the modules
#-----------------------------------------------------#
classes = ()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

#-----------------------------------------------------#
#     unregister the modules
#-----------------------------------------------------#


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
