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
from . import bgee_config, bgee_component, bgee_tagslayers

class GameEditorEntityPanel(bpy.types.Panel):
    bl_idname = "bgee_entity_panel"
    bl_label = "Entity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Entity"
        
    def draw(self, context):
        gm = context.blend_data.objects["GameManager"]
        layout = self.layout
        # Selected entities names, location, rotation, scale
        row = layout.row(align=True)
        row.label(text="Entities selected:")
        row = layout.row(align=True)
        box = row.box()
        for ob in context.selected_objects:
            boxrow = box.row(align=True)
            boxrow.label(text=ob.name)
            boxrow.prop(ob.entityProps, "active")
            boxrow = box.row(align=True)
            boxrow.prop(ob.entityProps, "prefab")
            boxrow = box.row(align=True)
            if (len(context.selected_objects) > 1):
                # Check tag equals
                pass
            else:
                boxrow.label("Tag:")
                boxrow.prop(context.active_object, "bgeeTag")
                boxrow = box.row(align=True)
                boxrow.label("Layers:")
                boxcolumn = boxrow.column(align=True)
                for layId,lay in enumerate(context.active_object.entityProps.layers):
                    boxrowcolumn = boxcolumn.row(align=True)
                    boxrowcolumn.label(lay.first)
                    if (lay.first != "None"):
                        remParam = boxrowcolumn.operator("bgee.remove_entity_layer", icon="X")
                        remParam.selectedLayer = layId
                        remParam.selectedEntity = context.active_object.name
                boxcolumn.separator()
                boxrowcolumn = boxcolumn.row(align=True)
                boxrowcolumn.prop(gm, "bgeeLayer")
                addOp = boxrowcolumn.operator("bgee.add_entity_layer", "Add")
                addOp.selectedEntity = ob.name
                addOp.selectedLayer = gm.bgeeLayer
                
        row = layout.row(align=True)
        row.prop(gm.entityTransform, "location")
        row = layout.row(align=True)
        row.prop(gm.entityTransform, "rotation")
        row = layout.row(align=True)
        row.prop(gm.entityTransform, "scale")

# START Multiselection transform methods
def update_location(self, context):
    gm = context.blend_data.objects["GameManager"]
    obs = context.selected_objects
    for ob in obs:
        ob.location = gm.entityTransform.location

def update_rotation(self, context):
    gm = context.blend_data.objects["GameManager"]
    obs = context.selected_objects
    for ob in obs:
        ob.rotation_euler = gm.entityTransform.rotation

def update_scale(self, context):
    gm = context.blend_data.objects["GameManager"]
    obs = context.selected_objects
    for ob in obs:
        ob.scale = gm.entityTransform.scale

def update_transform(context): # TODO: NOT WORKING WELL
    gm = context.blend_data.objects["GameManager"]
    obs = context.selected_objects
    if (len(obs) > 0):
        locationX, locationY, locationZ, rotationX, rotationY, rotationZ, scaleX, scaleY, scaleZ = True, True, True, True, True, True, True, True, True
        # Location
        for ob in obs:
            if (obs[0].location.x != ob.location.x):
                locationX = False
        if (locationX):
            gm.entityTransform.location[0] = obs[0].location[0]
    else:
        print("No object selected")
# END Multiselection transform methods

class MultiEntityTransform(bpy.types.PropertyGroup):
    location = bpy.props.FloatVectorProperty(update=update_location)
    rotation = bpy.props.FloatVectorProperty(subtype="EULER", update=update_rotation)
    scale = bpy.props.FloatVectorProperty(update=update_scale)

    
class BGEE_OT_multiselection(bpy.types.Operator):
    bl_idname = "bgee.multiselection"
    bl_label = "Entity multiselection catcher"

    _updating = False
    _calcs_done = False
    _timer = None
    nObjects = None

    def selected_objects_changed(self, context):
        currentNObjects = len(context.selected_objects)
        if (self.nObjects is not None):
            if (self.nObjects != currentNObjects):
                self.nObjects = currentNObjects
                return True
            else:
                return False
        else:
            self.nObjects = currentNObjects
            return False
        #self._calcs_done = True

    def modal(self, context, event):
        if event.type == 'TIMER' and not self._updating:
            self._updating = True
            if (self.selected_objects_changed(context)):
                update_transform(context)
            self._updating = False
        if self._calcs_done:
            self.cancel(context)

        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        self._updating = False
        self._timer = context.window_manager.event_timer_add(0.2, context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self._timer = None
        return {'CANCELLED'}

# ENTITY PROPERTIES
class EntityProperties(bpy.types.PropertyGroup):
    active = bpy.props.BoolProperty(default=True, name="Active")
    prefab = bpy.props.BoolProperty(default=False, name="Prefab")
    #tag = bpy.props.EnumProperty(items=bgee_config.bgeeCurrentTags)
    layers = bpy.props.CollectionProperty(type=bgee_tagslayers.LayerItem)
    components = bpy.props.CollectionProperty(type=bgee_component.ObjectComponent)

class BGEE_OT_add_entity_layer(bpy.types.Operator):
    bl_idname = "bgee.add_entity_layer"
    bl_label = "Add Entity Layer"
    selectedLayer = bpy.props.StringProperty()
    selectedEntity = bpy.props.StringProperty()
    
    def execute(self, context):
        entity = bpy.data.objects[self.selectedEntity]
        # If same layer in dont add
        same = False
        for lay in entity.entityProps.layers:
            if (self.selectedLayer == lay.first):
                same = True
        if (not same):
            # If None is present
            if (len(entity.entityProps.layers) > 0):
                if (entity.entityProps.layers[0].first == "None"):
                    entity.entityProps.layers.remove(0)
            # If None is selected
            if (self.selectedLayer == "None"):
                while (len(entity.entityProps.layers) > 0):
                    entity.entityProps.layers.remove(0)
            addedLayer = entity.entityProps.layers.add()
            addedLayer.first, addedLayer.second, addedLayer.third = self.selectedLayer, self.selectedLayer, self.selectedLayer
            
        return {'FINISHED'}

class BGEE_OT_remove_entity_layer(bpy.types.Operator):
    bl_idname = "bgee.remove_entity_layer"
    bl_label = ""
    selectedLayer = bpy.props.IntProperty()
    selectedEntity = bpy.props.StringProperty()
    
    def execute(self, context):
        entity = bpy.data.objects[self.selectedEntity]
        entity.entityProps.layers.remove(self.selectedLayer)
        if (len(entity.entityProps.layers) < 1):
            noneLayer = entity.entityProps.layers.add()
            noneLayer.first, noneLayer.second, noneLayer.third = "None", "None", "None"
            
        return {'FINISHED'}


''' COMING SOON        
class EntityList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob = data
        slot = item
        ma = slot.material

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(ob.name)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon_value=icon)
'''
