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

'''Game Manager Class'''
class GameManager():
    name = None
    gameEditorLayoutRef = None
    activated = None
    emptyObject = None
    version = None
    
    def __init__(self, name = bgee_config.GAME_MANAGER_NAME):
        self.name = name
        self.activated = False
        
    def set_object(self, ob):
        self.emptyObject = ob
        self.emptyObject.name = self.name
        
    def SetLayoutReference(self,ref):
        self.gameEditorLayoutRef = ref

def prepare_entity(obList):
    ''' Create entity bgee properties  '''
    if (obList != None):
        for ob in obList:
            if (ob.name != "GameManager"):
                if (not("entityProps" in ob.keys())):
                    ob.entityProps.active = True
                    ob.entityProps.prefab = False
                    bpy.types.Object.bgeeTag = bpy.props.EnumProperty(items=bgee_config.bgeeCurrentTags, name="")
                    ob.bgeeTag = "None"
                    oLayer = ob.entityProps.layers.add()
                    oLayer.first, oLayer.second, oLayer.third = "None", "None", "None"
                bpy.types.Object.bgeeTag = bpy.props.EnumProperty(items=bgee_config.bgeeCurrentTags, name="")
                bpy.types.Object.bgeeLayer = bpy.props.EnumProperty(items=bgee_config.bgeeCurrentLayers, name="")

def prepare_scene(scList):
    ''' Create scene bgee properties (IT MUST BE A LIST!) '''
    if (scList != None):
        for sc in scList:
            if (not("BgeeActive" in sc.keys())):
                sc.BgeeActive = True
    