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


import os

class TypeProperty():
    name = None
    type = None
    value = None
    
    def __init__(self, n, t, v):
        self.name = n
        self.type = t
        self.value = v

class BGEE_ScriptCatch():
    sensors = list()
    properties = list()
    bgeeFile = None # File pointer
    bgeeScriptLines = None # File content
    decodeState = None
    
    def __init__(self, fPath):
        self.sensors.clear()
        self.properties.clear()
        if (self.read_file(fPath)):
            if (self.check_file()):
                self.decode_file()
            else:
                print("It's not a Bgee file")
        else:
            print("File not found or corrupted")

    def get_properties(self):
        return self.properties
    
    def get_sensors(self):
        return self.sensors
    
    def translate_boolean(self, value):
        retValue = False
        if (value == "True"):
            retValue = True
            
        return retValue
    
    def add_property(self, prop):
        self.properties.append(prop)
        
    def read_file(self, fPath):
        check = False
        # Read bgee script file
        try:
            self.bgeeFile = open(fPath, "r")
            self.bgeeScriptLines = self.bgeeFile.readlines()
            self.bgeeFile.close()
        except:
            check = False
            print("Error opening file!")
        else:
            check = True
            print("File read")
        
        return check

    def check_file(self):
        # Some line must contains "BGEE_Component"
        check = False
        for fLine in self.bgeeScriptLines:
            if ("BGEE_Component" in fLine):
                check = True
                break
        return check

    def decode_file(self):
        self.decodeState = "Searching"
        for fLine in self.bgeeScriptLines:
            self.decode_line(fLine)

    def decode_line(self, line):
        if ("EndBgeeProperties" in line):
            self.decodeState = "Searching"
            print("Bgee properties end found")
            
        # Decoding
        # Properties
        if (self.decodeState == "ReadingProperties"):
            lineSplitted = line.split(sep="=")
            propName = lineSplitted[0].strip()
            decPart = lineSplitted[1].split("(")
            decPart = decPart[1].split(")")
            value = decPart[0]
            decType = None
            if ("BgeeFloat" in line):
                decType = "BgeeFloat"
                value = float(value)
            elif ("BgeeInteger" in line):
                decType = "BgeeInteger"
                value = int(value)
            elif ("BgeeString" in line):
                decType = "BgeeString"
                value = str(value.strip('"'))
            elif ("BgeeBoolean" in line):
                decType = "BgeeBoolean"
                value = self.translate_boolean(value)
            elif ("BgeeEntity" in line):
                decType = "BgeeEntity"
                value = str(value.strip('"'))
            elif ("BgeeMaterial" in line):
                decType = "BgeeMaterial"
                value = str(value.strip('"'))
            elif ("BgeeTexture" in line):
                decType = "BgeeTexture"
                value = str(value.strip('"'))
                
            self.add_property(TypeProperty(propName, decType, value))
            print("Added property:", propName, decType, value)
            
        if ("BeginBgeeProperties" in line):
            # Catching properties
            self.decodeState = "ReadingProperties"
            print("Bgee properties begin found")
        
