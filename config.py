from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['RESTX_JSON'] = {'ensure_ascii': False}
db = SQLAlchemy(app)
api = Api(app)