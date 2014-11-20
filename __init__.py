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
            ''' TODO: WHEN INPUT WAS FINISHED
            bpy.utils.register_class(bgee_input.InputGroup)
            bpy.utils.register_class(bgee_input.CreateInputGroup)
            '''
            bpy.utils.register_class(bgee_input.GameEditorInputPanel)
            # Registering entity operators/panels
            bpy.utils.register_class(bgee_entity.GameEditorEntityPanel)
            
            return {"FINISHED"}
        else:
            print("Game editor not loaded")
            
            return {"CANCELLED"}

class CreateGameManager(bpy.types.Operator):
    bl_idname = "bgee.create_gamemanager"
    bl_label = "Create GameManager"
    
    def create_properties(self, context):
        # Config gamemanager properties
        # General
        ao = context.active_object
        bpy.types.Object.GameName = StringProperty(name="Game Name")
        ao.GameName = "New Game"
        bpy.types.Object.Version = IntVectorProperty(name="Version")
        ao.Version = (1,0,0)
        bpy.types.Object.Workspace = StringProperty(name="Workspace")
        ao.Workspace = ""
        
        # Publish
        bpy.types.Scene.BgeeActive = BoolProperty(name="")
        for sce in bpy.data.scenes:
            sce.BgeeActive = True
        bpy.types.Object.BgeeTarget = PointerProperty(type=bgee_publish.PlatformTarget)
        ao.BgeeTarget.windows = True
        ao.BgeeTarget.mac = False
        ao.BgeeTarget.linux = False
        
        # Audio
        bpy.types.Object.AudioVolume = IntProperty(name="Audio volume")
        ao.AudioVolume = bgee_config.DEFAULT_AUDIO_VOLUME
        
        # Tags
        bpy.utils.register_class(bgee_tagslayers.TagItem)
        bpy.types.Object.currentTags = CollectionProperty(type=bgee_tagslayers.TagItem)
        bgee_tagslayers.reset_tags(ao)
        bgee_tagslayers.update_tags(ao)

        # Layers
        bpy.utils.register_class(bgee_tagslayers.LayerItem)
        bpy.types.Object.currentLayers = CollectionProperty(type=bgee_tagslayers.LayerItem)
        bgee_tagslayers.reset_layers(ao)
        bgee_tagslayers.update_layers(ao)

        # Inputs
        ''' TODO: CREATE A COLLECTION OF COLLECTIONS OF INPUTKEY
        bpy.utils.register_class(bgee_input.InputKey)
        bpy.types.Object.currentInputs = CollectionProperty(type=bpy.types.IntProperty)
        '''
        
        '''
        bpy.types.Object.BgeeComponentType = EnumProperty(items = bgee_config.bgeeComponentTypes, name = "Type")
        ao.BgeeComponentType = "Physics"
        bpy.utils.register_class(bgee_input.InputGroup)
        bpy.types.Object.BgeeInputs = CollectionProperty(type=bgee_input.InputGroup)
        bpy.utils.register_class(bgee_publish.PlatformTarget)
        '''
        
    def execute(self, context):
        global bgeeManager
        bgeeManager = bgee_gamemanager.GameManager()
        gmExists = False
        for ob in bpy.data.objects:
            if (ob.name == "GameManager"):
                bgeeManager.set_object(ob)
                gmExists = True
                break
        if (not gmExists):
            bpy.ops.object.empty_add()
            self.create_properties(context)
            bgeeManager.set_object(context.active_object)
            # can't view properties of a hidden object?
            # bgeeManager.emptyObject.hide = True 
            bgeeManager.emptyObject.Workspace = os.path.normpath((os.path.join(os.path.dirname(bpy.data.filepath), (bpy.path.basename(bpy.data.filepath)).replace(".blend", "_") + bgee_config.GAME_EDITOR_WORKSPACE_PATH)))

        return {"FINISHED"}

def InitSystem():
    # Game properties
    bpy.types.Screen.EntityPosition = FloatVectorProperty(name="Position")
    context.screen.EntityPosition = (0.0,0.0,0.0)
    bpy.types.Screen.EntityRotation = FloatVectorProperty(name="Rotation")
    context.screen.EntityRotation = (0.0,0.0,0.0)
    bpy.types.Screen.EntityScale = FloatVectorProperty(name="Scale")
    context.screen.EntityScale = (0.0,0.0,0.0)
    
    # Scene properties
    bpy.types.Scene.BgeeActive = BoolProperty(name="")
        
    # Entity properties
    bpy.types.Object.BgeeType = EnumProperty(items = bgeeTypes, name = "Type")
    context.active_object.BgeeType = "Object"        
    bpy.types.Object.Tag = EnumProperty(items = tags, name = "Tag")
    context.active_object.Tag = "None"
    bpy.types.Object.BgeeLayer = EnumProperty(items = layers, name = "Layer")
    context.active_object.BgeeLayer = "None"
    bpy.types.Object.BgeeActive = BoolProperty(name = "", description = "Activate/Deactivate entity", default = True)
    context.active_object.BgeeActive = True
    bpy.utils.register_class(ObjectComponent)
    bpy.types.Object.Components = bpy.props.CollectionProperty(type=ObjectComponent)
    # Entity triggers
    #bpy.types.Object.Triggers = EnumProperty(items = layers, name = "Layer")
    #context.active_object.Triggers = "None"
    # Options
    bpy.types.Screen.BgeeTriggerTypes = EnumProperty(items = bgeeTriggerTypes, name = "Type")
    context.screen.BgeeTriggerTypes = "Near"
    
    # Workspace
    bpy.ops.bgee.create_workspace()
    #context.screen['Tags'] = 0

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
    
    '''
    #bpy.utils.unregister_class(UpdateInputMenu)
    bpy.utils.unregister_class(bgee_tagslayers.GameEditorDeleteTag)
    bpy.utils.unregister_class(bgee_tagslayers.GameEditorEditTag)
    bpy.utils.unregister_class(bgee_tagslayers.GameEditorDeleteLayer)
    bpy.utils.unregister_class(bgee_tagslayers.GameEditorEditLayer)
    bpy.utils.unregister_class(bgee_publish.GameEditorPublish)
    bpy.utils.unregister_class(GameEditorPlay)
    bpy.utils.unregister_class(bgee_input.CreateInputGroup)
    bpy.utils.unregister_class(bgee_component.DeleteComponent)
    bpy.utils.unregister_class(bgee_component.CreateComponent)
    bpy.utils.unregister_class(bgee_config.LoadWorkspace)
    bpy.utils.unregister_class(bgee_config.CreateWorkspace)
    bpy.utils.unregister_class(bgee_tagslayers.UpdateTags)
    bpy.utils.unregister_class(bgee_tagslayers.UpdateLayers)
    bpy.utils.unregister_class(bgee_tagslayers.AddTag)
    bpy.utils.unregister_class(bgee_tagslayers.AddLayer)
    #bpy.utils.unregister_class(InitSystem)
    bpy.utils.unregister_class(CreateGameManager)
    bpy.utils.unregister_class(bgee_layout.UnloadLayout)
    bpy.utils.unregister_class(bgee_layout.LoadLayout)
    bpy.utils.unregister_class(bgee_layout.CreateLayout)
    bpy.utils.unregister_class(bgee_layout.DeleteLayout)
    #bpy.utils.unregister_class(ActivateGameEditorPanel)
    bpy.utils.unregister_class(bgee_trigger.GameEditorAddTrigger)
    bpy.utils.unregister_class(bgee_tagslayers.GameEditorTagsPanel)
    bpy.utils.unregister_class(bgee_component.GameEditorComponentsPanel)
    bpy.utils.unregister_class(bgee_input.GameEditorInputPanel)
    bpy.utils.unregister_class(bgee_publish.GameEditorPublishPanel)
    bpy.utils.unregister_class(bgee_collider.GameEditorColliderPanel)
    bpy.utils.unregister_class(bgee_trigger.GameEditorTriggerPanel)
    bpy.utils.unregister_class(bgee_data.GameEditorDataPanel)
    bpy.utils.unregister_class(bgee_entity.GameEditorEntityPanel)
    bpy.utils.unregister_class(GameEditorPanel)
    bpy.utils.unregister_class(bgee_component.ObjectComponent)
    bpy.utils.unregister_class(bgee_input.InputGroup)
    bpy.utils.unregister_class(bgee_publish.PlatformTarget)
    #bpy.app.handlers.load_pre.remove(handler_carga_blend)
    '''
    
if __name__ == "__main__":
    register()