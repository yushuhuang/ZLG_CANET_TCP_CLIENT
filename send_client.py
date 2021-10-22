import socket

EXTENDED_FRAME = 1
STD_FRAME = 0
REMOTE_FRAME = 1
DATA_FRAME = 0

HOST = '192.168.0.178'
PORT = 4001


def build_frame(*, FF: bool, RTR: bool, LEN: int, FRAME_ID: int, DATA: int) -> bytes:
    assert 0 <= LEN <= 8, "'LEN' out of range"
    assert FRAME_ID <= 0x1fffffff, "'FRAME_ID' out of range"
    assert DATA <= 0xffffffffffffffff, "'DATA' out of range"

    FRAME_INFO = LEN | FF << 7 | RTR << 6
    return FRAME_INFO.to_bytes(1, 'big') + FRAME_ID.to_bytes(4, 'big') + DATA.to_bytes(8, 'big')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(build_frame(FF=STD_FRAME, RTR=DATA_FRAME, LEN=6,
              FRAME_ID=0x100, DATA=0x00112233445566ff))
