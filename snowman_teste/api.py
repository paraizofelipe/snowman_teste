import hug

from snowman_teste.resources.user import UserApi
from snowman_teste.resources.tour_point import TourPointApi
from snowman_teste.resources.authentication import AuthenticatorApi
from snowman_teste.resources.category import CategoryApi


def create_api():
    api = hug.API(__name__)
    api.http.output_format = hug.output_format.pretty_json

    routes = hug.route.API(__name__)
    routes.object(urls='/tour_points')(TourPointApi)
    routes.object(urls='/users')(UserApi)
    routes.object(urls='/auths')(AuthenticatorApi)
    routes.object(urls='/categorys')(CategoryApi)

    return api