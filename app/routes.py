import flask
from app import app, db


@app.route('/')
def index():
    return 'Index Page'


@app.route('/news')
def hello():
    print(db.getNews())
    return 'Hello, World'
