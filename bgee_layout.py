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


class LoadLayout(bpy.types.Operator):
    bl_idname="bgee.load_layout"
    bl_label = 'Load Layout'

    _timer = None
    gameLogicLoaded = False
    ret = False
    
    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if event.type == 'TIMER':
            if (not self.gameLogicLoaded):
                self.gameLogicLoaded = True
                bpy.context.window.screen = bpy.data.screens["Game Logic"]
                context.scene.render.engine = "BLENDER_GAME"
                return self.cancel(context)
            else:
                return self.cancel(context)
        return {'RUNNING_MODAL'}
        '''    
        if (gameLogicLoaded and    
        if (self.gameLogicLoaded):
            bpy.ops.screen.new()
        ret = bpy.ops.screen.area_join(min_x=area1.x,min_y=area1.y, max_x=area2.x, max_y=area2.y)
        if ret == {'FINISHED'}:
            self.area_count -= 1
            print(self.area_count)
            break
        else:
            context.area.type == 'VIEW_3D'
            print(context.area.type)
            return self.cancel(context)
        '''

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)            
        return {'CANCELLED'}

class CreateLayout(bpy.types.Operator):
    bl_idname="bgee.create_layout"
    bl_label = 'Create Layout'

    _timer = None
    gameLogicLoaded = False
    ret = False
    
    def modal(self, context, event):
        if event.type == 'ESC':
           return self.cancel(context)

        if event.type == 'TIMER':
            if (self.ret == {"FINISHED"}):
                bpy.context.window.screen.name = bgee_configGAME_EDITOR_LAYOUT_NAME
                outlinerArea = find_area_by_type("OUTLINER")
                viewArea = find_area_by_type("VIEW_3D")
                if (outlinerArea != None and viewArea != None):
                    outlinerArea.type = "VIEW_3D"
                    ret2 = bpy.ops.screen.area_join(min_x=outlinerArea.x,min_y=outlinerArea.y, max_x=viewArea.x, max_y=viewArea.y)
                    bpy.ops.screen.screen_full_area()
                    bpy.ops.screen.screen_full_area()
                    viewArea = find_area_by_type("VIEW_3D")
                    for re in viewArea.regions:
                        if (re.type == "TOOLS" and re.width == 1):
                            #TODO: rewidth the toolshelf to 300
                            override = bpy.context.copy()
                            override['area'] = viewArea
                            bpy.ops.view3d.toolshelf(override)
                            #TODO: change shelf selected to gamemaker                    
                return self.cancel(context)
            else:
                return self.cancel(context)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.ret = bpy.ops.screen.new()
        global bgeel
        bgeel.activated = True
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        bpy.ops.bgee.create_gamemanager()
        return {'CANCELLED'}

class DeleteLayout(bpy.types.Operator):
    bl_idname="bgee.delete_layout"
    bl_label = 'Delete Layout'

    def execute(self, context):
        bpy.ops.screen.delete()
        global bgeel
        bgeel.activated = False
        return {'FINISHED'}

class UnloadLayout(bpy.types.Operator):
    bl_idname="bgee.unload_layout"
    bl_label = 'Unload Layout'

    def execute(self, context):
        print("Game Editor Layout deleted!")

        return({'FINISHED'}) 

