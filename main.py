import cx_Oracle
import pandas as pd
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
    df = focco(carrega)
    nv_1 = df.loc[df['DESC_TECNICA'].str.contains("EXP"), 'NUM_ORDEM']
    print(nv_1)
    return redirect(url_for('index'))


def focco(carrega):
    dsn = cx_Oracle.makedsn("10.40.3.10", 1521, service_name="f3ipro")
    connection = cx_Oracle.connect(user=r"focco_consulta", password=r'consulta3i08', dsn=dsn, encoding="UTF-8")
    cur = connection.cursor()
    ordem = carrega.split()
    carr = ','.join(ordem)
    cur.execute(
        r"SELECT DISTINCT TPL.COD_ITEM,  "
        r"TOR.NUM_ORDEM, "
        r"TOR.QTDE,  "
        r"TIT.DESC_TECNICA  "
        r"FROM FOCCO3I.TITENS_PLANEJAMENTO TPL "
        r"INNER JOIN FOCCO3I.TITENS_EMPR EMP      ON TPL.ITEMPR_ID = EMP.ID "
        r"INNER JOIN FOCCO3I.TITENS TIT           ON EMP.ITEM_ID = TIT.ID  "
        r"INNER JOIN FOCCO3I.TORDENS TOR          ON TPL.ID = TOR.ITPL_ID "
        r"INNER JOIN FOCCO3I.TDEMANDAS TDE        ON TOR.ID = TDE.ORDEM_ID "
        r"INNER JOIN FOCCO3I.TORDENS_ROT ROT      ON TOR.ID = ROT.ORDEM_ID "
        r"INNER JOIN FOCCO3I.TORD_ROT_FAB_MAQ FAB ON ROT.ID = FAB.TORDEN_ROT_ID "
        r"INNER JOIN FOCCO3I.TMAQUINAS MAQ        ON FAB.MAQUINA_ID = MAQ.ID "
        r"INNER JOIN FOCCO3I.TITENS_PLAN_FUNC PLA ON TPL.ID = PLA.ITPL_ID "
        r"INNER JOIN FOCCO3I.TFUNCIONARIOS TFUN   ON PLA.FUNC_ID = TFUN.ID "
        r"INNER JOIN FOCCO3I.TSRENG_ORDENS_VINC_CAR VINC ON TOR.ID = VINC.ORDEM_ID "
        r"INNER JOIN FOCCO3I.TSRENGENHARIA_CARREGAMENTOS CAR  ON VINC.CARERGAM_ID = CAR.ID "
        r"WHERE TOR.ID IN( "
        r"                SELECT TOR.ID "
        r"                FROM FOCCO3I.TORDENS TOR "
        r"                INNER JOIN FOCCO3I.TSRENG_ORDENS_VINC_CAR VINC      ON TOR.ID = VINC.ORDEM_ID "
        r"                INNER JOIN FOCCO3I.TSRENGENHARIA_CARREGAMENTOS CAR  ON VINC.CARERGAM_ID = CAR.ID "
        r"                AND CAR.SITUACAO = 'A' "
        r"                AND CAR.CARREGAMENTO in (" + carr + ") "
        r"                ) "
    )
    df = cur.fetchall()
    df = pd.DataFrame(df, columns=['COD_ITEM', 'NUM_ORDEM', 'QTDE', 'DESC_TECNICA'])
    print(df.to_string())
    return df


if __name__ == '__main__':
    app.run(host='10.40.3.48', port=8000, debug=True)
