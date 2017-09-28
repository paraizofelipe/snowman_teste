import hug
import json
from falcon import HTTP_400
# from snowman_teste.models import TourPoint, session
# from snowman_teste.schemas import TourPointSchema


class TourPointApi:

    def __init__(self):
        pass

    @hug.object.get()
    def get_all(self):
        try:
            list_tour_point = session.query(TourPoint).all()
            if len(list_tour_point) > 0:
                tour_point_schema = TourPointSchema(many=True)
                response = tour_point_schema.dump(list_tour_point).data
                return response
            else:
                return {}
        except Exception as error:
            raise error

    @hug.object.get('{id}')
    def get_by_id(self, id: int):
        pass

    @hug.object.post()
    def add(self, body):
        try:
            if not body:
                return {}
            tour_point_schema = TourPointSchema(many=False)
            tour_point = tour_point_schema.load(body, session=session).data
            session.add(tour_point)
            session.commit()
            return tour_point_schema.dump(tour_point).data
        except Exception as error:
            raise error

    @hug.object.put()
    def update(self):
        pass