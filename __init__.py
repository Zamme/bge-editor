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
    "name": "BGE Editor",
    "description": "Blender Game Engine Editor",
    "author": "Jaume Castells",
    "version": (0,2,0),
    "wiki_url": "http://zammedev.blogspot.com", 
    "category": "Game Engine"}

#'''For release
if "bpy" in locals():
    import imp
    imp.reload(bgee_types)
    imp.reload(bgee_collider)
    imp.reload(bgee_component)
    imp.reload(bgee_config)
    imp.reload(bgee_data)
    imp.reload(bgee_entity)
    imp.reload(bgee_gamemanager)
    imp.reload(bgee_input)
    #imp.reload(bgee_layout)
    imp.reload(bgee_publish)
    imp.reload(bgee_tagslayers)
    imp.reload(bgee_trigger)
    imp.reload(bgee_audio)
else:
    from . import bgee_types, bgee_collider, bgee_component, bgee_config, bgee_data, bgee_entity, bgee_gamemanager, bgee_input, bgee_publish, bgee_tagslayers, bgee_trigger, bgee_audio #, bgee_layout
#'''

import bpy
from bpy.props import *
from bpy.types import Header, Menu

import os
import shutil


bgeeManager = None


def add_to_menu(self, context) :
    #TODO: Check if it's in the correct layout
    #self.layout.operator("bgee.create_layout", icon = "PLUGIN")
    #global bgeeManager
    #if (bgeeManager.activated):
        #if (context.scene.screen.name == bgee_config.GAME_EDITOR_LAYOUT_NAME):
            self.layout.operator("bgee.load_editor", icon = "PLUGIN")
    #else:
        #if (context.scene.screen.name == "Game Logic"):        
            #self.layout.operator("bgee.create_layout", icon = "PLUGIN")

class GameEditorPanel(bpy.types.Panel):
    bl_idname = "bgee_gameeditor_panel"
    bl_label = bgee_config.GAME_EDITOR_LAYOUT_NAME
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = bgee_config.GAME_EDITOR_TAB
    
    def draw(self, context):
        global bgeeManager
        layout = self.layout
        row = layout.row(align=True)
        row.prop(bgeeManager.emptyObject, "GameName")
        row = layout.row(align=True)
        row.prop(bgeeManager.emptyObject, "Version")
        row = layout.row(align=True)
        row.prop(bgeeManager.emptyObject, "Workspace")
        row = layout.row(align=True)
        row.operator("bgee.play", "Play")
                
class GameEditorPlay(bpy.types.Operator):
    bl_idname = "bgee.play"
    bl_label = "Play"
    
    def execute(self, context):
        bpy.ops.view3d.game_start()
        return {"FINISHED"}

class LoadGameEditor(bpy.types.Operator):
    bl_idname = "bgee.load_editor"
    bl_label = "Load Game Editor"
    
    def execute(self, context):
        if (bpy.ops.bgee.load_workspace() == {"FINISHED"}):
            # Registering publishing classes
            bpy.utils.register_class(bgee_publish.PlatformTarget)
            bpy.utils.register_class(bgee_publish.GameEditorPublish)
            # Registering gamemanager classes
            bpy.utils.register_class(CreateGameManager)
            bpy.ops.bgee.create_gamemanager()
            bpy.utils.unregister_class(CreateGameManager)
            # Registering gamemanager and publishing panels
            bpy.utils.register_class(GameEditorPlay)
            bpy.utils.register_class(GameEditorPanel)
            bpy.utils.register_class(bgee_publish.GameEditorPublishPanel)
            bpy.utils.register_class(bgee_audio.GameEditorAudioPanel)
            # Registering tags and layers operators/panels
            bpy.utils.register_class(bgee_tagslayers.GameEditorEditTag)
            bpy.utils.register_class(bgee_tagslayers.GameEditorDeleteTag)
            bpy.utils.register_class(bgee_tagslayers.GameEditorEditLayer)
            bpy.utils.register_class(bgee_tagslayers.GameEditorDeleteLayer)
            bpy.utils.register_class(bgee_tagslayers.AddTag)
            bpy.utils.register_class(bgee_tagslayers.AddLayer)
            bpy.utils.register_class(bgee_tagslayers.UpdateLayers)
            bpy.utils.register_class(bgee_tagslayers.UpdateTags)
            bpy.utils.register_class(bgee_tagslayers.GameEditorTagsPanel)
            # Registering input operators/panels
            bpy.utils.register_class(bgee_input.CreateInputKey)
            bpy.utils.register_class(bgee_input.CreateInputGroup)
            bpy.utils.register_class(bgee_input.GameEditorInputPanel)
            # Registering entity operators/panels
            #bpy.utils.register_class(bgee_entity.EntityList)
            bpy.utils.register_class(bgee_entity.GameEditorEntityPanel)
            
            return {"FINISHED"}
        else:
            print("Game editor not loaded")
            
            return {"CANCELLED"}

class CreateGameManager(bpy.types.Operator):
    bl_idname = "bgee.create_gamemanager"
    bl_label = "Create GameManager"
    
    def load_classes(self, context):
        bpy.utils.register_class(bgee_tagslayers.TagItem)
        bpy.utils.register_class(bgee_tagslayers.LayerItem)
        bpy.utils.register_class(bgee_input.InputKey)
        bpy.utils.register_class(bgee_input.InputGroup)
        bpy.utils.register_class(bgee_entity.MultiEntityTransform)
        bpy.utils.register_class(bgee_entity.BGEE_OT_multiselection)
        bpy.utils.register_class(bgee_component.ObjectComponent) # Needed by EntityProperties
        bpy.utils.register_class(bgee_entity.EntityProperties)
        bpy.types.Object.entityProps = PointerProperty(type=bgee_entity.EntityProperties)                    
        bpy.utils.register_class(bgee_component.DeleteComponent)
        bpy.utils.register_class(bgee_component.GameEditorComponentsPanel)
        
    def load_types(self, context):
        bpy.types.Object.GameName = StringProperty(name="Game Name")
        bpy.types.Object.Version = IntVectorProperty(name="Version")
        bpy.types.Object.Workspace = StringProperty(name="Workspace")
        bpy.types.Scene.BgeeActive = BoolProperty(name="")
        bpy.types.Object.BgeeTarget = PointerProperty(type=bgee_publish.PlatformTarget)
        bpy.types.Object.AudioVolume = IntProperty(name="Audio volume")
        bpy.types.Object.currentTags = CollectionProperty(type=bgee_tagslayers.TagItem)
        bpy.types.Object.currentLayers = CollectionProperty(type=bgee_tagslayers.LayerItem)
        bpy.types.Object.currentInputs = CollectionProperty(type=bgee_input.InputGroup)
        bpy.types.Object.entityTransform = PointerProperty(type=bgee_entity.MultiEntityTransform)
        bpy.types.Object.entityProps = PointerProperty(type=bgee_entity.EntityProperties)
        
    def create_properties(self, context):
        # Config gamemanager properties
        # General
        ao = context.active_object
        ao.GameName = "New Game"
        ao.Version = (1,0,0)
        ao.Workspace = ""
        
        # Publish
        for sce in bpy.data.scenes:
            sce.BgeeActive = True
        ao.BgeeTarget.windows = True
        ao.BgeeTarget.mac = False
        ao.BgeeTarget.linux = False
        
        # Audio
        ao.AudioVolume = bgee_config.DEFAULT_AUDIO_VOLUME
        
        # Tags
        bgee_tagslayers.reset_tags(ao)
        bgee_tagslayers.update_tags(ao)

        # Layers
        bgee_tagslayers.reset_layers(ao)
        bgee_tagslayers.update_layers(ao)

        # Inputs
        bgee_input.reset_inputs(ao)
        
        # Entity main
        ao.entityTransform.location, ao.entityTransform.rotation, ao.entityTransform.scale = (0,0,0), (0,0,0), (1,1,1)
        bpy.ops.bgee.multiselection()
        # Entity properties
        bgee_entity.prepare_entity(context.blend_data.objects)

        # Components
        
        '''
        bpy.types.Object.BgeeComponentType = EnumProperty(items = bgee_config.bgeeComponentTypes, name = "Type")
        ao.BgeeComponentType = "Physics"
        bpy.utils.register_class(bgee_input.InputGroup)
        bpy.types.Object.BgeeInputs = CollectionProperty(type=bgee_input.InputGroup)
        bpy.utils.register_class(bgee_publish.PlatformTarget)
        '''
        
    def execute(self, context):
        self.load_classes(context)
        self.load_types(context)
        global bgeeManager
        bgeeManager = bgee_gamemanager.GameManager()
        gmExists = False
        for ob in bpy.data.objects:
            if (ob.name == "GameManager"):
                bgeeManager.set_object(ob)
                #print(bgeeManager.emptyObject.name)
                gmExists = True
                break
        if (not gmExists):
            bpy.ops.object.empty_add()
            bgeeManager.set_object(context.active_object)
            self.create_properties(context)
            # can't view properties of a hidden object?
            # bgeeManager.emptyObject.hide = True 
            bgeeManager.emptyObject.Workspace = os.path.normpath((os.path.join(os.path.dirname(bpy.data.filepath), (bpy.path.basename(bpy.data.filepath)).replace(".blend", "_") + bgee_config.GAME_EDITOR_WORKSPACE_PATH)))
        else:
            bgee_entity.prepare_entity(context.blend_data.objects)
        
        return {"FINISHED"}

def Unregister_tabs():
    try:
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_add_object)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_add_mesh_edit)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_object)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_relations)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_animation)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_rigid_body)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_transform_mesh)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_meshedit)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_grease_pencil)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_history)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_transform)
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_tools_objectmode)
    except:
        print("Tabs not registered?")    
    
def register():
    bpy.utils.register_class(LoadGameEditor)
    bpy.types.INFO_MT_window.prepend(add_to_menu)
    bpy.utils.register_class(bgee_config.LoadWorkspace)

def unregister():
    bpy.utils.unregister_class(LoadGameEditor)
    bpy.types.INFO_MT_window.remove(add_to_menu)
    bpy.utils.unregister_class(bgee_publish.GameEditorPublishPanel)
        
if __name__ == "__main__":
    register()