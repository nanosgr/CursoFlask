from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "fauth.login"

from my_app.product.product import product
from my_app.product.category import category
#from my_app.auth.views import auth
from my_app.fauth.views import fauth
# Importar las vistas
app.register_blueprint(product)
app.register_blueprint(category)
#app.register_blueprint(auth)
app.register_blueprint(fauth)

db.create_all()

@app.template_filter('mydouble')
def mydouble_filter(n):
    if n:
        return n*2
    return "Dato no válido"