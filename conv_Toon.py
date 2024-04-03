####### Command for control conveyor #################
#### activate tcp        = activate,tcp
#### power on servo      = pwr_on,conv,0
#### power off servo     = pwr_off,conv,0
#### set velocity x mm/s = set_vel,conv,x   # x = 0 to 200
#### jog forward         = jog_fwd,conv,0
#### jog backward        = jog_bwd,conv,0
#### stop conveyor       = jog_stop,conv,0
#########################################################




import socket, time
from socket import *


host    = '10.10.0.98'
port_conv = 2002

c = socket(AF_INET, SOCK_STREAM)
#c.bind(('10.10.0.98', 2002))



#c = socket.socket()

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
c.bind((host , port_conv))
print ("socket binded to %s" %(port_conv))

c.listen(5)
print ("socket is listening")
conv, addr = c.accept()
with conv:
    print(f"Connected by {addr}")
    conv.send(b'activate,tcp\n')
    conv.send(b'pwr_on,conv,0\n')
    time.sleep(0.5)

    speed = 10
    ok = conv.sendall(b'set_vel,conv,0\n')
    if ok != None:
        print("Not ok")
    print("Sleeping...")
    time.sleep(2)

    # conv.sendall(b'jog_bwd,conv,0\n')
    # time.sleep(2.5)

    print("Yo, I'm going forward")
    conv.sendall(b'jog_fwd,conv,0\n')
    time.sleep(2)

    conv.send(b'jog_bwd,conv,0\n')
    time.sleep(2)

    conv.send(b'jog_stop,conv,0\n')
    time.sleep(0.5)
    conv.send(b'pwr_off,conv,0\n')
    conv_recv = conv.recv(100)
    print(conv_recv)
 

"""
# print ('0000000000000000')
# cmd = input('cmd to conv:\n')
# print(f'You entered {cmd}')
cmd = "activate,tcp,0.0\n"
c.send(b'activate,tcp,0.0\n')
#c.sendall(cmd.encode())
#conv.sendall(cmd.encode())
time.sleep(1)

conv.sendall(b'pwr_on,conv,0\n')
# time.sleep(1)

# conv.sendall(b'set_vel,conv,10\n')
# time.sleep(1)

# conv.sendall(b'jog_fwd,conv,0\n')
# time.sleep(1)

conv_recv = conv.recv(10)
print (conv_recv)
"""