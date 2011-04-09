import os
import json

datas = { 'Yossi_Sarid'   : {"name":"Yossi Sarid", "age":70, "city":"Jerusalem"},
	  	  'Zvulun_Orlev'  : {"name":"Zvulun Orlev", "age":73, "city":"Tel-Aviv"},
	  	  'Amram_Mitzna'  : {"name":"Amram Mitzna", "age":67, "city":"Netanya"},
	  	  'Yossef_Aridor' : {"name":"Yossef Aridor", "age":77, "city":"Modi'in"}, }

for s,d in datas.iteritems():
      i,o=os.popen2('lwp-request -m DELETE 127.0.0.1:5000/mks/%s' % s)
      print o.read()
      i,o=os.popen2('lwp-request -c application/json -m POST 127.0.0.1:5000/mks/%s' % s)
      i.write(json.dumps(d))
      i.close()
      print o.read()
