from flask import Blueprint, render_template, flash, request, redirect, url_for
from werkzeug.exceptions import abort

from my_app.auth.model.user import User, UserForm
from my_app import db

from my_app.product.model.product import ProductForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=('GET', 'POST'))
def register():
   form = UserForm(meta={'csrf':False})

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