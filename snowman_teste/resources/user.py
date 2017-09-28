import hug
from tinydb import TinyDB, Query
from falcon import HTTP_400, HTTP_500
from snowman_teste.models import User as ModelUser
from snowman_teste.schemas import UserSchema

db = TinyDB('snowman.json')


class UserApi:

    def __init__(self):
        pass

    @hug.object.get()
    def get_all(self):
        try:
            schema = UserSchema(only=('created_at', 'name', 'authenticator.api_token', 'email'), many=True)
            list_user = db.all()
            result, erros = schema.dump(list_user)
            return result
        except Exception as error:
            raise error

    @hug.object.get('{id}')
    def get_by_id(self, id: int):
        pass

    @hug.object.post()
    def add(self, body, response):
        try:
            user = ModelUser(name=body['name'], email=body['email'], password=body['password'])
            schema = UserSchema(only=('created_at', 'name', 'authenticator.api_token', 'email'))
            result, erros = schema.dump(user)
            db.insert(result)
            return result
        except KeyError:
            response.status = HTTP_400
            return {'error': HTTP_400}
        except Exception:
            response.status = HTTP_500
            return {'error': HTTP_500}

    @hug.object.put()
    def update(self):
        pass
