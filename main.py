from controller import Controller
from gripper import Gripper
from conveyor import Conveyor

controller = Controller()
gripper = Gripper()
conveyor = Conveyor()

# Extract coords from vision system
ni_coords = controller.ni_get_coords()
print(ni_coords)

# Move to object
controller.robot_move_util(x=ni_coords[0], y=ni_coords[1], rz=ni_coords[2])
# Grip
gripper.grip_control(255)
# Move up
# Release
gripper.grip_control(0)
# Move robot back to home
controller.robot_to_home()
