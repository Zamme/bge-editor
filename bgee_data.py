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

class GameEditorDataPanel(bpy.types.Panel):
    bl_idname = "bgee_data_panel"
    bl_label = "Data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Entity"
    
    @classmethod
    def poll(self, context):
        return (context.selected_objects)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if (context.active_object.type == "MESH"):
            self.bl_label = "Mesh properties"
            row.template_ID(context.active_object, "data")
        elif (context.active_object.type == "CAMERA"):
            self.bl_label = "Camera properties"
            cam = context.active_object.data
            row.prop(cam, "type", expand=True)
            row = layout.row(align=True)
            split = row.split()
            col = split.column()
            if cam.type == 'PERSP':
                row2 = col.row()
                if cam.lens_unit == 'MILLIMETERS':
                    row2.prop(cam, "lens")
                elif cam.lens_unit == 'FOV':
                    row2.prop(cam, "angle")
                row2.prop(cam, "lens_unit", text="")
            elif cam.type == 'ORTHO':
                col.prop(cam, "ortho_scale")
            ''' PANO LENS IN BGE?    
            elif cam.type == 'PANO':
                row = col.row()
                if cam.lens_unit == 'MILLIMETERS':
                    row.prop(cam, "lens")
                elif cam.lens_unit == 'FOV':
                    row.prop(cam, "angle")
                row.prop(cam, "lens_unit", text="")
            '''
            split = layout.split()
            col = split.column(align=True)
            col.label(text="Shift:")
            col.prop(cam, "shift_x", text="X")
            col.prop(cam, "shift_y", text="Y")

            col = split.column(align=True)
            col.label(text="Clipping:")
            col.prop(cam, "clip_start", text="Start")
            col.prop(cam, "clip_end", text="End")
        elif (context.active_object.type == "LAMP"):
            self.bl_label = "Light properties"
            light = context.active_object.data
            row.prop(light, "type", expand=True)
            row = layout.row(align=True)
            row.prop(light, "color")
            row = layout.row(align=True)
            row.prop(light, "energy")
