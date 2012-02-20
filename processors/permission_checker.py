import os
import json

from md5 import md5
import urlparse

from flask import g

from log import L

from processor import Processor

from internal_db_ops import internal_find
from config import MAGIC_KEY, ADMIN_APIKEY

@Processor.processor
class PermissionChecker(Processor):
    
    def stop(self):
        return self.should_stop

    def validate_api(self,api_key):
        try:
            L.info("PermissionChecker:: api_key = %s" % api_key)
            api_key = api_key.decode('hex')
            api_key = json.loads(api_key)
            provider = api_key['p']
            user_id = api_key['u']
            magic = api_key['m']
            magic_calc = "%s%s%s" % (provider,user_id,MAGIC_KEY)
            magic_calc = md5(magic_calc).hexdigest()
            assert( magic_calc == magic )
            self.app = provider
            self.user = '%s:%s' % (provider,user_id)
            self.token.data['_userid'] = self.user
#            L.info('PermissionChecker:: api_key = %s' % api_key)
#            api_key = api_key.decode('base64')
#            api_key = json.loads(api_key)
#            app = api_key['a']
#            referrer = api_key['r']
#            request_referrer = self.token.request.referrer
#            request_referrer = urlparse.urlparse(request_referrer).netloc
#            L.info('PermissionChecker:: app = %s, referrer = %s, req.referrer = %s' % (app, referrer, request_referrer))
#            assert( referrer == request_referrer )
#            secret = api_key['s']
#            assert( secret == md5().update("%s:%s:p4tpp" % (app,referrer)).hexdigest()[:8] )
#            self.app = "%s@%s" % (app,referrer)
        except:
            return False 
    
    def match_auth(self,auth):
        if auth.get('anonymous',False):
            return True
        if auth.get('app','not-an-app') == self.app:
            return True
        if auth.get('user','not-a-user') == self.user:
            return True
        return False
    
    def process(self):
        
        method = self.token.request.method
        
        self.should_stop = False 

        self.user = None ## TODO: '''<<getuser>>'''

        self.validate_api(self.token.request.args.get('apikey',''))

        if self.token.slug != None:
            fullpath = os.path.join(self.token.path, self.token.slug)
        else:
            fullpath = self.token.path
        L.debug("PermissionChecker: full_path=%r" % fullpath)
        fullpath = fullpath.split('/')
        L.debug("PermissionChecker: full_path=%r" % fullpath)
        
        perms = set()
        
        for i in range(len(fullpath)):
            partial_path = fullpath[0:i+1]
            L.debug("PermissionChecker: partial_path=%r" % partial_path)
            spec = json.dumps({ "ref" : "/" + "/".join(partial_path) })
            data = internal_find('/data/admin/permissions/',query=spec,apikey=ADMIN_APIKEY)
            for rec in data:
                auth = rec.get('auth')
                if self.match_auth(auth):
                    perms.update(set(rec.get('perms',set())))
                    L.info("PermissionChecker: rule %s, perms=%r" % (rec.get('_src'),set(rec.get('perms',set()))))
        
        if ( (method == "POST"   and "new"    in perms) or
             (method == "DELETE" and "delete" in perms) or
             (method == "PUT"    and "edit"   in perms) or
             (method == "GET"    and "read"   in perms) ):
            pass
        else:
            self.should_stop = True
