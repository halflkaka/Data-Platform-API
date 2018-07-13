from flask import Blueprint, request, session, jsonify
from Utils import Config, MongoConn, JSONUtils
from bson import ObjectId
from Wrapper import AuthWrapper
from datetime import datetime

bp = Blueprint('api_endpoints', __name__, url_prefix='/api/endpoints')


# endpoint management root
@bp.route('/', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_endpoint_api():
    msg = {
        'Welcome': session['user']['username'],
        'Message': Config.ADMIN_ENDPOINT_API_DES
    }

    return jsonify(msg)


# list all the endpoints
@bp.route('/list', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_endpoint_api_list():
    endpoint = MongoConn.get_endpoints_col()

    endpoints = list(endpoint.find())

    return JSONUtils.JSONEncoder().encode(endpoints)


# create an endpoint
@bp.route('/create', methods=['POST'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_endpoint_api_create():
    endpoint = MongoConn.get_endpoints_col()
    date = datetime.now()

    json = request.json

    # Duplicate name could happen here.

    endpoint.insert({
        'create_at_ts': date.strftime('%S'),
        'create_at_str': date.strftime('%Y-%m-%d %H:%M:%S'),
        'username': session['user']['username'],
        'endpoint_name': json['endpoint_name'], # Better have some restriction on no-space.
        'endpoint_desc': json['endpoint_desc'],
        'collection_list': json['collection_list'] # Better have some restriction on no-space.
    })

    return jsonify({'result': "successful", "msg": "Endpoint " + json['endpoint_name'] + " created"})


# remove a endpoint
@bp.route('/<endpoint_id>', methods=['DELETE'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_right
def admin_endpoint_api_remove(endpoint_id):

    endpoint = MongoConn.get_endpoints_col()
    ept = endpoint.find_one({'_id':ObjectId(endpoint_id)})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])
        collections = list(collection_list.find())
        for i in collections:
          print(i['collection_name'])
          print("finding " + i['collection_name'])

          c = MongoConn.get_collection(i['collection_name'])

          if c is not None:
            print("removing " + i['collection_name'])
            c.drop()

        collection_list.drop()
        endpoint.delete_one({'_id': ObjectId(endpoint_id)})
        msg = {'result':'successful','msg': "Endpoint removed."}
    else:
        msg = {'result':'failed','msg': "Endpoint does not exist."}

    return jsonify(msg)
