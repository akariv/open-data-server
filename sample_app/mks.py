from flask import Flask
from apps import dbserver

app = Flask(__name__)

MKS_DB_URL = 'http://127.0.0.1:5555/mks/'

@app.route("/")
@dbserver(MKS_DB_URL)
def mk_list(data):
    return "\n".join( [ "<html><body>",
                        "\n".join( [ "<p><b>%(name)s</b>: %(age)s years old, lives in %(city)s</p>" % rec for rec in data ] ),
                        "</body></html>" ] ) 

@app.route("/<slug>")
@dbserver(MKS_DB_URL)
def mk_page(data):
    return """<html>
    <body>
        <h1>%(name)s</h1>
        <p>Age: %(age)s</p>
        <p>City: %(city)s</p>
    </body>
    </html>
    """ % data

if __name__ == "__main__":
    app.run()
