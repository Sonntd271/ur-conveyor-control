from socket import *
import time
import yaml
from utils import encode_with_newline, prettify_decorator, extract_coords

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
        # print(self.joint_speed, self.default_x, self.default_y)

        # Connect with the robot and vision system(Edit config.yaml to change address)
        self.robot_connection()
        self.ni_connection()

        # Move robot to home position
        self.robot_to_home()

    @prettify_decorator
    def robot_connection(self):
        '''
        Connect to UR controller
        '''
        # Open a socket for the robot controller
        self.robot_fd = socket(AF_INET, SOCK_STREAM)
        self.robot_fd.connect(self.robot_addr)

        # Verify robot controller connection
        if self.robot_fd.recv(4096):
            print("Successfully connected to Robot RTDE!")
        else:
            print("Failure connecting to Robot RTDE")
    
    @prettify_decorator
    def robot_to_home(self):
        '''
        Move the UR arm to home position, can be configured on config.yaml
        '''
        print("Moving UR back to home position")
        default_ur_coords = config["default"]["ur_coords"]
        self.current_position = [
            default_ur_coords["x"],
            default_ur_coords["y"],
            default_ur_coords["z"],
            default_ur_coords["rx"],
            default_ur_coords["ry"],
            default_ur_coords["rz"]
        ]
        # print(default_ur_coords, move_positions)

        # Send command to move UR to home position
        move_cmd = encode_with_newline(f"movel(p{self.current_position},0.5,0.5,0,0)")
        self.robot_fd.send(move_cmd)
        print(f"Command sent!: {move_cmd}")
        time.sleep(1)

    @prettify_decorator
    def robot_move_util(self, x=0, y=0, z=0, rx=0, ry=0, rz=0, mode="man"):
        '''
        Used for moving the UR arm. There are two modes of movement: "man" and "rel".
        "man" tracks by using recorded position, whereas "rel" works by dynamically 
        computing with the current pose.
        '''
        print(f"Moving UR to (x, y, z, rx, ry, rz): ({x}, {y}, {z}, {rx}, {ry}, {rz})")
        gripper_to_cam = config["default"]["gripper_to_cam"] / 100

        speed_offset = config["default"]["speed_offset"] / 100
        # Change (x, y, z) from cm to m
        x /= 100
        y /= 100
        z /= 100

        if mode == "man":
            default_ur_coords = config["default"]["ur_coords"]
            print("Moving manually... NOTE: RELATIVE TO HOME POSITION")
            self.current_position[0] = default_ur_coords["x"] + gripper_to_cam - speed_offset + y
            self.current_position[1] = default_ur_coords["y"] - x
            self.current_position[2] = z
            # self.current_position[3] += rx
            # self.current_position[4] += ry
            # self.current_position[5] += rz
        elif mode == "rel":
            print("Moving relatively...")
        else:
            print("Invalid mode, skipping...")

        # Send command to move UR arm to the desired position
        move_cmd = encode_with_newline(f"movel(p{self.current_position},0.5,0.5,0,0)")
        self.robot_fd.send(move_cmd)
        print(f"Command sent!: {move_cmd}")
        time.sleep(1)

    @prettify_decorator
    def ni_connection(self):
        '''
        Connect to NI Vision Builder as a client
        '''
        self.ni_fd = socket(AF_INET, SOCK_STREAM)
        self.ni_fd.connect(self.ni_addr) # Raises timeout error if unable to connect
        print("Successfully connected to Vision System!")

    @prettify_decorator
    def ni_get_coords(self):
        '''
        Receive coordinates from NI Vision Builder
        '''
        while True:
            # Receive data from vision system
            print("Sending start signal to CV system...")
            self.ni_fd.send(b'start!')
            vision_data = self.ni_fd.recv(20).decode()
            print(f"Received: {vision_data}")
            
            # Extract coordinates from vision data
            self.ni_coords = extract_coords(vision_data)
            if not self.ni_coords:
                print("Empty coords, skipping...")
                continue
            print(f"Extracted coordinates (x, y, rz): {self.ni_coords}")
            
            # return self.ni_coords
            break
    
    @prettify_decorator
    def terminate(self):
        self.robot_fd.close()
        self.ni_fd.close()


if __name__ == "__main__":
    controller = Controller()
