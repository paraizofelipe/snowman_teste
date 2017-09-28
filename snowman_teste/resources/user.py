import hug
from snowman_teste.resources.crud import CRUD
from snowman_teste.models import User
from snowman_teste.schemas import UserSchema


class UserApi(CRUD):

    def __init__(self):
        super().__init__(User, UserSchema)

    @hug.object.get('{id_model}/users/{id_point}')
    def get_point_by_user(self, id_model, id_point):
        try:
            pass
        except Exception as error:
            raise error

    # @hug.object.get()
    # def get_all(self, response):
    #     try:
    #         schema = UserSchema(many=True)
    #         list_user = Session.query(User).all()
    #         result, erros = schema.dump(list_user)
    #         return result
    #     except Exception as error:
    #         response.status = {"error": HTTP_500}
    #         raise error
    #
    # @hug.object.get('{obj_id}')
    # def get_by_id(self, obj_id, response):
    #     try:
    #         schema = UserSchema()
    #         user = Session.query(User).filter_by(id=obj_id).one()
    #         result, erros = schema.dump(user)
    #         return result
    #     except NoResultFound:
    #         response.status = HTTP_404
    #         return {"error": HTTP_404}
    #     except Exception as error:
    #         response.status = {"error": HTTP_500}
    #         raise error
    #
    # @hug.object.post()
    # def add(self, body, response):
    #     try:
    #         schema = UserSchema()
    #         user, erros = schema.load(body, session=Session)
    #         Session.add(user)
    #         Session.commit()
    #         result, erros = schema.dump(user)
    #         return result
    #     except KeyError as error:
    #         response.status = {"error": HTTP_400}
    #         raise error
    #     except Exception as error:
    #         response.status = {"error": HTTP_500}
    #         raise error
    #
    # @hug.object.delete('{obj_id}')
    # def remove(self, obj_id, response):
    #     try:
    #         Session.query(User).filter_by(id=obj_id).delete()
    #         Session.commit()
    #         return {}
    #     except NoResultFound:
    #         response.status = HTTP_404
    #         return {"error": HTTP_404}
    #     except Exception as error:
    #         response.status = HTTP_500
    #         raise error
    #
    # @hug.object.put()
    # def update(self):
    #     pass
