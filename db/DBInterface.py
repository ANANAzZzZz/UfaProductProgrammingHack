import psycopg
from config import Config
from werkzeug.security import check_password_hash


class DBInterface:
    @staticmethod
    def getNews():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()
            cur.execute('SELECT * FROM News')
            result = cur.fetchall()
            if not result:
                print('News not found')
                return None
            return result

    @staticmethod
    def find_user_by_email(email):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()
            cur.execute("SELECT * FROM \"User\" WHERE email = %s", (email,))
            result = cur.fetchone()
            if not result:
                return None
            return result

    @staticmethod
    def add_user(username, password, email, role, photo):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()
            cur.execute("INSERT INTO \"User\" (username, password, email, role, photo) VALUES (%s, %s, %s, %s, %s) RETURNING username",
                        (username, password, email, role, photo))
            result = cur.fetchone()
            con.commit()
            if not result:
                return None
            return result

    @staticmethod
    def find_user_by_username(username):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:

            cur = con.cursor()
            cur.execute("SELECT * FROM \"User\" WHERE username = %s", (username,))
            result = cur.fetchone()
            if not result:
                return None
            return result
