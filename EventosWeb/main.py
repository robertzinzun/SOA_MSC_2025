from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap

app=Flask(__name__)
Bootstrap(app)
app.secret_key='MyCla4ve'
@app.route('/')
def index():
    return render_template('usuarios/login.html')
@app.route('/principal')
def principal():
    return render_template('comunes/principal.html')
@app.route('/login',methods=['post'])
def login():
    return render_template('comunes/principal.html')
@app.route('/eventos',methods=['Get'])
def consultarEventos():
    return render_template('eventos/listar.html')
@app.route('/eventos/nuevo',methods=['get'])
def nuevaSolicitud():
    return render_template('eventos/crear.html')
@app.route('/eventos/ver/<int:id>')
def verSolicitud(id):
    return render_template('eventos/editar.html')
@app.route('/eventos/reprogramar',methods=['Post'])
def reprogramar():
    return render_template('eventos/listar.html')
if __name__ == '__main__':
    app.run(host="127.0.0.1",port=7000,debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
