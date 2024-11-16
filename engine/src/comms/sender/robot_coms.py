# Interfaz de la radio para comunicarse con sim y cancha. 
#Esto es para evitar la divergencia entre codigo simulador y cancha
from comms.sender.grsim import Grsim
from constants import *
import threading
from sysmic_kit import Vector2, TeamColor

class RobotComms:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if COMMUNICATION_MODE == 1:
            self.grsim = Grsim()

    def send_robot_data(self, id, team : TeamColor, 
                          velangular = 0, kickspeedx = 0, kickspeedz = 0,
                          vel : Vector2 = Vector2(0,0), spinner = 0,
                          wheelsspeed = False) -> None:
        if COMMUNICATION_MODE == 1:
            self.grsim.communicate_grsim(id, team, velangular= velangular, 
                                         kickspeedx=kickspeedx, kickspeedz=kickspeedz, vel=vel,
                                         spinner= spinner,
                                         wheelsspeed=wheelsspeed)     
            
            
            
    
