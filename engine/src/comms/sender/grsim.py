from comms.sender.proto_compiled import *
import socket, math
from sysmic_kit import Vector2, TeamColor
from constants import *

class Grsim:
    def __init__(self) -> None:
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def communicate_grsim(self, id, team : TeamColor, 
                          velangular = 0, kickspeedx = 0, kickspeedz = 0,
                          vel : Vector2 = Vector2(0,0), spinner = 0,
                          wheelsspeed = False) -> None:
        
        package = grSim_Packet()
        command = grSim_Robot_Command()

        command.id = id
        command.velangular = velangular
        command.kickspeedx = kickspeedx
        command.kickspeedz = kickspeedz
        command.veltangent = vel.x
        command.velnormal = vel.y
        command.spinner = spinner
        command.wheelsspeed = wheelsspeed
        
        package.commands.robot_commands.append(command)
        package.commands.timestamp = 0
        package.commands.isteamyellow = int(team.value)
            
        data = package.SerializeToString(True)
        if data:
            self.send_socket.sendto(data, (LOCALHOST, GRSIM_COMMAND_PORT))

    # dir es con ángulo
    def communicate_pos_robot(self, id = 0, yellowteam = 0, 
                        x = 0, y = 0, dir = 0) -> None:
        dir = math.degrees(dir)
        package = grSim_Packet()
        command = grSim_RobotReplacement()

        command.id = id
        command.x = x
        command.y = y
        command.dir = dir
        command.yellowteam = yellowteam

        package.replacement.robots.append(command)
            
        data = package.SerializeToString(True)
        if data:
            self.send_socket.sendto(data, (LOCALHOST, GRSIM_COMMAND_PORT))