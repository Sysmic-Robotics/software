from sysmic_kit import *
from ai.robot import Robot
from world.world import World
from ai.fsm.fsm import FiniteStateMachine, State
from ai.fsm.transition_utils import TransitionUtils
import math

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
        pos = (self.robot.state.position - ball).normalize()*0.18 + ball
        self.robot.move_to2(pos)
        self.robot.face_to(ball)


class AimBall(State):
    def __init__(self, name, robot : Robot):
        super().__init__(name)
        self.world = World()
        self.robot = robot
        
    def loop(self):
        # Get ball position
        ball : Vector2 = self.world.get_ball_pos()
        self.robot.face_to(ball)


class Dribble(State):
    def __init__(self, name, robot : Robot):
        super().__init__(name)
        self.world = World()
        self.robot = robot
        
        self.new_pos = True
        
    def loop(self):
        # Get ball position
        self.robot.spinner(10)
        # If ball is not detected then pass to next state
        self.robot.face_to(Vector2(0,0))


class TouchBall(State):
    def __init__(self, name, robot : Robot):
        super().__init__(name)
        self.world = World()
        self.robot = robot
        
        self.new_pos = True


    def loop(self):
        # Get ball position
        if self.new_pos:
            ball : Vector2 = self.world.get_ball_pos() 
            self.to_pos = (ball - self.robot.state.position).normalize()*1 + ball
            self.new_pos = False
        ball : Vector2 = self.world.get_ball_pos()
        dir = (ball - self.robot.state.position).normalize()
        pos = ball + dir*(0.18/3)
        
        self.robot.spinner(10)
        self.robot.move_to2(pos)

    
class Kick(State):
    def __init__(self, name, robot : Robot):
        super().__init__(name)
        self.world = World()
        self.robot = robot
    
    def loop(self):
        # Get ball position
        self.robot.spinner(0)
        self.robot.kick(2)


class KickTheBall(FiniteStateMachine):
    def __init__(self, robot : Robot):
        super().__init__()
        # Define states
        self.states["stop"] = Stop("stop")
        self.states["approach"] = ApproachBall("approach", robot)
        self.states["aim_ball"] = AimBall("aim_ball", robot)
        self.states["touch_ball"] = TouchBall("touch_ball", robot)
        self.states["dribble"] = Dribble("dribble", robot)
        self.states["kick"] = Kick("kick", robot)
        
        # Set initial states
        self.state = self.states["stop"]
        self.robot = robot
        self.world = World()
        self.debug = True
        
    def get_transition(self, state_name):
        if state_name == "stop":
            if self.robot.state.position.distance_to( self.world.ball.position) > 0.18:
                return self.states["aim_ball"]
        
        elif state_name == "approach":
            if self.robot.state.position.distance_to( self.world.ball.position) <= 0.18:
                return self.states["stop"]
            elif not TransitionUtils.is_facing_point(self.robot, self.world.ball.position, 0.20):
                return self.states["aim_ball"]
        
        elif state_name == "aim_ball":
            if TransitionUtils.is_facing_point(self.robot, self.world.ball.position) and \
                abs(self.robot.state.angular_velocity) <= 0.01:
                return self.states["approach"]

        return None 