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

# BGEE_Component (Mandatory for bgee catch)

# Motor.py

from bgee_types import *

# BeginBgeeProperties
velocity = BgeeFloat(0.1)
angularVelocity = BgeeFloat(0.01)
name = BgeeString("motor")
lives = BgeeInteger(3)
proyectile = BgeeString("proyectile")
shotVelocity = BgeeFloat(0.5)
dead = BgeeBoolean(False)
entity1 = BgeeEntity()
material1 = BgeeMaterial()
texture1 = BgeeTexture()
# EndBgeeProperties

#BeginSensors
left = "KeyboardLeftSensor"
right = "KeyboardRightSensor"
up = "KeyboardUpSensor"
down = "KeyboardDownSensor"
fire1 = "KeyboardFire1Sensor"
jump = "KeyboardJumpSensor"
#EndSensors

