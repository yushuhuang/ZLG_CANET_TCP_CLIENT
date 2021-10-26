import canet

HOST = '192.168.0.178'
PORT = 4001

msg = canet.Message(arbitration_id=0x100, is_extended_id=False, data=[
    0, 17, 34, 51, 68, 85, 102, 255])

with canet.Connection((HOST, PORT)) as c:
    c.send(msg)

print(msg)
