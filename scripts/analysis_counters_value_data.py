import csv
import datetime as dt
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from time import sleep


class PostgresDataUpdater:
    def __init__(self, connection: _connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def count_records(self, table_name) -> int:
        query = f'SELECT COUNT(*) FROM {table_name};'
        self.cursor.execute(query)
        return int(self.cursor.fetchall()[0][0])

    def load_record(self, table_name, id):
        query = f"SELECT * FROM {table_name} WHERE id='{str(id)}';"
        self.cursor.execute(query)
        data = self.cursor.fetchall()[0]
        return data

    def load_counters_record(self, table_name, time_start:dt.datetime, time_end:dt.datetime):
        query = f"SELECT * FROM {table_name} WHERE time>='{time_start}' AND time<='{time_end}';"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def analysis_counters_record(self,table_name, time_start:dt.datetime, time_end:dt.datetime,
                               line_number=1, k=1.0, old_value=0):
        counters = self.load_counters_record(table_name=table_name,
                                         time_start=time_start,
                                         time_end=time_end)
        length_pred = 0
        for counter in counters:
            id = counter[0]
            lengths = counter[2]
            length = int(float(lengths[line_number-1]/1000))

            print((counter[1], length, length - length_pred))
            length_pred = length


if __name__ == '__main__':
    load_dotenv()
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user':  os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           #'host': os.environ.get('DB_HOST', 'db'),
           'host': '127.0.0.1',
           # 'host': 'localhost',
           'port': 5432,
           }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as connection:
        print(connection)
        pdl = PostgresDataUpdater(connection)
        pdl.analysis_counters_record(table_name='counters',
                                 time_start=dt.datetime(2026, 3, 29, 14, 10, 0),
                                 time_end=dt.datetime(2026, 3, 29, 15, 50, 0),
                                 line_number=76,

                                )

        print('Записей в таблице counters  = ', pdl.count_records('counters'))
