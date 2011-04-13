from flask import Flask, g, request, Response
from pymongo import Connection
from process import process
from log import L

app = Flask(__name__)

@app.before_request
def before_request():
    g.db_connection = Connection()
    g.db = g.db_connection.hasadna.data
    g.app = app

@app.after_request
def after_request(response):
    g.db_connection.end_request()
    return response

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
