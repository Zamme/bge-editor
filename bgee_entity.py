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
from . import bgee_config

class GameEditorEntityPanel(bpy.types.Panel):
    bl_idname = "bgee_entity_panel"
    bl_label = "Entity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Entity"
        
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Entities selected:")
        for ob in context.selected_objects:
            row = layout.row(align=True)
            row.prop(ob, "name")
        
        '''
        row = layout.row(align=True)
        if (context.selected_objects):
            if (len(context.selected_objects) == 1): #Check all properties
                row.prop(context.active_object, "GmActive")
                row.prop(context.active_object, "name")
                row = layout.row(align=True)
                row.prop(context.active_object, "GmType")
                row = layout.row(align=True)
                row.prop(context.active_object, "Tag")
                row.operator("bgee.add_tag", "New")
                row = layout.row(align=True)
                row.prop(context.active_object, "GmLayer")
                row.operator("bgee.add_layer", "New")
                # Position of selected objects
                row = layout.row(align=True)
                row.prop(context.screen, "EntityPosition")            
                row = layout.row(align=True)
                row.prop(context.screen, "EntityRotation")            
                row = layout.row(align=True)
                row.prop(context.screen, "EntityScale")            
                               
                context.screen.EntityPosition = context.active_object.location
                #TODO: convert euler to angle
                context.screen.EntityRotation = context.active_object.rotation_euler
                context.screen.EntityScale = context.active_object.scale
            else:
                pass   
        else:
            row.label(text="No object selected")
        '''