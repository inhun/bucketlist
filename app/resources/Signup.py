import bcrypt
from datetime import timedelta
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_claims,
    create_refresh_token, jwt_refresh_token_required
)
from flask_cors import cross_origin
from app.models.response import error_response, ok_response
from flask import current_app as app
from sqlalchemy import text


# POST /signup
class POSTSignup(Resource):
    @cross_origin()
    def post(self):

        if not request.is_json:
            return error_response(400, 'JSON 형식으로 전달해주세요.')

        try:
            user_id = request.json.get('id', None)
            password = request.json.get('password', None)
            name = request.json.get('name', None)
            if (not user_id) or (not password) or (not name):
                return error_response(400, '파라미터가 부족합니다.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            app.database.execute(text('''
                INSERT INTO users (id, password, name)
                VALUES (:id, :password, :name)
            '''), {
                'id': user_id,
                'password': hashed,
                'name': name
            })
        except Exception as exc:
            return error_response(500, str(exc))
        
        return ok_response(None)
        