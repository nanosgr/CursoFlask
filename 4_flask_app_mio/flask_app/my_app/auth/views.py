from flask import Blueprint, session, render_template, flash, request, redirect, url_for
from werkzeug.exceptions import abort

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db

from my_app.product.model.product import ProductForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=('GET', 'POST'))
def register():
   form = RegisterForm(meta={'csrf':False})

   if form.validate_on_submit():

      if User.query.filter_by(username=form.username.data).first():
         flash('El usuario ya existe', 'danger')
      else:
         # Creamos el usuario
         p = User(form.username.data, form.password.data)
         db.session.add(p)
         db.session.commit()
         flash("Usuario creado con éxito")
      
      return redirect(url_for('auth.register'))

   return render_template('auth/register.html', form=form)


@auth.route('/login', methods=('GET', 'POST'))
def login():
   form = LoginForm(meta={'csrf': False})

   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user and User.check_password(user, form.password.data):
         # Registramos la sesión.
         session['username'] = user.username
         session['rol'] = user.rol.value
         session['id'] = user.id
         flash("Bienvenido nuevamente " + user.username)
         return redirect(url_for('product.index'))
      else:
         # Error de password
         flash('Usuario o Contraseña Incorrectos', 'danger')

   return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    # Se usa en este caso el método pop para eliminar
    # cada uno de los elementos de session
    session.pop('username')
    session.pop('id')
    session.pop('rol')

    return redirect(url_for('auth.login'))
