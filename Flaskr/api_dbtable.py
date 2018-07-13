from flask import Blueprint, request, session, jsonify
from Utils import Config, MongoConn, JSONUtils, PostgreConn
from bson import ObjectId
from Wrapper import AuthWrapper
from datetime import datetime

bp = Blueprint('api_dbtable', __name__, url_prefix='/api/dbtable')

#create table
@bp.route('/', methods=['POST'])
@AuthWrapper.require_api_token
# @AuthWrapper.require_admin_right
def db_table_api_create():
    json = request.json

    try:
        PostgreConn.create_table(json)
            
        msg = {
                'Welcome': session['user']['username'],
                'Message': "Succesfully create table"
        }
    except:
        msg = {
            'Welcome': session['user']['username'],
            'Message': "Table already existed"
        }

    return jsonify(msg)

@bp.route('/select', methods=['POST'])
@AuthWrapper.require_api_token
def db_select():
    json = request.json

    rows = PostgreConn.db_table_select(json)

    return JSONUtils.JSONEncoder().encode(rows)

@bp.route('/create',methods=['POST'])
@AuthWrapper.require_api_token
def db_create():
    json = request.json

    PostgreConn.db_table_create(json)

    msg = {
                'Welcome': session['user']['username'],
                'Message': "Succesfully create table"
    }

    return jsonify(msg)

@bp.route('/drop', methods=['POST'])
@AuthWrapper.require_api_token
def db_drop():
    json = request.json

    PostgreConn.db_table_drop(json)

    msg = {
                'Welcome': session['user']['username'],
                'Message': "Succesfully drop"
    }

    return jsonify(msg)




