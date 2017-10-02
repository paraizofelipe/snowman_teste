import jwt
import hashlib
from snowman_teste.settings import CONFIG


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


def token_verify(token):
    try:
        return jwt.decode(token, CONFIG['auth']['secret'], algorithm='HS256')
    except jwt.DecodeError:
        return None
