from flask import request, jsonify
from werkzeug.security import generate_password_hash

from app import app, db


@app.route('/')
def index():
    return 'Last edit - 23:07'


@app.route('/news')
def retNews():
    news = db.getNews()

    if not news:
        return []

    newsList = []
    for el in news:
        dict = {
            'id': el[0],

            'userId': el[1],
            'dateStamp': el[2],
            'description': el[3]
        }
        newsList.append(dict)
    return newsList


@app.route('/playgrounds')
def retPlaygrounds():
    playgrounds = db.getPlaygrounds()

    if not playgrounds:
        return []

    playgroundList = []
    for el in playgrounds:
        dict = {
            'id': el[0],
            'name': el[1],
            'geolocation': el[2]
        }
        playgroundList.append(dict)
    return playgroundList


@app.route('/friends')
def retFriends():
    userId = request.args.get('userId')

    friends = db.getFriendsById(userId)

    if not friends:
        return []

    friendsList = []
    for el in friends:
        dict = {
            'friendId': el[0]
        }
        friendsList.append(dict)
    return friendsList


@app.route("/registration", methods=["POST"])
def registration():
    data = request.get_json()
    if not data:
        return jsonify("Missing data"), 400

    username = data.get('username')
    mail = data.get('mail')
    password = data.get('password')
    role = data.get('role')
    photo = data.get('photo')
    user = db.find_user_by_email(mail)

    if user:
        return jsonify("A user with such mail already exists")
    user = db.find_user_by_username(username)
    if user:
        return jsonify("A user with such name already exists")
    user = db.add_user(username, generate_password_hash(password), mail, role, photo)
    if user:
        user = db.find_user_by_username(username)
        return jsonify(id=user[0], username=user[1], email=user[3], photo=user[4], role=user[5]), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return "Bad request"

    user = db.getUserByLoginPassword(data)
    if user:
        return jsonify(id=user[0], username=user[1], email=user[3], photo=user[4], role=user[5]), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


@app.route('/followToUser', methods=["POST"])
def followToUser():
    data = request.get_json()
    if not data:
        return jsonify("Missing data"), 400
    userid = data.get('userid')
    friendid = data.get('friendid')

    db.add_invitation_to_db(userid, friendid)
    return jsonify(message='успешно подписались!'), 200


@app.route('/duels', methods=["GET", "POST"])
def duels():
    if request.method == "GET":
        duels = db.getDuels()

        if not duels:
            return []

        duelsList = []
        for el in duels:
            dict = {
                'id': el[0],
                'creatorId': el[1],
                'name': el[2],
                'description': el[3],
                'password': el[4],
                'playground': el[5],
                'type': el[6],
                'isOfficially': el[7],
                'playersCount': el[8]
            }
            duelsList.append(dict)
        return duelsList

    if request.method == "POST":
        data = request.get_json()

        if db.addDuels(data):
            return jsonify(message='Дуэль успешно добавлена'), 200
        else:
            return jsonify(message='При добавлении произошла ошибка'), 400


@app.route('/takePartInEvent', methods=["POST"])
def takePartInEvent():
    data = request.get_json()

    if not data:
        return jsonify("Missing data"), 400

    db.addUserInEvent(data)
    return jsonify(message='Участие пользователя успешно обработано'), 200


@app.route('/getUserAchievement', methods=["GET"])
def getUserAchievement():
    data = request.get_json()
    if not data:
        return jsonify("Missing data"), 400
    userid = data.get('id')
    achievementList = db.getUserAchievement(userid)
    if not achievementList:
        return jsonify("Missing data"), 400
    achievementDict = []
    for achievement in achievementList:
        dict = {
            'id': achievement[0],
            'name': achievement[1],
            'photo': achievement[2]
        }
        achievementDict.append(dict)

    return achievementDict


@app.route('/eventMembers')
def eventMembers():
    eventId = request.args.get('eventId')

    events = db.getUsersByEvent(eventId)

    if not events:
        return []

    resList = []
    for el in events:
        dict = {
            'userId': el[0]
        }
        resList.append(dict)
    return resList


@app.route('/usersWithoutFriend', methods=["GET"])
def usersWithoutFriend():
    data = request.get_json()
    if not data:
        return jsonify("Missing data"), 400
    userid = data.get('userid')
    users = db.usersWithoutFriend(userid)
    if not users:
        return jsonify("Людей, кроме друзей, нет"), 400
    usersDict = []
    for user in users:
        dict = {
            'id': user[0],
            'username': user[1],
            'photo': user[2],
            'role': user[3]
        }
        usersDict.append(dict)

    return usersDict


@app.route('/notOfficialRankFromDuel', methods=["GET", "POST"])
def notOfficialRankFromDuel():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify("Missing data"), 400
        userid1 = data.get('userid1')
        userid2 = data.get('userid2')
        raiting_a = int(db.getNotOfficialRaiting(userid1))
        if raiting_a == 0:
            raiting_a = db.setNotOfficialRankFromDuelResult(userid1, 800)
        raiting_b = int(db.getNotOfficialRaiting(userid2))
        if raiting_b == 0:
            raiting_b = db.setNotOfficialRankFromDuelResult(userid2, 800)
        a_is_win = data.get('a_is_win')
        k = 30

        ea = 1 / (1 + 10 ** ((raiting_b - raiting_a) / 400))
        eb = 1 / (1 + 10 ** ((raiting_a - raiting_b) / 400))

        b_is_win = 1 - a_is_win

        new_raiting_a = int(raiting_a + k * (a_is_win - ea))
        new_raiting_b = int(raiting_b + k * (b_is_win - eb))

        db.updateNotOfficialRankFromDuelResult(userid1, new_raiting_a)
        db.updateNotOfficialRankFromDuelResult(userid2, new_raiting_b)

        return jsonify("Изменения успешно внесены"), 200

    elif request.method == "GET":
        data = request.get_json()
        if not data:
            return jsonify("Missing data"), 400
        userid1 = data.get('userid1')
        userid2 = data.get('userid2')
        res1 = int(db.getNotOfficialRaiting(userid1))
        if not res1:
            res1 = 800
        res2 = int(db.getNotOfficialRaiting(userid2))
        if not res2:
            res2 = 800

        return jsonify(res1, res2)


@app.route('/getProfile', methods=["GET"])
def getProfile():
    data = request.get_json()
    if not data:
        return jsonify("Missing data"), 400
    idUser = data.get('id')

    user = db.get_user_by_id(idUser)
    if not user:
        return jsonify("Пользователь не найден"), 400
    return jsonify(user)
