#include <arpa/inet.h>
#include <cstring>
#include <inttypes.h>
#include <iostream>
#include <netinet/in.h>
#include <stdint.h>
#include <stdio.h>
#include <string>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <vector>

#define HOST "192.168.0.178"
#define PORT 4002

void parse_frame(const char (&frame)[13]) {
  uint8_t FRAME_INFO = frame[0];
  bool extend_flag = FRAME_INFO >> 7;
  bool remote_flag = FRAME_INFO >> 6;
  uint8_t frame_len = FRAME_INFO & 0xf;

  uint32_t FRAME_ID;
  memcpy(&FRAME_ID, &frame[1], 4);
  FRAME_ID = ntohl(FRAME_ID);
  FRAME_ID &= extend_flag ? 0x1fffffff : 0x7ff;

  uint64_t DATA{0};
  memcpy(&DATA, &frame[5], frame_len);
  DATA = be64toh(DATA);
  DATA = DATA >> (8 * (8 - frame_len));

  printf("%s %s 帧长度: %d\n", extend_flag ? "扩展帧" : "标准帧",
         remote_flag ? "远程帧" : "数据帧", frame_len);
  printf("FRAME ID: 0x%0*x\n", extend_flag ? 8 : 4, FRAME_ID);
  printf("DATA: 0x%0*lx\n", frame_len * 2, DATA);
  printf("%s\n", std::string(80, '-').c_str());
}

int main() {
  int sock_fd;
  if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    std::cerr << "socket creation failed" << std::endl;
    exit(1);
  }
  sockaddr_in addr_serv{};
  int len;
  addr_serv.sin_family = AF_INET;
  addr_serv.sin_addr.s_addr = inet_addr(HOST);
  addr_serv.sin_port = htons(PORT);
  len = sizeof(addr_serv);
  if (connect(sock_fd, (sockaddr *)&addr_serv, len) < 0) {
    std::cerr << "Connection Failed" << std::endl;
  }

  char frame[13];
  for (;;) {
    recv(sock_fd, &frame, 13, 0);
    parse_frame(frame);
  }

  close(sock_fd);
  return 0;
}