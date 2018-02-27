from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown


bootstrap = Bootstrap()
db = SQLAlchemy()
config = Config()
login_manager = LoginManager()
pagedown = PageDown()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



def creat_app():
	app = Flask(__name__)
	bootstrap.init_app(app)
	Config.init_app(config,app)
	db.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint,url_prefix='/auth')

	return app
