from sysmic_kit import *
from control.bangbang_control import LinearControl
from control.linear_pid import LinearControlPID
from world.world import World
from ai.task import TaskState
from comms.sender.robot_coms import RobotComms
from control.angular_control import AngularControl
from control.angular_control_agr import AngularControlAgr
import math
import time

class Robot:
    def __init__(self, id : int, team : TeamColor):
        self.id = id
        self.team = team
        self.world = World()
        self.state : RobotState = self.world.get_robot(id, team)
        self.linear_control : LinearControl = LinearControl(id, team)
        #PID parameters x,y
        self.Kp = 20
        self.Ki = 10
        self.Kd = 0.1

        self.lineal_control_PID : LinearControlPID = LinearControlPID(id, team, self.state, self.Kp, self.Ki, self.Kd)
        
        self.in_linear_task = False
        self.task_point : Vector2 = Vector2(1000,1000)
        
        self.in_angular_task = False
        self.angular_control = None
        self.robot_comms = RobotComms()

        self.last_time = time.time()
         
    def get_data(self) -> RobotState:
        self._update_state()
        return self.state
    
    def get_position(self) -> Vector2:
        state = self.get_state()
        return state.position

    def _update_state(self):
        self.state : RobotState = self.world.get_robot(self.id, self.team)
    
    def testing_follow_path(self, path : list[Vector2]):
        """ Follow path for testing """
        self._update_state()
        """ This function is planned to be used in a loop > FRAME_RATE """
        if not self.in_linear_task:
            # Creathe new task
            self.linear_control.set_path(path, self.state)
            self.in_linear_task = True
        result = self.linear_control.follow_path(self.state)
        # Task finished
        if result:
            self.in_linear_task = False
            return True
        return False

    def move_to(self, point : Vector2):
        # TO DO: Change move_to -> loop_move_to
        """ Go to point avoiding any obstacle """
        self._update_state()
        path = [point]
        self.linear_control.set_path(path, self.state)
        result = self.linear_control.follow_path(self.state)
        # Task finished
        if result:
            return True
        return False
    
    def move_to2(self, point : Vector2):
        # TO DO: Change move_to -> loop_move_to
        """ Go to point avoiding any obstacle """
        self._update_state()
        path = [point]
        self.lineal_control_PID.set_path(path, self.state)
        vel = self.lineal_control_PID.compute(self.state,point)
        vel.x = 1*vel.x
        vel.y = 1*vel.y

        Vmax = 50
        vel.x = vel.x if vel.x < Vmax else Vmax
        vel.x = vel.x if vel.x > -Vmax else -Vmax
        vel.y = vel.y if vel.y < Vmax else Vmax
        vel.y = vel.y if vel.y > -Vmax else -Vmax

        self.robot_comms.send_robot_velocity(self.id, self.team, velocity=vel)
        # Task finished
        if vel != None:
            return True
        return False
        
    def face_to(self, point : Vector2) -> bool:
        state = self.state
            # Creathe new task
        angle_rads = (point - state.position).angle_with_x_axis()
        if angle_rads < 0:
            angle_rads += math.pi*2
        angle_rads = angle_rads%( math.pi*2 )

        self.angular_control = AngularControl(self.id, self.team, state, angle_rads)
        result = self.angular_control.control(state)
        # Task finished
        if result:
            return True
        return False
    
    def face_to_agr(self, point : Vector2) -> bool:
        state = self.state
            # Creathe new task
        angle_rads = (point - state.position).angle_with_x_axis()
        if angle_rads < 0:
            angle_rads += math.pi*2
        angle_rads = angle_rads%( math.pi*2 )

        self.angular_control = AngularControlAgr(self.id, self.team, state, angle_rads)
        result = self.angular_control.control(state)
        # Task finished
        if result:
            return True
        return False      

    def rotate_to(self, angle_rads : float) -> bool:
        state = self.state
        if not self.in_angular_task:
            # Creathe new task
            angle_rads = angle_rads%( math.pi*2 )
            self.angular_control = AngularControl(self.id, self.team, state, angle_rads)
            self.in_angular_task = True
        result = self.angular_control.control(state)
        # Task finished
        if result:
            self.in_angular_task = False
            return True
        return False
    
    def spinner(self, vel : float) -> float:
        self.robot_comms.send_robot_spinner(self.id, self.team, vel)

    def kick(self, power : int):
        self.robot_comms.send_robot_kick(self.id, self.team, power)