from redis import StrictRedis
from tools.logger import Logger
from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
import enum
import math

#5種cache運作方式
class CacheType(enum.IntEnum):
    AUTO = 0
    READONLY = 1
    IGNORE = 2
    RENEW = 3
    BUILD = 4


class RedisDb:
    _host = ''
    _port = 80
    _password = None
    _cache_type = CacheType.AUTO
    _expiry_hours = 360

    #取得預設的RedisDb instance
    @classmethod
    def default(clz):
        clz.check_cache_config()
        redis_db = clz(clz._host, clz._port, clz._password)
        return redis_db


    @classmethod
    def cache_type(clz):
        clz.check_cache_config()
        return clz._cache_type


    @classmethod
    def check_cache_config(clz):
        if clz._host == '':
            cache_config = ConfigLoader.config("cache")
            cache_connection = cache_config["connection"]
            clz._host = cache_connection["host"]
            clz._port = int(cache_connection["port"])
            clz._password = SecretLoader.secret("redis")['pass']
            clz._cache_type = CacheType[cache_config["type"]]
            clz._expiry_hours = float(cache_config["expiry_hours"])


    @classmethod
    def reset_cache_config(clz):
        clz._host = ''
        clz._port = 80
        clz._cache_type = CacheType.AUTO
        clz._expiry_hours = 360


    #產生RedisDb instance
    def __init__(self, host, port, password):
        self.redis = StrictRedis(host=host, port=port, password=password, encoding='utf8', decode_responses=True)
        # self.redis = StrictRedis(host='10.55.8.21', port='27774', encoding='utf8',password='innodriveredis', decode_responses=True)
        self.logger = Logger.default()


    def get(self, key):
        self.logger.info(f'Get cache key: {key}')

        return self.redis.get(key)


    #如果expiry_hours==None，採用預設的預期時間(來自設定檔)
    #如果expiry_hours<=0，不設定expiry
    #轉為整數的秒，使用ceil，避免0~1秒轉為0秒
    def set(self, key, value, expiry_hours=None):
        self.logger.info(f'Set cache key: {key}')
        self.logger.debug(f'Set cache value: {value}')

        if expiry_hours is None:
            expiry_hours = self._expiry_hours

        expiry_secs = math.ceil(expiry_hours * 60 * 60)

        if expiry_secs <= 0:
            self.redis.set(key, value)
        else:
            self.redis.set(key, value, ex=int(expiry_secs))

