import flask
from app import app, db


@app.route('/')
def index():
    return 'Index Page'


@app.route('/news')
def retNews():
    news = db.getNews()

    if not news:
        return []  # "No avaliable tracks"

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


