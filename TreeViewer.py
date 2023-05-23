from conecta_db import Conn_DB
from flask import Flask, render_template, request, redirect, session, flash, url_for


class Carregamento:
    def __init__(self, carregamento):
        self.carregamento = carregamento


lista_ordens = []
app = Flask(__name__)
app.secret_key = 'kbca'


@app.route('/')
def index():
    return render_template('template.html', titulo='Ordens', itens=lista_ordens)


@app.route('/criar', methods=['POST', ])
def criar():
    carrega = request.form['ordem']
    car = Conn_DB(carrega)
    df = car.focco()
    nv_1 = df.loc[df['DESC_TECNICA'].str.contains("EXP"), 'NUM_ORDEM']
    print(nv_1)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='10.40.3.48', port=8000, debug=True)
