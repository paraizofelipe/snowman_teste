import hug

from snowman_teste import endpoints
from snowman_teste import authentication


# @hug.extend_api()
def load_endpoints():
    return [endpoints, authentication]


if __name__ == '__main__':
    api = hug.API(__name__)
    api.http.output_format = hug.output_format.pretty_json

    hug.extend_api()(load_endpoints)

    api.http.serve()