import csv
import datetime as dt
import os
from datetime import datetime

import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from time import sleep


class PostgresDataLoader:
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

    def add_counters_record(self,
                               in_time: dt.datetime,
                               lengths: str,
                               connection_counters: str = '{0}',
                           ):
            insert_query = """ INSERT INTO counters (time, lengths, connection_counters) VALUES (%s,%s, %s)"""
            self.cursor.execute(insert_query, (in_time, lengths, connection_counters))
            connection.commit()

    def read_old_data_csv_file(self, file_name):
        date = dt.datetime.strptime(os.path.split(file_name)[1], "Lines_data_%Y_%m_%d.csv")
        print(date)
        with open(file_name, newline='') as f:
            for row in csv.reader(f, delimiter=';', quotechar='"'):
                if row[0] != 'Time - 7h':
                    time = dt.datetime.strptime(row[0], '%H:%M')
                    dtime = dt.timedelta(hours=time.hour,
                                         minutes=time.minute)
                    dtime_7_hours = dt.timedelta(hours=7)
                    date_time = date + dtime + dtime_7_hours
                    print(date_time)
                    row = [x if x != '' else '0' for x in row]
                    lengths = '{' + ','.join(row[1:]) + '}'

                    self.add_counters_record(date_time, lengths)
                    print(row)
                    print(lengths)

    def load_old_data(self):
        self.read_old_data_csv_file(file_name = '/home/amd/projects/kmv_2/app/Lines_data_2021_5_24.csv')


POSTGRES_PASSWORD = 'secret'
POSTGRES_USER = 'username'
POSTGRES_DB = 'lines_database'

if __name__ == '__main__':
    sleep(5)
    # dsl = {'dbname': POSTGRES_DB, 'user': POSTGRES_USER, 'password': POSTGRES_PASSWORD, 'host': 'db', 'port': 5432}
    dsl = {'dbname': POSTGRES_DB, 'user': POSTGRES_USER, 'password': POSTGRES_PASSWORD, 'host': 'localhost', 'port': 5432}
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as connection:
        print(connection)
        pdl = PostgresDataLoader(connection)
        pdl.load_old_data()
        print('Записей в таблице counters  = ', pdl.count_records( 'counters'))
