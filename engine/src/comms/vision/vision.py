from comms.vision.proto_compiled import *
import socket, threading, time
from constants import *
from sysmic_kit import *
import queue

ListPackets = list[SSL_WrapperPacket]

class Vision:
    """ Deserializa packetes de vision """

    def __init__(self, multi_cast_address, port_ssl, queue : queue):
        self.queue = queue
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
        self.time_between_packet = 0

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
        #if DEBUG:
        self.time_between_packet = (current_time - self.last_packet_time)
        #print(f"\rTime between packets: {time_difference:.4f} [s]", end="")
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
                self.ball = ball
            # Update robots
            for robot_data in det.robots_blue:
                robots_blue[robot_data.robot_id] = robot_data
            for robot_data in det.robots_yellow:
                robots_yellow[robot_data.robot_id] = robot_data
        self._update_world(robots_blue.values(), robots_yellow.values(), self.ball)
    
    def _update_world(self, blue : list[SSL_DetectionRobot], yellow : list[SSL_DetectionRobot], ball : SSL_DetectionBall):
        
        blue_data = []
        for robot in blue:
            data = RobotState(robot.robot_id, TeamColor.BLUE)
            data.position = Vector2(robot.x/1000,robot.y/1000)
            data.orientation = robot.orientation
            data.last_time_update = time.time()
            blue_data.append(data)
        
        yellow_data = []
        for robot in yellow:
            data = RobotState(robot.robot_id, TeamColor.YELLOW)
            data.position = Vector2(robot.x/1000,robot.y/1000)
            data.orientation = robot.orientation
            data.last_time_update = time.time()
            yellow_data.append(data)

        ball_data = BallData()
        ball_data.position = Vector2(ball.x/1000, ball.y/1000)
        ball_data.last_time_update = time.time()
        
        all_data = (blue_data, yellow_data, ball_data)
        self.queue.put(all_data)