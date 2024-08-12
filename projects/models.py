# Create your models here.
from django.db import models
import oracledb
from urllib.parse import quote_plus
from datetime import datetime
import pandas as pd

d = r'C:\Users\met.officer4\Downloads\instantclient-basic-windows.x64-21.13.0.0.0dbru\instantclient_21_13'
oracledb.init_oracle_client(d)
DB_URL = "safetd/safetd@//itsc-c2-scan:1521/SCTDDB"


# Function to establish a database connection
def connect_to_database():
    connection = oracledb.connect(DB_URL)
    return connection


class Project(models.Model):

    @classmethod
    def fetch_all(cls):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TD_AMR.FDR_INFO ORDER BY STATION")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_details_by_station(cls):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT 
                            CASE 
                                WHEN INSTR(STATION, ' ') > 0 AND INSTR(SUBSTR(STATION, INSTR(STATION, ' ') + 1), '/') > 0 THEN 
                                    SUBSTR(STATION, 1, INSTR(STATION, ' ') - 1)
                                ELSE 
                                    STATION 
                            END AS STATION
                        FROM TD_AMR.FDR_INFO ORDER BY STATION""")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_details_by_category(cls, station):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TD_AMR.FDR_INFO WHERE STATION LIKE :STATION || '%'", 
                       {'STATION': station})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_details_by_feeder(cls, station_name):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM TD_AMR.FDR_INFO WHERE
                       STATION IS NOT NULL AND CATEGORY='Feeder' 
                       AND STATION LIKE :STATION || '%'""",
                       {'STATION': station_name})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_details_by_option(cls, st_name, fd_name):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM TD_AMR.FDR_INFO WHERE STATION LIKE :STATION || '%' AND 
                       REPLACE(REPLACE(FEEDER_NAME, '/',''),'//','') = :FEEDER_NAME""",
                       {'STATION':st_name,'FEEDER_NAME':fd_name})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]
    
    @classmethod
    def fetch_station_by_dtr(cls, sname):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT(STATION) FROM TD_AMR.FDR_INFO 
                       where REPLACE(REPLACE(:SNAME,'/',''),'.',' ') LIKE STATION || '%'
                       OR REPLACE(REPLACE(:SNAME,'/',''),'.',' ') LIKE '%' || STATION || '%'""",
                       {'SNAME':sname})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_details_by_dtr(cls, station):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""SELECT SNAME FROM HTMETER.SINFO 
                       where REPLACE(REPLACE(SNAME,'/',''),'.',' ') LIKE :STATION || '%'
                       OR REPLACE(REPLACE(SNAME,'/',''),'.',' ') LIKE '%' || :STATION || '%'""",
                       {'STATION':station})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_details_by_dtr_category(cls, dtr_id):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""select * from HTMETER.SINFO
                       where REPLACE(REPLACE(SNAME,'/',''),'.','') = :SNAME""",
                       {'SNAME': dtr_id})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]

    # @staticmethod
    # def insert_details(station_name, feeder_name, child_type, dt1, dt2):
    #     """
    #     Insert details into the fdr_aud_matrix table.
    #     """
    #     connection = connect_to_database()

    #     cursor = connection.cursor() 

    #     child_code = 'SCODE' if child_type == 'dtr' else 'CONS_NUM'
        

    #     sql_query = """
    #     INSERT INTO TD_AMR.FDR_AUD_MATRIX (station, feeder_code, feeder_name, child_code, child_type, dt1, dt2)
    #     VALUES (:STATION, (SELECT FEEDER_CODE FROM TD_AMR.FDR_INFO WHERE REPLACE(REPLACE(FEEDER_NAME, '/',''),'//','') = :FEEDER_NAME),
    #             :FEEDER_NAME, (SELECT SCODE FROM HTMETER.SINFO WHERE REPLACE(REPLACE(SNAME,'/',''),'.','')=:child_type), :child_type, to_date(:from_date,'YYYY-MM-DD'), to_date(:to_date,'YYYY-MM-DD'))
    #     """
    #     cursor.execute(sql_query, {'STATION':station_name, 'FEEDER_NAME':feeder_name, 'child_type': child_type, 'from_date':dt1, 'to_date':dt2})

    #     cursor.close()
    #     connection.commit()
    #     connection.close()

    # @classmethod
    # def fetch_requested_details(cls, station, feeder, dtrs, hts, from_date, to_date):
    #     connection = connect_to_database()
    #     cursor = connection.cursor()
    #     cursor.execute("""select * from TD_AKMR""",
    #                    {'SNAME': dtr_id})
    #     columns = [col[0] for col in cursor.description]
    #     rows = cursor.fetchall()
    #     cursor.close()
    #     connection.close()

    #     return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def fetch_overall(cls):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""select station,feeder_code,feeder_name,dt1,dt2
                       from TD_AMR.FDR_AUD_MATRIX
                       group by station,feeder_code,feeder_name,dt1,dt2""")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]
    
    @classmethod
    def fetch_overall_consumption(cls,feeder_code,date):
        consumption = f"""
                        select y.*,
                        (
                        select sum(SIGMA_KWH) from TD_AMR.FDR_AUD_DATA d where d.dt = y.dt and d.code = y.feeder_code
                        ) as feeder_sigma_kwh,
                        (
                        select count(*) from TD_AMR.FDR_AUD_DATA d where d.dt = y.dt and d.code = y.feeder_code
                        ) as feeder_sigma_kwh_count,
                        (
                        select sum(SIGMA_KWH) from TD_AMR.FDR_AUD_DATA d where typ = 'D' and d.dt = y.dt and d.code in 
                        (select child_code from TD_AMR.FDR_AUD_MATRIX m where m.feeder_code = y.feeder_code )
                        ) as dtr_sigma_kwh,
                        (
                        select count(*) from TD_AMR.FDR_AUD_DATA d where typ = 'D' and d.dt = y.dt and d.code in
                        (select child_code from TD_AMR.FDR_AUD_MATRIX m where m.feeder_code = y.feeder_code )
                        ) as dtr_sigma_kwh_count,
                        (
                        select sum(SIGMA_KWH) from TD_AMR.FDR_AUD_DATA d where typ = 'H' and d.dt = y.dt and d.code in 
                        (select child_code from TD_AMR.FDR_AUD_MATRIX m where m.feeder_code = y.feeder_code )
                        ) as htc_sigma_kwh,
                        (
                        select count(*) from TD_AMR.FDR_AUD_DATA d where typ = 'H' and d.dt = y.dt and d.code in
                        (select child_code from TD_AMR.FDR_AUD_MATRIX m where m.feeder_code = y.feeder_code )
                        ) as htc_sigma_kwh_count
                        from
                        (
                        select x.station,x.feeder_code,x.feeder_name,(x.dt1+level-1) dt
                        from
                        (
                        select station, feeder_code, feeder_name, dt1, dt2
                        from td_amr.fdr_aud_matrix m
                        where m.feeder_code = '{feeder_code}' and m.dt2 = to_date('{date}','ddmmrr')
                        group by station, feeder_code, feeder_name, dt1, dt2
                        ) x
                        connect by level <= dt2-dt1+1
                        ) y
                        """
        connection = connect_to_database()
        cursor = connection.cursor()
        # cursor.execute(consumption,{'feeder_code':feeder_code,'date':date})
        cursor.execute(consumption)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(zip(columns, row)) for row in rows]
        
    