import bpy
from .addon import SpeedSeamsProps

classes = (

)

def register_properties():
    from bpy.utils import register_class
    bpy.utils.register_class(SpeedSeamsProps)
    #for cls in classes:
    #register_class(cls)


def unregister_properties():
    from bpy.utils import unregister_class
    bpy.utils.unregister_class(SpeedSeamsProps)
    #for cls in reversed(classes):
    #unregister_class(cls)
