from comms.vision.proto_compiled import *
import socket, threading, time
from constants import *
from world.world import World
from sysmic_kit import *

ListPackets = list[SSL_WrapperPacket]

class Vision:
    """ Deserializa packetes de vision """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, multi_cast_address, port_ssl, world : World):
        self.world = world
        self.ball: SSL_DetectionBall = SSL_DetectionBall()

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind(('', port_ssl))

        # Join the multicast group
        mreq = socket.inet_aton(multi_cast_address) + socket.inet_aton('0.0.0.0')
        # ERROR: NO SUCH DEVICE CUANDO EL PC NO ESTA CONECTADO A INTERNET
        self.udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # For debug purposes
        self.last_packet_time = time.time()

        self.last_frame = -1

    def loop(self):
        while True:
            self._receive_vision_packets()
            time.sleep(FRAME_RATE)

    def _receive_vision_packets(self):
        packets: ListPackets = []  # List of SSL_WrapperPackets
        current_time = time.time()

        try:
            while True:
                # Set a timeout so we don't block indefinitely if there's no data
                self.udp_socket.settimeout(0.001)
                
                # Receive data
                data, _ = self.udp_socket.recvfrom(4096)  # Buffer size of 4096 bytes
                packet = SSL_WrapperPacket()

                if not packet.ParseFromString(data):
                    print('Error in _receive_vision_packets: cannot parse packet')
                else:
                    packets.append(packet)
        except socket.timeout:
            # Expected to timeout when there are no more packets
            pass
        if DEBUG:
            time_difference = (current_time - self.last_packet_time)
            print(f"\rTime between packets: {time_difference:.4f} [s]", end="")
        if packets:
            self.last_packet_time = current_time
            #print(len(packets))
            self._update(packets)

    def _update(self, packets: ListPackets):
        robots_blue : dict[int, SSL_DetectionRobot] = {}
        robots_yellow  : dict[int, SSL_DetectionRobot]= {}
        for packet in packets:
            det = packet.detection # paquete con detección desreferenciado
            # Update ball
            for ball in det.balls:
                if ball.confidence >= self.ball.confidence:
                    self.ball = ball
            # Update robots
            for robot_data in det.robots_blue:
                robots_blue[robot_data.robot_id] = robot_data
            for robot_data in det.robots_yellow:
                robots_yellow[robot_data.robot_id] = robot_data
        self._update_world(robots_blue.values(), robots_yellow.values(), self.ball)
    

    def _update_world(self, blue : list[SSL_DetectionRobot], yellow : list[SSL_DetectionRobot], ball : SSL_DetectionBall):
        for robot in blue:
            data = RobotData(robot.robot_id, TeamColor.BLUE)
            data.position = Vector2(robot.x/1000,robot.y/1000)
            data.orientation = robot.orientation
            data.last_time_update = time.time()
            self.world._vision_robot_update(data)
        for robot in yellow:
            data = RobotData(robot.robot_id, TeamColor.YELLOW)
            data.position = Vector2(robot.x/1000,robot.y/1000)
            data.orientation = robot.orientation
            data.last_time_update = time.time()
            self.world._vision_robot_update(data)
        
        self.world._vision_ball_update( Vector2(ball.x/1000, ball.y/1000) )