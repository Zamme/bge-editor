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

def reset_inputs(gm):
    gm.currentInputs.clear()
    newInputGroup = gm.currentInputs.add()
    newInputGroup.inputGroupName = "Input1"
    for inp in bgee_config.DEFAULT_INPUT:
        newInput = newInputGroup.groups.add()
        newInput.inputName = inp[0]
        newInput.keyRef = inp[1]
        
class InputKey(bpy.types.PropertyGroup):
    inputName = bpy.props.StringProperty(name="Name", default="INPUTNAME")
    keyRef = bpy.props.StringProperty(name="Key", default="KEYREF")
    
class InputGroup(bpy.types.PropertyGroup):
    inputGroupName = bpy.props.StringProperty(name="Group", default="Input")
    groups = bpy.props.CollectionProperty(type=InputKey)
    
class GameEditorInputPanel(bpy.types.Panel):
    bl_idname = "gamemaker_input_panel"
    bl_label = "Input"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Input"
            
    def draw(self, context):
        gm = context.blend_data.objects["GameManager"]
        layout = self.layout
        for groupId,inpGroup in enumerate(gm.currentInputs):
            row = layout.row(align=True)
            box = row.box()
            rowbox = box.row(align=True)
            rowbox.prop(inpGroup, "inputGroupName")
            for inp in inpGroup.groups:
                rowbox = box.row(align=True)
                rowbox.prop(inp, "inputName")
                rowbox.prop(inp, "keyRef")
            rowbox = box.row(align=True)
            rowbox.operator("bgee.create_inputkey", "Add key").ig=groupId
        
        row = layout.row(align=True)
        row.operator("bgee.create_inputgroup", "Add Input Group")

class CreateInputKey(bpy.types.Operator):
    bl_idname = "bgee.create_inputkey"
    bl_label = ""
    ig = bpy.props.IntProperty()
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        newInputKey = gm.currentInputs[self.ig].groups.add()
        
        return {"FINISHED"}
    
class CreateInputGroup(bpy.types.Operator):
    bl_idname = "bgee.create_inputgroup"
    bl_label = ""
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        newInputGroup = gm.currentInputs.add()
        
        return {"FINISHED"}

