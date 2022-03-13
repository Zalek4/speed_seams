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
        scale = 1.2

        row.label(text="Texel Density Checker (3.3 or higher) and UVPackmaster 3 are recommended for maximum functionality", icon='INFO')
        
        row = col.row(align=True)
        row.scale_y = scale
        row.operator("wm.url_open", text="Texel Density Checker").url = "https://mrven.gumroad.com/l/CEIOR"
        row.operator("wm.url_open", text="UVPackmaster 3").url = "https://blendermarket.com/products/uvpackmaster"