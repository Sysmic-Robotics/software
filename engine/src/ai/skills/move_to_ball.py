from sysmic_kit import *
from ai.robot import Robot
from world.world import World

class Stop(State):
    pass

class ApproachBall(State):
    def __init__(self, name, robot : Robot):
        super().__init__(name)
        self.world = World()
        self.robot = robot
        
    def loop(self):
        # Get ball position
        ball : Vector2 = self.world.get_ball_pos()
        self.robot.move_to(ball)


class MoveToBall(FiniteStateMachine):
    def __init__(self, robot : Robot):
        super().__init__()
        
        self.states["stop"] = Stop("stop")
        self.states["approach"] = ApproachBall("approach", robot)
        
        self.state = self.states["approach"]
        self.robot = robot
        self.world = World()
        self.debug = True
        
    def get_transition(self, state_name):
        if state_name == "stop":
            if self.robot.get_data().position.distance_to( self.world.ball.position) > 0.18:
                return self.states["approach"]
        elif state_name == "approach":
            if self.robot.get_data().position.distance_to( self.world.ball.position) < 0.18:
                return self.states["stop"]
        return None 