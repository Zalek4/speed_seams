import bpy
from bpy.props import PointerProperty
from ..utilities.addon import addon_name, get_prefs

class SpeedSeamsProps(bpy.types.AddonPreferences):
    bl_idname = addon_name

    def draw(self, context):
        prefs = get_prefs()
        layout = self.layout
        scene = context.scene
        sc = scene.sc_settings
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
