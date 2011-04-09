import json
from functools import wraps

from flask import request, abort

from urllib2 import urlopen,URLError,HTTPError

# decorator for flask views
def dbserver(api_url):
    def decorator(f):
        @wraps(f)
        def decorated_function(slug=""):
            if request.method == 'GET':
                try:
                    data = urlopen(api_url+slug).read()
                except HTTPError, e:
                    abort(e.code)
                data = json.loads(data)
                if data == None:
                    abort(404)
                return f(data)
            elif request.method == 'POST':
                data = json.loads(request.data)
                return f(data)
            
        return decorated_function
    return decorator
