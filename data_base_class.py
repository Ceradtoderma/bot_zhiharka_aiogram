import psycopg2
import urllib.parse as urlparse
from psycopg2 import Error
import os


class DataBase:

    def __init__(self, *args):


        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        self.connection = psycopg2.connect(user=user,
                                           # пароль, который указали при установке PostgreSQL
                                           password=password,
                                           host=host,
                                           port=port,
                                           database=dbname)
        self.cursor = self.connection.cursor()
        self.err = ''

    def read_all(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            record = self.cursor.fetchall()
            return record

        except (Exception, Error) as error:
            self.err = "Ошибка при работе с PostgreSQL: \n" + error

    def read_one(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            record = self.cursor.fetchone()
            return record
        except (Exception, Error) as error:
            self.err = "Ошибка при работе с PostgreSQL: \n" + str(error)

    def insert(self, sql_query, *args):
        try:
            self.cursor.execute(sql_query, args)
            self.connection.commit()

        except (Exception, Error) as error:
            self.err = "Ошибка при работе с PostgreSQL: \n" + str(error)

    def update(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            self.connection.commit()

        except (Exception, Error) as error:
            self.err = "Ошибка при работе с PostgreSQL: \n" + str(error)

    def close(self):

        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    # print(dbname, user, password, host, port)

    db = DataBase()
    print(db.read_all())
    db.delete(14)
    print(db.read_all())


