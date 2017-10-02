import hug
import traceback
from falcon import HTTP_400, HTTP_500, HTTP_404
from snowman_teste.models import Session
from sqlalchemy.orm.exc import NoResultFound
from snowman_teste.utils import token_verify


def api_crud(model_class, schema_class):

    class CRUD:

        token_key_authentication = hug.authentication.token(token_verify)

        @hug.object.get()
        def get_all(self, response):
            try:
                schema = schema_class(many=True)
                list_user = Session.query(model_class).all()
                result, erros = schema.dump(list_user)
                return result
            except Exception:
                response.status = {"error": HTTP_500}
                traceback.print_exc()
                return {"error": HTTP_500}

        @hug.object.get(urls='{id_model}')
        def get_by_id(self, id_model, response):
            try:
                schema = schema_class()
                user = Session.query(model_class).filter_by(id=id_model).one()
                result, erros = schema.dump(user)
                return result
            except NoResultFound:
                response.status = HTTP_404
                traceback.print_exc()
                return {"error": HTTP_404}
            except Exception:
                response.status = HTTP_500
                traceback.print_exc()
                return {"error": HTTP_500}

        @hug.object.post()
        def add(self, body, response):
            try:
                schema = schema_class()
                user, erros = schema.load(body, session=Session)
                Session.add(user)
                Session.commit()
                result, erros = schema.dump(user)
                return result
            except KeyError:
                response.status = HTTP_400
                traceback.print_exc()
                return {"error": HTTP_400}
            except Exception:
                response.status = HTTP_500
                traceback.print_exc()
                return {"error": HTTP_500}

        @hug.object.delete('{id_model}')
        def remove(self, id_model, response):
            try:
                Session.query(model_class).filter_by(id=id_model).delete()
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

    return CRUD
