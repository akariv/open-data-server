import json

from flask import g

from log import L

from processor import Processor

@Processor.processor
class MultiLang(Processor):

    LANGS = [ u'he', u'en', u'ar', u'ru' ]

    def handle_object(self,obj):
        if type(obj) == dict and len(obj.keys())>0:
            all_langs = True
            for k,v in obj.iteritems():
                all_langs = all_langs and k in self.LANGS
                all_langs = all_langs and (type(k) == str or type(k) == unicode)
                all_langs = all_langs and (type(v) == str or type(v) == unicode)
            if all_langs:
                for lang in self.preferred_langs:
                    try:
                        return obj[lang]
                    except:
                        pass
                return obj.values()[0]
            else:
                for k,v in obj.iteritems():
                    if type(v) == dict:
                        obj[k] = self.handle_object(v)
        elif type(obj) == list:
            return [ self.handle_object(el) for el in obj]
        return obj

    def process(self):
        self.preferred_langs = self.token.request.args.get('lang','').split(',')
        self.preferred_langs.extend(self.LANGS)
        self.token.response = self.handle_object(self.token.response)
