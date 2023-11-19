import os

from flask import Flask, render_template

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

def create_app():
    from tasks.models import Task
    from tasks.serializers import TaskSchema

    app = Flask(__name__)

    @app.route('/')
    def index():
        return '<h1>ECM Bonjour</h1>'

    @app.route('/user/<name>')
    def user(name):
        return render_template('user.html', name=name)

    @app.route('/professor')
    def my_api_route():
        return {
            "name": "Adrien",
            "birthday": "02 January",
            "age": 85,
            "sex": None,
            "friends": ["Amadou", "Mariam"]
        }

    @app.route('/todoz')
    def my_better_api_route():
        tasks = Task.query.all()
        return {"results": TaskSchema(many=True).dump(tasks)}

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    Migrate(app, db)

    return app
