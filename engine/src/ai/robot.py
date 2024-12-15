from sysmic_kit import *
from control.bangbang_control import LinearControl
from world.world import World
from ai.task import TaskState
from control.angular_control import AngularControl
import math

class Robot:
    def __init__(self, id : int, team : TeamColor, world : World):
        self.id = id
        self.team = team
        self.world = world
        self.data : RobotData = self.world.get_robot(id, team)
        self.control : LinearControl = LinearControl(id, team)
        self.in_task = False
        self.angular_control = None
    
    def get_data(self) -> RobotData:
        self._update_data()
        return self.data

    def _update_data(self):
        self.data : RobotData = self.world.get_robot(self.id, self.team)
    
    def testing_follow_path(self, path : list[Vector2]):
        """ Follow path for testing """
        self._update_data()
        """ This function is planned to be used in a loop > FRAME_RATE """
        if not self.in_task:
            # Creathe new task
            self.control.set_path(path, self.data)
            self.in_task = True
        result = self.control.follow_path(self.data)
        # Task finished
        if result:
            self.in_task = False
            return True
        return False

    def move_to(self, point : Vector2):
        """ Go to point avoiding any obstacle """
        self._update_data()
        """ This function is planned to be used in a loop > FRAME_RATE """
        if not self.in_task:
            # Creathe new task
            path = [self.data.position, point]
            self.control.set_path(path, self.data)
            self.in_task = True
        result = self.control.follow_path(self.data)
        # Task finished
        if result:
            self.in_task = False
            return True
        return False


    def face_to(self, point : Vector2) -> bool:
        data = self.get_data()
        if not self.in_task:
            # Creathe new task
            angle_rads = (point - data.position).angle_with_x_axis()
            if angle_rads < 0:
                angle_rads += math.pi*2
            angle_rads = angle_rads%( math.pi*2 )
            self.angular_control = AngularControl(self.id, self.team, data, angle_rads)
            self.in_task = True
        result = self.angular_control.control(data)
        # Task finished
        if result:
            self.in_task = False
            return True
        return False
        

    def rotate_to(self, angle_rads : float) -> bool:
        data = self.get_data()
        if not self.in_task:
            # Creathe new task
            angle_rads = angle_rads%( math.pi*2 )
            self.angular_control = AngularControl(self.id, self.team, data, angle_rads)
            self.in_task = True
        result = self.angular_control.control(data)
        # Task finished
        if result:
            self.in_task = False
            return True
        return False