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

import os
import shutil

class BGEE_OT_update_component_type_selector(bpy.types.Operator):
    bl_idname = "bgee.update_component_type_selector"
    bl_label = ""
    
    def execute(self, context):
        bgee_config.update_bgee_components()
        gm = context.blend_data.objects["GameManager"]
        bpy.types.Object.BgeeComponentTypeSelected = EnumProperty(items = bgee_config.bgeeComponentTypes, name = "Type")
        
        return {"FINISHED"}

class ComponentScriptIntegerProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.IntegerProperty()
    
class ComponentScriptFloatProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.FloatProperty()

class ComponentScriptStringProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.StringProperty()

class ComponentScriptBooleanProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.BoolProperty()

class ObjectComponent(bpy.types.PropertyGroup):
    cActive = bpy.props.BoolProperty(name="", description="Active", default=True)
    cType = bpy.props.StringProperty(name="Component", default="Unknown")
    cScript = bpy.props.StringProperty(name="Script", default="Script")
    cName = bpy.props.StringProperty(name="", default="Name")                    
    cScriptIntegerProperties = bpy.props.CollectionProperty(type=ComponentScriptIntegerProperty)
    cScriptFloatProperties = bpy.props.CollectionProperty(type=ComponentScriptFloatProperty)
    cScriptStringProperties = bpy.props.CollectionProperty(type=ComponentScriptStringProperty)
    cScriptBooleanProperties = bpy.props.CollectionProperty(type=ComponentScriptBooleanProperty)

class GameEditorComponentsPanel(bpy.types.Panel):
    bl_idname = "bgee_components_panel"
    bl_label = "Components"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Entity"
            
    @classmethod
    def poll(self, context):
        return (context.selected_objects)

    def draw(self, context):
        gm = context.blend_data.objects["GameManager"]
        layout = self.layout
        row = layout.row(align=True)
        row.prop(gm, "BgeeComponentTypeSelected")
        row.operator("bgee.create_component", "Add")
        if (len(context.selected_objects) > 1):
            for ob in context.selected_objects:
                if (ob.is_property_set("entityProps")):
                    if (ob.entityProps.components):
                        for comp in ob.entityProps.components:
                            row = layout.row(align=True)
                            box = row.box()
                            row = box.row(align=True)
                            row.alignment = "RIGHT"
                            row.operator("bgee.delete_component", icon="X")
                            row = box.row(align=True)
                            row.prop(comp, "cActive")
                            row.label(text=comp.cType)
                            row.prop(comp, "cName")
        else:
            if ("entityProps" in context.active_object.keys()):
                if (context.active_object.entityProps.components):
                    for compIndex,comp in enumerate(context.active_object.entityProps.components):
                        row = layout.row(align=True)
                        box = row.box()
                        row = box.row(align=True)
                        row.alignment = "RIGHT"
                        row.operator("bgee.delete_component", icon="X")
                        row = box.row(align=True)
                        row.prop(comp, "cActive")
                        row.label(text=comp.cType)
                        row.prop(comp, "cName")
                    

class DeleteComponent(bpy.types.Operator):
    bl_idname = "bgee.delete_component"
    bl_label = ""
    compID = None
    
    def execute(self, context):
        # TODO: How can I delete a component without reference in button/operator?
        print("component deleted!")
        
        return {"FINISHED"}
        
class CreateComponent(bpy.types.Operator):
    bl_idname="bgee.create_component"
    bl_label = 'Create Component'

    def create_properties(self, context, fp, compo):
        # Read bgeescript file
        bgeeFile = open(fp, "r")
        self.bgeeScriptLines = bgeeFile.readlines()
        bgeeFile.close()
        
        # Create entity bgee properties from bgeetypes lines
        compo.cScriptIntegerProperties.clear()
        compo.cScriptFloatProperties.clear()
        compo.cScriptStringProperties.clear()
        compo.cScriptBooleanProperties.clear()
        for line in self.bgeeScriptLines:
            #print(line)
            if (line.startswith("#")):
                continue
            if ("bgeeInteger" in line):
                lineSplitted = line.split(sep="=")
                propName = lineSplitted[0].strip()
                decPart = lineSplitted[1].split("(")
                decPart = decPart[1].split(")")
                decPart = decPart[0]
                createdProp = compo.cScriptIntegerProperties.add()
                createdProp.name = propName
                createdProp.value = int(decPart)
            elif ("bgeeFloat" in line):
                lineSplitted = line.split(sep="=")
                propName = lineSplitted[0].strip()
                decPart = lineSplitted[1].split("(")
                decPart = decPart[1].split(")")
                decPart = decPart[0]
                createdProp = compo.cScriptFloatProperties.add()
                createdProp.name = propName
                createdProp.value = float(decPart)
            elif ("bgeeString" in line):
                lineSplitted = line.split(sep="=")
                propName = lineSplitted[0].strip()
                decPart = lineSplitted[1].split('("')
                decPart = decPart[1].split('")')
                decPart = decPart[0]
                createdProp = compo.cScriptStringProperties.add()
                createdProp.name = propName
                createdProp.value = str(decPart)
    
    ''' TODO: CHECK IT IN PLAY OPERATOR  // APPLY LOGIC BRICKS IN PLAY OPERATOR TOO?  
    def create_bricks(self, context, compo):
        # For script
        bpy.ops.logic.sensor_add(type="ALWAYS", name=compo.type)
        bpy.ops.logic.controller_add(type="PYTHON", name=(compo.type + "Python"))
        alwaysBrick = context.active_object.game.sensors[compo.type]
        pythonBrick = context.active_object.game.controllers[compo.type + "Python"]
        bpy.ops.text.open(filepath = compo.script)
        pythonBrick.text = context.blend_data.texts[os.path.basename(compo.script)]
        alwaysBrick.link(controller=pythonBrick)
        
        # For others
        reading = False
        for line in self.bgeeScriptLines:
            if (reading and (not (bgee_config.SCRIPT_SENSORS_BEGIN in line)) and (not(bgee_config.SCRIPT_SENSORS_END in line))) :
                splittedLine = line.strip()
                splittedLine = line.split(sep="=")
                sensorName = (splittedLine[0] + "Sensor")
                controllerName = (splittedLine[0] + "And")
                actuatorName = (splittedLine[0] + "Actuator")
                bpy.ops.logic.sensor_add(type="KEYBOARD", name=sensorName)
                bpy.ops.logic.controller_add(type="LOGIC_AND", name=controllerName)
                bpy.ops.logic.actuator_add(type="MOTION", name=actuatorName)
                sensorBrick = context.active_object.game.sensors[sensorName]
                controllerBrick = context.active_object.game.controllers[controllerName]
                actuatorBrick = context.active_object.game.actuators[actuatorName]
                sensorBrick.link(controller=controllerBrick)
                controllerBrick.link(actuator=actuatorBrick)
                actuatorBrick.mode = "OBJECT_CHARACTER"
                if ("left" in splittedLine[0]):
                    sensorBrick.key = context.screen.bgeeInputs[compo.input].left
                    actuatorBrick.offset_rotation = (0,0,context.active_object.game.properties["angularVelocity"].value)        
                elif ("right" in splittedLine[0]):
                    sensorBrick.key = context.screen.bgeeInputs[compo.input].right        
                    actuatorBrick.offset_rotation = (0,0, -(context.active_object.game.properties["angularVelocity"].value))        
                elif ("up" in splittedLine[0]):
                    sensorBrick.key = context.screen.bgeeInputs[compo.input].up        
                    actuatorBrick.offset_location = (0,context.active_object.game.properties["velocity"].value,0)        
                elif ("down" in splittedLine[0]):
                    sensorBrick.key = context.screen.bgeeInputs[compo.input].down        
                    actuatorBrick.offset_location = (0,-(context.active_object.game.properties["velocity"].value),0)        
                elif ("jump" in splittedLine[0]):
                    sensorBrick.key = context.screen.bgeeInputs[compo.input].jump
                    actuatorBrick.use_character_jump = True        
                elif ("fire1" in splittedLine[0]):
                    sensorBrick.key = context.screen.bgeeInputs[compo.input].fire1
                    actuatorBrick.type = "EDIT_OBJECT"
                    actuatorBrick.mode = "ADDOBJECT"
                    actuatorBrick.linear_velocity = (0, context.active_object.game.properties["shotVelocity"].value,0)        
            if (bgee_config.SCRIPT_SENSORS_BEGIN in line):
                reading = True
            elif(bgee_config.SCRIPT_SENSORS_END in line):
                reading = False
    '''
                
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        for ob in context.selected_objects:
            component = context.active_object.entityProps.components.add()
            component.cType = gm.BgeeComponentTypeSelected
            wsp = gm.Workspace
            try:
                dstFilePath = os.path.join(wsp, bgee_config.GAME_EDITOR_WORKSPACE_SCRIPTS_PATH, component.cType +  str(len(context.active_object.entityProps.components)) + ".py")
                if (os.path.exists(dstFilePath)):
                    print("File exists in scripts dir")
                else:
                    shutil.copy(os.path.join(wsp, bgee_config.GAME_EDITOR_WORKSPACE_TEMPLATES_PATH, (component.cType  + ".py")), dstFilePath)
            except:
                print("Component cant be created")
            else:
                component.cScript = bpy.path.relpath(dstFilePath)
                print("component created!", component.cScript)
                #self.create_properties(context, dstFilePath, component)
                #self.create_bricks(context, component)
        return {'FINISHED'}
