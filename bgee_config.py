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

import os, shutil

import bpy

GAME_EDITOR_ADDON_PATH = "bge_editor"
GAME_EDITOR_LAYOUT_NAME = "Game Editor"
GAME_MANAGER_NAME = "GameManager"
GAME_EDITOR_WORKSPACE_PATH = "bgee_workspace"
GAME_EDITOR_WORKSPACE_TEMPLATES_PATH = "templates"
GAME_EDITOR_WORKSPACE_SCRIPTS_PATH = "scripts"
INPUT_GROUP_NAME = "Input"
SCRIPT_FILE_BEGIN = "# BGEE_Component"
SCRIPT_SENSORS_BEGIN = "#BeginSensors"
SCRIPT_SENSORS_END = "#EndSensors"
GAME_EDITOR_TAB = GAME_EDITOR_LAYOUT_NAME

DEFAULT_AUDIO_VOLUME = 1

TEMP_GMTEMPLATES_PATH = "/Users/zamme8rosa/Desktop/GameEditor"

DEFAULT_TAGS = [("None", "None", "None"),
        ("Player", "Player", "Player"),
        ("MainCamera", "MainCamera", "MainCamera"),
        ("Wall", "Wall", "Wall")]
        
DEFAULT_LAYERS = [("None", "None", "None"),
          ("Players", "Players", "Players"),
          ("Cameras", "Cameras", "Cameras"),
          ("Walls", "Walls", "Walls")]

DEFAULT_INPUT = [("Left", "LEFT_ARROW"),
                 ("Right", "RIGHT_ARROW"),
                 ("Up", "UP_ARROW"),
                 ("Down", "DOWN_ARROW"),
                 ("Fire", "LEFT_CTRL"),
                 ("Jump", "SPACE")]

BGEE_OBJECT_TYPES = [("Object", "Object", "Object"),
          ("Prefab", "Prefab", "Prefab")]

BGEE_TRIGGER_TYPES = [("Near", "Near", "Near"),
                    ("Radar", "Radar", "Radar")]

bgeeComponentTypes = list() # Loaded from templates directory

bgeeInputsMenu = [("None", "None", "None"),]

bgeeCurrentTags = list()

bgeeCurrentLayers = list()

class CreateWorkspace(bpy.types.Operator):
    bl_idname="bgee.create_workspace"
    bl_label = 'Create workspace'

    def execute(self, context):
        wsp = os.path.normpath((os.path.join(os.path.dirname(bpy.data.filepath), (bpy.path.basename(bpy.data.filepath)).replace(".blend", "_") + GAME_EDITOR_WORKSPACE_PATH)))
        #print(wsp)
        print("Dir %s does not exist" % (wsp))
        print("Creating workspace directory...")
        try:
            os.mkdir(wsp)
        except:
            print("Error creating workspace directory")
        else:
            print("...Done")
            print("Creating scripts directory...")
            try:
                os.mkdir(os.path.join(wsp, GAME_EDITOR_WORKSPACE_SCRIPTS_PATH))
            except:
                print("Error creating scripts directory")
            else:
                print("...Done")
                print("Creating templates directory...")
                try:
                    os.mkdir(os.path.join(wsp, GAME_EDITOR_WORKSPACE_TEMPLATES_PATH))
                except:
                    print("Error creating templates directory")
                else:
                    print("...Done")
                    print("Installing templates...")
                    try:
                        path_addons = os.path.join(bpy.utils.user_resource('SCRIPTS', "addons", create=False), GAME_EDITOR_ADDON_PATH)
                        path_addons = os.path.join(path_addons, GAME_EDITOR_WORKSPACE_TEMPLATES_PATH)
                        
                        templates = os.listdir(path_addons)
                        #print(templates)
                        for tFile in templates:
                            shutil.copy(os.path.join(path_addons, tFile), os.path.join(wsp, GAME_EDITOR_WORKSPACE_TEMPLATES_PATH))
                    except:
                        print("Error installing templates")
                    else:
                        print("...Done")
                        
                           
        return {'FINISHED'}

def Check_workspace():
    wspExists = False
    wsp = os.path.normpath((os.path.join(os.path.dirname(bpy.data.filepath), (bpy.path.basename(bpy.data.filepath)).replace(".blend", "_") + GAME_EDITOR_WORKSPACE_PATH)))
    if (os.path.isdir(wsp)):
        if (os.path.isdir(os.path.join(wsp, GAME_EDITOR_WORKSPACE_SCRIPTS_PATH))):
            if (os.path.isdir(os.path.join(wsp, GAME_EDITOR_WORKSPACE_TEMPLATES_PATH))):
                wspExists = True
    
    return wspExists

def Check_workspace_structure():
    state = None
    print("Checking workspace structure...")
    
    # Debug: for loading good
    state = True
    
    if (state):
        print("Workspace structure ok")
    else:
        print("Error in workspace structure")
    return state

def update_bgee_components():
    try:
        bgeeComponentTypes.clear()
        templatesPath = os.path.join(os.path.normpath((os.path.join(os.path.dirname(bpy.data.filepath), (bpy.path.basename(bpy.data.filepath)).replace(".blend", "_") + GAME_EDITOR_WORKSPACE_PATH))), GAME_EDITOR_WORKSPACE_TEMPLATES_PATH)
        templateFiles = os.listdir(templatesPath)
        print(templateFiles)
        for tFileName in templateFiles:
            if (tFileName.endswith(".py")):
                option = tFileName.replace(".py", "")
                bgeeComponentTypes.append((option, option, option))
                print(tFileName.replace(".py", ""), "added to components")
    except:
        print("Error updating components")
    else:
        print("Components updated")

class LoadWorkspace(bpy.types.Operator):
    bl_idname="bgee.load_workspace"
    bl_label = 'Load workspace'

    def execute(self, context):
        # Check if blend file is saved
        if (bpy.data.filepath == ""):
            # Blend file not saved
            print("Blend file not saved")
            print("Save file before")
            # TODO: CREATE WARNING DIALOG
            self.report({'INFO'}, "Save file before start")
            return {'CANCELLED'}
        else:
            # Blend file is saved. Check workspace
            if (not (Check_workspace())):
                # Create new workspace
                bpy.utils.register_class(CreateWorkspace)
                bpy.ops.bgee.create_workspace()
                bpy.utils.unregister_class(CreateWorkspace)
                update_bgee_components()
            else:
                # Check workspace structure
                if (Check_workspace_structure()):
                    # Load workspace
                    print("Loading workspace...")
                    update_bgee_components()
                else:
                    # Fix workspace structure
                    print("Fixing workspace structure...")
                    
        
            return {'FINISHED'}

