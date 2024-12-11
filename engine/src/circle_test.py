from comms.vision.vision import Vision
from world.world import World
import threading
from constants import *
from ai.robot import Robot
from sysmic_kit import *
import time
from comms.sender.grsim import Grsim
import math
from ui.ui import UI

# Initialize world
world : World = World(1,1)
vision : Vision = Vision(VISION_IP, VISION_PORT, world)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()

# Wait to open the simulator
time.sleep(1)
# Game loop
robot : Robot = Robot(0, TeamColor.BLUE, world)

grsim = Grsim()
ui : UI = UI(world)

def generate_circular_path():
    points = []
    center = Vector2(0,0)
    n_points = 8
    for i in range(0,n_points):
        theta = 2*(math.pi/n_points)*i
        point = center + Vector2(0,1.5).rotate(theta)
        points.append(point)
    return points

path = generate_circular_path()
path.append(path[0] )
path = [Vector2(0,0)]#, Vector2(2,2.5), Vector2(2.5,-2) ]
while True:
    data = robot.get_data()
    finish = robot.testing_follow_path(path)
    if finish:
        break
    if not ui.loop():
        break

print("Finish")

