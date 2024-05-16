import psycopg
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash


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

    @staticmethod
    def add_user(username, password, email, role, photo):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO \"User\" (username, password, email, role, photo) VALUES (%s, %s, %s, %s, %s) RETURNING username",
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

    @staticmethod
    def get_user_id(username):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM  \"User\" WHERE username = %s", (username,))
            user_id = cur.fetchone()
            return user_id

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
    def getDuels():
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM "Event"')

            result = cur.fetchall()

            if not result:
                print('Duels not found')
                return None
            return result

    def add_invitation_to_db(self, username, friendname):
        user_id = self.get_user_id(username)[0]
        friend_id = self.get_user_id(friendname)[0]
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO usersfriend (userid, friendid) VALUES(%s, %s)", (user_id, friend_id))

    @staticmethod
    def addDuels(data):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            if not data:
                print("Неверные параметры")
                return None

            creatorId = data.get("creatorId")
            name = data.get("name")
            description = data.get("description")
            hashPassword = generate_password_hash(data.get("password"))
            playgroundId = data.get("playgroundId")
            type = data.get("type")
            isOfficially = data.get("isOfficially")
            playersCount = data.get("playersCount")

            cur.execute('INSERT INTO "Event"(creatorid, name, description, password, playgroundid, type,'
                        ' isoficially, playerscount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (creatorId, name, description, hashPassword, playgroundId, type, isOfficially, playersCount))

            print("Дуэль добавлена")
            return True

    @staticmethod
    def addUserInEvent(data):
        with psycopg.connect(host=Config.DB_SERVER,
                             user=Config.DB_USER,
                             password=Config.DB_PASSWORD,
                             dbname=Config.DB_NAME) as con:
            cur = con.cursor()

            userId = data.get("userId")
            eventId = data.get("eventId")

            cur.execute('INSERT INTO userinevent(userid, eventid) VALUES (%s, %s)',
                        (userId, eventId
                         ))

            print("Участие пользователя успешно обработано")
            return True
