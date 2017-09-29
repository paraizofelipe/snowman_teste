import hug
import googlemaps
from snowman_teste.resources.pattern_api import api_crud
from snowman_teste.models import TourPoint, User, Session
from snowman_teste.schemas import TourPointSchema
from snowman_teste.project import CONFIG

CRUD = api_crud(TourPoint, TourPointSchema)


class TourPointApi(CRUD):

    def __init__(self):
        self.gmaps = googlemaps.Client(key=CONFIG['api']['google_key'])

    @hug.object.get('{id_model}/users/{id_user}')
    def get_point_by_user(self, id_model, id_user):
        try:
            pass
        except Exception as error:
            raise error

    @hug.object.get('users/{id_user}/near')
    def get_point_near(self, origins, id_user):
        try:
            list_near = []
            tour_point_schema = TourPointSchema(many=True)
            list_tour_points = Session.query(TourPoint).filter_by(user_id=id_user).all()

            for tour_point in list_tour_points:
                geocode = self.gmaps.reverse_geocode(origins)[0]
                matrix = self.gmaps.distance_matrix(origins=geocode['formatted_address'],
                                                    destinations=tour_point.address)
                distance = matrix['rows'][0]['elements'][0]['distance']['value']
                if distance < 5000:
                    list_near.append(tour_point)
            result, erros = tour_point_schema.dump(list_near)
            return result
        except Exception as error:
            raise error
