import json
cache = {}

def clear_cache(key):
    if key in cache.keys():
        del cache[key]

def hit_cache(key):
    key = json.dumps(key)
    value = cache.get(key)
    if value != None:
        return json.loads(value)
    else:
        return None

def store_in_cache(key,value):
    key = json.dumps(key)
    cache[key] = json.dumps(value)
