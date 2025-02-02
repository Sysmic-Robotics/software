from comms.vision.vision import Vision
from world.world import World
import threading
from constants import *
from ai.robot import Robot
from sysmic_kit import *
import time
from comms.sender.grsim import Grsim
from comms.sender.robot_coms import RobotComms
import math
import random

# Initialize world
world : World = World(1,1)
vision : Vision = Vision(VISION_IP, VISION_PORT, world)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()

radio : RobotComms = RobotComms()
radio_t = threading.Thread(target=radio.loop)
radio_t.start()

# Wait to open the simulator
time.sleep(1)
# Game loop
robot : Robot = Robot(0, TeamColor.BLUE)
points = []
center = Vector2(0,0)
n_points = 8
for i in range(0,n_points):
    theta = 2*(math.pi/n_points)*i
    point = center + Vector2(0,1).rotate(theta)
    points.append(point)
grsim = Grsim()
i = 0
next_point = points.pop(0)
grsim.communicate_pos_robot(0,0, next_point.x, next_point.y, random.uniform(0, 2*math.pi))


test_failed = []
while True:
    #time.sleep(0.0016)
    finish = robot.move_to(Vector2(0,0))
    if finish:
        error = robot.data.position.distance_to(next_point)
        if error > 0.05:
            test_failed.append( (next_point, error) )
        if len(points) == 0:
            break
        i += 1
        next_point = points.pop(0)
        grsim.communicate_pos_robot(0,0, next_point.x, next_point.y , random.uniform(0, 2*math.pi))
        time.sleep(0.5)

print("Test finish", test_failed)

