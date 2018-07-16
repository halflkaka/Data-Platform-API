import FT_API_Utils as api
import requests
import json
import urllib

endpoint = {
    "endpoint_name" : "drivertest",
    "endpoint_desc" : "N/A",
    "collection_list" : "driverCollection"
}

collection = {
	"collection_name" : "driverCollectionName",
	"collection_des" : "driverCollectionDes"
}

data = [
    {"name" : "data1", "value" : "1"},
    {"name" : "data2", "value" : "2"}
]

query = {
      "$or": [
          {"name": "data1"}, {"name":"data2"}
      ]
}


aggregate = [
     { "$match" : { "id" : { "$gt" : 1, "$lte" : 3 } } },
     { "$group": { "_id": "$id", "count": { "$sum": 1 } } }
]

params = {
    "limit" : 2,
    "offset" : 0
}




if __name__ == '__main__':
    # create endpoint
    api.ft_create_endpoint(json.dumps(endpoint))

    # create collection
    api.ft_create_collection('wanxiang/',json.dumps(collection))

    #upload data
    api.ft_upload('wanxiang/','5b34a149f0e6b125193dc721',json.dumps(data))

    #update data
    api.ft_update('wanxiang/','5b34a149f0e6b125193dc721',json.dumps(data))

    #query
    api.ft_query('wanxiang/','5b34a149f0e6b125193dc721',json.dumps(query))

    #aggregate
    api.ft_aggregate('wanxiang/','5b34a149f0e6b125193dc721',json.dumps(aggregate))

    #download
    api.ft_download('wanxiang/','5b34a149f0e6b125193dc721',urllib.urlencode(params))



