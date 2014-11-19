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
from bpy.props import *

class GameEditorTagsPanel(bpy.types.Panel):
    bl_idname = "gamemaker_tags_panel"
    bl_label = "Tags & Layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tags & Layers"
    
    def draw(self, context):
        gm = context.blend_data.objects["GameManager"]
        layout = self.layout
        
        # TAGS
        row = layout.row(align=True)
        row.label(text="Tags")
        row = layout.row(align=True)
        row.operator("bgee.add_tag", "Add")
        ''' TODO: FIX TAGS MANAGER
        row = layout.row(align=True)
        box = row.box()
        for tag in gm.tags:
            row = box.row(align=True)
            row.label(text=tag[0])
            row.operator("bgee.edit_tag", "Edit")
            row.operator("bgee.delete_tag", icon="X")
        '''
        # LAYERS
        row = layout.row(align=True)
        row.label(text="Layers")
        row = layout.row(align=True)
        row.operator("bgee.add_layer", "Add")
        ''' TODO: FIX LAYERS MANAGER
        row = layout.row(align=True)
        box = row.box()
        for layer in layers:
            row = box.row(align=True)
            row.label(text=layer[0])
            row.operator("bgee.edit_layer", "Edit")
            row.operator("bgee.delete_layer", icon="X")
        '''

class GameEditorEditTag(bpy.types.Operator):
    bl_idname = "bgee.edit_tag"
    bl_label = "Edit Tag"
    
    def execute(self, context):
        print("Editing tag")
        
        return {"FINISHED"}

class GameEditorDeleteTag(bpy.types.Operator):
    bl_idname = "bgee.delete_tag"
    bl_label = ""
    
    def execute(self, context):
        print("Deleting tag")
        
        return {"FINISHED"}

class GameEditorEditLayer(bpy.types.Operator):
    bl_idname = "bgee.edit_layer"
    bl_label = "Edit Tag"
    
    def execute(self, context):
        print("Editing layer")
        
        return {"FINISHED"}

class GameEditorDeleteLayer(bpy.types.Operator):
    bl_idname = "bgee.delete_layer"
    bl_label = ""
    
    def execute(self, context):
        print("Deleting layer")
        
        return {"FINISHED"}

class AddTag(bpy.types.Operator):
    bl_idname="bgee.add_tag"
    bl_label = 'Add tag'

    newTag = StringProperty(name="New Tag")
    
    def execute(self, context):
        message = "Tag added: '%s'" % (self.newTag)
        self.report({'INFO'}, message)
        tags.append((self.newTag, self.newTag, self.newTag))
        bpy.ops.bgee.update_tags()
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class AddLayer(bpy.types.Operator):
    bl_idname="bgee.add_layer"
    bl_label = 'Add layer'

    newLayer = StringProperty(name="New Layer")
    
    def execute(self, context):
        message = "Layer added: '%s'" % (self.newLayer)
        self.report({'INFO'}, message)
        layers.append((self.newLayer, self.newLayer, self.newLayer))
        bpy.ops.bgee.update_layers()
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class UpdateLayers(bpy.types.Operator):
    bl_idname="bgee.update_layers"
    bl_label = 'Update Layers'

    def execute(self, context):
        bpy.types.Object.GmLayer = EnumProperty(items = layers, name = "Layer")
        return {'FINISHED'}
    
class UpdateTags(bpy.types.Operator):
    bl_idname="bgee.update_tags"
    bl_label = 'Update Tags'

    def execute(self, context):
        bpy.types.Object.Tag = EnumProperty(items = tags, name = "Tag")
        return {'FINISHED'}
    
