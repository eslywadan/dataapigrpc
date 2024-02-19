from grpc_cust.clientapival_client import get_clientinfo, get_clientapikey, get_verified_apikey, SERVER_ADDRESS as server_address
from hybrid_server import SERVER_ADDRESS

def test_clientapival_client():
    assert server_address == SERVER_ADDRESS
    info = get_clientinfo("mfg")
    assert info is not None

    apikey = get_clientapikey("mfg","mfg")
    token = apikey.apikey
    verifiedresult = get_verified_apikey(token)
    assert verifiedresult.assertion == "mfg:QUERY:/mfg"

    apikey = get_clientapikey("eng","eng")
    token = apikey.apikey
    verifiedresult = get_verified_apikey(token)
    assert verifiedresult.assertion ==  "eng:QUERY:/eng"




    
