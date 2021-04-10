from my_app import app

@app.route('/')
@app.route('/hello')
def hello():
   return "Hola mundo!!!!"