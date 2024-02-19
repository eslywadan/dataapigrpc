from concurrent import futures
from threading import Thread
from urllib import response
from tools.account import check_and_log, get_client_info
from tools.account import check_client_id_password
import grpc
import grpc_cust.clientapival_pb2 as clientapival_pb2
import grpc_cust.clientapival_pb2_grpc as clientapival_pb2_grpc
from tools.config_loader import ConfigLoader
from tools.logger import Logger


__all__ = 'ClientApiVal'

clientapival_server = ConfigLoader.config("grpc")["clientapival"]["server"]
clientapival_port = ConfigLoader.config("grpc")["clientapival"]["port"]

SERVER_ADDRESS = "%s:%s" %(clientapival_server,clientapival_port)

class ClientAPIValServicer(clientapival_pb2_grpc.ClientAPIValServicer):

    def clientinfo(self, request, context):
      # print("Request Client Info called by client(%s)" %(request.clientid))
      Logger.log(f'Request Client Info called by client {request.clientid}')
      info = get_client_info(request.clientid)
      if(info["CLIENT_ID"]!={}):
          # print("client id %s has registered info" %(request.clientid))
          Logger.log(f'client id {request.clientid} has registered info')
          response = clientapival_pb2.ClientInfo(
            clientid=request.clientid,
            password = str(info["PASSWORD"][0]),
            type = info["TYPE"][0],
            expiry = str(info["EXPIRY"][0]),
            permission = str(info["PERMISSION"][0])
          )
      else:
          print("client id %s has NO registered info" %(request.clientid))
          response = clientapival_pb2.ClientInfo(
            client_id=request.clientid,
            password = "",
            type = 0,
            expiry = "1900-01-01",
            permission = "None")

      return response

    def clientapikey(self, request, context):
      print("Request Client API Key called by client(%s)" %(request.clientid))
      apikey = check_client_id_password(request.clientid, request.password)
      print("Requested Key:%s" %(apikey))
      if(apikey is not None):
          # print("client id %s has the apikey" %(request.clientid))
          Logger.log(f'client id {request.clientid} has the apikey')
          response = clientapival_pb2.ClientAPIKey(
            clientid = str(apikey["clientid"]),
            apikey = str(apikey["apikey"]),
            expiry = str(apikey["expiry"])
          )
      else:
          # print("client id %s has not the api key " %(request.clientid))
          Logger.log(f'client id {request.clientid} has not the api key ')
          response = clientapival_pb2.ClientAPIKey(
            clientid=request.clientid,
            apikey = "",
            expiry = "1900-01-01")

      return response

    def verifiedapikey(self, request, context):
      # print("Request Verify Client API Key called by client(%s)" %(request.clientid))
      Logger.log(f'Request Verify Client API Key called by token{request.apikey}')
      verifiedresult = check_and_log(request.apikey)
      # print("Verified Result:%s" %(verifiedresult))
      Logger.log(f'Verified Result:{verifiedresult}')
      
      response = clientapival_pb2.VerifiedAPIKey(
            apikey = str(request.apikey),
            assertion = str(verifiedresult))

      return response


def valclientserver():
    server = grpc.server(futures.ThreadPoolExecutor())

    clientapival_pb2_grpc.add_ClientAPIValServicer_to_server(ClientAPIValServicer(),server)

    server.add_insecure_port(SERVER_ADDRESS)
    print("---------------Start Python Client Auth Server----------------------------------")
    server.start()
    print("ClientAPIValServicer.clientinfo listen on server(%s)" %(SERVER_ADDRESS))
    server.wait_for_termination()


class GrpcSvr():
    def __init__(cls):
        cls.server = grpc.server(futures.ThreadPoolExecutor())

        clientapival_pb2_grpc.add_ClientAPIValServicer_to_server(ClientAPIValServicer(),cls.server)

        cls.server.add_insecure_port(SERVER_ADDRESS)
        print("---------------Start Python Client Auth Server----------------------------------")
        cls.server.start()
        print("ClientAPIValServicer.clientinfo listen on server(%s)" %(SERVER_ADDRESS))

    def stop(cls):
        grace = True
        cls.server.stop(grace)


if __name__ == '__main__':
  valclientserver()