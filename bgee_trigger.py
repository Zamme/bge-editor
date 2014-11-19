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

class GameEditorTriggerPanel(bpy.types.Panel):
    bl_idname = "gamemaker_trigger_panel"
    bl_label = "Triggers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Entity"
    
    @classmethod
    def poll(self, context):
        return (context.selected_objects)
        
    def draw(self, context):
        layout = self.layout
        if (len(context.active_object.game.sensors) > 0):
            for sens in context.active_object.game.sensors:
                if (sens.type == "NEAR"):
                    row = layout.row(align=True)
                    box = row.box()
                    row = box.row(align=True)
                    row.prop(sens, "active", text="")
                    row.label(sens.type)
                    row.prop(sens, "name")
                    row = box.row(align=True)
                    row.prop(sens, "distance")
                    box2 = box.box()
                    row = box2.row(align=True)
                    row.label(text = "Advanced :")
                    row = box2.row(align=True)
                    row.prop(sens, "invert")
                    row.prop(sens, "frequency")
                    row = box2.row(align=True)
                    row.prop(sens, "reset_distance")
                elif (sens.type == "RADAR"):
                    row = layout.row(align=True)
                    box = row.box()
                    row = box.row(align=True)
                    row.prop(sens, "active", text="")
                    row.label(sens.type)
                    row.prop(sens, "name")
                    row = box.row(align=True)
                    row.prop(sens, "angle")
                    row.prop(sens, "distance")
                    row = box.row(align=True)
                    row.prop(sens, "axis")
                    box2 = box.box()
                    row = box2.row(align=True)
                    row.label(text = "Advanced :")
                    row = box2.row(align=True)
                    row.prop(sens, "invert")
                    row.prop(sens, "frequency")
        else:
            row = layout.row(align=True)
            row.label("No triggers attached")
        '''    
        row = row.split()
        row = layout.row(align=True)
        row.prop(context.screen, "GmTriggerTypes")        
        row.operator("bgee.add_trigger", "Add")
        '''
        
class GameEditorAddTrigger(bpy.types.Operator):
    bl_idname = "bgee.add_trigger"
    bl_label = "Add Trigger"
    
    def execute(self, context):
        # TODO: Prepare for multiple objects
        if (context.screen.GmTriggerTypes == "Near"):
            bpy.ops.logic.sensor_add(type='NEAR')
        else:
            bpy.ops.logic.sensor_add(type="RADAR")    
        self.report({'INFO'}, "Trigger added")
        
        return {"FINISHED"}
    
