from flask import Flask, g, request, Response, redirect, render_template, session
from flaskext.openid import OpenID
#from pymongo import Connection
from process import process
from log import L
from processors.mongodb_proxy import DB
from flask.helpers import url_for
from internal_db_ops import internal_find, internal_save

app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'my-very-secretive-secret',
)
oid = OpenID(app,'/tmp/',fallback_endpoint='http://api.yeda.us')

@app.before_request
def before_request():
    g.db = DB()
    g.app = app
    g.user = None
    if 'openid' in session:
        openid_key = session['openid'].encode('hex')
        user = internal_find('/data/admin/users/%s' % openid_key)
        if user != None:
            g.user = user

@app.after_request
def after_request(response):
    g.db.after_request()
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=[ 'email', 'fullname', ] )
    return render_template('login.html', next=oid.get_next_url(),
                           error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    openid_key = session['openid'].encode('hex')
    user = internal_find('/data/admin/users/%s' % openid_key)
    if user != None:
        L.info(u'Successfully signed in fullname=%s, email=%s (%r)' % (resp.fullname, resp.email, resp.__dict__))
    else:
        data = { "fullname"     : resp.fullname,
                 "email"        : resp.email,
                 "key"          : openid_key }
        user = internal_save('/data/admin/users/%s' % openid_key, data)
        L.info(u'Successfully created fullname=%s, email=%s (%r)' % (resp.fullname, resp.email, resp.__dict__))
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
    L.info("%s %s %s" % (str(response)[:128], content_type, headers))
    return Response(response=response, content_type=content_type, headers=headers)
