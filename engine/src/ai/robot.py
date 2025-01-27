from sysmic_kit import *
from control.bangbang_control import LinearControl
from world.world import World
from ai.task import TaskState
from comms.sender.robot_coms import RobotComms
from control.angular_control import AngularControl
import math

class Robot:
    def __init__(self, id : int, team : TeamColor):
        self.id = id
        self.team = team
        self.world = World()
        self.data : RobotData = self.world.get_robot(id, team)
        self.linear_control : LinearControl = LinearControl(id, team)
        
        self.in_linear_task = False
        self.task_point : Vector2 = Vector2(1000,1000)
        
        self.in_angular_task = False
        self.angular_control = None
        self.robot_comms = RobotComms()
         
    def get_data(self) -> RobotData:
        self._update_data()
        return self.data
    
    def get_position(self) -> Vector2:
        data = self.get_data()
        return data.position

    def _update_data(self):
        self.data : RobotData = self.world.get_robot(self.id, self.team)
    
    def testing_follow_path(self, path : list[Vector2]):
        """ Follow path for testing """
        self._update_data()
        """ This function is planned to be used in a loop > FRAME_RATE """
        if not self.in_linear_task:
            # Creathe new task
            self.linear_control.set_path(path, self.data)
            self.in_linear_task = True
        result = self.linear_control.follow_path(self.data)
        # Task finished
        if result:
            self.in_linear_task = False
            return True
        return False

    def move_to(self, point : Vector2):
        # TO DO: Change move_to -> loop_move_to
        """ Go to point avoiding any obstacle """
        self._update_data()
        
        #if self.task_point.distance_to(point) > 0.01:
            # Creathe new task
        path = [point]
        self.linear_control.set_path(path, self.data)
        self.task_point = point
        result = self.linear_control.follow_path(self.data)
        # Task finished
        if result:
            return True
        return False
        
    def face_to(self, point : Vector2) -> bool:
        data = self.get_data()
        if not self.in_angular_task:
            # Creathe new task
            angle_rads = (point - data.position).angle_with_x_axis()
            if angle_rads < 0:
                angle_rads += math.pi*2
            angle_rads = angle_rads%( math.pi*2 )
            self.angular_control = AngularControl(self.id, self.team, data, angle_rads)
            self.in_angular_task = True
        result = self.angular_control.control(data)
        # Task finished
        if result:
            self.in_angular_task = False
            return True
        return False    

    def rotate_to(self, angle_rads : float) -> bool:
        data = self.get_data()
        if not self.in_angular_task:
            # Creathe new task
            angle_rads = angle_rads%( math.pi*2 )
            self.angular_control = AngularControl(self.id, self.team, data, angle_rads)
            self.in_angular_task = True
        result = self.angular_control.control(data)
        # Task finished
        if result:
            self.in_angular_task = False
            return True
        return False
    
    def spinner(self, vel : float) -> float:
        self.robot_comms.send_robot_spinner(self.id, self.team, vel)

    def kick(self, power : int):
        self.robot_comms.send_robot_kick(self.id, self.team, power)