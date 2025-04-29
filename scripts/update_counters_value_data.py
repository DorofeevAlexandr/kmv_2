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

    def update_counters_record(self,table_name, time_start:dt.datetime, time_end:dt.datetime,
                               line_number=1, k=1.0):
        counters = self.load_counters_record(table_name=table_name,
                                         time_start=time_start,
                                         time_end=time_end)

        for counter in counters:
            id = counter[0]
            length = counter[2]
            if len(length) >= line_number:
                length[line_number-1] = int(float(length[line_number-1]) * k)

                print(counter)
                self.update_record(id=id,
                                   lengths=length)
            else:
                print(counter)

    def update_record(self,
                               id,
                               lengths,
                           ):
        str_lengths = '{' + ','.join(map(str, lengths)) + '}'
        query = """ UPDATE counters SET lengths = %s WHERE id = %s"""
        self.cursor.execute(query, (str_lengths, str(id)))
        connection.commit()


if __name__ == '__main__':
    load_dotenv()
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user':  os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           #'host': os.environ.get('DB_HOST', 'db'),
           'host': '192.168.0.246',
           # 'host': 'localhost',
           'port': 5432,
           }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as connection:
        print(connection)
        pdl = PostgresDataUpdater(connection)
        pdl.update_counters_record(table_name='counters',
                                 time_start=dt.datetime(2025, 4, 7, 10, 10, 0),
                                 time_end=dt.datetime(2025, 4, 28, 21, 50, 0),
                                 line_number=2,
                                 k=0.09802400846783833
                                )
        print('Записей в таблице counters  = ', pdl.count_records('counters'))
