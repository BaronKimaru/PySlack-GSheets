
import psycopg2
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from config import app_config




def create_app(config_name):
	"""Creates the app to run the program"""
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	register_blueprints(app)
	#intitialize_extensions(app)
	
	return app

def register_blueprints(app):
	from pages import pages_blueprint
	from services import services_blueprint
	
	app.register_blueprint(services_blueprint)
	app.register_blueprint(pages_blueprint)




