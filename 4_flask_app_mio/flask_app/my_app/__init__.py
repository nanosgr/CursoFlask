from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps

app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "fauth.login"


def role_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.rol.value != 'admin':
            #Acá colocamos la funcionalidad necesaria para manejar
            #los permisos usando la fx unauthorized de la libreria login_manager
            logout_user()
            return redirect(url_for('fauth.login'))

        return f(*args, **kwds)
    return wrapper


from my_app.product.product import product
from my_app.product.category import category
#from my_app.auth.views import auth
from my_app.fauth.views import fauth

#Rest API
from my_app.rest_api.product_api import product_view

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