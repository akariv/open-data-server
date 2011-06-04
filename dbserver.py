from flask import Flask, g, request, Response, redirect, render_template, session
from flaskext.openid import OpenID
#from pymongo import Connection
from process import process
from log import L
from processors.mongodb_proxy import DB
from flask.helpers import url_for

app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'my-very-secretive-secret',
)
oid = OpenID(app,'/tmp/')

@app.before_request
def before_request():
    g.db = DB()
    g.app = app
    g.user = None
    if 'openid' in session:
        g.user = session['openid']

@app.after_request
def after_request(response):
    g.db.after_request()
    return response

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'fullname',
                                                  'nickname'])
    return render_template('login.html', next=oid.get_next_url(),
                           error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):
    user = session['openid'] = resp.identity_url
    L.info(u'Successfully signed in %s, %r' % (user, request.values))
    L.info(u'Successfully signed in %s, %s' % (request.values.name, request.values.email))
    g.user = user
    return redirect(oid.get_next_url())
#    return redirect(url_for('create_profile', next=oid.get_next_url(),
#                            name=resp.fullname or resp.nickname,
#                            email=resp.email))

@app.route('/logout')
def logout():
    session.pop('openid', None)
    L.info(u'You have been signed out')
    return redirect(oid.get_next_url())

@app.route('/')
def index():
    return render_template('api_playground.html')

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
    L.info("%s %s %s" % (response, content_type, headers))
    return Response(response=response, content_type=content_type, headers=headers)
