import bpy
from bpy.types import(Menu, UIList)
'''
type (enum in [‘MESH_CACHE’, ‘UV_PROJECT’, ‘UV_WARP’, ‘VERTEX_WEIGHT_EDIT’, ‘VERTEX_WEIGHT_MIX’, ‘VERTEX_WEIGHT_PROXIMITY’, ‘ARRAY’, ‘BEVEL’, ‘BOOLEAN’, ‘BUILD’, ‘DECIMATE’, ‘EDGE_SPLIT’, ‘MASK’, ‘MIRROR’, ‘MULTIRES’, ‘REMESH’, ‘SCREW’, ‘SKIN’, ‘SOLIDIFY’, ‘SUBSURF’, ‘TRIANGULATE’, ‘WIREFRAME’, ‘ARMATURE’, ‘CAST’, ‘CURVE’, ‘DISPLACE’, ‘HOOK’, ‘LAPLACIANSMOOTH’, ‘LAPLACIANDEFORM’, ‘LATTICE’, ‘MESH_DEFORM’, ‘SHRINKWRAP’, ‘SIMPLE_DEFORM’, ‘SMOOTH’, ‘WARP’, ‘WAVE’, ‘CLOTH’, ‘COLLISION’, ‘DYNAMIC_PAINT’, ‘EXPLODE’, ‘FLUID_SIMULATION’, ‘OCEAN’, ‘PARTICLE_INSTANCE’, ‘PARTICLE_SYSTEM’, ‘SMOKE’, ‘SOFT_BODY’, ‘SURFACE’])
'''

#============================================
# what does our object coneects to
#============================================
class ConnectsToObjects(bpy.types.Operator):
    """this operator returns all connections our object makes"""
    bl_idname = "object.connects_to_objects"
    bl_label = "Connects To Objects"
    
    
    def execute(self, context):
        obname = context.active_object.name
        modifiers = bpy.data.objects[obname].modifiers
        for modifier in modifiers:
            if modifier.type == 'SHRINKWRAP': #do we need this or can we just look for targets in all modifiers?
                modName = modifier.name
                print("Connection to: ", modifiers[modName].target.name)
        return {'FINISHED'}
            


#============================================
# get objects that connect to our active object
#============================================
class ConnectsFromObjects(bpy.types.Operator):
    """ this lists all connections that are meade to our object"""
    bl_idname = "object.connects_from_objects"
    bl_label = "Connects From Objects"
                
    def execute(self, context):
        #get all the connections to the active object
        active = bpy.context.active_object
        for ob in bpy.context.scene.objects: #objects in scene
            #check if objects connect to our active mesh
            connections_to_active(ob, active)
        return{'FINISHED'}
    
def connections_to_active(ob, active):
    obname = ob.name
    modifiers = bpy.data.objects[obname].modifiers
    for modifier in modifiers:
        if modifier.type == 'SHRINKWRAP': #do we need this or can we just look for targets in all modifiers?
            modName = modifier.name
            modTarget = modifiers[modName].target.name
            if modTarget == active.name:
                print(obname, "-->", modTarget)
                return obname
   
           
class DrawObjectConnections(bpy.types.Panel):
    bl_label = "Object Connections"
    bl_idname = "OBJECT_PT_CONNECTIONS"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    
    def draw(self, context):
        
        layout = self.layout
        col = layout.column()
        
        row = col.row(align=True)
        row.operator("object.connects_to_objects", text = "Connects To Objects")
        row.operator("object.connects_from_objects", text = "Connects From Objects")
        
       
        ob = context.object        
        group = ob.vertex_groups.active
        
        rows = 2        
        row = layout.row(align=True)
        #http://www.blender.org/documentation/blender_python_api_2_72_0/bpy.types.UILayout.html?highlight=template_list#bpy.types.UILayout.template_list
        #template_list(listtype_name, list_id="", dataptr, propname, active_dataptr, active_propname, rows=5, maxrows=5, type='DEFAULT', columns=9)
        row.template_list("MESH_UL_connections", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows, type='DEFAULT')    
        row.template_list("MESH_UL_connections", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows, type='DEFAULT')
        
        col = row.column(align=True)
        col.operator("object.vertex_group_add", icon='ZOOMIN', text="")
        col.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
        col.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")
        
        
class MESH_UL_connections(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # assert(isinstance(item, bpy.types.VertexGroup))
        vgroup = item
        if self.layout_type in {'DEFAULT', 'GRID'}:
            layout.prop(vgroup, "name", text="", emboss=False, icon_value=icon)
            icon = 'LOCKED' if vgroup.lock_weight else 'UNLOCKED'
            layout.prop(vgroup, "lock_weight", text="", icon=icon, emboss=False)
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)           
            
   
     

def register():
    bpy.utils.register_module(__name__)  


def unregister():
    bpy.utils.unregister_module(__name__) 

if __name__ == "__main__":
    register()

