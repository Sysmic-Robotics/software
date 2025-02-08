# Interfaz de la radio para comunicarse con sim y cancha. 
# Esto es para evitar la divergencia entre codigo simulador y cancha
from comms.sender.grsim import Grsim
from constants import *
import threading
from sysmic_kit import Vector2, TeamColor
from comms.sender.radio_2 import Radio

class RobotComms:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, n_blues : int = 0, n_yellows : int = 0) -> None:
        if hasattr(self, "initialized") and self.initialized:
            return  # Prevent reinitialization
        self.initialized = True  # Mark the instance as initialized
        
        if COMMUNICATION_MODE == 1:
            self.grsim = Grsim()
        else:
            self.radio = Radio()
        # The dictionary key is ID-Team'
        # Example: 01-0
        self.robot_packets = {}
        
    def send_packets(self):
        if COMMUNICATION_MODE == 1:
            for robot_id in self.robot_packets.keys():
                    packet = self.robot_packets[robot_id]
                    if packet["has_data"] == True:
                        self.grsim.communicate_grsim(id= packet['id'], 
                                                    team= packet['team'], 
                                                    velangular= packet['angular'], 
                                                    kickspeedx= packet['kick_x'], 
                                                    kickspeedz= packet['kick_z'], 
                                                    vel= packet['velocity'],
                                                    spinner= packet['spinner'],
                                                    wheelsspeed= packet['wheelsspeed'])
                        # Reset packet to default
                        self.robot_packets[robot_id]["has_data"] = self.create_packet(packet['id'],
                                                                                    packet['team'])
        else:
            packets = []
            
            for robot_id in self.robot_packets.keys():
                packet = self.robot_packets[robot_id]
                if packet["has_data"] == True:
                    self.radio.add_to_robot_queue(robot_id=packet['id'], drb=packet['spinner'], 
                                                  kick=packet['kick_x'], cb=0, x=int(packet['velocity'].x*-200), 
                                                  y=int(packet['velocity'].y*100), r= int(packet['angular']*4 ) )
                    self.robot_packets[robot_id]["has_data"] = self.create_packet(packet['id'],
                                                                                  packet['team'])
            self.radio.send_data()
                    

    def send_robot_velocity(self, id : int, team : TeamColor, velocity : Vector2):
        robot_id = str(id) + '-' + str(team.value)
        if not(robot_id in self.robot_packets.keys()):
            self.create_packet(id, team)
        self.robot_packets[robot_id]["has_data"] = True
        self.robot_packets[robot_id]["velocity"] = velocity
        
    def send_robot_angular_velocity(self, id : int, team : TeamColor, velocity : float):
        robot_id = str(id) + '-' + str(team.value)
        if not(robot_id in self.robot_packets.keys()):
            self.create_packet(id, team)
        self.robot_packets[robot_id]["has_data"] = True
        self.robot_packets[robot_id]["angular"] = velocity    
    
    def create_packet(self, id : int, team : TeamColor):
        robot_id = str(id) + '-' + str(team.value)
        self.robot_packets[robot_id] = {}
        self.robot_packets[robot_id]['has_data'] = False
        self.robot_packets[robot_id]['id'] = id
        self.robot_packets[robot_id]['team'] = team
        self.robot_packets[robot_id]['angular'] = 0
        self.robot_packets[robot_id]['kick_x'] = 0
        self.robot_packets[robot_id]['kick_z'] = 0
        self.robot_packets[robot_id]['velocity'] = Vector2(0,0)
        self.robot_packets[robot_id]['spinner'] = 0
        self.robot_packets[robot_id]['wheelsspeed'] = False


    def send_robot_data(self, id : int, team : TeamColor, 
                          velangular = 0, kickspeedx = 0, kickspeedz = 0,
                          vel : Vector2 = Vector2(0,0), spinner = 0,
                          wheelsspeed = False) -> None:
        #print("Deprecated")
        print(1/0)
        pass
    
    def send_robot_spinner(self, id : int, team : TeamColor, spinner : float):
        robot_id = str(id) + '-' + str(team.value)
        if not(robot_id in self.robot_packets.keys()):
            self.create_packet(id, team)
        self.robot_packets[robot_id]["has_data"] = True
        self.robot_packets[robot_id]["spinner"] = spinner
    
    def send_robot_kick(self, id : int, team : TeamColor, kick : int):
        robot_id = str(id) + '-' + str(team.value)
        if not(robot_id in self.robot_packets.keys()):
            self.create_packet(id, team)
        self.robot_packets[robot_id]["has_data"] = True
        self.robot_packets[robot_id]["kick_x"] = kick
            
    
