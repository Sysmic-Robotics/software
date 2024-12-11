from sysmic_kit import Vector2
import math
from control.trajectory_1d import Trajectory1D

class Trajectory2D:
    def __init__(self, a_max, v_max, v0 : Vector2, from_point : Vector2, to_point : Vector2):
        self.trajectory = {"traj_x":None, "traj_y":None}
        # Sync DOFS using bisection method
        min_alpha = 0
        max_alpha = math.pi/2
        epsilon = 0.05
        wfx =  to_point.x - from_point.x 
        wfy = to_point.y - from_point.y
        for i in range(0, 20):
            mid_alpha = (min_alpha + max_alpha)/2
            traj_x = Trajectory1D(a_max*math.cos(mid_alpha), 
                                  v_max*math.cos(mid_alpha), 
                                  v0.x, wfx)
            traj_y = Trajectory1D(a_max*math.sin(mid_alpha), 
                                  v_max*math.sin(mid_alpha), 
                                  v0.y, wfy)
            
            if traj_x.tf() == 0.0 or traj_y.tf() == 0.0:
                self.trajectory["traj_x"] = traj_x
                self.trajectory["traj_y"] = traj_y
                break

            if abs(traj_x.tf() - traj_y.tf()) < epsilon:
                # Keep the solutions and stop the search
                self.trajectory["traj_x"] = traj_x
                self.trajectory["traj_y"] = traj_y
                break

            if traj_x.tf() > traj_y.tf():
                max_alpha = mid_alpha
            else:   
                min_alpha = mid_alpha


    def get_next_velocity(self) -> Vector2:
        if self.trajectory["traj_x"] == None and self.trajectory["traj_y"] == None:
            return Vector2(0,0)
        x_sol = Vector2.from_tuple(self.trajectory["traj_x"].get_solution())
        y_sol = Vector2.from_tuple(self.trajectory["traj_y"].get_solution())
        velocity = Vector2(x_sol.y, y_sol.y)
        return velocity