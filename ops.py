import bpy
from bpy.types import UIList
from bpy.types import Panel

mod_icon_map = {m.identifier: m.icon for m in bpy.types.OBJECT_OT_modifier_add.bl_rna.properties['type'].enum_items}
    
    
# modify active modifier in stack
class OBJECT_OT_modifier_move(bpy.types.Operator): 
    bl_idname = "object.modifier_action"
    bl_label = "Modifier Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('LEFT', "Left", ""),
            ('REMOVE', "Remove", ""),
        )
    )

    def invoke(self, context, event):
        ob = context.object
        idx = ob.modifier_active_index
        try:
            mod = ob.modifiers[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(ob.modifiers) - 1:
                if bpy.ops.object.modifier_move_down(modifier=mod.name) == {'FINISHED'}:
                    ob.modifier_active_index += 1
            elif self.action == 'UP' and idx >= 1:
                if bpy.ops.object.modifier_move_up(modifier=mod.name) == {'FINISHED'}:
                    ob.modifier_active_index -= 1                
            elif self.action == 'REMOVE':
                bpy.ops.object.modifier_remove(modifier=mod.name)
                if idx >= 1:
                    ob.modifier_active_index -= 1
        return {"FINISHED"}
    

def SearchForTargets(ob, modifiers, modifier):
    try:                
        if modifiers[modifier.name].target or modifiers[modifier.name].object:    
            if modifiers[modifier.name].target:
                target = modifiers[modifier.name].target            
            elif modifiers[modifier.name].object:                        
                target = modifiers[modifier.name].object                
            return target
    except():
        print("no dependencies found on", ob.name)
        pass
                     
  
# custom UIList type for modifiers
class MODIFIER_UL_listtype(UIList,Panel):
    
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    
    def draw_item(self, context, layout, data, item, active_data, active_propname, index):
        modifier = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            config = bpy.context.scene.CONFIG_ModifierDependencies    
            ob = context.active_object   
            
            if not config.active_object_as_target:
                modifiers = bpy.data.objects[ob.name].modifiers 
                
                layout.prop(context.active_object, "name", text="", emboss=False)      
                layout.prop(modifier, "name", text="", emboss=False, icon=mod_icon_map[modifier.type])     
                                                      
                target = SearchForTargets(ob, modifiers, modifier)
                if target:                                      
                    layout.prop(target, "name", text="", emboss=False) 
                else:                        
                    layout.label(icon='NONE', text="")                    
                
                # modifier icons
                icon = 'RESTRICT_RENDER_OFF' if modifier.show_render else 'RESTRICT_RENDER_ON'
                layout.prop(modifier, "show_render", text="", icon=icon, emboss=False)
                icon = 'RESTRICT_VIEW_OFF' if modifier.show_viewport else 'RESTRICT_VIEW_ON'
                layout.prop(modifier, "show_viewport", text="", icon=icon, emboss=False)
                icon = 'EDITMODE_HLT' if modifier.show_in_editmode else 'OBJECT_DATAMODE'
                layout.prop(modifier, "show_in_editmode", text="", icon=icon, emboss=False)
            
            elif config.active_object_as_target:
                # here we want to look through all objects in the scene that use our active object as target
                
                try:  
                    for dep in bpy.data.objects:    
                        if not dep.name == ob.name:   
                           
                            # only retunr if modifier has a target
                            #        therefore we need to define modifiers and modifier of dep objects
                            print("depend:", dep.name)                         
                            modifiers = bpy.data.objects[dep.name].modifiers
                            print(modifiers)
                            for modifier in modifiers:     
                                print(modifier.name)                                              
                                target = SearchForTargets(dep, modifiers, modifier)      
                                print(target)
                                
                                if target:       
                                    layout.prop(dep, "name", text="", emboss=False)      
                                    layout.prop(modifier, "name", text="", emboss=False, icon=mod_icon_map[modifier.type])                               
                                    layout.prop(target, "name", text="", emboss=False) 
                                else:                        
                                    layout.label(icon='NONE', text="")
                                    
                    # modifier icons
                    '''
                    icon = 'RESTRICT_RENDER_OFF' if modifier.show_render else 'RESTRICT_RENDER_ON'
                    layout.prop(modifier, "show_render", text="", icon=icon, emboss=False)
                    icon = 'RESTRICT_VIEW_OFF' if modifier.show_viewport else 'RESTRICT_VIEW_ON'
                    layout.prop(modifier, "show_viewport", text="", icon=icon, emboss=False)
                    icon = 'EDITMODE_HLT' if modifier.show_in_editmode else 'OBJECT_DATAMODE'
                    layout.prop(modifier, "show_in_editmode", text="", icon=icon, emboss=False)
                    '''
                    print("-" * 40)
                     
                except:
                    # print("failing test")
                    pass                

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon=mod_icon_map[modifier.type])

   
class OBJECT_PT_ModifierDependencies(Panel):
    bl_label = "Modifier Dependencies"
    bl_idname = "OBJECT_PT_ModifierDependencies"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        config = bpy.context.scene.CONFIG_ModifierDependencies 
        scene = bpy.context.scene
        ob = context.object   
          
        layout = self.layout  
        row = layout.row(align=True)   
        row.prop(config, "active_object_as_target")
        #row.prop(config, "filter_modifiers")
        
        row = layout.row(align=True)           
        rows = 4      
               
        # template_list("UI_UL_list", '', props, <collection prop>, props, <int prop>)
        # template_list(listtype_name, list_id="", dataptr, propname, active_dataptr,
        #               active_propname, item_dyntip_propname="", rows=5, maxrows=5, type='DEFAULT', columns=9)
        """
        dataptr (AnyType)                       – Data from which to take the Collection property
        propname (string, (never None))         – Identifier of the Collection property in data
        active_dataptr (AnyType, (never None))  – Data from which to take the integer property, index of the active item
        active_propname (string, (never None))  – Identifier of the integer property in active_data, index of the active item
        """

        if config.active_object_as_target == False: 
            row.template_list("MODIFIER_UL_listtype", "", ob, "modifiers", ob, "modifier_active_index", rows=rows, type='DEFAULT')
        else:
            obs = bpy.context.scene.objects
            row.template_list("MODIFIER_UL_listtype", "", obs, "active", obs, 'l', rows=rows, type='DEFAULT')

        col = row.column(align=True)
        col.operator("object.modifier_add", icon='ZOOMIN', text="")
        col.operator("object.modifier_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        
        col.separator()
        col.separator()
        col.operator("object.modifier_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("object.modifier_action", icon='TRIA_DOWN', text="").action = 'DOWN'
