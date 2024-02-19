from tools.redis_db import RedisDb

def test_requirepass():
    redisdb = RedisDb.default()
    requirepass=  redisdb.redis.config_get('requirepass')
    assert requirepass["requirepass"] is not None