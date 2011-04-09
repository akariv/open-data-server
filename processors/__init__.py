#import os
import glob

from processor import Processor

for f in glob.glob('processors/*py'):
    __import__(f.replace("/",".").replace(".py",""))    
