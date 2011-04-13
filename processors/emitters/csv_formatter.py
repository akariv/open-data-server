import csv

from base import Emitter
from StringIO import StringIO

@Emitter.emitter
class CsvFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        return format == 'csv' and type(self.token.response)==list
    
    def format(self):
        self.token.content_type = 'text/csv'
        fields = set()
        for rec in self.token.response:
            fields.update(rec.keys())
        out = StringIO()
        writer = csv.DictWriter(out,list(fields))
        writer.writerow(dict(zip(fields,fields)))
        writer.writerows(self.token.response)
        self.token.response = out.getvalue()
