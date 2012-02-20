from flask import Flask, g, request, Response, redirect, render_template, session
from process import process
from log import L, snip
from processors.mongodb_proxy import DB
from flask.helpers import url_for
from internal_db_ops import internal_find
import urllib

app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'my-very-secretive-secret',
)

@app.route('/')
def index():
    return render_template('api_playground.html')

@app.route("/<slug>", methods=['GET'])
def data(slug):
    path=''
    L.info("dbserver::data::%s:%s, %s, %s" % (request.method,path,slug,request.url))
    response, content_type, headers = process(path,slug)
    return Response(response=response, content_type=content_type, headers=headers)

@app.route("/<path:path>/<slug>", methods=['GET'])
def slug(path,slug):
    L.info("dbserver::slug::%s:%s, %s, %s" % (request.method,path,slug,request.url))
    response, content_type, headers = process(path,slug)
    return Response(response=response, content_type=content_type, headers=headers)

@app.route("/<path:path>/", methods=['GET'])
def noslug(path):
    L.info("dbserver::noslug::%s:%s, %s" % (request.method,path,request.url))
    response, content_type, headers = process(path,None)
    L.info("%s %s %s" % (snip(response), content_type, headers))
    return Response(response=response, content_type=content_type, headers=headers)
