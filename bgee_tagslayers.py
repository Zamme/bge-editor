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


# Tags classes/functions
def reset_tags(gm):
    gm.currentTags.clear()
    bgee_config.bgeeCurrentTags.clear()
    for tag in bgee_config.DEFAULT_TAGS:
        newTag = gm.currentTags.add()
        newTag.first = tag[0]
        newTag.second = tag[1]
        newTag.third = tag[2]
        bgee_config.bgeeCurrentTags.append((tag[0], tag[1], tag[2]))
    #print("Reset tags:", gm.currentTags)

def update_tags(gm):
    bgee_config.bgeeCurrentTags.clear()
    for tag in gm.currentTags:
        bgee_config.bgeeCurrentTags.append((tag.first, tag.second, tag.third))
    bpy.types.Object.Tags = EnumProperty(items = bgee_config.bgeeCurrentTags)
    #print("update tags:", tags)
    gm.Tags = "None"
    bpy.types.Object.tagSelected = EnumProperty(items=bgee_config.bgeeCurrentTags)
    gm.tagSelected = "None"
    
class TagItem(bpy.types.PropertyGroup):
    first = bpy.props.StringProperty(name="")
    second = bpy.props.StringProperty(name="")
    third = bpy.props.StringProperty(name="")
# END Tags classes/functions

# Layers classes/functions
def reset_layers(gm):
    gm.currentLayers.clear()
    bgee_config.bgeeCurrentLayers.clear()
    for lay in bgee_config.DEFAULT_LAYERS:
        newLayer = gm.currentLayers.add()
        newLayer.first = lay[0]
        newLayer.second = lay[1]
        newLayer.third = lay[2]
        bgee_config.bgeeCurrentLayers.append((lay[0], lay[1], lay[2]))
    #print("Reset newLayer:", gm.currentLayers)

def update_layers(gm):
    bgee_config.bgeeCurrentLayers.clear()
    for lay in gm.currentLayers:
        bgee_config.bgeeCurrentLayers.append((lay.first, lay.second, lay.third))
    bpy.types.Object.Layers = EnumProperty(items = bgee_config.bgeeCurrentLayers)
    #print("update layers:", layers)
    gm.Layers = "None"
    bpy.types.Object.layerSelected = EnumProperty(items=bgee_config.bgeeCurrentTags)
    gm.tagSelected = "None"
    
class LayerItem(bpy.types.PropertyGroup):
    first = bpy.props.StringProperty(name="")
    second = bpy.props.StringProperty(name="")
    third = bpy.props.StringProperty(name="")
# END Layers classes/functions


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
        row = layout.row(align=True)
        box = row.box()
        for id,tag in enumerate(gm.currentTags):
            if (tag.first == "None"):
                continue
            row = box.row(align=True)
            row.label(text=tag.first)
            row.operator("bgee.edit_tag", "Edit").tagID=id
            row.operator("bgee.delete_tag", icon="X").tagID=id
            
        # LAYERS
        row = layout.row(align=True)
        row.label(text="Layers")
        row = layout.row(align=True)
        row.operator("bgee.add_layer", "Add")
        row = layout.row(align=True)
        box = row.box()
        for id,lay in enumerate(gm.currentLayers):
            if (lay.first == "None"):
                continue
            row = box.row(align=True)
            row.label(text=lay.first)
            row.operator("bgee.edit_layer", "Edit").layerID=id
            row.operator("bgee.delete_layer", icon="X").layerID=id

class GameEditorEditTag(bpy.types.Operator):
    bl_idname = "bgee.edit_tag"
    bl_label = "Edit Tag"
    
    tagID = IntProperty()
    
    tagName = StringProperty(name="Tag Name")
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        message = "Tag editted: '%s'" % (self.tagName)
        self.report({'INFO'}, message)
        selectedTag = gm.currentTags[self.tagID]
        selectedTag.first, selectedTag.second, selectedTag.third = self.tagName, self.tagName, self.tagName
        update_tags(gm)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class GameEditorDeleteTag(bpy.types.Operator):
    bl_idname = "bgee.delete_tag"
    bl_label = ""
    tagID = IntProperty()
    
    def execute(self, context):
        print("Deleting tag", self.tagID)
        gm = context.blend_data.objects["GameManager"]
        gm.currentTags.remove(self.tagID)
        
        return {"FINISHED"}

class GameEditorEditLayer(bpy.types.Operator):
    bl_idname = "bgee.edit_layer"
    bl_label = "Edit Tag"
    layerID = IntProperty()
        
    layerName = StringProperty(name="Layer Name")
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        message = "Layer editted: '%s'" % (self.layerName)
        self.report({'INFO'}, message)
        selectedLayer = gm.currentLayers[self.layerID]
        selectedLayer.first, selectedLayer.second, selectedLayer.third = self.layerName, self.layerName, self.layerName
        update_layers(gm)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class GameEditorDeleteLayer(bpy.types.Operator):
    bl_idname = "bgee.delete_layer"
    bl_label = ""
    layerID = IntProperty()
    
    def execute(self, context):
        print("Deleting layer", self.layerID)
        gm = context.blend_data.objects["GameManager"]
        gm.currentLayers.remove(self.layerID)
        
        return {"FINISHED"}

class AddTag(bpy.types.Operator):
    bl_idname="bgee.add_tag"
    bl_label = 'Add tag'

    newTag = StringProperty(name="New Tag")
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        message = "Tag added: '%s'" % (self.newTag)
        self.report({'INFO'}, message)
        createdTag = gm.currentTags.add()
        createdTag.first, createdTag.second, createdTag.third = self.newTag, self.newTag, self.newTag
        update_tags(gm)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class AddLayer(bpy.types.Operator):
    bl_idname="bgee.add_layer"
    bl_label = 'Add layer'

    newLayer = StringProperty(name="New Layer")
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        message = "Layer added: '%s'" % (self.newLayer)
        self.report({'INFO'}, message)
        createdLayer = gm.currentLayers.add()
        createdLayer.first, createdLayer.second, createdLayer.third = self.newLayer, self.newLayer, self.newLayer
        update_layers(gm)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

''' Use update_layers '''
class UpdateLayers(bpy.types.Operator):
    bl_idname="bgee.update_layers"
    bl_label = 'Update Layers'

    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        bpy.types.Object.GmLayer = EnumProperty(items = gm.currentLayers, name = "Layer")
        return {'FINISHED'}

''' Use update_tags '''
class UpdateTags(bpy.types.Operator):
    bl_idname="bgee.update_tags"
    bl_label = 'Update Tags'

    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        bpy.types.Object.Tag = EnumProperty(items = gm.currentTags, name = "Tag")
        return {'FINISHED'}
    
