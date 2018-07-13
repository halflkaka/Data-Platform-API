import requests
import json

basicURL = "http://127.0.0.1:8080/api/"

headers = {
    "x-access-token" : ".......",
    "Content-Type" : "application/x-www-form-urlencoded"
}


# you need to write following two methods
# to support the creation of endpoints and collections
def ft_create_endpoint(endpoint):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+"endpoints/create",endpoint,headers=headers)

    return json.loads(r.content)


def ft_create_collection(endpoint, collection):#collection here is a json object
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+"create",collection,headers=headers)

    return json.loads(r.content)


def ft_download(endpoint, col_id, params):
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    r = requests.get(basicURL+endpoint+col_id,params,headers=headers)

    return json.loads(r.content)


def ft_upload(endpoint, col_id, data):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+col_id,data,headers=headers)

    return json.loads(r.content)


def ft_update(endpoint, col_id, data):
    headers["Content-Type"] = "application/json"
    r = requests.put(basicURL+endpoint+col_id,data,headers=headers)

    return json.loads(r.content)


def ft_query(endpoint,col_id,query):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+col_id+"/query",query,headers=headers)

    return json.loads(r.content)


def ft_aggregate(endpoint,col_id,query):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+col_id+"/aggregate",query,headers=headers)

    return json.loads(r.content)


def ft_upload_dict(endpoint,col_id, dict):
    headers["Content-Type"] = "application/json"

    uploadingList = []

    for key in dict:
        uploadingList.append(dict[key])
        if (len(uploadingList) == 100):
            ft_upload(endpoint,col_id,json.dumps(uploadingList))
            uploadingList[:] = []

    if (len(uploadingList) > 0):
        ft_upload(endpoint, col_id, json.dumps(uploadingList))
        uploadingList[:] = []


#testing code
# accessPoint = "gps/"
# link = "createCollection"
# data = {"collectionName": "collectionofGPSData", "description": "the collection to test the creation of gps collection"}
#
# # postResult = FMSUpload(accessPoint, link, data)
# # print(postResult)
# #
# # colId = postResult["records"]["_id"]
#
# colId = "5a16be17a0f4d93df72fdb43"
# # data =[{"lat" :0.111, "log" : 2.0111},{"lat" :0.2222, "log" : 2.0111}]
# #
# # uResult = FMSUpload(accessPoint, colId, json.dumps(data))
# # print(uResult)
#
# # params = {}
# # dResult = FMSDownload(accessPoint, colId, params)
# # print(dResult)
#
# query = [{
#     "collectionID":colId,
#     "limit": 100,
#     "skip": 0,
#     "query" :{
#         "record.lat" : 0.111
#     }
# }]
#
# qResult = FMSQuery(accessPoint, json.dumps(query))
# print(qResult)
#
# record = qResult["records"][0]
#
# updateRecord = record["record"]
#
# updateRecord["lat"] = 10000
#
# print updateRecord
#
# aRecord = [{
#     'id': record['_id'],
#     'record': updateRecord
# }]
#
# updateResult = FMSUpdate(accessPoint, colId, json.dumps(aRecord))
#
# print(updateResult)