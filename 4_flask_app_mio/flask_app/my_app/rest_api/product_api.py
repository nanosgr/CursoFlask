from flask.views import MethodView
from my_app.product.model.product import Product
from my_app import app


class ProductAPI(MethodView):
    def get(self):
        products = Product.query.all()
        # Ahora utilizamos JSON
        return products

product_view = ProductAPI.as_view('product_view')
app.add_url_rule('/api/products/',
                 view_func=product_view,
                 methods=['GET'])