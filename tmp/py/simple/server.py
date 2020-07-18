#!/usr/bin/python env
# coding:utf-8
import socket
import os

ip_port = ('127.0.0.1', 8081)
back_log = 10
buffer_size = 1024

alldata = "<h1>Hello1 World</h1>"


def main():
    webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    webserver.bind(ip_port)
    webserver.listen(back_log)

    while True:
        conn, addr = webserver.accept()
        print(addr)
        recvdata = conn.recv(buffer_size)

        conn.sendall(bytes("HTTP/1.1 201 OK\r\n\r\n", "utf-8"))  # 响应头

        fileUrl = "./resource";
        # print()
        s = ""
        for name in os.listdir(fileUrl):
            s += name;
        conn.sendall(bytes(s, "utf-8"))

        conn.close()


if __name__ == '__main__':
    main()