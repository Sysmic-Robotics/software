from sysmic_kit.geometry import Vector2
from enum import Enum


class TeamColor(Enum):
    BLUE = 0
    YELLOW = 1

class BallData:
    '''Clase que representa un balon, con sus atributos de posicion y confianza'''
    def __init__(self):
        self.position : Vector2 = Vector2(0,0)

class RobotData:
    '''Clase que representa un robot, con sus atributos de posicion y confianza'''
    def __init__(self, id : int, team : TeamColor):
        self.id = id
        self.team : TeamColor = team
        
        self.orientation = .0 # Radians
        self.position : Vector2 = Vector2(0,0) # Position m, m
        self.velocity : Vector2 = Vector2(0,0) # m/s

        self.is_active = True
        self.last_time_update = 0 # in seconds