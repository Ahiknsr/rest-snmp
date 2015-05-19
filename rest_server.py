import sqlite3 
from flask import Flask, request, session, g, jsonify
from flask.ext.restful import Api, Resource

from dbfunctions import get_db , query_db
from views import PDU , Status , ChangeState


# create our little application :)
app = Flask(__name__)
app.config.from_pyfile('application.cfg')
api = Api(app)


@app.before_request
def before_request():
    g.db = get_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


api.add_resource(PDU, '/pdu/', endpoint = 'pdu')
api.add_resource(Status, '/status/<int:id>/<tower>/<int:outlet>', endpoint = 'status')
api.add_resource(ChangeState, '/changestate/' , endpoint = 'changestate')


if __name__ == '__main__':
    app.run()
