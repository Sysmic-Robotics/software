from control.trajectory_2d import Trajectory2D
from comms.sender.robot_coms import RobotComms
from sysmic_kit import *
from constants import *
import time
import math

# Moves the robot throught set of points
class LinearControlPID:
    # Control the robot to follow the desired list of points
    def __init__(self, id : int, team : TeamColor, state : RobotState, kp : float, ki : float, kd : float):
        self.robot_id = id
        self.team = team
        self.state = state
        # Current goal
        self.goal : Vector2 = Vector2(10000,10000)


        self.kp = kp
        self.ki = ki
        self.kd = kd

        #Utility
        self.last_time = time.time()
        self.last_state : RobotState = state
        self.error_last : RobotState = state.position - state.position

    def set_path(self, path : list[Vector2], state : RobotState):
        self.active = True
        self.path = path
        if len(self.path) == 0:
            self.active = False
            return
        self.goal = path.pop(0)
    
    def compute(self, state : RobotState , pointSp : Vector2) -> Vector2:
        
        error = pointSp - self.state.position
        error_module = error.module()
        if error_module < 0.05:
            return Vector2(0,0)
        error_angle = error.angle_with_x_axis()

        deltaT=5
        error_dif = (error_module - self.error_last.module())/deltaT
        error_acum = (error_module + self.error_last.module())*deltaT



        vel_modulus = self.kp * error_module + self.ki * error_acum + self.kd * error_dif

        vel = error.normalize() * vel_modulus*10

        self.error_last = error
        self.last_state = state

        #rotation
        vel = vel.rotate(-state.orientation)
        vel.x = -vel.x
        print(vel)
        return vel