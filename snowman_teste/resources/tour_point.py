import hug
from snowman_teste.resources.crud import CRUD
from snowman_teste.models import TourPoint
from snowman_teste.schemas import TourPointSchema


class TourPointApi(CRUD):

    def __init__(self):
        super().__init__(TourPoint, TourPointSchema)

    @hug.object.get('{id_model}/tour_points/{id_user}')
    def get_point_by_user(self, id_model, id_user):
        try:
            pass
        except Exception as error:
            raise error
