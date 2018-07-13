from flask import Blueprint, session, jsonify
from Utils import Config
from Wrapper import AuthWrapper

bp = Blueprint('api_home', __name__, url_prefix='/api')


# API root
@bp.route('/', methods=['GET'])
@AuthWrapper.require_api_token
def enter_api_root():

    print (session)
    msg ={
        'Welcome': session['user']['username'],
        'Message': Config.API_DES
    }

    return jsonify(msg)