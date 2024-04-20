import time
import threading
from controller import Controller
from gripper import Gripper
from conveyor import Conveyor

def conveyor_task():
    conveyor = Conveyor()
    conveyor.conveyor_control()

controller = Controller()
gripper = Gripper()

time.sleep(0.5)
controller.robot_to_home()
time.sleep(0.5)

# Start conveyor as a thread
conveyor_thread = threading.Thread(target=conveyor_task)
conveyor_thread.start()

# Extract coords from vision system
controller.ni_get_coords()
ni_coords = controller.ni_coords
print(ni_coords)

# Move to object

time.sleep(0.4)
# z = -23
x_cm = ni_coords[0]/10
y_cm = ni_coords[1]/10

controller.robot_move_util(x=x_cm, y=y_cm, z=-22, rz=0)
# Grip


gripper.grip_control(255)
# Move up
controller.robot_move_util(x=x_cm, y=y_cm, z=-2, rz=0)
# Release
# gripper.grip_control(0)
# Move robot back to home
time.sleep(0.5)

controller.robot_move_util(x=x_cm, y=y_cm, z=-21, rz=0)
gripper.grip_control(0)

time.sleep(1)

controller.robot_to_home()
print(ni_coords)

# using locked axis
# [-22, 13, 1]
# [-16, 27, 346]
