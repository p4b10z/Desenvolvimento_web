from flask import Flask, render_template, request
from controllers.ProblemaController import ProblemaController
from controllers.AutorController import AutorController
from controllers.StaticController import StaticController

app = Flask(__name__, template_folder='views', static_folder='static')

problema_controller = ProblemaController()
autor_controller = AutorController()
static_controller = StaticController()

@app.route('/')
def index():
    return problema_controller.index()

@app.route('/problema', methods=['GET', 'POST'])
def problema():
    if request.method == 'POST':
        dados = request.form.get('dados')
        return problema_controller.problema(dados)
    return problema_controller.problema()

@app.route('/autor')
def autor():
    return autor_controller.autor()

@app.route('/static/<path:filename>')
def static_files(filename):
    return static_controller.serve_static(filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)