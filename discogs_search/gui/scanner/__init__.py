from flask import Blueprint

scanner = Blueprint('scanner', __name__)

from . import routes, events
