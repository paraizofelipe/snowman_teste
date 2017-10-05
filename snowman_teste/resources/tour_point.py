import hug
import traceback
from sqlalchemy.orm.exc import NoResultFound
from falcon import HTTP_500, HTTP_400, HTTP_404
from snowman_teste.utils import token_verify
from snowman_teste.models import TourPoint, Session
from snowman_teste.schemas import TourPointSchema


class TourPointApi:
    """
    Classe contendo os metodos URIs para o endpoint tour_points.
    """
    token_key_authentication = hug.authentication.token(token_verify)

    @hug.object.get()
    def get_point_by_user(self, response):
        try:
            tour_point_schema = TourPointSchema()
            list_tour_points = Session.query(TourPoint).filter_by(category='restaurant').all()
            result, erros = tour_point_schema.dump(list_tour_points, many=True)
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
