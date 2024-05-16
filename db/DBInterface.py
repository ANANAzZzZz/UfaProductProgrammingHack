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
    def getPlaygrounds():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM Playground')

            result = cur.fetchall()

            if not result:
                print('Playgrounds not found')
                return None
            return result

    @staticmethod
    def getFriendsById(userId):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT friendId FROM \"User" INNER JOIN usersfriend u on "User".id = u.userid'
                        ' WHERE userid = %s', (userId,))

            result = cur.fetchall()

            if not result:
                print('friends not found')
                return None
            return result
