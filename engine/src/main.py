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
import queue

# Initialize world
world : World = World(1,1)

vision_buffer = queue.Queue(5)
vision : Vision = Vision(VISION_IP, VISION_PORT, vision_buffer)
vision_t = threading.Thread(target=vision.loop)
vision_t.start()

radio : RobotComms = RobotComms()


#ui : UI = UI(world, vision)
# Game loop
robot : Robot = Robot(0, TeamColor.BLUE)
kick_the_ball = KickTheBall(robot)


start_time = time.time()
delta = 0
while True:
    current_time = time.time()
    delta += current_time - start_time
    start_time = current_time
    if True:#delta > 0.016:
        try:
            # Attempt to get an update from the queue without waiting
            data = vision_buffer.get(timeout= FRAME_RATE/2) # Non-blocking check
            world.update_world(data)  # Update the world state
        except queue.Empty:
            pass

        kick_the_ball.loop()
 
        radio.send_packets()
        delta -= 0.016

    #fps_counter.update()
