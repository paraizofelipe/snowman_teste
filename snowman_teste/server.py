import hug

from snowman_teste.resources.user import UserApi
from snowman_teste.resources.tour_point import TourPointApi

if __name__ == '__main__':
    api = hug.API(__name__)
    api.http.output_format = hug.output_format.pretty_json

    routes = hug.route.API(__name__)
    routes.object(urls='/tour_points')(TourPointApi)
    routes.object(urls='/users')(UserApi)

    api.http.serve()
