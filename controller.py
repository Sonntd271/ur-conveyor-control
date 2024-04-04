from socket import *
import time
import math
import yaml
from utils import encode_with_newline

config = yaml.safe_load(open("config.yaml"))
# print(config)


class Controller:
    def __init__(self) -> None:
        # Declare addresses for connection
        self.robot_addr = (config["robot"]["ip"], config["robot"]["port"])
        self.ni_addr = (config["ni"]["ip"], config["ni"]["port"])
        print(self.robot_addr, self.ni_addr)

        # Declare default variables
        self.joint_speed = config["default"]["joint_speed"]
        self.default_x, self.default_y = config["default"]["vision_coords"]["x"], config["default"]["vision_coords"]["y"]
        print(self.joint_speed, self.default_x, self.default_y)

        # Move robot to home position
        self.robot_to_home()

    def robot_connection(self):
        # Open a socket for the robot controller
        self.robot_fd = socket(AF_INET, SOCK_STREAM)
        self.robot_fd.connect(self.robot_addr)

        # Verify robot controller connection
        if self.robot_fd.recv(4096):
            print("Successfully connected to Robot RTDE!")
        else:
            print("Failure connecting to Robot RTDE")

    def ni_connection(self):
        # Connect to NI Vision Builder as a client
        self.ni_fd = socket(AF_INET, SOCK_STREAM)
        self.ni_fd.connect(self.ni_addr) # Raises timeout error if unable to connect
        print("Successfully connected to Vision System!")
        self.v_data = ""

        return self.v_data
    
    def robot_to_home(self):
        print("Moving UR back to home position")
        default_ur_coords = config["default"]["ur_coords"]
        move_positions = [
            default_ur_coords["x"],
            default_ur_coords["y"],
            default_ur_coords["z"],
            default_ur_coords["rx"],
            default_ur_coords["ry"],
            default_ur_coords["rz"]
        ]
        # print(default_ur_coords, move_positions)

        # Send command to move UR to home position
        move_cmd = encode_with_newline(f"movel(p{move_positions})")
        self.robot_fd.send(move_cmd)
        print(f"Command sent!: {move_cmd}")
        time.sleep(1)

    def robot_move_util(self, x, y, rz):
        pass


if __name__ == "__main__":
    controller = Controller()
