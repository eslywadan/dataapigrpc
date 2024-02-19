from dbtools.db_connection import DbConnection
import tools.crypto as crypto
import pandas as pd
from dbtools.sql_buffer import SqlBuffer
from tools.redis_db import RedisDb
from datetime import datetime
from tools.logger import Logger



def get_client_info(client_id):
    sql = '''
    SELECT CLIENT_ID, PASSWORD, TYPE, EXPIRY, PERMISSION, REGISTRY 
      FROM ACCOUNT'''
    buf = SqlBuffer(sql).add("CLIENT_ID", client_id)
    cn = DbConnection.default()
    df = pd.read_sql_query(buf.sql, cn)

    info = df.to_dict()
    
    return info


def check_client_id_password(client_id, password):

    info = get_client_info(client_id)
    
    if len(info["PASSWORD"]) > 0:
        Logger.log(f'2.Client info: {info}')
        password_correct = info["PASSWORD"][0]
        type = int(info["TYPE"][0])
        expiry = info["EXPIRY"][0]
        permission = info["PERMISSION"][0]
        registry = info["REGISTRY"][0]
        
        check_ok = (password_correct == crypto.crypto_password(type, password))
        Logger.log(f'check_ok 1: {check_ok}')

        if check_ok:
            today = datetime.today().strftime("%Y-%m-%d")
            check_ok = expiry > today
            Logger.log(f'check_ok 2: {check_ok}')

        if check_ok:
            token = crypto.get_account_token(client_id)
            redis = RedisDb.default()
            redis.set(token, f"{client_id}:{permission}:{registry}", expiry_hours=24)
            client_api_key = {"clientid":client_id,"apikey":token,"expiry":24}
            Logger.log(f'check_ok 3: {check_ok}')
            return client_api_key

    return None


def check_and_log(token=None):

    if token is not None:
        redis = RedisDb.default()
        client_info = redis.get(token)
    if client_info is not None:
        client_id = client_info.split(":")[0]
        permission = client_info.split(":")[1]
        registry = client_info.split(":")[2]
        if permission:
            permission_list = permission.split("|")
            if "QUERY" in permission_list:
                Logger.log(f'Issue request: @{client_id} {token} {registry}')
                return client_info

    Logger.log(f'Deny request: {token}')
    return False

