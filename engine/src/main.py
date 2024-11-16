from comms.vision.vision import Vision
from world.world import World
import threading
from constants import *
from ai.robot import Robot
from sysmic_kit import *
import time
from debug_tools.robot_plot import RobotPlot

# Initialize world
world : World = World(1,1)
vision : Vision = Vision(VISION_IP, VISION_PORT, world)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()

time.sleep(1)

plot = RobotPlot()
robot : Robot = Robot(0, TeamColor.BLUE, world)

# Game loop
point = Vector2(4,0)
while True:
    data = robot.get_data()
    plot.update_plot(data)
    finish = robot.move_to(point)
    if finish:
        point = -1*point
print("FINISH ")