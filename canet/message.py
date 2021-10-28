from typing import Optional, Union, Iterable


class Message:

    def __init__(
        self,
        arbitration_id: int = 0,
        is_extended_id: bool = True,
        is_remote_frame: bool = False,
        dlc: Optional[int] = None,
        data: Optional[Union[bytes, bytearray, int, Iterable[int]]] = None,
    ):
        self.arbitration_id = arbitration_id
        self.is_extended_id = is_extended_id
        self.is_remote_frame = is_remote_frame

        if data is None or is_remote_frame:
            self.data = bytearray()
        elif isinstance(data, bytearray):
            self.data = data
        else:
            try:
                self.data = bytearray(data)
            except TypeError as error:
                err = f"Couldn't create message from {data} ({type(data)})"
                raise TypeError(err) from error

        self.dlc = len(self.data) if not dlc else dlc

    def __str__(self) -> str:
        field_strings = [
            f"{['标准帧', '扩展帧'][self.is_extended_id]} {['数据帧', '远程帧'][self.is_remote_frame]} 帧长度：{self.dlc}"]
        field_strings.append(
            f'FRAME ID: 0x{self.arbitration_id:0{[4, 8][self.is_extended_id]}x}')
        field_strings.append(f'DATA: 0x{self.data.hex()[:self.dlc*2]}')
        return "    ".join(field_strings)
