# BgeeTypes.py
# Classes for BGEE values reading

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


class BgeeType:
    value = None
    type = None
    
    def __init__(self, val = None):
        self.value = val
        
class BgeeString(BgeeType):
    
    def __init__(self, val = ""):
        self.value = val
        self.type = "bgeestring"
    
class BgeeInteger(BgeeType):
    
    def __init__(self, val = 0):
        self.value = val
        self.type = "bgeeinteger"
        
class BgeeFloat(BgeeType):
    
    def __init__(self, val = 0.0):
        self.value = val
        self.type = "bgeefloat"
                    
class BgeeBoolean(BgeeType):
    
    def __init__(self, val = False):
        self.value = val
        self.type = "bgeeboolean"

# Special types for especific pointers

class BgeeEntity(BgeeType):
    ''' Name of an entity to use as a pointer'''
    def __init__(self, val = ""):
        self.value = val
        self.type = "bgeeentity"

class BgeeMaterial(BgeeType):
    ''' Name of a material to use as a pointer'''
    def __init__(self, val = ""):
        self.value = val
        self.type = "bgeematerial"

class BgeeTexture(BgeeType):
    ''' Name of a texture to use as a pointer'''
    def __init__(self, val = ""):
        self.value = val
        self.type = "bgeetexture"
