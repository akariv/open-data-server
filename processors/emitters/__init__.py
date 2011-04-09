import glob

from base import Emitter

for f in glob.glob('processors/emitters/*py'):
    __import__(f.replace("/",".").replace(".py",""))
