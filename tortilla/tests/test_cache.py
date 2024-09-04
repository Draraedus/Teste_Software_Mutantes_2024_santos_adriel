import pytest
from time import time, sleep
from tortilla.cache import CacheWrapper, DictCache, RedisCache, BaseCache

class MockRedis:
    def __init__(self):
        self.storage = {}

    def hget(self, namespace, key):
        return self.storage.get(namespace, {}).get(key)

    def hset(self, namespace, key, value):
        if namespace not in self.storage:
            self.storage[namespace] = {}
        self.storage[namespace][key] = value

    def hdel(self, namespace, key):
        if namespace in self.storage and key in self.storage[namespace]:
            del self.storage[namespace][key]

    def delete(self, namespace):
        if namespace in self.storage:
            del self.storage[namespace]


# Testes para CacheWrapper
def test_cachewrapper_set_and_get():
    cache = DictCache()
    wrapper = CacheWrapper(cache)

    wrapper.set('test', 'value', lifetime=1)
    assert wrapper.get('test') == 'value'

    sleep(2)
    assert wrapper.get('test') is None


def test_cachewrapper_delete():
    cache = DictCache()
    wrapper = CacheWrapper(cache)

    wrapper.set('test', 'value')
    assert wrapper.get('test') == 'value'

    wrapper.delete('test')
    assert wrapper.get('test') is None


def test_cachewrapper_clear():
    cache = DictCache()
    wrapper = CacheWrapper(cache)

    wrapper.set('test', 'value')
    wrapper.clear()

    assert wrapper.get('test') is None


# Testes para DictCache
def test_dictcache_set_and_get():
    cache = DictCache()
    cache.set('test', 'value')
    assert cache.get('test') == 'value'

def test_dictcache_delete():
    cache = DictCache()
    cache.set('test', 'value')
    cache.delete('test')
    assert cache.get('test') is None

def test_dictcache_clear():
    cache = DictCache()
    cache.set('test', 'value')
    cache.clear()
    assert cache.get('test') is None


# Testes para RedisCache
def test_rediscache_set_and_get():
    redis = MockRedis()
    cache = RedisCache(redis)

    cache.set('test', 'value')
    assert cache.get('test') == 'value'

def test_rediscache_delete():
    redis = MockRedis()
    cache = RedisCache(redis)

    cache.set('test', 'value')
    cache.delete('test')
    assert cache.get('test') is None

def test_rediscache_clear():
    redis = MockRedis()
    cache = RedisCache(redis)

    cache.set('test', 'value')
    cache.clear()
    assert cache.get('test') is None
