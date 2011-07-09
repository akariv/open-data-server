import json

from flask import g

from processor import Processor

from log import L

from cache_checker import hit_cache, store_in_cache

@Processor.processor
class DBOperation(Processor):

    DATA_EL = 'd'
    META_EL = 'm'
    PATH_EL = 'path'
    ID_EL   = 'id' 
    SOURCE_EL   = '_src' 
    META_PATH = '.'.join([META_EL,PATH_EL])
    META_ID = '.'.join([META_EL,ID_EL])
        
    def process(self):
        
        method = self.token.request.method

        self.query = self.token.request.args.get('query',"{}")
        self.query = json.loads(self.query)
        self.query=dict([("%s.%s" % (self.DATA_EL,k),v) for k,v in self.query.iteritems()])

        self.order = self.token.request.args.get('order',"[]")
        self.order = json.loads(self.order)
        self.order=[("%s.%s" % (self.DATA_EL,k),v) for k,v in self.order]

        self.start = self.token.request.args.get('start',0)
        self.start = int(self.start)
        
        self.limit = self.token.request.args.get('limit',1000)
        self.limit = int(self.limit)
        if self.limit == 0:
            self.limit = None

        self.fields = self.token.request.args.get('fields')
        if self.fields != None:
            self.fields = json.loads(self.fields)
            self.fields =[ "%s.%s" % (self.DATA_EL,k) for k in self.fields]
            self.fields.append(self.META_EL)

        self.count = self.token.request.args.get('count',0)
        self.count = int(self.count)

        L.debug("DBOperation:: method=%r" % method)
        L.debug("DBOperation:: path=%r slug=%r data=%r" % (self.token.path, self.token.slug, self.token.data))
        if method in ['GET', 'PUT', 'POST', 'DELETE']:
            getattr(self,method.lower())()
        L.debug("DBOperation:: result=%s" % repr(self.token.response)[:2048])
        
    def get(self):
        def get_data(rec):
            x = rec.get(self.DATA_EL,{})
            x[self.SOURCE_EL] = "%s/%s" % (rec[self.META_EL][self.PATH_EL], rec[self.META_EL][self.ID_EL])
            x[self.SOURCE_SLUG_EL] = x[self.SOURCE_EL].replace('/','__')
            return x
        
        if self.token.slug != None:
            rec = g.db.find_one( {self.META_PATH : self.token.path,
                                  self.META_ID   : self.token.slug } )
            if rec != None:
                ret = get_data(rec)
            else:
                ret = None
            self.token.response = ret
        else:
            if self.query != None:
                self.query.update({self.META_PATH : self.token.path })
            else:
                self.query = {self.META_PATH : self.token.path }
            L.debug("DBOperation:: find using query=%r" % self.query)
            if self.count == 0:
                recs = g.db.find(self.query,fields=self.fields,limit=self.limit,start=self.start)
                recs = [ get_data(rec) for rec in recs ]
                ret = recs
            else:
                ret = g.db.count(self.query,fields=self.fields,limit=self.limit,start=self.start)
            self.token.response = ret
            
    def put(self):
        try:
            rec = g.db.find_one({self.META_PATH : self.token.path,
                                 self.META_ID   : self.token.slug })
            if rec != None:
                rec[self.DATA_EL] = self.token.data
                g.db.save(rec)
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
                             self.DATA_EL : self.token.data })
            else:
                rec[self.DATA_EL] = self.token.data
                g.db.save(rec)
                
            self.token.response = True
        except:
            L.exception('db_op::post')
            self.token.response = False

    def delete(self):
        try:
            if self.token.slug != None:
                g.db.remove({ self.META_PATH : self.token.path,
                              self.META_ID   : self.token.slug })
            else:
                g.db.remove({ self.META_PATH : self.token.path })
                
            
            self.token.response = True
        except:
            self.token.response = False
