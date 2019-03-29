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

bl_info = {
    "name": "Mesh Dependencies",
    "author": "Daniel Grauer",
    "version": (0, 1, 0),
    "blender": (2, 7, 7),
    "category": "Modifiers",
    "location": "Properties > Modifiers > Mesh Dependencies",
    "description": "shows dependencies (like modifier targets) from and to active object",
    "warning": '',
    "wiki_url": "",
    "tracker_url": ""
}

if "bpy" in locals():
    import importlib
    importlib.reload(ops)
else:
    from . import ops

import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, CollectionProperty)

from bl_ui.properties_material import active_node_mat


class TEST_PT_map_slot_settings( bpy.types.Panel ):
    bl_label = "Material Creation Helper"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        row = layout.row()


class UIElements(bpy.types.PropertyGroup):
    active_object_as_target = bpy.props.BoolProperty(name="Active Object As Target",
                                                     default=False,
                                                     description="changes direction of dependencies, "
                                                     "looking for active object in other objects modifiers"
                                                     )
    filter_modifiers = bpy.props.BoolProperty(name="Show All Modifiers",
                                              default=False,
                                              description="shows all modifiers, not only dependencies"
                                              )


classes = {
    UIElements,
    ops.OBJECT_OT_modifier_move,
    ops.MODIFIER_UL_listtype,
    ops.OBJECT_PT_ModifierDependencies,
    TEST_PT_map_slot_settings,
    }


def register():
    [bpy.utils.register_class(c) for c in classes]

    bpy.types.Object.modifier_active_index = bpy.props.IntProperty(default=0)
    bpy.types.Scene.CONFIG_MeshDep = bpy.props.PointerProperty(type=UIElements)



def unregister():
    del bpy.types.Object.modifier_active_index
    if bpy.context.scene.get('CONFIG_MeshDep') is not None:
        del bpy.context.scene['CONFIG_MeshDep']
    try:
        del bpy.types.Scene.CONFIG_MeshDep
    except():
        pass

    [bpy.utils.unregister_class(c) for c in classes]
