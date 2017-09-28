import hashlib


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