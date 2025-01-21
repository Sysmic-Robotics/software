from sysmic_kit import *
from ai.robot import Robot
class StopState(State):
    pass

class ApproachBall(State):
    def loop(self, delta):
        # Get ball position
        # Get robot position
        # Move robot to ball position
        pass

class MoveToBall(FiniteStateMachine):
    def __init__(self, robot : Robot):
        super().__init__()
        
        self.states_id[0] = StopState("stop_state", 0)
        self.states_id[1] = ApproachBall("approach", 1)
        
        self.state = self.states_id[0]
        self.robot = robot
        
    def get_transition(self, state_name):
        if state_name == "stop_state":
            #if self.robot.get_data().position > 
            pass
        