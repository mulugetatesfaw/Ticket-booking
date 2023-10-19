from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.buses import *
from api.v1.views.bus_service import *
from api.v1.views.users import *
from api.v1.views.ticket import *
from api.v1.views.route import *
from flask import Blueprint
from api.v1.views.tickets import *
