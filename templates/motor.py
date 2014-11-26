# BGEE_Component

# Motor.py

import GmTypes

velocity = GmTypes.GmFloat(0.1)
angularVelocity = GmTypes.GmFloat(0.01)
name = GmTypes.GmString("motor")
lives = GmTypes.GmInteger(3)
proyectile = GmTypes.GmString("proyectile")
shotVelocity = GmTypes.GmFloat(0.5)

import bge
import bpy

#BeginSensors
left = "KeyboardLeftSensor"
right = "KeyboardRightSensor"
up = "KeyboardUpSensor"
down = "KeyboardDownSensor"
fire1 = "KeyboardFire1Sensor"
jump = "KeyboardJumpSensor"
#EndSensors

