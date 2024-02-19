'''Hybride server combines clientapival_server.py and valclient_server.py 
into one'''
from concurrent import futures
from threading import Thread

import grpc
import grpc_cust.clientapival_pb2 as clientapival_pb2
import grpc_cust.clientapival_pb2_grpc as clientapival_pb2_grpc
import grpc_cust.valclient_pb2 as valclient_pb2
import grpc_cust.valclient_pb2_grpc as valclient_pb2_grpc

from valclient_server import ValClientServicer
from clientapival_server import ClientAPIValServicer

from tools.config_loader import ConfigLoader
from tools.logger import Logger


__all__ = 'HybridgRPCServer'

clientapival_server = ConfigLoader.config("grpc")["hybrid"]["server"]
clientapival_port = ConfigLoader.config("grpc")["hybrid"]["port"]

SERVER_ADDRESS = "%s:%s" %(clientapival_server,clientapival_port)

class GrpcServer():
  
    def __init__(cls):
        cls.server = grpc.server(futures.ThreadPoolExecutor())

    def add_servicer(cls):
        clientapival_pb2_grpc.add_ClientAPIValServicer_to_server(ClientAPIValServicer(),cls.server)
        valclient_pb2_grpc.add_ValclientServicer_to_server(ValClientServicer(),cls.server)

    def add_port(cls,SERVER_ADDRESS):
        cls.server.add_insecure_port(SERVER_ADDRESS)
        cls.serveraddress = SERVER_ADDRESS
        
    
    def start(cls):
        cls.server.start()
        print("---------------Start Python gRPC Server----------------------------------")
        print("Servicers listen on server(%s)" %(cls.serveraddress))
        Logger.log(f"HybridgRPCServer listen on {cls.serveraddress}")
        Logger.log(f"Log on {Logger._filename}")
        cls.server.wait_for_termination()

    def qstart(cls):
        cls.add_servicer()
        cls.add_port(SERVER_ADDRESS)
        cls.server.start()
        print("---------------Start Python gRPC Server----------------------------------")
        print("Servicers listen on server(%s)" %(cls.serveraddress))
        Logger.log(f"HybridgRPCServer listen on {cls.serveraddress}")
        Logger.log(f"Log on {Logger._filename}")
        cls.server.wait_for_termination()

    def stop(cls):
        grace = True
        cls.server.stop(grace)
        print("---------------Stop Python gRPC Server----------------------------------")
        Logger.log(f"HybridgRPCServer Stopped on {cls.serveraddress}")


if __name__ == '__main__':
  grpcserver = GrpcServer()
  grpcserver.add_servicer()
  grpcserver.add_port(SERVER_ADDRESS)
  grpcserver.start()