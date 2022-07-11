from flask import Flask, request

from app.setup_db import db
from app.api import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False}

db.init_app(app)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)