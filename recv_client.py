import canet

HOST = '192.168.0.178'
PORT = 4002


with canet.Connection((HOST, PORT)) as c:
    while True:
        msg = c.recv()
        print(msg)
