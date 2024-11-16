from comms.vision.vision import Vision
from world.world import World
import threading
from constants import *
from ai.robot import Robot
from sysmic_kit import *
import time
from comms.sender.robot_coms import RobotComms
import math
import random

import keyboard as kb
# Initialize world
world : World = World(1,1)
vision : Vision = Vision(VISION_IP, VISION_PORT, world)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()


# Game loop
robot : Robot = Robot(0, TeamColor.BLUE, world)
speed = 5
comms = RobotComms()
while True:
    dir = Vector2(0,0)
    if kb.is_pressed('left'):
        dir += Vector2(-1,0)
    if kb.is_pressed('right'):
        dir += Vector2(1,0)
    if kb.is_pressed('up'):
        dir += Vector2(0,1)
    if kb.is_pressed('down'):
        dir += Vector2(0,-1)
    global_vel = dir.normalize()*speed
    data = robot.get_data()
    local_vel = global_vel.rotate(-data.orientation)
    comms.send_robot_data(0, TeamColor.BLUE, vel=local_vel)
print("Test finish", test_failed)

