import socket

HOST = '192.168.0.178'
PORT = 4002


def parse_frame(frame: bytes) -> None:
    FRAME_INFO = frame[0]
    extend_flag = FRAME_INFO >> 7
    remote_flag = FRAME_INFO >> 6
    frame_len = FRAME_INFO & 0xf

    frame_id = int.from_bytes(frame[1:5], byteorder='big', signed=False)
    frame_id &= [0x7ff, 0x1fffffff][extend_flag]

    data = int.from_bytes(frame[5:5+frame_len], byteorder='big', signed=False)

    print('{} {} 帧长度: {}'.format(['标准帧', '扩展帧']
          [extend_flag], ['数据帧', '远程帧'][remote_flag], frame_len))
    print('FRAME ID: 0x{0:0{1}x}'.format(frame_id, [4, 8][extend_flag]))
    print('DATA: 0x{0:0{1}x}'.format(data, frame_len * 2))
    print('-' * 80)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(13)
        parse_frame(data)
