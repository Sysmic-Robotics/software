from comms.vision.vision import Vision
from world.world import World
import threading
from constants import *
from ai.robot import Robot
from comms.sender.robot_coms import RobotComms
from sysmic_kit import *
import time
from ui.ui import UI
import math
from ai.skills.kick_the_ball import KickTheBall

# Initialize world
world : World = World(1,1)
vision : Vision = Vision(VISION_IP, VISION_PORT, world)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()

radio : RobotComms = RobotComms()
radio_t = threading.Thread(target=radio.loop)
radio_t.start()

robot : Robot = Robot(0, TeamColor.BLUE)
ui : UI = UI(world, vision)
# Game loop
time_t = time.time()
time.sleep(1)

kick_the_ball = KickTheBall(robot)

class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        # Update and print FPS every second
        if elapsed_time >= 1.0:
            fps = self.frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            self.start_time = current_time
            self.frame_count = 0

fps_counter = FPSCounter()
while True:    
    ui.loop()
    kick_the_ball.loop()
    fps_counter.update()
