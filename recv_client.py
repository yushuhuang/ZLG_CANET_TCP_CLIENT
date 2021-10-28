import canet
import sys

if len(sys.argv) == 2:
    HOST, PORT = sys.argv[1], int(sys.argv[2])
else:
    HOST = '192.168.0.178'
    PORT = 4002

with canet.Connection() as c:
    c.connect((HOST, PORT))
    while True:
        msg = c.recv()
        if msg:
            print(msg)
