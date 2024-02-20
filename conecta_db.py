import pandas as pd
import cx_Oracle


class DB:
    def __init__(self):
        self.db_connection = None

    @staticmethod
    def get_connection():
        dsn = cx_Oracle.makedsn("10.40.3.10", 1521, service_name="f3ipro")
        connection = cx_Oracle.connect(user=r"focco_consulta", password=r'consulta3i08', dsn=dsn, encoding="UTF-8")
        cur = connection.cursor()
        return cur

    def car(self, carregamento):
        cur = self.get_connection()
        cur.execute(
            r"SELECT DISTINCT TPL.COD_ITEM,  "
            r"TOR.NUM_ORDEM, "
            r"TOR.QTDE,  "
            r"TOR.tipo_ordem, "
            r"TIT.DESC_TECNICA, "
            r"TFUN.NOME AS PLANEJADOR, "
            r"PDV.NUM_ITEM "
            r"FROM FOCCO3I.TITENS_PLANEJAMENTO TPL "
            r"INNER JOIN FOCCO3I.TITENS_EMPR EMP          ON TPL.ITEMPR_ID = EMP.ID "
            r"INNER JOIN FOCCO3I.TITENS TIT               ON EMP.ITEM_ID = TIT.ID  "
            r"INNER JOIN FOCCO3I.TORDENS TOR              ON TPL.ID = TOR.ITPL_ID "
            r"INNER JOIN FOCCO3I.TDEMANDAS TDE            ON TOR.ID = TDE.ORDEM_ID "
            r"INNER JOIN FOCCO3I.TORDENS_ROT ROT          ON TOR.ID = ROT.ORDEM_ID "
            r"INNER JOIN FOCCO3I.TORD_ROT_FAB_MAQ FAB     ON ROT.ID = FAB.TORDEN_ROT_ID "
            r"INNER JOIN FOCCO3I.TMAQUINAS MAQ            ON FAB.MAQUINA_ID = MAQ.ID "
            r"INNER JOIN FOCCO3I.TITENS_PLAN_FUNC PLA     ON TPL.ID = PLA.ITPL_ID "
            r"INNER JOIN FOCCO3I.TFUNCIONARIOS TFUN       ON PLA.FUNC_ID = TFUN.ID "
            r"INNER JOIN FOCCO3I.TORDENS_VINC_ITPDV IT    ON IT.ORDEM_ID = TOR.ID "
            r"INNER JOIN FOCCO3I.TITENS_PDV PDV           ON PDV.ID = IT.ITPDV_ID "
            r"WHERE TOR.ID IN( "
            r"                SELECT TOR.ID "
            r"                FROM FOCCO3I.TORDENS TOR "
            r"                INNER JOIN FOCCO3I.TSRENG_ORDENS_VINC_CAR VINC      ON TOR.ID = VINC.ORDEM_ID "
            r"                INNER JOIN FOCCO3I.TSRENGENHARIA_CARREGAMENTOS CAR  ON VINC.CARERGAM_ID = CAR.ID "
            r"                WHERE CAR.CARREGAMENTO IN (" + str(carregamento) + ") "
            r"                ) "
            r"GROUP BY TPL.COD_ITEM, TOR.NUM_ORDEM, TOR.QTDE, TIT.DESC_TECNICA, TFUN.NOME, TOR.tipo_ordem, PDV.NUM_ITEM "
        )
        df = cur.fetchall()
        df = pd.DataFrame(df, columns=['COD_ITEM', 'NUM_ORDEM', 'QTDE', 'TIPO_ORDEM', 'DESC_TECNICA', 'PLANEJADOR',
                                       'NUM_ITEM'])
        df['QTDE'] = df['QTDE'].astype(int)
        return df


    def filhos(self, carregamento, ordem):
        cur = self.get_connection()
        cur.execute(
            r"SELECT DISTINCT OPFI.NUM_ORDEM, TPL.COD_ITEM, OPPAI.DT_EMISSAO "
            r"FROM FOCCO3I.TORDENS OPPAI "
            r"INNER JOIN FOCCO3I.TDEMANDAS TDE                    ON TDE.ORDEM_ID = OPPAI.ID "
            r"INNER JOIN FOCCO3I.TORDENS OPFI                     ON OPFI.ITPL_ID = TDE.ITPL_ID "
            r"INNER JOIN FOCCO3I.TSRENG_ORDENS_VINC_CAR VINC      ON VINC.ORDEM_ID = OPFI.ID "
            r"INNER JOIN FOCCO3I.TSRENGENHARIA_CARREGAMENTOS CAR  ON CAR.ID = VINC.CARERGAM_ID "
            r"INNER JOIN FOCCO3I.TITENS_PLANEJAMENTO TPL          ON TPL.ID = OPFI.ITPL_ID "
            r"WHERE OPPAI.NUM_ORDEM IN ("+str(ordem)+") "
            r"AND CAR.CARREGAMENTO = "+str(carregamento)+" "
        )
        df = pd.DataFrame(cur.fetchall(), columns=["NUM_ORDEM", "COD_ITEM", "DT_EMISSAO"])
        cur.close()
        return df
