from tools.config_loader import ConfigLoader
from tools.redis_db import RedisDb
from tools.logger import Logger
from dbtools.db_connection import DbConnection


def reset_config():
    ConfigLoader.reset_config_loader()
    RedisDb.reset_cache_config()
    Logger.reset_log_config()
    DbConnection.reset_db_config()
