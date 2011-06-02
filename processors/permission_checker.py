import json

from flask import g

from processor import Processor

from log import L
from django.utils.http import urlencode
import os

@Processor.processor
class PermissionChecker(Processor):
    
    def stop(self):
        return self.should_stop

    def validate_api(self,api_key):
        return False ## TODO
    
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

        self.app = self.token.request.args.get('apikey',None)
        if self.app != None:
            if self.app == "admin":
                return
            
            if not self.validate_api(self.app):
                return

        self.user = None ## TODO: '''<<getuser>>'''


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
            params = [('query',spec),('apikey','admin')]
            params = urlencode(params)
            data = g.app.test_client().get('/data/admin/permissions/?%s' % params).data
            data = json.loads(data)
            for rec in data:
                auth = rec.get('auth')
                if self.match_auth(auth):
                    perms.update(set(rec.get('perms',set())))
                    L.info("PermissionChecker: rule %s, perms=%r" % (rec.get('_src'),set(rec.get('perm',set()))))
        
        if ( (method == "POST"   and "new"    in perms) or
             (method == "DELETE" and "delete" in perms) or
             (method == "PUT"    and "edit"   in perms) or
             (method == "GET"    and "read"   in perms) ):
            pass
        else:
            self.should_stop = True
