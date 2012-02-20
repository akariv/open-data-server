import json
from md5 import md5

##########################
MAGIC_KEY = 'CHANGE ME!'  #
##########################

def admin_apikey():
    provider = 'admin'
    user_id = ''
    magic_calc = "%s%s%s" % (provider,user_id,MAGIC_KEY)
    magic_calc = md5(magic_calc).hexdigest() 
    api_key = { 'p' : provider,
                'u' : user_id,
                'm' : magic_calc }
    api_key = json.dumps(api_key)
    api_key = json.encode('hex')
    return api_key

ADMIN_APIKEY = admin_apikey()   
