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
        row = layout.row(align=True)
        row.prop(gm.entityTransform, "location")
        row = layout.row(align=True)
        row.prop(gm.entityTransform, "rotation")
        row = layout.row(align=True)
        row.prop(gm.entityTransform, "scale")

class MultiEntityTransform(bpy.types.PropertyGroup):
    location = bpy.props.FloatVectorProperty()
    rotation = bpy.props.FloatVectorProperty()
    scale = bpy.props.FloatVectorProperty()

def update_transform(context):
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
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self._timer = None
        return {'CANCELLED'}
    
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
