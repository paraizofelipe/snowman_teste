import hug
from snowman_teste.resources.pattern_api import api_crud
from snowman_teste.models import User
from snowman_teste.schemas import UserSchema

CRUD = api_crud(User, UserSchema)


class UserApi(CRUD):

    @hug.object.get('{id_model}/tour_points/{id_point}')
    def get_point_by_user(self, id_model, id_point):
        try:
            pass
        except Exception as error:
            raise error