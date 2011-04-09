from flask import Flask, g, request, Response
from pymongo import Connection
from process import process
from log import L

app = Flask(__name__)

@app.before_request
def before_request():
    g.db_connection = Connection()
    g.db = g.db_connection.hasadna.data

@app.after_request
def after_request(response):
    g.db_connection.end_request()
    return response

@app.route("/<path:path>/<slug>", methods=['GET', 'PUT', 'DELETE', 'POST'])
def slug(path,slug):
    L.info("dbserver::slug::%s:%s, %s" % (request.method,path,slug))
    response, content_type = process(path,slug)
    return Response(response=response, content_type=content_type)

@app.route("/<path:path>/", methods=['GET', 'POST'])
def noslug(path):
    L.info("dbserver::noslug::%s:%s" % (request.method,path))
    response, content_type = process(path,None)
    return Response(response=response, content_type=content_type)
