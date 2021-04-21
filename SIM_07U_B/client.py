import message_pb2
import socket
import time
import datetime
import random
import string

from enum import Enum


class Sensor(Enum):
    GPS = 0
    US = 1
    INFRARED = 2
    LIDAR = 3


class TimeStamp:
    def __init__(self, h, m, s, ms):
        self.h = h
        self.m = m
        self.s = s
        self.ms = ms


IP = "127.0.0.1"
PORT = 5005
BUFFER = 1024

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

status = message_pb2.Status()


sensor_gps = status.sensordata.add()
sensor_gps.id = 1
sensor_gps.sensortype = 0

sent = 0

while True:
    time.sleep(0.5)
    timestamp = TimeStamp(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second, datetime.datetime.now().microsecond)

    status.id = sent
    status.timestamp.h = timestamp.h
    status.timestamp.m = timestamp.m
    status.timestamp.s = timestamp.s
    status.timestamp.ms = timestamp.ms

    sensor_gps.timestamp.h = timestamp.h
    sensor_gps.timestamp.m = timestamp.m
    sensor_gps.timestamp.s = timestamp.s
    sensor_gps.timestamp.ms = timestamp.ms

    sensorvalue = ""
    for _ in range(4):
        sensorvalue += random.choice(string.ascii_letters)

    sensor_gps.sensorvalue = sensorvalue

    message = status.SerializeToString()

    clientSock.sendto(message, (IP, PORT))

    sent += 1

