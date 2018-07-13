import jwt
from functools import wraps
from flask import request, session, Response, jsonify
from Utils import Config, MongoConn

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session

        # print (request.headers)

        headers = request.headers

        if Config.TOKEN_HEADER_KEY not in headers:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return Response("Access denied, pls provide " + Config.TOKEN_HEADER_KEY + " in http(s) header")
        else:
            try:
                token = headers[Config.TOKEN_HEADER_KEY].encode('utf-8')
                print(token)
                decode = jwt.decode(token, Config.API_SECRET, algorithms=Config.TOKEN_ALG)

                print (decode)

                session['user'] = decode
            except Exception as e:
                print (e)
                return Response("Access denied, pls provide correct " + Config.TOKEN_HEADER_KEY + "")

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_token


def require_admin_right(func):
    @wraps(func)
    def check_admin(*args, **kwargs):
        user = session['user']
        users = MongoConn.get_user_col()
        u = users.find_one({'username': user['username']})

        if u is None:
            return jsonify({'result': 'failed', 'reason': "Access denied, invalid token."})
            # return Response("Access denied, invalid token")
        else:
            print (u)
            if u['role'] == Config.ADMIN:
                return func(*args, **kwargs)
            else:
                return jsonify({'result': 'failed', 'reason': "Access denied, admin only."})
                # return Response("Access denied, admin only")
    return check_admin


def require_admin_write_right(func):
    wraps(func)
    def check_admin_write(*args, **kwargs):
        user = session['user']
        users = MongoConn.get_user_col()
        u = users.find_one({'username': user['username']})

        if u is None:
            return jsonify({'result': 'failed', 'reason': "Access denied, invalid token."})
        else:
            print (u)
            if u['role'] == Config.ADMIN or u['role'] != Config.TYPE_ONE:
                return func(*args, **kwargs)
            else:
                return jsonify({'result': 'failed', 'reason': "Access denied, type1 is readonly."})
    check_admin_write.__name__ = func.__name__
    return check_admin_write


def require_admin_delete_right(func):
    wraps(func)
    def check_admin_delete(*args, **kwargs):
        user = session['user']
        users = MongoConn.get_user_col()
        u = users.find_one({'username': user['username']})

        if u is None:
            return jsonify({'result': 'failed', 'reason': "Access denied, invalid token."})
        else:
            print (u)
            if u['role'] == Config.ADMIN or u['role'] == Config.TYPE_THREE:
                return func(*args, **kwargs)
            else:
                return jsonify({'result': 'failed', 'reason': "Access denied, admin or type3 only."})
    check_admin_delete.__name__ = func.__name__
    return check_admin_delete 


def require_admin_read_right(func):
    wraps(func)
    def check_admin_read(*args, **kwargs):
        user = session['user']
        users = MongoConn.get_user_col()
        u = users.find_one({'username': user['username']})

        if u is None:
            return jsonify({'result': 'failed', 'reason': "Access denied, invalid token."})
        else:
            print(u)
            if u['role'] == Config.ADMIN or u['role'] == Config.TYPE_ONE or u['role'] == Config.TYPE_TWO or u['role'] == Config.TYPE_THREE:
                return func(*args, **kwargs)
            else:
                return jsonify({'result': 'failed', 'reason': "Access denied, admin or type1,2,3 only."})
    check_admin_read.__name__ = func.__name__
    return check_admin_read


