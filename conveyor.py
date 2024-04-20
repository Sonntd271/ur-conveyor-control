import time
import yaml
from socket import *
from utils import encode_with_newline, prettify_decorator

config = yaml.safe_load(open("config.yaml"))
# print(config)


class Conveyor:
    def __init__(self) -> None:
        # Load conveyor address from config
        self.conveyor_addr = (config["conveyor"]["ip"], config["conveyor"]["port"])

        # Load default parameters
        self.conveyor_speed = config["default"]["conveyor_speed"]
        self.conveyor_duration = config["default"]["conveyor_duration"]

        # Setup server for the conveyor to connect to
        self.conveyor_connection()

    @prettify_decorator
    def conveyor_connection(self):
        '''
        Start a server to allow connection from the conveyor
        '''
        # Start a server to allow connection from conveyor
        self.server_fd = socket(AF_INET, SOCK_STREAM)
        self.server_fd.bind(self.conveyor_addr)
        print(f"Socket binded to {self.conveyor_addr[1]}")
        
        # Listen for 1 connection
        self.server_fd.listen(1)
        print("Waiting for connection...")
        self.conveyor_fd, self.client_addr = self.server_fd.accept()

        # Verify connection and activate
        # with self.conveyor_fd: (Verify whether needed)
        print(f"Connected by {self.client_addr}")
        self.conveyor_fd.send(encode_with_newline("activate,tcp"))
        self.conveyor_fd.send(encode_with_newline("pwr_on,conv,0"))

    @prettify_decorator
    def conveyor_control(self, speed=-1, duration=-1):
        '''
        Control the conveyor with speed (mm/s) and duration (s)
        '''
        if speed == -1:
            speed = self.conveyor_speed
        if duration == -1:
            duration = self.conveyor_duration
        self.conveyor_fd.send(encode_with_newline(f"set_vel,conv,{speed}"))
        print(f"Conveyor speed set to {speed} mm/s")
        time.sleep(0.5)

        print(f"Moving conveyor forward for {duration} seconds")
        self.conveyor_fd.send(encode_with_newline("jog_fwd,conv,0"))
        time.sleep(duration)

        # temporary remove backwards
        
        # print(f"Moving conveyor backward for {duration} seconds")
        # self.conveyor_fd.send(encode_with_newline("jog_bwd,conv,0"))
        # time.sleep(duration)

        # Stop conveyor
        self.conveyor_fd.send(encode_with_newline("jog_stop,conv,0"))
        time.sleep(0.5)
        print(f"Conveyor response: {self.conveyor_fd.recv(100)}")

    @prettify_decorator
    def terminate(self):
        self.conveyor_fd.send(encode_with_newline("pwr_off,conv,0"))
        self.conveyor_fd.close()
        self.server_fd.close()
            

if __name__ == "__main__":
    conveyor = Conveyor()
    conveyor.conveyor_control()
