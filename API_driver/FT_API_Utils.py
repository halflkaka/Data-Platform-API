import requests
import json

basicURL = "http://[server]:12012/api"
# basicURL = "http://localhost:5000/api/"

headers = {
    "Content-Type" : "application/x-www-form-urlencoded",
    #your password
    "Authorization" : "***"
}


def ft_create_endpoint(endpoint):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+"endpoints/create",endpoint,headers=headers)

    print r.content

    return json.loads(r.content)


def ft_create_collection(endpoint, collection):#collection here is a json object
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+"create",data=collection,headers=headers)

    print r.content

    return json.loads(r.content)


def ft_download(endpoint, col_id, params):
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    r = requests.get(basicURL+endpoint+col_id,params,headers=headers)
    print r.content

    return json.loads(r.content)


def ft_upload(endpoint, col_id, data):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+col_id,data,headers=headers)
    print r.content

    return json.loads(r.content)


def ft_update(endpoint, col_id, data):
    headers["Content-Type"] = "application/json"
    r = requests.put(basicURL+endpoint+col_id,data,headers=headers)

    return json.loads(r.content)


def ft_query(endpoint,col_id,query):
    headers["Content-Type"] = "application/json"
    r = requests.post(basicURL+endpoint+col_id+"/query",query,headers=headers)
    print r.content

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






