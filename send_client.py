import canet
import time
import sys

if len(sys.argv) == 3:
    HOST, PORT = sys.argv[1], int(sys.argv[2])
else:
    HOST = '192.168.0.178'
    PORT = 4001

msg = canet.Message(arbitration_id=0x100, is_extended_id=False, data=[
    0, 17, 34, 51, 68, 85, 102, 255])

with canet.Connection() as c:
    c.connect((HOST, PORT))
    while True:
        c.send(msg)
        print(msg)
        time.sleep(1)
