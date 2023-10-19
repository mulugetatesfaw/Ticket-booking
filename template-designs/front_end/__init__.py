
from front_end.auth import auth
from flask import Flask
from models import storage
from flask_login import LoginManager
from models.user import User
from front_end.views import views
"""from front_end.auth import auth"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'here is the secret for our application'


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

app.register_blueprint(views, url_prefix='/')

app.register_blueprint(auth, url_prefix='/')


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return storage.get(User, id)
