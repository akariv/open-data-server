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
    SOURCE_EL   = '_src' 
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
        def get_data(rec):
            x = rec.get(self.DATA_EL,{})
            x[self.SOURCE_EL] = "%s/%s" % (rec[self.META_EL][self.PATH_EL], rec[self.META_EL][self.ID_EL])
            return x
        
        if self.token.slug != None:
            rec = g.db.find_one({self.META_PATH : self.token.path,
                                 self.META_ID   : self.token.slug })
            if rec != None:
                self.token.response = get_data(rec)
            else:
                self.token.response = None
        else:
            recs = g.db.find({self.META_PATH : self.token.path })
            recs = [ get_data(rec) for rec in recs ]
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
            L.exception('db_op::post')
            self.token.response = False

    def delete(self):
        try:
            if self.token.slug != None:
                g.db.remove({ self.META_PATH : self.token.path,
                              self.META_ID   : self.token.slug },
                              safe = True)
            else:
                g.db.remove({ self.META_PATH : self.token.path },
                              safe = True)
                
            
            self.token.response = True
        except:
            self.token.response = False
