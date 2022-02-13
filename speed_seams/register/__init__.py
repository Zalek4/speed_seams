def register_addon():

    # Properties
    #from ..properties import register_properties
    # register_properties()

    # Operators
    from ..operators import register_operators
    register_operators()

    # Menus
    from ..menus import register_menus
    register_menus()


def unregister_addon():

    # Properties
    #from ..properties import unregister_properties
    # unregister_properties()

    # Operators
    from ..operators import unregister_operators
    unregister_operators()

    # Menus
    from ..menus import register_menus
    register_menus()
