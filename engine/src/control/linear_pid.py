from control.trajectory_2d import Trajectory2D
from comms.sender.robot_coms import RobotComms
from sysmic_kit import *
from constants import *
import time

# Moves the robot throught set of points
class LinearControlPID:
    # Control the robot to follow the desired list of points
    def __init__(self, id : int, team : TeamColor, state : RobotState, kp : float, ki : float, kd : float):
        self.robot_id = id
        self.team = team
        self.state = state
        # Current goal
        self.goal : Vector2 = Vector2(10000,10000)

        #Kinematic model a_max and v_max
        self.A_MAX = 2.5
        self.V_MAX = 5


        #Utility
        self.last_time = time.time()
        last_state : RobotState = None

    def set_path(self, path : list[Vector2], state : RobotState):
        self.active = True
        self.path = path
        if len(self.path) == 0:
            self.active = False
            return
        self.goal = path.pop(0)

    def follow_path(self, state : RobotState) -> bool:
        """This function is planned to be used in a loop > 60Hz"""
        # Run each FRAME_RATE [s]
        if not self.active:
            return True
        current_time = time.time()
        delta = current_time - self.last_time
        if delta < FRAME_RATE/2:
            return False
        
        self.last_time = current_time
        
        v = state.velocity
        pos = state.position
        new_traj = Trajectory2D(self.A_MAX, self.V_MAX, v, pos, self.goal)
        v : Vector2 = new_traj.get_next_velocity()
        
        local_v = v.rotate(-state.orientation)
        RobotComms().send_robot_velocity(state.id, state.team, velocity=local_v)

        # Change the point to not desaccelerate
        if len(self.path) != 0 and self.is_near_to_break(state, self.goal):
            self.goal = self.path.pop(0)
            return False
        # Finish control
        elif len(self.path) == 0 and pos.distance_to(self.goal) < 0.02:
            self.active = False
            return True
    
    def follow_point(self, state_sp : RobotState) -> Vector2:
        error = state_sp.position - self.state.position
        error_last = self.last_state.position - self.state.position
        error_dif = error - error_last
        error_acum = error + error_last

        vel = self.Kp * error + self.Ki * error_acum + self.Kd * error_dif

        error_last = error
        return vel




    def is_near_to_break(self, robot : RobotState, point : Vector2) -> bool:
        v = robot.velocity
        pos = robot.position
        dx_to_brake = ( (v.x**2)/(2*self.A_MAX) ) 
        dy_to_brake = ( (v.y**2)/(2*self.A_MAX) )
        if (dx_to_brake >= abs(pos.x - point.x) or
            dy_to_brake >= abs(pos.y - point.y) ):
                return True
        return False