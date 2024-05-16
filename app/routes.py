from flask import request, jsonify
from app import app, db
from werkzeug.security import generate_password_hash


@app.route('/')
def index():
    return 'Index Page'


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
    user = db.add_user(username,  generate_password_hash(password), mail, role, photo)
    if user:
        return jsonify(message='Вы успешно добавлены'), 200
    else:
        return jsonify(message='Неверные учетные данные'), 401


@app.route('/news')
def hello():
    print(db.getNews())
    return 'Hello, World'
