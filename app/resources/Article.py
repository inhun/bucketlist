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


class POSTArticle(Resource):
    @jwt_required
    @cross_origin()
    def post(self):
        claims = get_jwt_claims()

        try:
            title = request.json.get('title', None)
            content = request.json.get('content', None)
            if (not title) or (not content):
                return error_response(400, '파라미터가 부족합니다.')
        except Exception as exc:
            return error_response(400, 'Json 파싱 에러가 발생했습니다 : ' + str(exc))

        user_id = claims['id']
        
        try:
            app.database.execute(text('''
                INSERT INTO posts (title, content, author_id)
                VALUES (:title, :content, :author_id) 
            '''), {
                'title': title,
                'content': content,
                'author_id': user_id
            })
        except Exception as exc:
            return error_response(500, str(exc))
        
        return ok_response(None)


class GETArticle(Resource):
    @jwt_required
    @cross_origin()
    def get(self):
        claims = get_jwt_claims()

        try:
            result = app.database.execute(text('''
                SELECT id, title, content, published_at, author_id 
                FROM posts
            ''')).fetchall()
        except Exception as exc:
            return error_response(500, str(exc))
        
        
        posts = []
        for row in result:  
            posts.append({
                'id': row['id'],
                'title': row['title'],
                'content': row['content'],
                'published_at': row['published_at'],
                'author_id': row['author_id']
            })

        return ok_response({
            'posts_count': len(posts),
            'posts': posts 
        })


        return ok_response(None)