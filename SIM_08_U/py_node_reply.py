# C. Adolph
from concurrent import futures
import logging
import time
import grpc

from proto import service_pb2
from proto import service_pb2_grpc

# Address
ADDRESS = "localhost:23333"

class GetTime(service_pb2_grpc.GetTimeServicer):

    def GimmeTime(self, request, context):
        received = time.time()
        monotonic_1 = time.monotonic()
        #time.sleep(0.1)
        #monotonic_2 = time.monotonic()
        #sent = received + (monotonic_1 )
        return service_pb2.TimeResponse(time_received=received, time_sent=(received + (time.monotonic() - monotonic_1)))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_GetTimeServicer_to_server(GetTime(), server)
    server.add_insecure_port(ADDRESS)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
