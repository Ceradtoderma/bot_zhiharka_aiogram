import psycopg2
import urllib.parse as urlparse
from psycopg2 import Error
import os

class DataBase:

    def __init__(self, *args):

        self.args = args

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

    def insert(self):
        if len(self.args) != 4:
            self.err = f'Аргументов должно быть 4, а получено {len(self.args)}'
        else:
            try:
                insert_query = " INSERT INTO cheese (NAME, PRICE, DESCRIPTION, IMG) VALUES (%s, %s, %s, %s)"
                data_tuple = self.args
                self.cursor.execute(insert_query, data_tuple)
                self.connection.commit()
            except (Exception, Error) as error:
                self.err = "Ошибка при работе с PostgreSQL" + error
                print("Ошибка при работе с PostgreSQL", error)

    def read_all(self):
        try:
            self.cursor.execute("SELECT * from cheese")
            record = self.cursor.fetchall()
            return record

        except (Exception, Error) as error:
            self.err = "Ошибка при работе с PostgreSQL: \n" + error

    def read_name(self):
        if len(self.args) == 1:
            try:
                self.cursor.execute(f"""SELECT * from cheese where name='{self.args[0]}'""")
                record = self.cursor.fetchall()
                return record
            except (Exception, Error) as error:
                self.err = "Ошибка при работе с PostgreSQL: \n" + str(error)

    def read_id(self):
        if len(self.args) == 1:
            try:
                self.cursor.execute(f"""SELECT * from cheese where id='{self.args[0]}'""")
                record = self.cursor.fetchone()
                return record
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

    print(dbname, user, password, host, port)

    db = DataBase()
    print(db.read_all())


