import csv

from base import Emitter
from StringIO import StringIO

@Emitter.emitter
class ExcelFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        return format == 'excel' and type(self.token.response)==list
    
    def format(self):
        self.token.content_type = 'application/vnd.ms-excel'
        fields = set()
        for rec in self.token.response:
            fields.update(rec.keys())
        out = StringIO()
        writer = csv.DictWriter(out,list(fields))
        writer.writerow(dict(zip(fields,fields)))
        rows = [ dict([ (k,unicode(v).encode('utf8')) for k,v in row.iteritems() ]) for row in self.token.response ]
        writer.writerows(rows)
        self.token.response = out.getvalue()
        self.token.headers['content-disposition'] = 'attachment; filename=data.xls' 
