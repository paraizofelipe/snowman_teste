import hug
import traceback
import googlemaps
from sqlalchemy.orm.exc import NoResultFound
from falcon import HTTP_500, HTTP_400, HTTP_401, HTTP_404
from snowman_teste.settings import CONFIG
from snowman_teste.utils import hash_password, token_verify
from snowman_teste.models import User, TourPoint, Session
from snowman_teste.schemas import UserSchema, AuthenticatorSchema, TourPointSchema, AlchemyMarshSchema


class UserApi:
    """
    Classe contendo os metodos URIs para o endpoint users.
    """

    token_key_authentication = hug.authentication.token(token_verify)

    def __init__(self):
        hug.type()
        self.gmaps = googlemaps.Client(key=CONFIG['api']['google_key'])

    @hug.object.post()
    def add_user(self, body: AlchemyMarshSchema(UserSchema, Session)):
        try:
            user_schema = UserSchema()
            Session.add(body)
            Session.commit()
            user_dict, errors = user_schema.dump(body)
            return user_dict
        except Exception as error:
            raise error

    @hug.object.post('login')
    def login(self, body, response):
        try:
            auth_schema = AuthenticatorSchema()
            user = Session.query(User).filter_by(email=body['email']).one()
            if not user or user.password != hash_password(body['password'], user.authenticator.salt):
                response.status = HTTP_401
                return {"error": HTTP_401, 'msg': 'Invalid user or password!'}

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

    @hug.object.post('tour_points', requires=token_key_authentication)
    def add_tour_point(self, body: AlchemyMarshSchema(TourPointSchema, Session), payload: hug.directives.user, response):
        """
        Metodo para adicionar novos pontos de passeio para um usuário autenticado.
        :param body:
            Obejto JSON contendo as parametros do objeto TourPoint
        :param payload:
            Objeto contendo as informaçoes do payload do token JWT autenticado.
        :param response:
            Objeto para definir o status de resposta da requisição HTTTP.
        :return:
            Objeto TourPoint recem criado.
        """
        try:
            schema = TourPointSchema()
            user = Session.query(User).filter_by(email=payload['email']).one()
            Session.commit()
            body.user = user
            Session.add(body)
            Session.commit()
            result, erros = schema.dump(body,)
            return result
        except KeyError:
            response.status = HTTP_400
            traceback.print_exc()
            return {"error": HTTP_400}
        except Exception:
            response.status = HTTP_500
            traceback.print_exc()
            return {"error": HTTP_500}

    @hug.object.delete('tour_points/{id_point}', requires=token_key_authentication)
    def remove(self, payload: hug.directives.user, id_point, response):
        """
        Metodo para deletar os pontos de passeiao de um usuário autenticado.
        :param payload:
            Objeto contendo as informaçoes do payload do token JWT autenticado.
        :param id_point:
            ID do ponto de passeio cadastrado para o usuario.
        :param response:
            Objeto para definir o status de resposta da requisição HTTTP
        :return:
        """
        try:
            user = Session.query(User).filter_by(email=payload['email']).one()
            Session.query(TourPoint).filter_by(id=id_point, user_id=user.id).delete()
            Session.commit()
            return {}
        except NoResultFound:
            response.status = HTTP_404
            traceback.print_exc()
            return {"error": HTTP_404}
        except Exception:
            response.status = HTTP_500
            traceback.print_exc()
            return {"error": HTTP_500}

    @hug.object.get('near_points', requires=token_key_authentication)
    def get_point_near(self, origins, payload: hug.directives.user):
        try:
            list_near = []
            tour_point_schema = TourPointSchema(many=True)
            user = Session.query(User).filter_by(email=payload['email']).one()
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

    @hug.object.get('tour_points', requires=token_key_authentication)
    def get_point_by_user(self, payload: hug.directives.user, response):
        try:
            tour_point_schema = TourPointSchema()
            user = Session.query(User).filter_by(email=payload['email']).one()
            result, erros = tour_point_schema.dump(user.list_tour_points, many=True)
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