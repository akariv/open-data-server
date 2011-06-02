from pymongo import Connection

class DB(object):
    
    def __init__(self):
        self.db_connection = Connection()
        self.db = self.db_connection.hasadna.data

    def find_one(self,query_dict):
        return self.db.find_one(query_dict)

    def find(self,query_dict,fields=None,limit=None,start=None):
        return self.db.find(query_dict,limit=limit,skip=start,fields=fields)

    def save(self,doc):
        self.db.save(doc,safe=True)
        
    def remove(self,query_dict):
        self.db.remove(query_dict,safe=True)
            
    def after_request(self):
        self.db_connection.end_request()
