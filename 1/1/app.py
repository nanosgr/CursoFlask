from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/hola')
def HelloWorld():
    return 'Hola Mundo Flask!! '

@app.route('/test/')
@app.route('/test/<hi>')
def HelloWorldTest(hi='sebastian'):
    return 'Hola ' + hi

@app.route('/primer_html/<name>')
@app.route('/primer_html')
def primer_html(name='Sebastian'):
   return '''
   <html>
    <body>
        <h1>Hola Flask</h1>
        <p>Hola %s</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </body>
   </html>
   ''' % name

@app.route('/static_test')
def static_test():
   return "<img src='" + url_for("static", filename="img/logo-aerotec.png") + "'>"

@app.route('/mi_primer_template')
@app.route('/mi_primer_template/<name>')
def mi_primer_template(name=None):
   return render_template('view.html', name=name)

if __name__ == '__main__':
    app.run()