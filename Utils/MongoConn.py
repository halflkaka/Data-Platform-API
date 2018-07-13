import sys
from Utils import Config
from flask_pymongo import PyMongo

mongo = None


def init_db(app):
    app.config['MONGO_URI'] = Config.MONGO_URI
    global mongo
    mongo = PyMongo(app)


def get_user_col():
    return get_collection(Config.COL_USERS)


def get_endpoints_col():
    return get_collection(Config.COL_ENDPOINT)


def get_collection(name):
    if mongo is None:
        sys.exit("Pls init mongo connection first")
    return mongo.db[name]