import hug
from falcon import HTTP_400, HTTP_500, HTTP_404
from snowman_teste.models import Session
from sqlalchemy.orm.exc import NoResultFound


class CRUD:

    def __init__(self, model_class, schema_class):
        self.Model_class = model_class
        self.Schema_class = schema_class

    @hug.object.get()
    def get_all(self, response):
        try:
            schema = self.Schema_class(many=True)
            list_user = Session.query(self.Model_class).all()
            result, erros = schema.dump(list_user)
            return result
        except Exception as error:
            response.status = {"error": HTTP_500}
            raise error

    @hug.object.get(urls='{id_model}')
    def get_by_id(self, id_model, response):
        try:
            schema = self.Schema_class()
            user = Session.query(self.Model_class).filter_by(id=id_model).one()
            result, erros = schema.dump(user)
            return result
        except NoResultFound:
            response.status = HTTP_404
            return {"error": HTTP_404}
        except Exception as error:
            response.status = {"error": HTTP_500}
            raise error

    @hug.object.post()
    def add(self, body, response):
        try:
            schema = self.Schema_class()
            user, erros = schema.load(body, session=Session)
            Session.add(user)
            Session.commit()
            result, erros = schema.dump(user)
            return result
        except KeyError as error:
            response.status = {"error": HTTP_400}
            raise error
        except Exception as error:
            response.status = {"error": HTTP_500}
            raise error

    @hug.object.delete('{id_model}')
    def remove(self, id_model, response):
        try:
            Session.query(self.Model_class).filter_by(id=id_model).delete()
            Session.commit()
            return {}
        except NoResultFound:
            response.status = HTTP_404
            return {"error": HTTP_404}
        except Exception as error:
            response.status = HTTP_500
            raise error

    @hug.object.put()
    def update(self):
        pass