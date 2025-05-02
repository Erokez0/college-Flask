from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def init_app():
    app1 = Flask(__name__, template_folder='static')
    app1.config['SECRET_KEY'] = 'hard to guess string'
    return app1

def init_db(app1):
    db1 = SQLAlchemy(app1)
    app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    db1.init_app(app1)
    return db1

def init_migrate(app1, db1):
    migrate1 = Migrate(app1, db1)
    return migrate1

app = init_app()
db = init_db(app)
migrate = init_migrate(app, db)