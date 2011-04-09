import json

from flask import g

from processor import Processor

from log import L

@Processor.processor
class DBOperation(Processor):

    DATA_EL = '_'
    META_EL = 'm'
    PATH_EL = 'path'
    ID_EL   = 'id' 
    META_PATH = '.'.join([META_EL,PATH_EL])
    META_ID = '.'.join([META_EL,ID_EL])
        
    def process(self):
        
        method = self.token.request.method
        L.debug("DBOperation:: method=%r" % method)
        L.debug("DBOperation:: path=%r slug=%r data=%r" % (self.token.path, self.token.slug, self.token.data))
        if method in ['GET', 'PUT', 'POST', 'DELETE']:
            getattr(self,method.lower())()
        L.debug("DBOperation:: result=%r" % self.token.response)
        
    def get(self):
        if self.token.slug != None:
            rec = g.db.find_one({self.META_PATH : self.token.path,
                                 self.META_ID   : self.token.slug })
            if rec != None:
                self.token.response = rec.get(self.DATA_EL,None)
            else:
                self.token.response = None
        else:
            recs = g.db.find({self.META_PATH : self.token.path })
            recs = [ rec[self.DATA_EL] for rec in recs if self.DATA_EL in rec.keys() ]
            self.token.response = recs
            

    def put(self):
        try:
            rec = g.db.find_one({self.META_PATH : self.token.path,
                                 self.META_ID   : self.token.slug })
            if rec != None:
                rec[self.DATA_EL] = self.token.data
                g.db.save(rec,safe=True)
            self.token.response = True
        except:
            self.token.response = False

    def post(self):
        try:
            rec = g.db.find_one({self.META_PATH : self.token.path,
                                 self.META_ID   : self.token.slug })
            
            if rec == None:
                g.db.save( { self.META_EL : { self.PATH_EL : self.token.path,
                                              self.ID_EL   : self.token.slug },
                             self.DATA_EL : self.token.data },
                             safe = True)

            self.token.response = True
        except:
            self.token.response = False

    def delete(self):
        try:
            g.db.remove({ self.META_PATH : self.token.path,
                          self.META_ID   : self.token.slug },
                          safe = True)
            
            self.token.response = True
        except:
            self.token.response = False
