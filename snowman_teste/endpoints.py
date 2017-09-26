import hug
import jwt


authentication = hug.authentication.basic(hug.authentication.verify('User1', 'mypassword'))


@hug.get('/public')
def public_api_call():
    return "Metodo livre"


@hug.post('/login')
def post_here(body):
    return body


@hug.post('/token_generation')  # noqa
def token_gen_call(username, password):
    secret_key = 'super-kye'
    mockusername = 'User2'
    mockpassword = 'Mypassword'
    if mockpassword == password and mockusername == username: # This is an example. Don't do that.
        return {"token": jwt.encode({'user': username, 'data': 'mydata'}, secret_key, algorithm='HS256')}
    return 'Invalid username and/or password for user: {0}'.format(username)