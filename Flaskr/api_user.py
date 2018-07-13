from flask import Blueprint, request, session, jsonify
from Utils import Config, MongoConn, JSONUtils
from bson import ObjectId
from Wrapper import AuthWrapper

bp = Blueprint('api_user', __name__, url_prefix='/api/users')


# api user root
@bp.route('/', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_users_api():
    msg = {
        'Welcome': session['user']['username'],
        'Message': Config.ADMIN_USER_API_DES
    }

    return jsonify(msg)


# list all the users
@bp.route('/list', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_users_api_list():
    user = MongoConn.get_user_col()

    users = list(user.find())

    return JSONUtils.JSONEncoder().encode(users)


# give a role to the user
@bp.route('/set_role', methods=['post'])
@AuthWrapper.require_api_token
# @AuthWrapper.require_admin_right
def admin_users_api_set_role():
    user = MongoConn.get_user_col()
    u = user.find_one({'_id':ObjectId(request.json['user_id'])})
    role = request.json['user_role']
    print(role)
    if role == Config.ADMIN or role == Config.TYPE_ONE or role == Config.TYPE_TWO or role == Config.TYPE_THREE:

      #There are four types of users. Set role according to the request.

      user.update_one({'_id': u['_id']},{'$set': {'role': role}}, upsert=False)
      return jsonify({'result': "successful", "msg": "User " + u['username'] + "\'s role has been changed to " + role + "."})
    else:

      return jsonify({'result': "failed", "msg": role + " is not a valid user role."})


# remove a user
@bp.route('/<user_id>', methods=['DELETE'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_users_api_remove(user_id):
    user = MongoConn.get_user_col()
    u = user.find_one({'_id': ObjectId(user_id)})

    if u is not None:
        user.delete_one({'_id': ObjectId(user_id)})
        return jsonify({'result': "successful", "msg": "User " + u['username'] + " has been removed."})

    else:
        return jsonify({'result': "failed", "msg": "User " + u['username'] + " does not exist."})
