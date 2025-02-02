from control.control import Control
from sysmic_kit import *
from comms.sender.robot_coms import RobotComms
import math
import time


class AngularControl(Control):

    def __init__(self, id, team, data : RobotState, angle : float):
        super().__init__(id, team)
        # Normalize angle, to avoid negative angles
        angle = abs(angle)%(math.pi*2)
        robot_angle = data.orientation
        if robot_angle < 0:
            robot_angle += math.pi*2
        self.to_angle = angle
        self.PID = PID(2, 0.2, self.to_angle)
        self.robot_comms = RobotComms()
        
    def control(self, data : RobotState) -> bool:
        super().control()
        
        # Normalize angle, to avoid negative angles
        robot_angle = data.orientation
        if robot_angle < 0:
            robot_angle += math.pi*2
        
        vel : float = self.PID.compute(robot_angle)
        self.robot_comms.send_robot_angular_velocity(self.id, self.team, velocity=vel)
        if abs(self.to_angle - robot_angle) > 0.052:
            return False
        return True

class PID:
    def __init__(self, kP, kI, set_point):
        self.kP = kP
        self.kI = kI
        self.last_time = time.time()
        self.set_point = set_point
        self.i = 0

    def compute(self, measurement):
        error = self.set_point - measurement
        error = (error - math.pi) % math.pi*2 + math.pi if abs(error) > math.pi else error
        p = self.kP*error
        self.i = self.i + self.kI*error*(time.time() - self.last_time)
        self.last_time = time.time()
        PI = p + self.i
        return PI