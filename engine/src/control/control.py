from sysmic_kit import *
import time

# Moves the robot throught set of points
class Control:
    # Control the robot to follow the desired list of points
    def __init__(self, id : int, team : TeamColor):
        self.id = id
        self.team = team

        #Utility
        self.last_time = time.time()
        self.active = True
        self.frequency = 1/60

    def control(self) -> bool:
        """This function is planned to be used in a loop > 60Hz"""
        # Run each FRAME_RATE [s]
        if not self.active:
            return True
        current_time = time.time()

        delta = current_time - self.last_time
        if delta < self.frequency:
            return False
        self.last_time = current_time