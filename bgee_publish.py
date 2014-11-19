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

class GameEditorPublishPanel(bpy.types.Panel):
    bl_idname = "bgee_publish_panel"
    bl_label = "Publish"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = bgee_config.GAME_EDITOR_TAB
            
    def draw(self, context):
        gm = context.blend_data.objects["GameManager"]
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Scenes")
        row = layout.row(align=True)
        box = row.box()
        for sce in context.blend_data.scenes:
            row = box.row()
            row.label(text=sce.name)
            row.prop(sce, "BgeeActive")
        row = layout.row(align=True)
        row.label(text="Platforms")
        row = layout.row(align=True)
        box = row.box()    
        row = box.row(align=True)
        row.prop(gm.BgeeTarget, "windows")    
        row = box.row(align=True)
        row.prop(gm.BgeeTarget, "mac")    
        row = box.row(align=True)
        row.prop(gm.BgeeTarget, "linux")
        row = layout.row(align=True)    
        row.operator("bgee.publish")

class GameEditorPublish(bpy.types.Operator):
    bl_idname = "bgee.publish"
    bl_label = "Publish"
    
    def modal(self, context, event):
        #bpy.ops.wm.save_as_runtime()
         
        return {"PASS_THROUGH"}
    
    # TODO: Error exporting
    def invoke(self, context, event):
        self.execute(context)
        #bpy.ops.wm.save_as_runtime()
        #context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
        #return {"FINISHED"}
    
    def execute(self, context):
        gm = context.blend_data.objects["GameManager"]
        print("Publishing in platforms :")
        if (gm.BgeeTarget.windows):
            print("Windows")
        if (gm.BgeeTarget.mac):
            print("Mac")
        if (gm.BgeeTarget.linux):
            print("Linux")
        
        return {"FINISHED"}

class PlatformTarget(bpy.types.PropertyGroup):
    windows = bpy.props.BoolProperty(name="Windows", default=True)
    mac = bpy.props.BoolProperty(name="Mac", default=False)
    linux = bpy.props.BoolProperty(name="Linux", default=False)

