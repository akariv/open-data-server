
class Processor(object):
    
    def __init__(self,token):
        self.token = token

    def process(self):
        assert(False)

    def stop(self):
        return False 

    available_processors = {}

    @classmethod
    def get_processor(cls,*args):
        return cls.available_processors.get(*args)

    @classmethod
    def processor(cls,klass):
        cls.available_processors[klass.__name__] = klass
        return klass
