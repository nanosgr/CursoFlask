# from my_app import app
from flask import Blueprint, render_template, flash, request, redirect, url_for
from werkzeug.exceptions import abort
from flask_login import login_required

from my_app import db, role_admin_need
from my_app.product.model.category import Category
from my_app.product.model.category import CategoryForm

category = Blueprint('category', __name__)

@category.before_request
@login_required
@role_admin_need
def constructor():
    pass

@category.route('/category')
@category.route('/category/<int:page>')
def index(page=1):
   return render_template('category/index.html', categories=Category.query.order_by(Category.id.asc()).paginate(page, 5))


@category.route('/category-create', methods=('GET', 'POST'))
def create():
   form = CategoryForm(meta={'csrf':False})
   if form.validate_on_submit():
      # Creamos la categoría
      p = Category(request.form['name'])
      db.session.add(p)
      db.session.commit()
      flash("Categoría creada con éxito")
      return redirect(url_for('category.index'))

   return render_template('category/create.html', form=form)

@category.route('/category-update/<int:id>', methods=('GET', 'POST'))
def update(id):
   category = Category.query.get_or_404(id)
   form = CategoryForm(meta={'csrf':False})

   print(category.products)

   if request.method == 'GET':
      form.name.data = category.name

   if form.validate_on_submit():
      # Creamos el categoryo
      category.name = form.name.data

      db.session.add(category)
      db.session.commit()
      flash("Categoría actualizada con éxito")
      return redirect(url_for('category.index'))

   return render_template('category/update.html', category=category, form=form)   

@category.route('/category-delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
   category = Category.query.get_or_404(id)

   db.session.delete(category)
   db.session.commit()
   flash("Categoryo eliminado con éxito")
   return redirect(url_for('category.index'))

@category.route('/test')
def test():
   p = Category.query.limit(2).first()
   print(p)
   p = Category.query.order_by(Category.id.desc()).all()
   print(p)

   return "Flask"

@category.route('/filter')
@category.route('/filter/<int:id>')
def filter(id):
   category = PRODUCTS.get(id)
   return render_template('category/filter.html', category=category)