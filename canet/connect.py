import canet
import socket
from typing import Optional, Union, Tuple, Any

_Address = Union[Tuple[Any, ...], str, bytes]


def msg2frame(msg: canet.Message) -> bytes:
    FRAME_INFO = msg.dlc | msg.is_extended_id << 7 | msg.is_remote_frame << 6
    data = msg.data + bytearray([0] * (8 - len(msg.data)))
    return FRAME_INFO.to_bytes(
        1, 'big') + msg.arbitration_id.to_bytes(4, 'big') + data


def frame2msg(frame: bytes) -> canet.Message:
    FRAME_INFO = frame[0]
    extended_flag = FRAME_INFO >> 7 & 1
    remote_flag = FRAME_INFO >> 6 & 1
    frame_len = FRAME_INFO & 0xf

    arbitration_id = int.from_bytes(frame[1:5], byteorder='big', signed=False)
    arbitration_id &= [0x7ff, 0x1fffffff][extended_flag]

    msg = canet.Message(arbitration_id=arbitration_id, is_extended_id=extended_flag,
                        is_remote_frame=remote_flag, data=frame[5:5+frame_len])
    return msg


class Connection:

    def __init__(self, sock: socket = None):
        if sock:
            self.s = sock
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, __address: _Address):
        self.s.connect(__address)

    def close(self) -> None:
        try:
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
        except Exception:
            pass

    def send(self, msg: canet.Message) -> bool:
        try:
            self.s.sendall(msg2frame(msg))
            return True
        except BrokenPipeError:
            self.s.close()
            return False

    def recvall(self, n: int) -> Optional[bytes]:
        data = bytearray()
        while len(data) < n:
            packet = self.s.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def recv(self) -> Optional[canet.Message]:
        data = self.recvall(13)
        return frame2msg(data) if data else None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.s.close()
