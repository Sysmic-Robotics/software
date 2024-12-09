from comms.vision.vision import Vision
from world.world import World
import threading
from constants import *
from ai.robot import Robot
from sysmic_kit import *
import time
from ui.ui import UI

# Initialize world
world : World = World(1,1)
vision : Vision = Vision(VISION_IP, VISION_PORT, world)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()

robot : Robot = Robot(0, TeamColor.BLUE, world)
ui : UI = UI(world)
# Game loop
time_t = time.time()
path = [Vector2(0,0), Vector2(0,2)]

while True:
    data = robot.get_data()
    finish = robot.testing_follow_path(path)
    if finish:
        break
    if not ui.loop():
        break
    
print("Finish")