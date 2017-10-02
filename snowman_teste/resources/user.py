import hug
import traceback
import googlemaps
from sqlalchemy.orm.exc import NoResultFound
from falcon import HTTP_500, HTTP_400, HTTP_401, HTTP_404
from snowman_teste.settings import CONFIG
from snowman_teste.utils import hash_password, token_verify
from snowman_teste.models import User, TourPoint, Session
from snowman_teste.schemas import UserSchema, AuthenticatorSchema, TourPointSchema


class UserApi:

    token_key_authentication = hug.authentication.token(token_verify)

    def __init__(self):
        self.gmaps = googlemaps.Client(key=CONFIG['api']['google_key'])

    @hug.object.post('login')
    def login(self, body, response):
        try:
            auth_schema = AuthenticatorSchema()
            user = Session.query(User).filter_by(email=body['email']).one()
            if not user:
                response = HTTP_401
            if user.password == hash_password(body['password'], user.authenticator.salt):
                result, erros = auth_schema.dump(user.authenticator)
                return result
        except KeyError:
            response.status = HTTP_400
            traceback.print_exc()
            return {"error": HTTP_400}
        except Exception:
            response.status = HTTP_500
            traceback.print_exc()
            return {"error": HTTP_500}

    @hug.object.get('tour_points', requires=token_key_authentication)
    def get_point_by_user(self, user_req: hug.directives.user, response):
        try:
            schema = UserSchema()
            user = Session.query(User).filter_by(email=user_req['email']).one()
            list_tour_points = Session.query(TourPoint).filter_by(id=user.id).all()
            result, erros = schema.dump(list_tour_points, many=True)
            return result
        except NoResultFound as error:
            response.status = HTTP_404
            traceback.print_exc()
            return {"error": HTTP_404}
        except KeyError:
            response.status = HTTP_400
            traceback.print_exc()
            return {"error": HTTP_400}
        except Exception:
            response.status = {"error": HTTP_500}
            traceback.print_exc()
            return {"error": HTTP_500}

    @hug.object.get('near_points', requires=token_key_authentication)
    def get_point_near(self, origins, user_req: hug.directives.user):
        try:
            list_near = []
            tour_point_schema = TourPointSchema(many=True)
            user = Session.query(User).filter_by(email=user_req['email']).one()
            list_tour_points = Session.query(TourPoint).filter_by(user_id=user.id).all()

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
