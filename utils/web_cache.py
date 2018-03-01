from redis import Redis
import memcache


class Memcache(object):
    def __init__(self):
        self.cache = memcache.Client(['127.0.0.1:11211'], debug=True)

    def set(self, key, value, timeout=60 * 30):
        return self.cache.set(key, value, timeout)

    def get(self, key):
        return self.cache.get(key)


class RedisCache(object):
    def __init__(self):
        self.xredis = Redis(host='127.0.0.1', port=6379, decode_responses=True)

    def set(self, key, value, timeout=60 * 30):
        return self.xredis.set(key, value, timeout)

    def get(self, key):
        return self.xredis.get(key)
