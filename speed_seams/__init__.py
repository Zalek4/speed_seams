# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import importlib
import sys
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from .menus.pies import SPEEDSEAMS_MT_EdgeToolsPie, SPEEDSEAMS_MT_QuickSharpPie, SPEEDSEAMS_MT_TransformsToolsPie
from .operators import SPEEDSEAMS_OT_SharpenSlider

bl_info = {
    "name": "Speed Seams",
    "author": "Alex Hallenbeck, Blake Darrow",
    "version": (0, 5, 3),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Speed Seams",
    "description": "",
    "category": "Tools",
    "wiki_url": "",
    "warning": "GPU OVERLAYS ARE EXPERIMENTAL AND SHOULD NOT BE USED"
}


class SpeedSeamsSettings(bpy.types.PropertyGroup):
    smoothingAngle : bpy.props.FloatProperty(
        name="Sharp Edge Angle",
        description="Angle to use for smoothing",
        default=35,
        min=1,
        max=180,
        step=0.5,
        update=SPEEDSEAMS_OT_SharpenSlider.execute
    )

    seamBool : bpy.props.BoolProperty(
        name="Mark Seams",
        description="Marks sharp edges as seams as the 'Sharp Edge Angle' slider is updated",
        default=False
    )

    packmasterBool: bpy.props.BoolProperty(
        name="UVPackmaster",
        description="Uses UVPackmaster 2 or 3 if installed",
        default=False
    )

    uvTextureType: bpy.props.EnumProperty(
        name="",
        description="Texture resolution of UV checker texture",
        items=[('UVT0', "UV Grid", ""),
               ('UVT1', "Color Grid", ""),
               ]
    )

    uvTextureRes: bpy.props.EnumProperty(
        name="",
        description="Texture resolution of UV checker texture",
        items=[('UV0', "32", ""), 
                ('UV1', "64", ""),
               ('UV2', "128", ""),
               ('UV3', "256", ""),
               ('UV4', "512", ""),
               ('UV5', "1024", ""),
               ('UV6', "2048", ""),
               ('UV7', "4096", ""),
               ]
    )

    unwrapAlgorithm : bpy.props.EnumProperty(
        name="",
        description="Blender algorithm to use for unwraping UVs",
        items=[('UA1', "Conformal", ""),
               ('UA2', "Angle-Based", ""),
        ]
    )

#-----------------------------------------------------#
#     register the modules
#-----------------------------------------------------#

addon_keymaps = []

def register():
    from .register import register_addon
    register_addon()
    bpy.utils.register_class(SpeedSeamsSettings)
    bpy.types.Scene.ss_settings = PointerProperty(type=SpeedSeamsSettings)

    #Register Keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_edge_tools_pie = km.keymap_items.new("wm.call_menu_pie", "E", "PRESS", shift=True, ctrl=True)
    kmi_edge_tools_pie.properties.name = SPEEDSEAMS_MT_EdgeToolsPie.bl_idname

    kmi_transforms_pie = km.keymap_items.new("wm.call_menu_pie", "D", "PRESS", shift=True)
    kmi_transforms_pie.properties.name = SPEEDSEAMS_MT_TransformsToolsPie.bl_idname

    kmi_quick_sharp_pie = km.keymap_items.new("wm.call_menu_pie", "X", "PRESS", shift=True, ctrl=True)
    kmi_quick_sharp_pie.properties.name = SPEEDSEAMS_MT_QuickSharpPie.bl_idname

    addon_keymaps.append((km, kmi_edge_tools_pie, kmi_quick_sharp_pie, kmi_transforms_pie))

def unregister():
    from .register import unregister_addon
    unregister_addon()
    del bpy.types.Scene.ss_settings

    #Unregister Keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi_edge_tools_pie, kmi_quick_sharp_pie, kmi_transforms_pie in addon_keymaps:
            km.keymap_items.remove(kmi_edge_tools_pie)
            km.keymap_items.remove(kmi_quick_sharp_pie)
            km.keymap_items.remove(kmi_transforms_pie)
    addon_keymaps.clear()
