from flask import Flask, jsonify
from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'bucketlist'


from sqlalchemy import create_engine, text
app.config.from_pyfile('config.py')
database = create_engine(app.config['DB_URL'], encoding='utf-8')
app.database = database

from flask_jwt_extended import JWTManager
jwt_manager = JWTManager(app)
app.jwt_manager = jwt_manager



from app.api import build_api
build_api(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
