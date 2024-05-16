from flask import request, jsonify
from werkzeug.security import generate_password_hash

from app import app, db


@app.route('/')
def index():
    return 'Index Page'


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
        return jsonify(message='Вы успешно добавлены'), 200
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