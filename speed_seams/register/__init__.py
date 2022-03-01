import bpy
from .preferences import SpeedSeamsPreferences


def register_addon():
    # Preferences
    from . import preferences
    bpy.utils.register_class(SpeedSeamsPreferences)

    # Operators
    from ..operators import register_operators
    register_operators()

    # Menus
    from ..menus import register_menus
    register_menus()


def unregister_addon():
    # Preferences
    bpy.utils.unregister_class(SpeedSeamsPreferences)

    # Operators
    from ..operators import unregister_operators
    unregister_operators()

    # Menus
    from ..menus import unregister_menus
    unregister_menus()
