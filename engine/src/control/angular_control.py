from control.control import Control
from sysmic_kit import *
from comms.sender.robot_coms import RobotComms
from control.PID import PID


class AngularControl(Control):

    def __init__(self, id, team, angle):
        super().__init__(id, team)
        self.to_angle = angle
        self.PID = PID(1,0.5, angle)

    def control(self, current_angle : float):
        super().control()
        

        vel : float = self.PID.compute(current_angle)
        RobotComms().send_robot_data(self.id, self.team, velangular=vel)
        if abs(self.to_angle - current_angle) > 0.02:
            return False
        
        return True
