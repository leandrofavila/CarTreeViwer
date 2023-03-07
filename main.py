import cx_Oracle
import pandas as pd
from flask import Flask, render_template, request, redirect, session, flash, url_for


def recursaobd(ordem):
    dsn = cx_Oracle.makedsn("10.40.3.10", 1521, service_name="f3ipro")
    connection = cx_Oracle.connect(user=r"focco_consulta", password=r'consulta3i08', dsn=dsn, encoding="UTF-8")
    cur = connection.cursor()
    carregamento = ','.join('388300')
    exps = ','.join('63883')
    cur.execute(
        r"SELECT DISTINCT TEMPI.COD_ITEM,TIT.DESC_TECNICA, TOR.NUM_ORDEM, TOR.DT_EMISSAO "
        r"FROM FOCCO3I.TITENS_EMPR TEMPI "
        r",FOCCO3I.TROTEIRO TEIRO "
        r",FOCCO3I.TITENS TIT "
        r",FOCCO3I.TORDENS_VINC_ITPDV ITP "
        r",FOCCO3I.TITENS_PDV PDV "
        r",FOCCO3I.TPEDIDOS_VENDA VEN "
        r",FOCCO3I.TROT_FAB_MAQ TRMA "
        r",FOCCO3I.TMAQUINAS TMA "
        r",FOCCO3I.TORDENS TOR "
        r",FOCCO3I.TITENS_PLANEJAMENTO TPL "
        r",FOCCO3I.TOPERACAO TOP "
        r",FOCCO3I.TORDENS_ROT ROT "
        r",FOCCO3I.TSRENGENHARIA_CARREGAMENTOS CAR "
        r",FOCCO3I.TSRENG_ORDENS_VINC_CAR VINC "
        r"WHERE TEMPI.ID = TEIRO.ITEMPR_ID "
        r"AND TEIRO.ID= TRMA.TROTEIRO_ID "
        r"AND TEMPI.ITEM_ID = TIT.ID "
        r"AND TOR.ITPL_ID = TPL.ID "
        r"AND TPL.ITEMPR_ID = TEMPI.ID "
        r"AND ITP.ITPDV_ID = PDV.ID "
        r"AND ITP.ORDEM_ID = TOR.ID "
        r"AND PDV.PDV_ID = VEN.ID "
        r"AND TRMA.MAQUINA_ID = TMA.ID "
        r"AND ROT.ORDEM_ID = TOR.ID "
        r"AND TOP.ID = ROT.OPERACAO_ID "
        r"AND TOR.ID = VINC.ORDEM_ID "
        r"AND VINC.CARERGAM_ID = CAR. ID "
        r"AND TEMPI.COD_ITEM IN (SELECT DISTINCT TITFI.COD_ITEM "
        r"                        FROM FOCCO3I.TCAD_EST_ITE TCAD "
        r"                        ,FOCCO3I.TITENS TITPA "
        r"                        ,FOCCO3I.TITENS TITFI "
        r"                        ,FOCCO3I.TITENS_ENGENHARIA TENG "
        r"                        ,FOCCO3I.TITENS_EMPR TEMP "
        r"                        WHERE TCAD.PAI_ID =TITPA.ID "
        r"                        AND TCAD.FILHO_ID = TITFI.ID "
        r"                        AND TITFI.ID = TEMP.ITEM_ID "
        r"                        AND TEMP.ID = TENG.ITEMPR_ID "
        r"                        /*AND TENG.TP_ITEM = 'F'*/  START WITH TITPA.COD_ITEM in (" + exps + ") CONNECT BY PRIOR TCAD.PAI_ID = TCAD.FILHO_ID) "
        r"AND TIT.SIT = 1 "
        r"AND CAR.CARREGAMENTO in  (" + carregamento + ") "
    )
    df_recursao = cur.fetchall()
    df_recursao = pd.DataFrame(df_recursao, columns=['COD_ITEM', 'DESC_TECNICA', 'NUM_ORDEM', 'DT_EMISSAO'])
    print(df_recursao)
    return df_recursao


class Troca_dem:
    def __init__(self, carregamento):
        self.carregamento = carregamento


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('template.html', titulo='Ordens')


if __name__ == '__main__':
    app.run(host='192.168.1.2', port=8000, debug=True)
