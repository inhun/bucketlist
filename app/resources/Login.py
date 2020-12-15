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
class POSTLogin(Resource):
    @cross_origin()
    def post(self):
        print(request.data)
        if not request.is_json:
            print('json아님')
            return error_response(400, 'JSON 형식으로 전달해주세요.')

        try:
            user_id = request.json.get('id', None)
            password = request.json.get('password', None)
            if (not user_id) or (not password):
                return error_response(400, '파라미터가 부족합니다.')
        except Exception as exc:
            return error_response(400, 'JSON 파싱 에러가 발생했습니다 : ' + str(exc))
        print(user_id)
        print(password)

        try:
            result = app.database.execute(text('''
                SELECT count(id) AS counts, id, password, name
                FROM users WHERE id = :user_id
            '''), {
                'user_id': user_id
            }).fetchone()

            if int(result['counts']) == 0:
                return error_response(401, 'id가 잘못되었습니다.')
        except Exception as exc:
            return error_response(500, str(exc))

        print(type(result['id']), result['password'])
        
        try:
            if not bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
                return error_response(401, '비밀번호가 잘못되었습니다.')
        except Exception as exc:
            return error_response(401, '비밀번호가 잘못되었습니다 : ' + str(exc))

        user_claims = {
            'id': result['id'],
            'name': result['name']
        }
        print(user_claims)
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(hours=24),
            user_claims=user_claims
        )
        refresh_token = create_refresh_token(
            identity=user_id,
            user_claims=user_claims
        )
        return ok_response({
            'access_token': access_token,
            'refresh_token': refresh_token
        })


        


