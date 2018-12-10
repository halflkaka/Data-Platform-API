# API Description
ROOT_DES = {'Title': "Welcome to Fusion Tree RESTful API. New user please register an account via /register/ to use api via /api/"}
API_DES = {'Title': "Welcome to Fusion Tree RESTful API"}
ADMIN_USER_API_DES = {'Title': "Welcome to Fusion Tree RESTful API User Management Endpoint"}
ADMIN_ENDPOINT_API_DES = {'Title': "Welcome to Fusion Tree RESTful API Endpoint Management Endpoint"}
General_ENDPOINT_API_DES = {'Title': "Welcome to Fusion Tree RESTful API Endpoint"}

# Mongo

# MONGO_URI = 'mongodb://REST:RESTFMS2018@localhost:27017/restdb?authSource=admin'
MONGO_URI = 'mongodb://localhost:27017/restdb?authSource=admin'

#Postgre_URI
# POSTGRE_URI = 'postgresql://localhost/scjdb'

# API SECRET
API_SECRET = "..."
TOKEN_ALG = 'HS256'
#TOKEN_HEADER_KEY = "api_access_token"
TOKEN_HEADER_KEY = "Authorization"

# roles
ADMIN = 'admin'
TYPE_ONE = 'type_one'
TYPE_TWO = 'type_two'
TYPE_THREE = 'type_three'

# fixed collections
COL_USERS = "users"
COL_ENDPOINT = "endpoints"
