# The World class is what we use to represent the state of the world at any given time.
# # In this context, the world includes the positions and orientations of all robots on the field, #
# the position and velocity of the ball, the dimensions of the field being played on, and the current 
# referee commands.
# Altogether, it's the information we have at any given time that we can use to make decisions.

from sysmic_kit import *


class World():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(World, cls).__new__(cls)
        return cls._instance

    def __init__(self, n_blues: int = 6, n_yellow: int = 6) -> None:
        """Number of blue robots, Number of yellow robots"""
        if hasattr(self, "initialized") and self.initialized:
            return  # Prevent reinitialization
        self.initialized = True  # Mark the instance as initialized
        
        self.robots_blue : dict[RobotData] = {}
        self.robots_yellow : dict[RobotData] = {}
        self.ball : BallData = BallData()
        # Create robots
        for id in range(0, n_blues):
            self.robots_blue[id] = self._create_robot(id, TeamColor.BLUE) 
        for id in range(0, n_yellow):
            self.robots_yellow[id] = self._create_robot(id, TeamColor.YELLOW)
        
        print("-- World succesfully initiated --")
        print(" Blue team size ", len(self.robots_blue.keys()))
        print(" Yellow team size ", len(self.robots_yellow.keys()))

    # Create a robot from raw data
    def _create_robot(self, id : int, team : TeamColor) -> RobotData:
        new_robot = RobotData(id, TeamColor.BLUE)
        new_robot.team = team
        return new_robot
    
    def _vision_ball_update(self, ball : Vector2):
        self.ball.position = ball

    def _vision_robot_update(self, new_data : RobotData):
        if(not self._robot_exist(new_data.id, new_data.team)):
            print(f"Trying to update robot that doenst exist id:{new_data.id} team:{new_data.team}")
            return
        robot : RobotData = self.get_robot(new_data.id, new_data.team)
        delta_t = new_data.last_time_update - robot.last_time_update
        robot.velocity = (new_data.position - robot.position)/(delta_t)
        robot.position = new_data.position
        robot.orientation = new_data.orientation
        robot.last_time_update = new_data.last_time_update
        if(robot.team == TeamColor.BLUE):
            self.robots_blue[new_data.id] = robot
        elif(robot.team == TeamColor.YELLOW):
            self.robots_yellow[new_data.id] = robot

    def _robot_exist(self, id : int, team : TeamColor) -> bool:
        if(team == TeamColor.BLUE):
            return id in self.robots_blue.keys()
        else:
            return id in self.robots_yellow.keys()

    def get_robot(self, id : int, team : TeamColor) -> RobotData:
        if( not self._robot_exist(id, team) ):
            print("ERROR: Robot doesnt exist! ")
            return None
        if(team == TeamColor.BLUE):
            return self.robots_blue[id]
        elif(team == TeamColor.YELLOW):
            return self.robots_yellow[id]
    
    def get_ball_pos(self) -> Vector2:
        return self.ball.position
    
    def get_robots_blue(self) -> list[RobotData]:
        return self.robots_blue.values()