from socket import *
import time
import yaml
from utils import encode_with_newline, prettify_decorator

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

        # Connect with the gripper (Edit config.yaml to change address)
        self.gripper_connection()

    @prettify_decorator
    def gripper_connection(self):
        '''
        Connect to gripper
        '''
        # Open a socket for controlling the gripper
        self.gripper_fd = socket(AF_INET, SOCK_STREAM)
        self.gripper_fd.connect(self.gripper_addr)

        # Verify gripper connection
        self.gripper_fd.sendall(encode_with_newline("GET POS"))
        if str(self.gripper_fd.recv(10), "UTF-8"):
            self.gripper_fd.send(encode_with_newline("SET ACT 1"))
            print(str(self.gripper_fd.recv(10), "UTF-8"))

            gripper_commands = [
                "SET GTO 1",
                "SET SPE 255",
                "SET FOR 255"
            ]
            for cmd in gripper_commands:
                self.gripper_fd.send(encode_with_newline(cmd))
            print("Gripper activated")

        # Ensure release
        self.grip_control(0)

    @prettify_decorator
    def grip_control(self, value):
        '''
        Control gripping mechanism of the gripper,
        Release value = 0, Grab value = 255
        '''
        if value == 0 or value == 255:
            self.gripper_fd.send(encode_with_newline(f"SET POS {value}"))
        time.sleep(0.5)
        _ = str(self.gripper_fd.recv(10), "UTF-8")
        self.gripper_fd.send(encode_with_newline("GET POS"))
        
        recv_buf = str(self.gripper_fd.recv(10), "UTF-8")
        print(f"Gripper position = {recv_buf}")

    @prettify_decorator
    def terminate(self):
        self.gripper_fd.close()


if __name__ == "__main__":
    gripper = Gripper()
