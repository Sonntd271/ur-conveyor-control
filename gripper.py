from socket import *
import time
import math
import yaml
from utils import encode_with_newline

config = yaml.safe_load(open("config.yaml"))
# print(config)


class Gripper:
    def __init__(self) -> None:
        # Declare the gripper address
        self.gripper_addr = (config["gripper"]["ip"], config["gripper"]["port"])
        # print(self.gripper_addr)

        # Declare default variables
        self.joint_speed = config["default"]["joint_speed"]
        self.default_x, self.default_y = config["default"]["vision_coords"]["x"], config["default"]["vision_coords"]["y"]
        # print(self.joint_speed, self.default_x, self.default_y)

    def gripper_connection(self):
        # Open a socket for controlling the gripper
        self.gripper_fd = socket(AF_INET, SOCK_STREAM)
        self.gripper_fd.connect(self.gripper_addr)

        # Verify gripper connection
        self.gripper_fd.sendall(encode_with_newline("GET POS"))
        if str(self.gripper_fd.recv(10), "UTF-8"):
            self.gripper_fd.send(encode_with_newline("SET ACT 1"))
            print(str(self.gripper_fd.recv(10), "UTF-8"))
            time.sleep(3)
            
            gripper_commands = [
                "SET GTO 1",
                "SET SPE 255",
                "SET FOR 255"
            ]
            for cmd in gripper_commands:
                self.gripper_fd.send(encode_with_newline(cmd))
            print("Gripper activated")

    def grip_control(self, value):
        # Release value = 0, Grab value = 255
        if value == 0 or value == 255:
            self.gripper_fd.send(encode_with_newline(f"SET POS {value}"))
        time.sleep(1)
        _ = str(self.gripper_fd.recv(10), "UTF-8")
        self.gripper_fd.send(encode_with_newline("GET POS"))
        
        recv_buf = str(self.gripper_fd.recv(10), "UTF-8")
        print(f"Gripper position = {recv_buf}")


if __name__ == "__main__":
    gripper = Gripper()
