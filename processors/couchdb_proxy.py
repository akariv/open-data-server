from couchdb import Server
import json

class DB(object):
    
    def __init__(self):
        # For mongo
        #    g.db_connection = Connection()
        #    g.db = g.db_connection.hasadna.data
        self.db_connection = Server()
        try:
            self.db_connection.create('hasadna')
        except:
            pass
        self.db = self.db_connection['hasadna']

    def find_one(self,query_dict):
        map_fun = '''function(doc) {
                        if (%s)
                        emit(doc._id, doc);
                    }''' % ( "&&".join(["(doc.%s==%s)" % (k,json.dumps(v)) for k,v in query_dict.iteritems()]))
        results = self.db.query(map_fun)
        if len(results) == 1:
            return results.rows[0].value
        else:
            return None

    def find(self,query_dict):
        map_fun = '''function(doc) {
                        if (%s)
                           emit(doc._id, doc);
                    }''' % ( "&&".join(["(doc.%s==%s)" % (k,json.dumps(v)) for k,v in query_dict.iteritems()]))
        results = self.db.query(map_fun)
        def gen():
            for x in results:
                yield x.value
        return gen()

    def save(self,doc):
        self.db.save(doc)
        
    def remove(self,query_dict):
        recs = self.find(query_dict)
        for rec in recs:
            self.db.delete(rec)
            
    def after_request(self):
        # _connection.end_request()
        pass