import json
#from werkzeug.contrib.cache import SimpleCache as CacheEngine
from werkzeug.contrib.cache import MemcachedCache as CacheEngine

cache = CacheEngine(['127.0.0.1:11211'])

def clear_cache(key):
    cache.delete(key)

def clear_cache_for_path(path):
    pass
#    print "clearing cache for path: %s" % path
#    for key in cache.keys():
#        if key.startswith('"%s"' % path):
#            print "clearing cache key: %s" % key
#            del cache[key]

def hit_cache(key):
    return cache.get(key)
#    key = json.dumps(key)
#    value = cache.get(key)
#    if value != None:
#        return json.loads(value)
#    else:
#        return None

def store_in_cache(key,value):
    cache.set(key,value,60)
#    key = json.dumps(key)
#    cache[key] = json.dumps(value)
