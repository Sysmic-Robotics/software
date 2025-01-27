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
            self.to_pos = (ball - self.robot.data.position).normalize()*1 + ball
            self.new_pos = False
        ball : Vector2 = self.world.get_ball_pos()
        dir = (ball - self.robot.data.position).normalize()
        pos = ball + dir*(0.18/2)
        
        self.robot.spinner(10)
        self.robot.move_to(pos)
    
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
            if self.robot.get_data().position.distance_to( self.world.ball.position) > 0.18:
                return self.states["approach"]
        
        elif state_name == "approach":
            if self.robot.get_data().position.distance_to( self.world.ball.position) <= 0.18:
                return self.states["aim_ball"]
        
        elif state_name == "aim_ball":
            if self.robot.get_data().position.distance_to( self.world.ball.position) > 0.18:
                return self.states["approach"]
            elif TransitionUtils.is_facing_point(self.robot, self.world.ball.position) and \
                abs(self.robot.data.angular_velocity) <= 0.01:
                return self.states["touch_ball"]
        
        elif state_name == "touch_ball":
            if self.robot.get_data().position.distance_to( self.world.ball.position) >= 0.36:
                return self.states["approach"]
            elif self.robot.get_data().position.distance_to( self.world.ball.position) <= (0.18/2 + 0.025):
                return self.states["dribble"]
        
        elif state_name == "dribble":
            if (self.robot.get_data().position.distance_to( self.world.ball.position) >= 0.36):
                return self.states["approach"]
            elif not TransitionUtils.is_facing_point(self.robot, self.world.ball.position):
                return self.states["approach"]
            elif TransitionUtils.is_facing_point(self.robot, Vector2(0,0)) and  \
            TransitionUtils.is_facing_point(self.robot, self.world.ball.position) and \
            abs(self.robot.data.angular_velocity) <= 0.01:
                return self.states["kick"]

        elif state_name == "kick":
            if (self.robot.get_data().position.distance_to( self.world.ball.position) >= 0.18/2 + 0.025):
                return self.states["approach"]
        
        return None 