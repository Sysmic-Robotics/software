from control.bangbang.trajectory_generator import TrajectoryGenerator
from control.bangbang.utils import Constraints
from comms.sender.robot_coms import RobotComms
from sysmic_kit import *
from constants import *
import time
import numpy as np

# Moves the robot throught set of points
class LinearControl:
    # Control the robot to follow the desired list of points
    def __init__(self, id : int, team : TeamColor):
        self.robot_id = id
        self.team = team

        # Communications
        self.comms  : RobotComms = RobotComms()

        # Current goal
        self.goal : Vector2 = Vector2(10000,10000)

        #Kinematic model a_max and v_max
        self.constraints = Constraints(12.65, 5)

        #Utility
        self.last_time = time.time()
        self.current_trajectory : list[Vector2] = []
        self.last_vel = Vector2(0,0)

    def set_path(self, path : list[Vector2], data : RobotData):
        self.path = path
        self.last_vel = data.velocity
        if len(self.path) > 0:
            self.goal = path.pop(0)
          

    def follow_path(self, data : RobotData) -> bool:
        """This function is planned to be used in a loop > 60Hz"""
        # Run each FRAME_RATE [s]
        current_time = time.time()
        delta = current_time - self.last_time
        if delta < FRAME_RATE:
            return False
        self.last_time = current_time
        
        if self.last_vel.distance_to(data.velocity) > 0.3:
            print("updating vel")
            self.last_vel = data.velocity
        
        self.current_trajectory = TrajectoryGenerator(self.constraints).get_trajectory(
                self.last_vel, data.position, self.goal)
        if len(self.current_trajectory) > 2:
            self.current_trajectory.pop(0)

        # Follow the current trajectory
        if len(self.current_trajectory) != 0:
            global_vel : Vector2 = self.current_trajectory.pop(0)
            self.last_vel = global_vel
            local_vel : Vector2 = global_vel.rotate(-data.orientation)
            self.comms.send_robot_data(self.robot_id, self.team, vel=local_vel)
            return False

        # Is near to the point and is not the last point
        if len(self.path) >= 1 and self.is_near_to_break(data, self.goal):
            # Then go to next point
            self.goal = self.path.pop(0)
            return False
        elif len(self.path) >= 1 and data.position.distance_to(self.goal) < 0.05:
            self.goal = self.path.pop(0)
            return False
        return True

    def is_near_to_break(self, robot : RobotData, point : Vector2) -> bool:
        v = robot.velocity
        pos = robot.position
        dx_to_brake = ( (v.x**2)/(2*self.constraints.a_max) ) 
        dy_to_brake = ( (v.y**2)/(2*self.constraints.a_max) )
        if (dx_to_brake >= abs(pos.x - point.x) or
            dy_to_brake >= abs(pos.y - point.y) ):
                return True
        return False