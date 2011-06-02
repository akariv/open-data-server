from flask import Flask, g, request, Response
#from pymongo import Connection
from process import process
from log import L
from processors.mongodb_proxy import DB

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = DB()
    g.app = app

@app.after_request
def after_request(response):
    g.db.after_request()
    return response

@app.route("/<slug>", methods=['GET', 'PUT', 'DELETE', 'POST'])
def data(slug):
    path=''
    L.info("dbserver::data::%s:%s, %s, %s" % (request.method,path,slug,request.url))
    response, content_type, headers = process(path,slug)
    return Response(response=response, content_type=content_type, headers=headers)

@app.route("/<path:path>/<slug>", methods=['GET', 'PUT', 'DELETE', 'POST'])
def slug(path,slug):
    L.info("dbserver::slug::%s:%s, %s, %s" % (request.method,path,slug,request.url))
    response, content_type, headers = process(path,slug)
    return Response(response=response, content_type=content_type, headers=headers)

@app.route("/<path:path>/", methods=['GET', 'POST', 'DELETE'])
def noslug(path):
    L.info("dbserver::noslug::%s:%s, %s" % (request.method,path,request.url))
    response, content_type, headers = process(path,None)
    return Response(response=response, content_type=content_type, headers=headers)
