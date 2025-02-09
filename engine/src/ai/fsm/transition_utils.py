from sysmic_kit.geometry import Vector2
from ai.robot import Robot
from world.world import World


class TransitionUtils:

    @staticmethod
    def is_facing_point(robot : Robot, pos : Vector2, error = 0.02) -> bool:
        robot_pos : Vector2 = robot.state.position
        dir_to_point : Vector2 = (pos - robot_pos).normalize()
        robot_dir : Vector2 = Vector2(1,0).rotate(robot.state.orientation)
        if (dir_to_point).dot(robot_dir) >= 1 - error:
            return True
        return False