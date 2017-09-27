import hug

from snowman_teste.schemas import UserSchema


class UserApi:

    def __init__(self):
        pass

    @hug.object.get()
    def get_all(self):
        pass

    @hug.object.get('{id}')
    def get_by_id(self, id: int):
        pass

    @hug.object.post()
    def add(self):
        pass

    @hug.object.put()
    def update(self):
        pass
