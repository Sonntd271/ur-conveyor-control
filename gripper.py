from socket import *
import time
import math

ROBOT_ADDR = ("10.0.0.14", 30003) # (IP, Port)
GRIPPER_PORT = 63352
NI_ADDR = ("10.10.1.10", 2024) # (IP, Port)

JOINT_SPEED = 0.1
VISION_DEFAULT_COORDS = (0, 0) # (x_pos, y_pos)


class Gripper:
    def __init__(self) -> None:
        # Declare addresses for connection
        self.robot_addr = ROBOT_ADDR
        self.gripper_addr = (self.robot_addr[0], GRIPPER_PORT)
        self.ni_addr = NI_ADDR

        # Declare default variables
        self.joint_speed = JOINT_SPEED
        self.default_x, self.default_y = VISION_DEFAULT_COORDS

    def robot_connection(self):
        # Open a socket for the robot controller
        self.robot_fd = socket(AF_INET, SOCK_STREAM)
        self.robot_fd.connect(self.robot_addr)

        # Verify robot controller connection
        if self.robot_fd.recv(4096):
            print("Successfully connected to Robot RTDE!")
        else:
            print("Failure connecting to Robot RTDE")

    def gripper_connection(self):
        # Open a socket for controlling the gripper
        self.gripper_fd = socket(AF_INET, SOCK_STREAM)
        self.gripper_fd.connect(self.gripper_addr)

        # Verify gripper connection
        self.gripper_fd.sendall("GET POS\n".encode())
        if str(self.gripper_fd.recv(10), "UTF-8"):
            self.gripper_fd.send("SET ACT 1\n".encode())
            print(str(self.gripper_fd.recv(10), "UTF-8"))
            time.sleep(3)
            gripper_commands = [
                "SET GTO 1\n",
                "SET SPE 255\n",
                "SET FOR 255\n"
            ]
            for cmd in gripper_commands:
                self.gripper_fd.send(cmd.encode())
            print("Gripper activated")
