import hug
import googlemaps
from snowman_teste.resources.pattern_api import api_crud
from snowman_teste.models import TourPoint, Session
from snowman_teste.schemas import TourPointSchema

CRUD = api_crud(TourPoint, TourPointSchema)


class TourPointApi(CRUD):

    @hug.object.get('{id_model}/users/{id_user}')
    def get_point_by_user(self, id_model, id_user):
        try:
            pass
        except Exception as error:
            raise error
