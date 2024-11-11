import datetime as dt
import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
from time import sleep


POSTGRES_PASSWORD = 'secret'
POSTGRES_USER = 'username'
POSTGRES_DB = 'lines_database'


if __name__ == '__main__':
    sleep(5)
    dsl = {'dbname': POSTGRES_DB, 'user': POSTGRES_USER, 'password': POSTGRES_PASSWORD, 'host': 'db', 'port': 5432}
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as connection:
        print(connection)
        try:
            cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных в таблицу
            insert_query = """ INSERT INTO counters (time, lengths, connection_counters) VALUES (%s,%s, %s)"""
            item_time = dt.datetime(
                year=2026,
                month=11,
                day=12,
                hour=12,
                minute=34
            )
            lengths = '{1, 10, 100, 1000}'
            connection_counters = '{1, 0, 1, 0}'
            cursor.execute(insert_query, (item_time, lengths, connection_counters))
            connection.commit()
            print(" запись успешно вставлена")

            # Получить результат
            # cursor.execute("SELECT * from counters where time=%s", (item_time,))
            # record = cursor.fetchall()
            # print("Результат", record)

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
