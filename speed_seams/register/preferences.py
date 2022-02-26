import bpy
from bpy.types import AddonPreferences

class SpeedSeamsPreferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        print("Drawing Preferences...")
        layout = self.layout
        scene = context.scene
        ss = scene.ss_settings
        box = layout.box()
        scale = 1.2
        col = box.column(align=True)
        row = col.row(align=True)
        row.scale_y = scale

        box.label(text="Smoothing and UV Tools")