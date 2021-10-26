import canet
import socket
from typing import Union, Tuple, Any

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

    def __init__(self, __address: _Address):
        self.__address = __address
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect(self.__address)

    def close(self) -> None:
        try:
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
        except Exception:
            pass

    def send(self, msg: canet.Message) -> None:
        self.s.sendall(msg2frame(msg))

    def recv(self) -> canet.Message:
        data = self.s.recv(13)
        return frame2msg(data)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.s.close()
