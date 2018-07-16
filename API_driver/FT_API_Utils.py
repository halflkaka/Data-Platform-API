import requests
import json

basicURL = "http://47.100.217.149:12012/api"
# basicURL = "http://localhost:5000/api/"

headers = {
    "Content-Type" : "application/x-www-form-urlencoded",
    #your password
    "Authorization" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImhhbGZsa2FrYSIsInBhc3N3b3JkIjoiJHBia2RmMi1zaGEyNTYkMjAwMDAwJGk5RWFZNndWSWdTZ2RPN2R1emNHUUEkOGRuQ2ZwV2tCUU9oOFdGRGFFSGNmam1EOHFuOVN2SkRFY2ppa3JKOHYuSSJ9.kRKeWHa9i7mUm5CoB6qkth-xeTnWGpt4R5JlR6I90Q4"
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






