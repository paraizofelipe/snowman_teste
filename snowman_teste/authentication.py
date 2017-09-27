import os
import hug
import jwt
import hashlib
from tinydb import TinyDB, Query

db = TinyDB('db.json')

# TODO mover para arquivo de configuração
secret_key = 'super-secret-key-please-change'


def hash_password(password, salt):
    """
    Função para encodar a senha em hash
    :param password:
    :param salt:
    :return: Codificação hash Hex SHA512 da senha fornecida
    """
    password = str(password).encode('utf-8')
    salt = str(salt).encode('utf-8')
    return hashlib.sha512(password + salt).hexdigest()


@hug.post('/add_user')
def add_user(username, password):
    """
    Função para adicionar um usuário ao banco de dados
    :param username:
    :param password:
    :return: Status de saida em JSON
    """
    user_model = Query()
    if db.search(user_model.username == username):
        return {
            'error': 'Usuário {0} já existe'.format(username)
        }

    salt = hashlib.sha512(str(os.urandom(64)).encode('utf-8')).hexdigest()
    api_token = jwt.encode({'user': username, 'payload': 'pizza'}, secret_key, algorithm='HS256')
    password = hash_password(password, salt)

    user = {"username": username, "password": password, "api_token": api_token.decode('utf-8')}
    user_id = db.insert(user)

    return {'result': 'success', 'eid': user_id, 'salt': salt, 'user_created': user}


def token_verify(token):
    try:
        return jwt.decode(token, secret_key, algorithm='HS256')
    except jwt.DecodeError:
        return False


def authenticate_user(username, password):
    """
    Autenticar um usuario no banco de dados
    :param username:
    :param password:
    :return: usuario autenticado
    """
    user_model = Query()
    user = db.get(user_model.username == username)

    if not user:
        return False

    if user['password'] == hash_password(password, user.get('salt')):
        return user['username']

    return False


token_key_authentication = hug.authentication.token(token_verify)
basic_authentication = hug.authentication.basic(authenticate_user)


@hug.get('/token_authenticated', requires=token_key_authentication)  # noqa
def token_auth_call(user: hug.directives.user):
    return 'Usuario: {0} com dados {1}'.format(user['user'], user['data'])


@hug.post('/login', requires=basic_authentication)
def login(authed_user: hug.directives.user):
    """
    :param :
    :return:
    """
    user_model = Query()
    user = db.search(user_model.username == authed_user)[0]

    if user:
        out = {
            'user': user['username'],
            'token': user['api_key']
        }
    else:
        out = {
            'error': 'User {0} does not exist'.format(authed_user)
        }

    return out


@hug.get('/public')
def public_api_call():
    return "Informação publica"


@hug.get('/private', requires=token_key_authentication)
def private_api_call():
    return "Informação privada"
