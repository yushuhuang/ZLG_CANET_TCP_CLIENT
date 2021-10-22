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

#define HOST "192.168.0.178"
#define PORT 4001

void build_frame(char (&frame)[13], bool FF, bool RTR, uint8_t LEN,
                 uint32_t FRAME_ID, uint64_t DATA) {
  uint8_t FRAME_INFO = LEN | FF << 7 | RTR << 6;
  FRAME_ID = htonl(FRAME_ID);
  DATA = htobe64(DATA);
  memcpy(frame, &FRAME_INFO, sizeof(FRAME_INFO));
  memcpy(&frame[1], &FRAME_ID, sizeof(FRAME_ID));
  memcpy(&frame[5], &DATA, sizeof(DATA));
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
  build_frame(frame, false, false, 8, 0x100, 0x00112233445566ee);
  send(sock_fd, &frame, sizeof(frame), 0);

  close(sock_fd);
  return 0;
}