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
        pos = (self.robot.data.position - ball).normalize()*0.18 + ball
        self.robot.move_to(pos)

class AimBall(State):
    def __init__(self, name, robot : Robot):
        super().__init__(name)
        self.world = World()
        self.robot = robot
        
    def loop(self):
        # Get ball position
        ball : Vector2 = self.world.get_ball_pos()
        self.robot.face_to(ball)


class KickTheBall(FiniteStateMachine):
    def __init__(self, robot : Robot):
        super().__init__()
        # Define states
        self.states["stop"] = Stop("stop")
        self.states["approach"] = ApproachBall("approach", robot)
        self.states["aim_ball"] = AimBall("aim_ball", robot)
        
        # Set initial states
        self.state = self.states["approach"]
        self.robot = robot
        self.world = World()
        self.debug = True
        
    def get_transition(self, state_name):
        if state_name == "stop":
            if self.robot.get_data().position.distance_to( self.world.ball.position) > 0.18:
                return self.states["approach"]
        elif state_name == "approach":
            if self.robot.get_data().position.distance_to( self.world.ball.position) <= 0.18:
                return self.states["aim_ball"]
        elif state_name == "aim_ball":
            if self.robot.get_data().position.distance_to( self.world.ball.position) > 0.36:
                return self.states["approach"]
        return None 