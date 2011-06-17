import json
from urllib import urlencode

from flask import g
from log import L

def internal_save(url,obj):
    data = json.dumps(obj)
    data = g.app.test_client().post(url,data=data,content_type="application/json")

def internal_find(url,follow=True,lang=None,query=None,apikey=None):
    params = {}
    params['follow'] = "yes" if follow else "no"
    if lang:    params['lang'] = lang
    if query:   params['query'] = query
    if apikey:  params['apikey'] = apikey
    L.info("internal_find: Attempting to fetch %s with %s" % (url,params))
    
    params = urlencode(params)
    url += "?" + params
    data = g.app.test_client().get(url).data
    print ">>>>",url,data
    data = json.loads(data)
    return data
