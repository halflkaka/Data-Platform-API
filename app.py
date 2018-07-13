from flask import Flask
from flask import jsonify
from Utils import Config, MongoConn, PostgreConn
from flask_cors import CORS
from Flaskr import (auth, api_home, api_user,
                    api_endpoints, api_endpoint_collections, api_dbtable)

app = Flask(__name__)
app.secret_key = 'FusionTreeAPI'
CORS(app)

# initialize mongodb connection
MongoConn.init_db(app)
PostgreConn.init_db()

# root api
@app.route('/', methods=['GET'])
def show_welcome():
    # return render_template("index.html")
    return jsonify(Config.ROOT_DES)


app.register_blueprint(auth.bp)
app.register_blueprint(api_home.bp)
app.register_blueprint(api_user.bp)
app.register_blueprint(api_endpoints.bp)
app.register_blueprint(api_endpoint_collections.bp)
app.register_blueprint(api_dbtable.bp)

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=5000)
