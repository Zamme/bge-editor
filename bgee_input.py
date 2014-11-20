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

class InputKey(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Name", default="Key ref")
    keyRef = bpy.props.StringProperty(name="Key", default="")
    
    
class GameEditorInputPanel(bpy.types.Panel):
    bl_idname = "gamemaker_input_panel"
    bl_label = "Input"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Input"
            
    def draw(self, context):
        layout = self.layout
        ''' TODO: FIX INPUTS PANEL
        for inp in context.screen.GmInputs:
            row = layout.row(align=True)
            box = row.box()
            rowbox = box.row(align=True)
            rowbox.prop(inp, "name")
            rowbox = box.row(align=True)
            rowbox.prop(inp, "left")
            rowbox = box.row(align=True)
            rowbox.prop(inp, "right")
            rowbox = box.row(align=True)
            rowbox.prop(inp, "up")
            rowbox = box.row(align=True)
            rowbox.prop(inp, "down")
            rowbox = box.row(align=True)
            rowbox.prop(inp, "jump")
            rowbox = box.row(align=True)
            rowbox.prop(inp, "fire1")
        '''
        row = layout.row(align=True)
        row.operator("bgee.create_inputgroup", "Add")

class CreateInputGroup(bpy.types.Operator):
    bl_idname = "bgee.create_inputgroup"
    bl_label = ""
    
    def execute(self, context):
        ''' TODO: FIX INPUT CREATION
        nGroup = context.screen.bgeeInputs.add()
        nGroup.name = (nGroup.name + str(len(context.screen.bgeeInputs)))
        '''
        return {"FINISHED"}

