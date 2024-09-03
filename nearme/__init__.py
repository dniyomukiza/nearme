import os
from flask import Flask
from .extensions import db
from .routes import main,login
from flask_login import LoginManager
from .models import User

login_manager=LoginManager()
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()

def create_app():
    app=Flask(__name__)
    app.secret_key =os.environ.get("SECRET_KEY")
    app.config['DEBUG'] = True
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
              # postgres://nearme_database_user:FQM2yrNKIFxXa6ONyYJGhup8QlEIaPVM@dpg-cplq9hij1k6c739ov3n0-a.oregon-postgres.render.com/nearme_database
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(main)

    return app

 