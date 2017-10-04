import hug
import traceback
from sqlalchemy.orm.exc import NoResultFound
from falcon import HTTP_500, HTTP_400, HTTP_401, HTTP_404
from snowman_teste.utils import token_verify
from snowman_teste.models import TourPoint, User, Session
from snowman_teste.schemas import TourPointSchema


class TourPointApi:
    """
    Classe contendo os metodos URIs para o endpoint tour_points.
    """
    token_key_authentication = hug.authentication.token(token_verify)

    @hug.object.post(requires=token_key_authentication)
    def add(self, body, payload: hug.directives.user, response):
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
            user = Session.query(User).filter_by(email=payload['email']).one()
            schema = TourPointSchema()
            tour_point, erros = schema.load(body, session=Session)
            Session.add(tour_point)
            Session.commit()
            result, erros = schema.dump(tour_point)
            return result
        except KeyError:
            response.status = HTTP_400
            traceback.print_exc()
            return {"error": HTTP_400}
        except Exception:
            response.status = HTTP_500
            traceback.print_exc()
            return {"error": HTTP_500}

    @hug.object.delete('{id_point}', requires=token_key_authentication)
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
