from flask import Blueprint

services_blueprint = Blueprint('services', __name__, template_folder = "templates", static_folder = None)

from . import views