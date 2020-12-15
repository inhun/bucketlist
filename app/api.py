from flask_restful import Api

from app.resources.Test import GETTest
from app.resources.Signup import POSTSignup
from app.resources.Login import POSTLogin
from app.resources.Article import POSTArticle, GETArticle



def build_api(app):
    api = Api()


    api.add_resource(GETTest, '/api/test')
    api.add_resource(POSTSignup, '/api/signup')
    api.add_resource(POSTLogin, '/api/login')
    api.add_resource(POSTArticle, '/api/article')
    api.add_resource(GETArticle, '/api/article')

    api.init_app(app)
    return api