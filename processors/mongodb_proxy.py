from pymongo import Connection

class DB(object):
    
    def __init__(self):
        self.db_connection = Connection()
        self.db = self.db_connection.hasadna.data
        self.db.ensure_index([("m.path",1), ("m.id",1)])

    def find_one(self,query_dict):
        return self.db.find_one(query_dict)

    def find(self,query_dict,fields=None,limit=None,start=None):
        return self.db.find(query_dict,limit=limit,skip=start,fields=fields)

    def count(self,*args,**kwargs):
        return self.find(*args,**kwargs).count()

    def save(self,doc):
	pass
        #self.db.save(doc,safe=True)
        
    def remove(self,query_dict):
	pass
        #self.db.remove(query_dict,safe=True)
            
    def after_request(self):
        self.db_connection.end_request()
