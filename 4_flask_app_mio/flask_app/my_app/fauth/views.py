from flask import Blueprint, session, render_template, flash, request, redirect, url_for
from werkzeug.exceptions import abort

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db
from flask_login import login_user, logout_user, current_user, login_required
from my_app import login_manager

fauth = Blueprint('fauth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@fauth.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm(meta={'csrf': False})

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


@fauth.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash("Ya estás autenticado")
        return redirect(url_for('product.index'))

    form = LoginForm(meta={'csrf': False})

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.check_password(user, form.password.data):
            # Registramos la sesión.
            login_user(user)
            flash("Bienvenido nuevamente " + user.username)

            next = request.form['next']
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #     return abort(400)

            return redirect(next or url_for('product.index'))
        else:
            # Error de password
            flash('Usuario o Contraseña Incorrectos', 'danger')

    return render_template('auth/login.html', form=form)


@fauth.route('/logout')
def logout():
    # Se usa en este caso el método pop para eliminar
    # cada uno de los elementos de session
    logout_user()

    return redirect(url_for('fauth.login'))


@fauth.route('/protegido')
@login_required
def protegido():
    return "<h1>Vista protegida</h1>"
