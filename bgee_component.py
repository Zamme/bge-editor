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
from . import bgee_config, bgee_script_reader

import os
import shutil

class BGEE_OT_update_component_type_selector(bpy.types.Operator):
    bl_idname = "bgee.update_component_type_selector"
    bl_label = ""
    
    def execute(self, context):
        bgee_config.update_bgee_components()
        bpy.types.Object.BgeeComponentTypeSelected = bpy.props.EnumProperty(items = bgee_config.bgeeComponentTypes, name = "Type")
        
        return {"FINISHED"}

'''
class BGEE_OT_update_current_entities_selector(bpy.types.Operator):
    bl_idname = "bgee.update_current_entities_selector"
    bl_label = ""
    
    def execute(self, context):
        bgee_config.update_current_entities()
        bpy.types.Object.BgeeCurrentEntitySelected = bpy.props.EnumProperty(items = bgee_config.bgeeCurrentEntities, name="Entity")
        
        return {"FINISHED"}
'''

class BGEE_OT_select_entity(bpy.types.Operator):
    bl_idname="bgee.select_entity"
    bl_label = 'Select'
    bl_property = "toEntity"
    
    selectedEntity = bpy.props.StringProperty()
    selectedComponent = bpy.props.IntProperty()
    selectedProp = bpy.props.IntProperty()
    
    def entities(self, context):
        return [(ent.name, ent.name, "") for ent in bpy.data.objects]
    
    toEntity = bpy.props.EnumProperty(items=entities)

    def execute(self, context):
        bpy.data.objects[self.selectedEntity].entityProps.components[self.selectedComponent].cScriptEntityProperties[self.selectedProp].value = self.toEntity
        
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'FINISHED'}

class BGEE_OT_select_material(bpy.types.Operator):
    bl_idname="bgee.select_material"
    bl_label = 'Select'
    bl_property = "toMaterial"
    
    selectedEntity = bpy.props.StringProperty()
    selectedComponent = bpy.props.IntProperty()
    selectedProp = bpy.props.IntProperty()
    
    def materials(self, context):
        return [(mat.name, mat.name, "") for mat in bpy.data.materials]
    
    toMaterial = bpy.props.EnumProperty(items=materials)

    def execute(self, context):
        bpy.data.objects[self.selectedEntity].entityProps.components[self.selectedComponent].cScriptMaterialProperties[self.selectedProp].value = self.toMaterial
        
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'FINISHED'}

class BGEE_OT_select_texture(bpy.types.Operator):
    bl_idname="bgee.select_texture"
    bl_label = 'Select'
    bl_property = "toTexture"
    
    selectedEntity = bpy.props.StringProperty()
    selectedComponent = bpy.props.IntProperty()
    selectedProp = bpy.props.IntProperty()
    
    def textures(self, context):
        return [(tex.name, tex.name, "") for tex in bpy.data.textures]
    
    toTexture = bpy.props.EnumProperty(items=textures)

    def execute(self, context):
        bpy.data.objects[self.selectedEntity].entityProps.components[self.selectedComponent].cScriptTextureProperties[self.selectedProp].value = self.toTexture
        
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'FINISHED'}

class ComponentScriptIntegerProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.IntProperty()
    
class ComponentScriptFloatProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.FloatProperty()

class ComponentScriptStringProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="")
    value = bpy.props.StringProperty(name="")

class ComponentScriptBooleanProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()
    value = bpy.props.BoolProperty(name="")

class ComponentScriptEntityProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="")
    value = bpy.props.StringProperty(name="")

class ComponentScriptMaterialProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="")
    value = bpy.props.StringProperty(name="")

class ComponentScriptTextureProperty(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="")
    value = bpy.props.StringProperty(name="")

class ObjectComponent(bpy.types.PropertyGroup):
    cActive = bpy.props.BoolProperty(name="", description="Active", default=True)
    cType = bpy.props.StringProperty(name="Component", default="Unknown")
    cScript = bpy.props.StringProperty(name="Script", default="Script")
    cName = bpy.props.StringProperty(name="", default="Name")                    
    cScriptIntegerProperties = bpy.props.CollectionProperty(type=ComponentScriptIntegerProperty)
    cScriptFloatProperties = bpy.props.CollectionProperty(type=ComponentScriptFloatProperty)
    cScriptStringProperties = bpy.props.CollectionProperty(type=ComponentScriptStringProperty)
    cScriptBooleanProperties = bpy.props.CollectionProperty(type=ComponentScriptBooleanProperty)
    cScriptEntityProperties = bpy.props.CollectionProperty(type=ComponentScriptEntityProperty)
    cScriptMaterialProperties = bpy.props.CollectionProperty(type=ComponentScriptMaterialProperty)
    cScriptTextureProperties = bpy.props.CollectionProperty(type=ComponentScriptTextureProperty)

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
                        delParameters = row.operator("bgee.delete_component", icon="X")
                        delParameters.entName = context.active_object.name
                        delParameters.compID = compIndex
                        row = box.row(align=True)
                        row.prop(comp, "cActive")
                        row.label(text=comp.cType)
                        row.prop(comp, "cName")
                        for compProp in comp.cScriptIntegerProperties:
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.prop(compProp, "value")
                        for compProp in comp.cScriptFloatProperties:
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.prop(compProp, "value")
                        for compProp in comp.cScriptStringProperties:
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.prop(compProp, "value")
                        for compProp in comp.cScriptBooleanProperties:
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.prop(compProp, "value")
                        for propId,compProp in enumerate(comp.cScriptEntityProperties):
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.label(compProp.value)
                            selEntOp = row.operator("bgee.select_entity", "Select")
                            selEntOp.selectedEntity = context.active_object.name
                            selEntOp.selectedComponent = compIndex
                            selEntOp.selectedProp = propId
                        for propId,compProp in enumerate(comp.cScriptMaterialProperties):
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.label(compProp.value)
                            selMatOp = row.operator("bgee.select_material", "Select")
                            selMatOp.selectedEntity = context.active_object.name
                            selMatOp.selectedComponent = compIndex
                            selMatOp.selectedProp = propId
                        for compProp in comp.cScriptTextureProperties:
                            row = box.row(align=True)
                            row.label(compProp.name)
                            row.label(compProp.value)
                            selTexOp = row.operator("bgee.select_texture", "Select")
                            selTexOp.selectedEntity = context.active_object.name
                            selTexOp.selectedComponent = compIndex
                            selTexOp.selectedProp = propId
                    

class DeleteComponent(bpy.types.Operator):
    bl_idname = "bgee.delete_component"
    bl_label = ""
    compID = bpy.props.IntProperty()
    entName = bpy.props.StringProperty()
    
    def execute(self, context):
        bpy.data.objects[self.entName].entityProps.components.remove(self.compID)
        print("component deleted!")
        
        return {"FINISHED"}
        
class CreateComponent(bpy.types.Operator):
    bl_idname="bgee.create_component"
    bl_label = 'Create Component'

    def create_properties(self, context, fp, compo):
        # Create entity bgee properties from bgeetypes lines
        compo.cScriptIntegerProperties.clear()
        compo.cScriptFloatProperties.clear()
        compo.cScriptStringProperties.clear()
        compo.cScriptBooleanProperties.clear()
        compo.cScriptEntityProperties.clear()
        compo.cScriptMaterialProperties.clear()
        compo.cScriptTextureProperties.clear()
        
        sCatch = bgee_script_reader.BGEE_ScriptCatch(fp)
        sProps = sCatch.get_properties()
        
        for prop in sProps:
            if (prop.type == "BgeeInteger"):
                createdProp = compo.cScriptIntegerProperties.add()
            elif (prop.type == "BgeeFloat"):
                createdProp = compo.cScriptFloatProperties.add()
            elif (prop.type == "BgeeString"):
                createdProp = compo.cScriptStringProperties.add()
            elif (prop.type == "BgeeBoolean"):
                createdProp = compo.cScriptBooleanProperties.add()
            elif (prop.type == "BgeeEntity"):
                createdProp = compo.cScriptEntityProperties.add()
            elif (prop.type == "BgeeMaterial"):
                createdProp = compo.cScriptMaterialProperties.add()
            elif (prop.type == "BgeeTexture"):
                createdProp = compo.cScriptTextureProperties.add()
            createdProp.name = prop.name
            createdProp.value = prop.value
    
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
                self.create_properties(context, dstFilePath, component)
                #self.create_bricks(context, component)
        return {'FINISHED'}
