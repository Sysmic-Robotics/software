from sysmic_kit import *
from control.bangbang_control import LinearControl
from world.world import World
from ai.task import TaskState

class Robot:
    def __init__(self, id : int, team : TeamColor, world : World):
        self.id = id
        self.team = team
        self.world = world
        self.data : RobotData = self.world.get_robot(id, team)
        self.control : LinearControl = LinearControl(id, team)
        self.in_task = False
    
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
        pass


    def rotate(self, angle : float) -> bool:
        pass