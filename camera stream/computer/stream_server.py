# -*- coding: utf-8 -*-

import cv2
import io
import numpy as np
import os
import socket
import struct
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../")
from config.settings import *


class VideoStreamingServer(object):
    def __init__(self, host, port):
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        # Accept a single connection and make a file-like object out of it
        self.connection = self.server_socket.accept()[0].makefile('rb')
        print("Streaming Socket Connected!")

    def streaming(self):

        try:
            #print("Host: ", self.host_name + ' ' + self.host_ip)
            #print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == "__main__":
    server = VideoStreamingServer(SERVER_HOST, VIDEO_STREAMING_PORT)
    server.streaming()
