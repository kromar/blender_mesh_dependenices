
# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from bpy.types import Operator,Object, Panel, Context, PropertyGroup
from bpy.props import StringProperty, BoolProperty, FloatProperty, PointerProperty


class MW_PG_Props(PropertyGroup):    
    bl_idname = __package__
    
    distance_threshold: FloatProperty(
        name="Distance",
        description="distance_threshold",
        default=0.0,
        min=0.000,
        soft_max=0.001,
        step=0.001,
        precision=4,
        subtype='DISTANCE') 
        
    connection_prefix: StringProperty(
        name="Prefix", 
        description="connection_prefix", 
        default="CON_")
            
    performance_profiling: BoolProperty(
        name="[Debug] Profiling",
        description="This is used to identiyfy slow code, note this will slow down your transfer if enabled!",
        default=True)
    
    selection_only: BoolProperty(
        name="Only Selected",
        description="",
        default=False)
        
    create_modifier_shrinkwrap: BoolProperty(
        name="Shrinkwrap",
        description="Create Shrinkwrap Modifier for Connection",
        default=False)
        

class MW_PT_UI(Panel):
    """Panel for the magic weights, located in Properties > Mesh."""

    bl_label = __package__
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_default_closed = False

    @classmethod
    def poll(cls, context): 
        return context.object.type == 'MESH'

    def draw(self, context):
        props = bpy.context.scene.CONFIG_VertexMaster

        layout = self.layout        
        layout.use_property_split = False

        box = layout.box()
        box.label(text='Connections', icon='IMPORT')

        row = box.row(align=True)
        row.prop(props, 'connection_prefix')
        row.prop(props, 'distance_threshold')
        
        col = box.column(align=True)
        row = col.row(align=True)
        #col.prop(props, 'selection_only')
        col.prop(props, 'create_modifier_shrinkwrap')
        col.prop(props, 'performance_profiling')
        
        col = box.column(align=True)
        row = col.row(align=True)
        row.operator('magic_weights.create_connections', text='Generate Connections')

        #box = layout.box()
        #box.label(text='Shading', icon='IMPORT')