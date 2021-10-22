import socket

HOST = '192.168.0.178'
PORT = 4002


def parse_frame(data: bytes) -> None:
    FRAME_INFO = data[0]
    extend_flag = FRAME_INFO >> 7
    remote_flag = FRAME_INFO >> 6
    frame_len = FRAME_INFO & 0xf

    frame_id_int = int.from_bytes(data[1:5], byteorder='big', signed=False)
    if extend_flag:
        frame_id_int &= 0x1fffffff
    else:
        frame_id_int &= 0x7ff

    DATA = data[5:5+frame_len]
    data_int = int.from_bytes(DATA, byteorder='big', signed=False)

    print('{} {} 帧长度: {}'.format(['标准帧', '扩展帧']
          [extend_flag], ['数据帧', '远程帧'][remote_flag], str(frame_len)))
    print('FRAME ID: ' + hex(frame_id_int))
    print('DATA: ' + hex(data_int))
    print('-' * 80)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(13)
        parse_frame(data)
