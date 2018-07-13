from flask import Blueprint
import jwt
from flask import request, jsonify
from Utils import Config, MongoConn, PwdUtils
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/user')


# user registration general
@bp.route('/')
def show_user_welcome():
    return jsonify({'title': "Welcome to user endpoint for user registration /register and authentication /authenticate"})


# get the access token
@bp.route('/authenticate', methods=['POST'])
def authenticate_user():
    user = MongoConn.get_user_col()

    username = request.json['username']
    password = request.json['password']

    u = user.find_one({'username': username})

    if u is None:
        return jsonify({'result': "Failed, user no not existed!"})
    else:
        pwd_hash = u['password']
        if (PwdUtils.verify_password(password, pwd_hash)):
            token = jwt.encode({'username': username, 'password': pwd_hash}, Config.API_SECRET,
                               algorithm=Config.TOKEN_ALG).decode('utf-8')

            query = {'_id': u['_id']}
            update_record = {'$set':{
                'token': token,
                'token_created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }

            user.update_one(query, update_record, upsert=True)

            return jsonify({'result': "successful", "token": token, "username": username, "role": u['role']})

        else:
            return jsonify({'result': "Failed, pls provide correct password!"})


# register a new user
@bp.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    password = request.json['password']

    user = MongoConn.get_user_col()

    u = user.find_one({'username': username})

    if u is None:
        date = datetime.now()

        encrypted_pwd = PwdUtils.set_password(password)

        token = jwt.encode({'username': username, 'password': encrypted_pwd}, Config.API_SECRET,
                           algorithm=Config.TOKEN_ALG).decode('utf-8')

        user.insert({
            'create_at_ts': date.strftime('%S'),
            'create_at_str': date.strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'role': Config.TYPE_ONE,
            'password': encrypted_pwd,
            'token': token,
            'token_created_at': date.strftime('%Y-%m-%d %H:%M:%S')
        })

        return jsonify({'result': "successful", "token": token, "username": username, "role": Config.TYPE_ONE})
    else:
        return jsonify({'result': "Failed, user existed!"})

