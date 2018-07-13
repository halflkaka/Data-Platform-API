from flask import Blueprint, request, session, jsonify
from Utils import Config, MongoConn, JSONUtils
from bson import ObjectId
from Wrapper import AuthWrapper
from datetime import datetime
import json


bp = Blueprint('api_endpoint_collections', __name__, url_prefix='/api')


# endpoint root
@bp.route('/<endpoint_name>/', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_read_right
def general_endpoint_api(endpoint_name):
    endpoint = MongoConn.get_endpoints_col()

    ept = endpoint.find_one({'endpoint_name': endpoint_name})

    if ept is not None:
        msg = {
            'Welcome': session['user']['username'],
            'Message': Config.General_ENDPOINT_API_DES,
            'Endpoint_name': endpoint_name,
            'Endpoint_desc': ept['endpoint_desc']
        }

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)


# list all collection under a endpoint
@bp.route('/<endpoint_name>/list', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_read_right
def general_endpoint_api_list(endpoint_name):
    endpoint = MongoConn.get_endpoints_col()

    ept = endpoint.find_one({'endpoint_name': endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])

        collections = list(collection_list.find())

        return JSONUtils.JSONEncoder().encode(collections)

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)


# create a collection
@bp.route('/<endpoint_name>/create', methods=['POST'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_write_right
def general_endpoint_api_create(endpoint_name):
    endpoint = MongoConn.get_endpoints_col()

    ept = endpoint.find_one({'endpoint_name': endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])
        json = request.json
        c = collection_list.find_one({'collection_name': json['collection_name']})

        if c is None:
            date = datetime.now()

            _id = collection_list.insert({
                'collection_name': json['collection_name'],
                'collection_des': json['collection_des'],
                'create_at_ts': date.strftime('%S'),
                'create_at_str': date.strftime('%Y-%m-%d %H:%M:%S'),
                'username': session['user']['username'],
            })

            msg = {'result': 'successful', 'msg': "Collection " + json['collection_name'] + " is created",
                   'collection_id': str(_id)}

        else:
            msg = {'result': 'failed', 'msg': "Collection " + json['collection_name'] + " exists"}
    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)


# remove a collection
@bp.route('/<endpoint_name>/<collection_id>', methods=['DELETE'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_delete_right
def general_collection_remove_api(endpoint_name, collection_id):
    endpoint = MongoConn.get_endpoints_col()
    ept = endpoint.find_one({'endpoint_name': endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])
        c = collection_list.find_one({'_id': ObjectId(collection_id)})

        if c is not None:
            collection_list.delete_one({'_id': ObjectId(collection_id)})
            collection = MongoConn.get_collection(c['collection_name'])
            if collection is not None:
                collection.drop()
            msg = {'result': 'successful',
                   'msg': "Collection_ID " + collection_id + " has been removed from " + endpoint_name}
        else:
            msg = {'result': 'failed', 'msg': "Collection_ID " + collection_id + " does not exist in " + endpoint_name}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)


# the router to get collection information
@bp.route('/<endpoint_name>/<collection_id>/info', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_read_right
def general_collection_info_api(endpoint_name, collection_id):
    endpoint = MongoConn.get_endpoints_col()
    print(endpoint_name)
    ept = endpoint.find_one({'endpoint_name': endpoint_name})
    print(session['user'])

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])
        c = collection_list.find_one({'_id': ObjectId(collection_id)})
        print(c)

        if c is not None:
            msg = {
                'Welcome': session['user']['username'],
                'Message': Config.General_ENDPOINT_API_DES,
                'Endpoint_name': endpoint_name,
                'Endpoint_desc': ept['endpoint_desc'],
                'Collection_name': c['collection_name'],
                'Collection_desc': c['collection_des']
            }
        else:
            msg = {'result': 'failed', 'msg': "Collection_ID " + collection_id + " does not exist in " + endpoint_name}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)


# get data from a collection
@bp.route('/<endpoint_name>/<collection_id>', methods=['GET'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_read_right
def general_endpoint_api_get(endpoint_name, collection_id):
    endpoint = MongoConn.get_endpoints_col()

    ept = endpoint.find_one({'endpoint_name': endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])

        c = collection_list.find_one({'_id': ObjectId(collection_id)})

        limit = int(request.args.get('limit'))
        offset = int(request.args.get('offset'))

        if c is not None:
            collection = MongoConn.get_collection(c['collection_name'])

            results = list(collection.find().skip(offset).limit(limit))

            msg = json.loads(JSONUtils.JSONEncoder().encode(results))

        else:
            msg = {'result': 'failed', 'msg': "Collection_id: " + collection_id + " does not exist"}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)


# save data to the collection
@bp.route('/<endpoint_name>/<collection_id>', methods=['POST'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_write_right
def general_endpoint_api_post(endpoint_name, collection_id):
    endpoint = MongoConn.get_endpoints_col()

    ept = endpoint.find_one({'endpoint_name': endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])

        c = collection_list.find_one({'_id': ObjectId(collection_id)})

        if c is not None:
            collection = MongoConn.get_collection(c['collection_name'])
            json = request.json  # Seems all json posted would be save into db, not sure how to restrict column.

            print(json)

            collection.insert_many(json)  # Insert number can not be only 1.

            msg = {'result': 'successful', 'msg': str(len(json)) + " records are saved to " + collection_id}

        else:
            msg = {'result': 'failed', 'msg': "Collection_id: " + collection_id + " does not exist"}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)

# update data in the collection
@bp.route('/<endpoint_name>/<collection_id>',methods=['PUT'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_write_right
def general_collection_api_put(endpoint_name, collection_id):
    endpoint = MongoConn.get_collection("endpoints")

    ept = endpoint.find_one({'endpoint_name':endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])

        c = collection_list.find_one({'_id': ObjectId(collection_id)})

        if c is not None:
            collection = MongoConn.get_collection(c['collection_name'])
            json = request.json
            print(json)

            #update
            for record in json:
                collection.replace_one({'_id':ObjectId(record['id'])},record)

            msg = {'result': 'successful', 'msg': str(len(json)) + " records  in Collection_id: " + collection_id + " are updated"}
        else:
            msg = {'result': 'failed', 'msg': "Collection_id: " + collection_id + " does not exist"}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}
    
    return jsonify(msg) 

#query in the collection
@bp.route('/<endpoint_name>/<collection_id>/query',methods=['POST'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_read_right
def general_collection_api_query(endpoint_name, collection_id):
    endpoint = MongoConn.get_collection("endpoints")

    ept = endpoint.find_one({'endpoint_name':endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])

        c = collection_list.find_one({'_id': ObjectId(collection_id)})

        if c is not None:
            collection = MongoConn.get_collection(c['collection_name'])
            req = request.json
            print(req)

            results = list(collection.find(req))

            msg = json.loads(JSONUtils.JSONEncoder().encode(results))

        else:
            msg = {'result': 'failed', 'msg': "Collection_id: " + collection_id + " does not exist"}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)

#aggregation
@bp.route('/<endpoint_name>/<collection_id>/aggregate',methods=['POST'])
@AuthWrapper.require_api_token
@AuthWrapper.require_admin_read_right
def general_collection_api_aggregate(endpoint_name, collection_id):
    endpoint = MongoConn.get_collection("endpoints")

    ept = endpoint.find_one({'endpoint_name':endpoint_name})

    if ept is not None:
        collection_list = MongoConn.get_collection(ept['collection_list'])

        c = collection_list.find_one({'_id': ObjectId(collection_id)})

        if c is not None:
            collection = MongoConn.get_collection(c['collection_name'])
            req = request.json
            print(req)

            results = list(collection.aggregate(req))

            msg = json.loads(JSONUtils.JSONEncoder().encode(results))

        else:
            msg = {'result': 'failed', 'msg': "Collection_id: " + collection_id + " does not exist"}

    else:
        msg = {'result': 'failed', 'msg': "Endpoint " + endpoint_name + " does not exist"}

    return jsonify(msg)

    
