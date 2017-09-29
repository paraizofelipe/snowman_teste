from snowman_teste.resources.pattern_api import api_crud
from snowman_teste.models import Category, Session
from snowman_teste.schemas import CategorySchema

CRUD = api_crud(Category, CategorySchema)


class CategoryApi(CRUD):
    pass
