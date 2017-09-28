import hug
from tinydb import TinyDB, Query
from snowman_teste.models import TourPoint
from snowman_teste.schemas import TourPointSchema

db = TinyDB('snowman.json')


class TourPointApi:

    def __init__(self):
        pass

    @hug.object.get()
    def get_all(self):
        try:
            return {}
        except Exception as error:
            raise error

    @hug.object.get('{id}')
    def get_by_id(self, id: int):
        pass

    @hug.object.post()
    def add(self, body):
        try:
            tour_point = TourPoint(name=body['name'], category=body['category'], )
            schema = TourPointSchema()
            result, erros = schema.dump(body)
            db.insert(result.data)
            return result.data
        except Exception as error:
            raise error

    @hug.object.put()
    def update(self):
        pass